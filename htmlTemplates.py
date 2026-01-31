# htmlTemplates.py
# UI templates for Streamlit: CSS + header + chat bubbles (Legal Assistant style)

css = """
<style>
/* ---------- Theme ---------- */
:root{
  --bg: #f3f5f7;
  --card: #ffffff;
  --text: #0f172a;
  --muted: #64748b;
  --border: #e5e7eb;
  --shadow: 0 10px 30px rgba(15, 23, 42, 0.08);

  --brand1:#0ea5a7;   /* teal */
  --brand2:#22c55e;   /* green */
  --user:#22c55e;     /* user bubble */
  --bot:#ffffff;
  --botBorder:#e6eef2;
}

/* Remove Streamlit default header/footer */
header[data-testid="stHeader"]{display:none;}
footer{visibility:hidden;}
#MainMenu{visibility:hidden;}

/* App background (dotted wallpaper like screenshot) */
.stApp{
  background:
    radial-gradient(circle at 1px 1px, rgba(15,23,42,0.06) 1px, transparent 0) 0 0/22px 22px,
    linear-gradient(var(--bg), var(--bg));
}

/* Main container: make it wider so header spans to the right */
.main .block-container{
  max-width: 100% !important;     /* FULL width main area */
  padding-left: 2rem !important;
  padding-right: 2rem !important;
  padding-top: 0.5rem !important; /* header lebih naik */
  padding-bottom: 1.2rem;
}

/* Sidebar as white panel */
section[data-testid="stSidebar"]{
  background: var(--card) !important;
  border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container{
  padding-top: 1rem;
}

/* ---------- Unified Buttons ---------- */
/* Primary: gradient (Upload & Process) */
/* ---------- Sidebar action buttons (Upload & Reset) ---------- */
section[data-testid="stSidebar"] .stButton > button{
  font-size: 13px !important;      /* perkecil font */
  height: 40px !important;         /* sedikit lebih ramping */
  padding: 0 14px !important;
  letter-spacing: 0.2px;
}

/* Icon di dalam button lebih proporsional */
section[data-testid="stSidebar"] .stButton > button span{
  font-size: 13px !important;
}

/* Primary (Upload & Process) tetap tegas tapi tidak terlalu besar */
section[data-testid="stSidebar"] button[kind="primary"]{
  font-size: 12px !important;
  font-weight: 800 !important;
}

/* Secondary (Reset) */
section[data-testid="stSidebar"] button[kind="secondary"]{
  font-size: 12px !important;
  font-weight: 800 !important;
}


/* ---------- Header (Gradient) ---------- */
.tm-header{
  width: 100%;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap: 12px;
  padding: 14px 18px;
  border-radius: 18px;
  background: linear-gradient(90deg, var(--brand1), var(--brand2));
  box-shadow: var(--shadow);
  margin-top: 0 !important;
  margin-bottom: 10px !important;
}

.tm-header .title{
  display:flex;
  align-items:center;
  gap: 12px;
  color: white;
}

.tm-header .badge{
  width: 36px;
  height: 36px;
  border-radius: 14px;
  background: rgba(255,255,255,0.18);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size: 18px;
}

.tm-header h1{
  font-size: 20px;
  line-height: 1.2;
  margin: 0;
  font-weight: 900;
}
.tm-header .subtitle{
  margin-top: 2px;
  font-size: 12px;
  opacity: 0.92;
  font-weight: 600;
}

/* Right slot inside header (for Clear Chat button) */
.tm-header-right{
  display:flex;
  align-items:center;
  justify-content:flex-end;
  min-width: 180px;
}

/* Clear Chat button styling when rendered inside .tm-header-right */
.tm-header-right .stButton > button{
  height: 38px !important;
  padding: 0 16px !important;
  border-radius: 999px !important;
  font-weight: 900 !important;
  background: rgba(15,23,42,0.92) !important;
  color: white !important;
  border: 1px solid rgba(255,255,255,0.15) !important;
  box-shadow: 0 10px 22px rgba(15, 23, 42, 0.18) !important;
}
.tm-header-right .stButton > button:hover{
  filter: brightness(1.05);
}

/* Make st.columns in header align nicely */
div[data-testid="stHorizontalBlock"]{
  gap: 12px;
}

/* ---------- Sidebar (Brand + Cards) ---------- */
.sb-brand{
  display:flex;
  align-items:center;
  gap:10px;
  margin-bottom: 10px;
}
.sb-brand .logo{
  width: 34px;
  height: 34px;
  border-radius: 12px;
  background: rgba(14,165,167,0.12);
  display:flex;
  align-items:center;
  justify-content:center;
  color: var(--brand1);
  font-size: 18px;
  font-weight: 900;
}
.sb-brand .name{
  font-weight: 900;
  color: var(--text);
  font-size: 18px;
}

.sb-card{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 14px;
  box-shadow: 0 8px 20px rgba(15,23,42,0.05);
  margin: 10px 0;
}
.sb-card h3{
  margin: 0 0 10px 0;
  font-size: 14px;
  font-weight: 900;
  color: var(--text);
}
.sb-muted{ color: var(--muted); font-size: 12px; }

.sb-status{
  border-radius: 14px;
  padding: 10px 12px;
  font-size: 12px;
  margin-top: 10px;
  border: 1px solid var(--border);
  background: #f8fafc;
  color: var(--text);
}
.sb-status.ok{
  border-color: rgba(34,197,94,0.35);
  background: rgba(34,197,94,0.08);
}
.sb-status.err{
  border-color: rgba(239,68,68,0.35);
  background: rgba(239,68,68,0.08);
}
.sb-doc{
  display:flex;
  gap:8px;
  align-items:center;
  padding: 8px 10px;
  border-radius: 12px;
  border: 1px dashed var(--border);
  background: #fbfdff;
  margin-top: 8px;
}
.sb-doc .dot{
  width: 10px; height: 10px; border-radius: 4px;
  background: rgba(34,197,94,0.85);
}

/* ---------- Chat Area ---------- */
.tm-chat-wrap{
  background: rgba(255,255,255,0.65);
  border: 1px solid rgba(229,231,235,0.8);
  border-radius: 18px;
  padding: 16px 14px;
  box-shadow: var(--shadow);
}

/* Bubble row */
.tm-row{
  display:flex;
  gap: 10px;
  align-items:flex-end;
  margin: 10px 0;
}
.tm-row.user{ justify-content:flex-end; }
.tm-row.bot{ justify-content:flex-start; }

/* Avatar - no external images */
.tm-avatar{
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: 1px solid rgba(15,23,42,0.10);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size: 18px;
  font-weight: 900;
  background: white;
  flex: 0 0 34px;
}
.tm-avatar.bot{ background: rgba(14,165,167,0.16); }
.tm-avatar.user{ background: rgba(34,197,94,0.16); }

/* Bubbles */
.tm-bubble{
  max-width: 74%;
  padding: 12px 14px;
  border-radius: 16px;
  font-size: 13.5px;
  line-height: 1.55;
  box-shadow: 0 8px 18px rgba(15,23,42,0.07);
  border: 1px solid transparent;
  white-space: pre-line;
}
.tm-bubble.user{
  background: var(--user);
  color: white;
  border-top-right-radius: 8px;
}
.tm-bubble.bot{
  background: var(--bot);
  color: var(--text);
  border: 1px solid var(--botBorder);
  border-top-left-radius: 8px;
}

/* Try chips */
.tm-try{
  display:flex;
  align-items:center;
  gap:10px;
  margin-top: 10px;
  color: var(--muted);
  font-size: 12px;
  flex-wrap: wrap;
}
.tm-chip{
  display:inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(15,23,42,0.10);
  background: rgba(255,255,255,0.85);
  cursor:pointer;
  font-weight: 900;
  color: #0f172a;
}
.tm-chip:hover{ background: white; }

/* Streamlit chat input - rounded bar */
div[data-testid="stChatInput"] textarea{
  border-radius: 999px !important;
  padding: 14px 16px !important;
  border: 1px solid rgba(15,23,42,0.10) !important;
  box-shadow: 0 10px 24px rgba(15,23,42,0.06) !important;
}
div[data-testid="stChatInput"] button{
  border-radius: 999px !important;
}
</style>
"""

# Header now supports a right-side slot for Clear Chat button
header_html = """
<div class="tm-header">
  <div class="title">
    <div class="badge">⚖️</div>
    <div>
      <h1>Legal Assistant</h1>
      <div class="subtitle">RAG multi-dokumen: pasal, kewajiban, sanksi, ringkasan</div>
    </div>
  </div>
  <div class="tm-header-right">
    
  </div>
</div>
"""

# Chat message templates (emoji avatar, no external images)
bot_template = """
<div class="tm-row bot">
  <div class="tm-avatar bot">⚖️</div>
  <div class="tm-bubble bot">{{MSG}}</div>
</div>
"""

user_template = """
<div class="tm-row user">
  <div class="tm-bubble user">{{MSG}}</div>
  <div class="tm-avatar user">👤</div>
</div>
"""
