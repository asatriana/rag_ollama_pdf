# ⚖️ Legal Assistant — Multi-Document RAG AI

Legal Assistant adalah aplikasi **RAG (Retrieval-Augmented Generation)** berbasis **Streamlit** untuk menganalisis dokumen hukum (UU, kontrak, SOP, kebijakan internal) secara interaktif.

Aplikasi ini memungkinkan pengguna untuk:
- Mengunggah **banyak dokumen sekaligus**
- Menanyakan **pasal, bab, sanksi, kewajiban, larangan**
- Mendapatkan **jawaban kontekstual + sumber halaman**
- Melihat **contoh penerapan kasus** berdasarkan isi dokumen

> Cocok untuk: Legal, Compliance, DPO, Konsultan, Auditor, dan Legal-Tech Engineer.

---

## ✨ Fitur Utama

### 📂 Multi-Document RAG
- Upload PDF / DOCX / TXT
- Semua dokumen diindeks bersama
- Jawaban bisa mengutip **lebih dari satu dokumen**

### 📜 Legal-Aware Question Routing
Aplikasi otomatis mengenali tipe pertanyaan:
- **“UU Nomor X Tahun Y tentang apa”**
- **Ringkasan dokumen**
- **Pasal sanksi**
- **Kewajiban & larangan**
- **Contoh penerapan kasus**

Tanpa hardcode pasal → berbasis **struktur & konteks dokumen**.

### 🧠 Context-Grounded Answer
- Jawaban **hanya berdasarkan isi dokumen**
- Tidak berhalusinasi
- Menampilkan **BAB / PASAL / isi pasal lengkap**
- Sumber ditampilkan dengan **halaman + cuplikan teks**

### 💬 Chat-Style UI (Legal Assistant)
- Bubble chat (user & assistant)
- Sidebar cards (upload, status, active documents)
- Gradient header + Clear Chat
- “Try chips” (klik → langsung kirim pertanyaan)

---

## 🏗️ Arsitektur Singkat

```text
User
 ↓
Streamlit UI
 ↓
Question Router
 ├─ Pasal Index (rule-aware)
 └─ Vector Retriever (semantic)
 ↓
LLM (Ollama)
 ↓
Answer + Source Documents
```
## 🧰 Teknologi Stack
```text
| Komponen   | Teknologi            |
| ---------- | -------------------- |
| UI         | Streamlit            |
| RAG        | LangChain (modular)  |
| LLM        | Ollama (local)       |
| Embeddings | HuggingFace / Ollama |
| Vector DB  | FAISS                |
| Loader     | PyPDF, Docx2txt      |
| Python     | 3.10 – 3.12          |
```

## 📦 Requirements
```text
Lihat file requirements.txt
Minimum:
Python >= 3.10 (disarankan 3.12)
Ollama ter-install di mesin lokal
```
## 🚀 Setup & Installation

1️⃣ Clone Repository
```text
git clone https://github.com/your-username/legal-assistant-rag.git
cd legal-assistant-rag
```
2️⃣ Buat Virtual Environment
```text
python -m venv venv
source venv/bin/activate   # macOS / Linux
# venv\Scripts\activate    # Windows
```
3️⃣ Install Dependencies
```text
pip install -r requirements.txt
```
4️⃣ Install & Pull Model Ollama
```text
brew install ollama            # macOS
ollama pull llama3.2:3b
Model default bisa diganti via .env
```

### 🔐 Environment Variables
```text
Buat file .env:
# LLM
OLLAMA_MODEL=llama3.2:3b

# Embeddings provider
EMBEDDING_PROVIDER=hf
HF_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
⚠️ Jangan commit .env ke GitHub.
```

### ▶️ Menjalankan Aplikasi
```text
streamlit run app.py
Akses via browser:
http://localhost:8501
```

### 🧪 Contoh Pertanyaan yang Didukung
```text
NOMOR 27 TAHUN 2022 itu tentang apa?
Ringkas isi dokumen
Apa pasal yang mengatur tentang sanksi?
Buatkan poin kewajiban & larangan
Berikan contoh penerapan kasus
```

## 📁 Struktur Folder
```text
.
├── app.py                 # Streamlit UI
├── rag_pipelines.py       # RAG logic & routing
├── htmlTemplates.py       # CSS & HTML templates
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

## 🧠 Design Principles
```text
❌ Tidak hardcode pasal tertentu
✅ Struktur-aware (Bab → Pasal → Ayat)
✅ Jawaban selalu bisa ditelusuri ke dokumen
✅ Bisa diganti LLM / Embedding tanpa ubah UI
🔮 Roadmap (Optional)
 Highlight teks pasal di UI
 Export hasil ke PDF
 Multi-language legal docs
 Role-based access (internal vs publik)
 Cloud deployment (OpenAI / VoyageAI)
```

## ⚠️ Disclaimer
```text
Aplikasi ini bukan pengganti nasihat hukum resmi.
Digunakan sebagai alat bantu analisis dokumen.
```

## 👨‍💻 Author
```text
Asatriana Built with ❤️ for Legal & Compliance use-cases.
Open for contribution & improvement.
```

## 📜 License
```text
MIT License
```
