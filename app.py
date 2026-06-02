"""
🏢 Multi-Agent Business Intelligence System
--------------------------------------------
- Sidebar radio navigation (5 ta sahifa)
- Har sahifada o'ziga xos KPI metrics + charts
- Pastda BARCHA sahifalar uchun umumiy chat interface
- Agent orchestrator user savoliga javob beradi
- session_state orqali navigatsiya va chat tarixi saqlanadi
"""
import streamlit as st

from data.mock_data import generate_data
from agents.orchestrator import answer, _get_model
from views import dashboard, sales, inventory, finance, hr

st.set_page_config(
    page_title="Multi-Agent BI System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------- DATA (cached) -----------------------
@st.cache_data
def load_data():
    return generate_data()

data = load_data()

# ----------------------- SESSION STATE -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ----------------------- SIDEBAR -----------------------
with st.sidebar:
    st.title("🏢 BI Platform")
    st.caption("Multi-Agent Business Intelligence")

    PAGES = {
        "Dashboard": ("📊", dashboard),
        "Sales Analysis": ("📈", sales),
        "Inventory": ("📦", inventory),
        "Finance": ("💰", finance),
        "HR Analytics": ("👥", hr),
    }

    page = st.radio(
        "Navigatsiya",
        list(PAGES.keys()),
        format_func=lambda p: f"{PAGES[p][0]}  {p}",
        key="page",
    )

    st.divider()
    try:
        api_ok = any(
            k in st.secrets and str(st.secrets[k]).strip()
            for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY")
        )
    except Exception:
        api_ok = False
    st.caption("🤖 Orchestrator rejimi:")
    if api_ok:
        st.success("LLM (Gemini) yoqilgan")
        st.caption(f"Model: {_get_model()}")
    else:
        st.info("Rule-based (API key yo'q)")

    if st.button("🗑️ Chatni tozalash", width="stretch"):
        st.session_state.messages = []
        st.rerun()

# ----------------------- PAGE CONTENT -----------------------
PAGES[page][1].render(data)

# ----------------------- COMMON CHAT (bottom) -----------------------
st.divider()
st.subheader("💬 Agent Orchestrator — savol bering")
st.caption("Masalan: \"Eng kuchli hudud qaysi?\", \"Foyda marjasi qancha?\", "
           "\"Qaysi tovarlar kam qoldi?\", \"Nechta xodim bor?\"")

# Chat tarixini ko'rsatish
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("agents"):
            st.caption("Javob bergan agent(lar): " + ", ".join(msg["agents"]))

# Yangi savol
if prompt := st.chat_input("Savolingizni yozing..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Orchestrator agentlarga yo'naltirmoqda..."):
            result = answer(prompt, data)
        st.markdown(result["text"])
        st.caption("Javob bergan agent(lar): " + ", ".join(result["agents"]))

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["text"],
        "agents": result["agents"],
    })
