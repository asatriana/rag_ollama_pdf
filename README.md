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
