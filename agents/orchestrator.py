"""
Orchestrator: user savolini tegishli agent(lar)ga yo'naltiradi.

Ishlash tartibi:
  1. Savoldagi kalit so'zlar bo'yicha mos agent(lar)ni tanlaydi.
  2. Agar Anthropic API key mavjud bo'lsa -> LLM mos agentlar konteksti asosida
     tabiiy, yaxlit javob yozadi.
  3. Aks holda -> qoidaga asoslangan (rule-based) javoblarni birlashtiradi.

Shu tariqa ilova API key BO'LMASA HAM to'liq ishlaydi (deploy uchun muhim).
"""
import os
from agents.specialists import ALL_AGENTS


def _get_api_key():
    # Streamlit secrets -> environment -> None
    try:
        import streamlit as st
        if "ANTHROPIC_API_KEY" in st.secrets:
            return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass
    return os.environ.get("ANTHROPIC_API_KEY")


def route(query: str):
    """Savolga mos agentlar ro'yxati (ball bo'yicha)."""
    scored = [(a, a.matches(query)) for a in ALL_AGENTS]
    matched = [a for a, s in scored if s > 0]
    if not matched:               # hech narsa mos kelmasa -> hammasi (umumiy savol)
        return ALL_AGENTS
    return sorted(matched, key=lambda a: -dict(scored)[a])


def _llm_answer(query: str, agents, data, api_key: str) -> str | None:
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        context = "\n".join(a.context(data) for a in agents)
        system = (
            "Sen 'Business Intelligence Orchestrator'san. Quyidagi kompaniya "
            "ma'lumotlari asosida foydalanuvchi savoliga aniq, qisqa va raqamlarga "
            "asoslangan javob ber. Faqat berilgan ma'lumotlardan foydalan, "
            "ma'lumot yo'q bo'lsa ochiq ayt. O'zbek tilida javob ber."
        )
        model = "claude-sonnet-4-20250514"
        try:
            import streamlit as st
            model = st.secrets.get("ANTHROPIC_MODEL", model)
        except Exception:
            pass

        resp = client.messages.create(
            model=model,
            max_tokens=700,
            system=system,
            messages=[{
                "role": "user",
                "content": f"KOMPANIYA MA'LUMOTLARI:\n{context}\n\nSAVOL: {query}",
            }],
        )
        parts = [b.text for b in resp.content if getattr(b, "type", "") == "text"]
        return "\n".join(parts).strip() or None
    except Exception as e:
        # Har qanday xatoda -> fallback. (model, kvota, tarmoq va h.k.)
        return f"⚠️ LLM DEBUG: {type(e).__name__}: {e}"


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
