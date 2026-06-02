# 🏢 Multi-Agent Business Intelligence System

Streamlit'da qurilgan ko'p-agentli biznes-tahlil platformasi. 5 ta sahifa va
barcha sahifalar uchun umumiy AI chat (agent orchestrator).

## Imkoniyatlar
- **Sidebar radio navigatsiya** — Dashboard, Sales, Inventory, Finance, HR
- **Har sahifada KPI metrics** (`st.columns` + `st.metric`) va alohida grafiklar
- **Umumiy chat** — pastda, har qanday savol; orchestrator mos agent(lar)ga yo'naltiradi
- **session_state** — navigatsiya va chat tarixi saqlanadi
- **LLM ixtiyoriy** — Google Gemini API key bo'lsa Gemini javob beradi, bo'lmasa
  rule-based (ilova doim ishlaydi)

## Lokal ishga tushirish
```bash
pip install -r requirements.txt
streamlit run app.py
```
Brauzerda `http://localhost:8501` ochiladi.

## (Ixtiyoriy) LLM rejimini yoqish
`.streamlit/secrets.toml.example` ni nusxalab `.streamlit/secrets.toml` qiling
(API key Google AI Studio'dan bepul olinadi: https://aistudio.google.com/apikey):
```toml
GEMINI_API_KEY = "AIza..."
```

## Streamlit Cloud'ga deploy
1. Loyihani GitHub repozitoriyga yuklang (`secrets.toml`siz).
2. https://share.streamlit.io → **New app** → repo + branch + `app.py`.
3. (Ixtiyoriy) **Advanced settings → Secrets**ga `GEMINI_API_KEY` qo' shing.
4. **Deploy** → live URL hosil bo'ladi.

## Struktura
```
app.py                  # kirish nuqtasi: nav + chat
requirements.txt
.streamlit/config.toml
agents/
  specialists.py        # 4 ta agent
  orchestrator.py       # routing + javob
data/mock_data.py       # mock biznes ma'lumotlari
views/                  # 5 ta sahifa
```
