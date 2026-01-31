import streamlit as st

from rag_pipelines import load_documents, create_vectorstore, build_pasal_index, route_question
from htmlTemplates import css, header_html, bot_template, user_template


# ---------- UI helpers ----------
def render_message(role: str, content: str):
    tpl = user_template if role == "user" else bot_template
    st.markdown(tpl.replace("{{MSG}}", content), unsafe_allow_html=True)

def render_typing():
    st.markdown(
        """
        <div class="tm-row bot">
          <div class="tm-avatar bot">⚖️</div>
          <div class="tm-bubble bot"><i>Analyzing document…</i></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def format_sources_with_snippet(docs, max_items=8):
    seen = set()
    out = []
    for d in docs:
        src = d.metadata.get("source", "unknown")
        page = d.metadata.get("page", None)
        key = (src, page)
        if key in seen:
            continue
        seen.add(key)

        snippet = " ".join((d.page_content or "").split())[:220]
        if page is not None:
            out.append(f"{src} (halaman {page}) — \"{snippet}...\"")
        else:
            out.append(f"{src} — \"{snippet}...\"")

        if len(out) >= max_items:
            break
    return out


def init_state():
    st.session_state.setdefault("vectorstore", None)
    st.session_state.setdefault("pasal_index", None)
    st.session_state.setdefault("docs_loaded", False)
    st.session_state.setdefault("active_docs", [])
    st.session_state.setdefault("status_kind", None)  # ok | err | None
    st.session_state.setdefault("status_text", None)
    st.session_state.setdefault("chat_history_ui", [])  # list[{role, content}]
    st.session_state.setdefault("last_sources_docs", None)
    st.session_state.setdefault("last_files_sig", None)


def reset_all():
    st.session_state.vectorstore = None
    st.session_state.pasal_index = None
    st.session_state.docs_loaded = False
    st.session_state.active_docs = []
    st.session_state.status_kind = None
    st.session_state.status_text = None
    st.session_state.chat_history_ui = []
    st.session_state.last_sources_docs = None
    st.session_state.last_files_sig = None


def files_signature(files):
    if not files:
        return None
    return tuple((f.name, getattr(f, "size", None)) for f in files)


# ---------- App ----------
def main():
    st.set_page_config(page_title="Legal Assistant", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")
    st.markdown(css, unsafe_allow_html=True)
    init_state()

    # ---------- Sidebar ----------
    with st.sidebar:
        st.markdown(
            """
            <div class="sb-brand">
              <div class="logo">⚖️</div>
              <div class="name">Legal Assistant</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sb-card">', unsafe_allow_html=True)
        st.markdown("<h3>Upload UU/Dokumen</h3>", unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            " ",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            process = st.button("⬆️ Process", use_container_width=True)
        with col2:
            clear = st.button("🧹 Reset", use_container_width=True)

        if clear:
            reset_all()
            st.rerun()

        if process:
            if not uploaded_files:
                st.session_state.status_kind = "err"
                st.session_state.status_text = "Tidak ada file. Pilih dokumen dulu."
            else:
                try:
                    sig = files_signature(uploaded_files)
                    need_reindex = (st.session_state.vectorstore is None) or (st.session_state.last_files_sig != sig)

                    if not need_reindex:
                        st.session_state.docs_loaded = True
                        st.session_state.status_kind = "ok"
                        st.session_state.status_text = "File belum berubah. Index dipakai ulang."
                    else:
                        with st.spinner("Processing (load → pasal index → vectorstore)..."):
                            docs = load_documents(uploaded_files)
                            st.session_state.pasal_index = build_pasal_index(docs)
                            st.session_state.vectorstore = create_vectorstore(docs)
                            st.session_state.docs_loaded = True
                            st.session_state.last_files_sig = sig
                            st.session_state.active_docs = [f.name for f in uploaded_files]

                        st.session_state.status_kind = "ok"
                        st.session_state.status_text = "Document uploaded and processed successfully."
                except Exception as e:
                    st.session_state.status_kind = "err"
                    st.session_state.status_text = "Processing gagal: " + str(e)

        # Status box
        if st.session_state.status_text:
            kind = st.session_state.status_kind or "ok"
            st.markdown(
                f'<div class="sb-status {kind}">✅ {st.session_state.status_text}</div>'
                if kind == "ok"
                else f'<div class="sb-status {kind}">⚠️ {st.session_state.status_text}</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)  # close card

        # Active documents card
        st.markdown('<div class="sb-card">', unsafe_allow_html=True)
        st.markdown("<h3>Active Documents</h3>", unsafe_allow_html=True)

        if st.session_state.active_docs:
            for name in st.session_state.active_docs:
                st.markdown(
                    f"""
                    <div class="sb-doc">
                      <div class="dot"></div>
                      <div class="sb-muted"><b>{name}</b><br/>indexed</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.markdown('<div class="sb-muted">Belum ada dokumen.</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Main header ----------
    hcol1, hcol2 = st.columns([8, 2])
    with hcol1:
        st.markdown(header_html, unsafe_allow_html=True)
    with hcol2:
        clear_chat = st.button("🧹 Clear Chat", use_container_width=True)
        if clear_chat:
            st.session_state.chat_history_ui = []
            st.session_state.last_sources_docs = None
            st.rerun()

    # ---------- Chat body ----------
    st.markdown('<div class="tm-chat-wrap">', unsafe_allow_html=True)

    if not st.session_state.chat_history_ui:
        render_message(
            "bot",
            "Halo! Upload dokumen (UU/kontrak/SOP) di panel kiri, klik **Upload & Process**, lalu tanya.\n\n"
            "Aku bisa:\n"
            "- Menampilkan **BAB + PASAL + isi pasal lengkap**\n"
            "- Ringkas dokumen\n"
            "- Daftar kewajiban & larangan\n"
            "- Pasal terkait sanksi\n"
            "- Contoh penerapan kasus (berdasarkan dokumen)",
        )
        if st.session_state.docs_loaded:
            render_message("bot", "✅ Dokumen sudah terindeks. Silakan tanya.")
    else:
        for m in st.session_state.chat_history_ui:
            render_message(m["role"], m["content"])

    st.markdown("</div>", unsafe_allow_html=True)

    # Try chips (static)
    st.markdown(
        """
        <div class="tm-try">
          <div><b>Try:</b></div>
          <div class="tm-chip">NOMOR 27 TAHUN 2022 itu tentang apa?</div>
          <div class="tm-chip">Ringkas isi dokumen</div>
          <div class="tm-chip">Apa pasal yang mengatur tentang sanksi?</div>
          <div class="tm-chip">Buatkan poin kewajiban & larangan</div>
          <div class="tm-chip">Berikan contoh penerapan kasus</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sources panel (latest)
    if st.session_state.last_sources_docs:
        with st.expander("Sources (latest)"):
            sources = format_sources_with_snippet(st.session_state.last_sources_docs, max_items=10)
            st.markdown("\n".join([f"- {s}" for s in sources]))

    # ---------- Input ----------
    user_query = st.chat_input("Tulis pertanyaan hukum kamu di sini...")
    if user_query:
        st.session_state.chat_history_ui.append({"role": "user", "content": user_query})

        if not st.session_state.docs_loaded or st.session_state.vectorstore is None or st.session_state.pasal_index is None:
            st.session_state.chat_history_ui.append({
                "role": "bot",
                "content": "Silakan upload dokumen dulu di panel kiri, lalu klik **Upload & Process**.",
            })
            st.rerun()

        # Call router
        # tampilkan typing indicator
        render_typing()
        with st.spinner("Menganalisis dokumen..."):
            answer, src_docs = route_question(
                st.session_state.vectorstore,
                st.session_state.pasal_index,
                user_query
            )

        st.session_state.chat_history_ui.append({"role": "bot", "content": answer})
        st.session_state.last_sources_docs = src_docs
        st.rerun()


if __name__ == "__main__":
    main()
