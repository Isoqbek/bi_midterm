"""
Orchestrator: user savolini tegishli agent(lar)ga yo'naltiradi.

Ishlash tartibi:
  1. Savoldagi kalit so'zlar bo'yicha mos agent(lar)ni tanlaydi.
  2. Agar Google Gemini API key mavjud bo'lsa -> LLM mos agentlar konteksti
     asosida tabiiy, yaxlit javob yozadi.
  3. Aks holda -> qoidaga asoslangan (rule-based) javoblarni birlashtiradi.

Shu tariqa ilova API key BO'LMASA HAM to'liq ishlaydi (deploy uchun muhim).
"""
import os
from agents.specialists import ALL_AGENTS

DEFAULT_MODEL = "gemini-2.5-flash"


def _get_api_key():
    """Streamlit secrets -> environment -> None.

    GEMINI_API_KEY yoki GOOGLE_API_KEY o'qiladi. Bo'sh (faqat probel) qiymat
    'yo'q' deb hisoblanadi, shunda ilova rule-based rejimga o'tadi.
    """
    names = ("GEMINI_API_KEY", "GOOGLE_API_KEY")
    try:
        import streamlit as st
        for name in names:
            if name in st.secrets and str(st.secrets[name]).strip():
                return st.secrets[name]
    except Exception:
        pass
    for name in names:
        val = os.environ.get(name)
        if val and val.strip():
            return val
    return None


def _get_model():
    """st.secrets'dan GEMINI_MODEL, aks holda DEFAULT_MODEL."""
    try:
        import streamlit as st
        if "GEMINI_MODEL" in st.secrets and str(st.secrets["GEMINI_MODEL"]).strip():
            return st.secrets["GEMINI_MODEL"]
    except Exception:
        pass
    return DEFAULT_MODEL


def route(query: str):
    """Savolga mos agentlar ro'yxati (ball bo'yicha)."""
    scored = [(a, a.matches(query)) for a in ALL_AGENTS]
    matched = [a for a, s in scored if s > 0]
    if not matched:               # hech narsa mos kelmasa -> hammasi (umumiy savol)
        return ALL_AGENTS
    return sorted(matched, key=lambda a: -dict(scored)[a])


def _llm_answer(query: str, agents, data, api_key: str) -> str | None:
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        context = "\n".join(a.context(data) for a in agents)
        system = (
            "Sen 'Business Intelligence Orchestrator'san. Quyidagi kompaniya "
            "ma'lumotlari asosida foydalanuvchi savoliga aniq, qisqa va raqamlarga "
            "asoslangan javob ber. Faqat berilgan ma'lumotlardan foydalan, "
            "ma'lumot yo'q bo'lsa ochiq ayt. O'zbek tilida javob ber."
        )
        resp = client.models.generate_content(
            model=_get_model(),
            contents=f"KOMPANIYA MA'LUMOTLARI:\n{context}\n\nSAVOL: {query}",
            config=types.GenerateContentConfig(
                system_instruction=system,
                max_output_tokens=700,
                temperature=0.3,
            ),
        )
        text = (resp.text or "").strip()
        return text or None
    except Exception:
        # Har qanday xatoda -> jim fallback (model, kvota, tarmoq va h.k.)
        return None


def answer(query: str, data) -> dict:
    """
    Returns: {"text": str, "agents": [agent names], "mode": "llm"|"rules"}
    """
    agents = route(query)
    api_key = _get_api_key()

    if api_key:
        llm = _llm_answer(query, agents, data, api_key)
        if llm:
            return {"text": llm,
                    "agents": [a.name for a in agents],
                    "mode": "llm"}

    # Rule-based fallback
    body = "\n\n".join(a.handle(query, data) for a in agents)
    header = ("Savolga bir nechta agent javob berdi:\n\n"
              if len(agents) > 1 else "")
    return {"text": header + body,
            "agents": [a.name for a in agents],
            "mode": "rules"}
