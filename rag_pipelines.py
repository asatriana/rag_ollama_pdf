import os
import re
import tempfile
from typing import List, Tuple

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama

from embedding_factory import get_embeddings


# =========================================================
# 1) LOAD DOCUMENTS (streamlit-friendly)
# =========================================================

def load_documents(files) -> list:
    """
    Terima list of UploadedFile (Streamlit),
    simpan ke temp dir, lalu load via LangChain loader.
    """
    docs = []
    tmp_dir = tempfile.mkdtemp(prefix="rag_upload_")

    for f in files:
        filename = os.path.basename(f.name)
        file_path = os.path.join(tmp_dir, filename)

        with open(file_path, "wb") as out:
            out.write(f.getbuffer())

        ext = os.path.splitext(filename)[1].lower()

        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".docx":
            loader = Docx2txtLoader(file_path)
        else:
            loader = TextLoader(file_path, encoding="utf-8")

        docs.extend(loader.load())

    return docs


# =========================================================
# 2) VECTORSTORE
# =========================================================

def create_vectorstore(docs) -> FAISS:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=200,
    )
    chunks = splitter.split_documents(docs)

    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore


# =========================================================
# 3) PASAL INDEX (deterministic legal retrieval)
# =========================================================

PASAL_PATTERN = re.compile(r"(?im)^\s*(Pasal\s+(\d+))\s*$")

def build_pasal_index(docs) -> list:
    """
    Extract semua blok Pasal dari dokumen.
    Return list of dict:
    {
      pasal_no,
      pasal_label,
      content,
      source,
      page
    }
    """
    pasals = []

    for d in docs:
        text = d.page_content or ""
        source = d.metadata.get("source", "unknown")
        page = d.metadata.get("page", None)

        matches = list(PASAL_PATTERN.finditer(text))
        if not matches:
            continue

        for i, m in enumerate(matches):
            pasal_label = m.group(1).strip()
            pasal_no = int(m.group(2))
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            body = text[start:end].strip()

            if body:
                pasals.append({
                    "pasal_no": pasal_no,
                    "pasal_label": pasal_label,
                    "content": body,
                    "source": source,
                    "page": page,
                })

    return pasals


# =========================================================
# 4) PASAL SCORING & FINDER
# =========================================================

SANCTION_KEYWORDS = [
    "sanksi", "denda", "pidana", "penjara",
    "kurungan", "administratif", "ganti rugi"
]

def score_pasal(content: str, query: str) -> int:
    t = content.lower()
    q = query.lower()
    score = 0

    for k in SANCTION_KEYWORDS:
        if k in q and k in t:
            score += 10

    for token in re.findall(r"\b[a-zA-Z]{4,}\b", q):
        if token in t:
            score += 1

    return score


def find_relevant_pasals(pasals: list, query: str, top_k: int = 3) -> list:
    scored = []
    for p in pasals:
        s = score_pasal(p["content"], query)
        if s > 0:
            scored.append((s, p))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[:top_k]]


def render_pasals(pasals: list) -> Tuple[str, list]:
    """
    Render PASAL + isi lengkap + metadata sumber
    """
    blocks = []
    src_docs = []

    for p in pasals:
        block = (
            f"{p['pasal_label']}\n"
            f"{p['content']}\n\n"
            f"(Sumber: {p['source']}"
            + (f", halaman {p['page']})" if p["page"] is not None else ")")
        )
        blocks.append(block)
        src_docs.append(type("Doc", (), {
            "page_content": p["content"],
            "metadata": {
                "source": p["source"],
                "page": p["page"],
            }
        }))

    return "\n\n---\n\n".join(blocks), src_docs


# =========================================================
# 5) GENERIC RAG ANSWER
# =========================================================

def rag_answer(vectorstore, query: str) -> Tuple[str, list]:
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 6, "fetch_k": 20},
    )
    docs = retriever.invoke(query)

    context = "\n\n".join(d.page_content for d in docs)

    prompt = f"""
Jawab secara DESKRIPTIF dan sesuai konteks dokumen.
Jangan menambah aturan di luar konteks.

KONTEKS:
{context}

PERTANYAAN:
{query}

JAWABAN:
"""

    llm = ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
        temperature=0.3,
    )
    msg = llm.invoke(prompt)
    answer = msg.content if hasattr(msg, "content") else str(msg)

    return answer, docs


# =========================================================
# 6) ROUTER (INTENT-AWARE)
# =========================================================

def route_question(vectorstore, pasal_index: list, query: str) -> Tuple[str, list]:
    q = query.lower()

    # --- A) Pasal sanksi / hukuman
    if any(k in q for k in SANCTION_KEYWORDS):
        pasals = find_relevant_pasals(pasal_index, query, top_k=5)
        if pasals:
            return render_pasals(pasals)

    # --- B) Tanya pasal tertentu (Pasal X)
    m = re.search(r"pasal\s+(\d+)", q)
    if m:
        target = int(m.group(1))
        pasals = [p for p in pasal_index if p["pasal_no"] == target]
        if pasals:
            return render_pasals(pasals)

    # --- C) Tentang apa UU Nomor X Tahun Y
    if "tentang apa" in q or "itu tentang apa" in q:
        return rag_answer(vectorstore, query)

    # --- D) Ringkasan dokumen
    if "ringkas" in q or "ringkasan" in q:
        prompt = f"Ringkas isi dokumen secara tematik.\n\n{query}"
        return rag_answer(vectorstore, prompt)

    # --- E) Kewajiban & larangan
    if "kewajiban" in q or "larangan" in q:
        prompt = f"""
Dari dokumen, buatkan:
- Poin KEWAJIBAN
- Poin LARANGAN
Gunakan bullet point.
"""
        return rag_answer(vectorstore, prompt)

    # --- F) Contoh kasus
    if "contoh" in q or "kasus" in q:
        prompt = f"""
Berdasarkan dokumen, berikan CONTOH KASUS PENERAPAN.
Jangan menambah aturan di luar dokumen.
"""
        return rag_answer(vectorstore, prompt)

    # --- Default fallback
    return rag_answer(vectorstore, query)
