# CLAUDE.md — Multi-Agent Business Intelligence System

Bu fayl **Claude Code** uchun loyiha xotirasi (project memory). Claude Code har
safar shu papkada ishlaganda bu faylni avtomatik o'qiydi va quyidagi qoidalarga
amal qiladi.

## Loyiha maqsadi
Streamlit'da ko'p-agentli (multi-agent) Business Intelligence platforma.
5 ta sahifa (Dashboard, Sales, Inventory, Finance, HR) + barcha sahifalar uchun
umumiy chat interfeysi. Chat savollarini "orchestrator" tegishli agentlarga
yo'naltiradi.

## Arxitektura
- `app.py` — kirish nuqtasi. Sidebar `st.radio` navigatsiya, `st.session_state`,
  sahifani render qilish, pastda umumiy `st.chat_input` chat.
- `views/` — har bir sahifa alohida modul, har birida `render(data)` funksiyasi.
- `agents/specialists.py` — SalesAgent, InventoryAgent, FinanceAgent, HRAgent.
  Har birida `keywords`, `context(data)`, `handle(query, data)`.
- `agents/orchestrator.py` — `route()` + `answer()`. API key bo'lsa LLM,
  bo'lmasa rule-based.
- `data/mock_data.py` — `generate_data()` seed bilan barqaror ma'lumot qaytaradi.

## Muhim qoidalar (Claude Code BULARGA AMAL QILSIN)
1. **Ilova API key BO'LMASA HAM ishlashi shart.** `st.secrets`ga murojaat
   doimo `try/except` ichida bo'lsin (aks holda secrets.toml yo'q bo'lsa ilova
   ishdan chiqadi).
2. KPI metrics har doim `st.columns` + `st.metric` orqali ko'rsatiladi.
3. Navigatsiya `st.sidebar.radio` (Streamlit'ning `pages/` papkasidan
   FOYDALANILMAYDI — talab radio navigatsiya).
4. Chat tarixi `st.session_state.messages` da saqlanadi.
5. Yangi agent qo'shilsa: `specialists.py`da klass yarating, `ALL_AGENTS`ga
   qo'shing, `keywords` (EN va UZ) bering.
6. `.streamlit/secrets.toml` hech qachon Git'ga yuborilmaydi (`.gitignore`da bor).
7. Yangi kutubxona qo'shilsa, `requirements.txt`ga ham yozilsin.

## Tekshirish (har o'zgartirishdan keyin)
```bash
python -m py_compile app.py agents/*.py data/*.py views/*.py
python -c "from streamlit.testing.v1 import AppTest; \
at=AppTest.from_file('app.py').run(); assert not at.exception, at.exception; print('OK')"
```

## Lokal ishga tushirish
```bash
pip install -r requirements.txt
streamlit run app.py
```
