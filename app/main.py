import streamlit as st
from app.config import APP_TITLE, APP_ICON
from app.data.database import init_db

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inizializzazione DB
if "db_initialized" not in st.session_state:
    init_db()
    st.session_state.db_initialized = True

st.title(f"{APP_ICON} {APP_TITLE}")
st.markdown("### Analisi professionale del tuo portafoglio di investimenti")

st.success("✅ Sprint 0 completato e corretto! Database e configurazione pronti.")

st.info("""
**Stato attuale:**  
- Struttura progetto pronta  
- Database SQLite con tutte le tabelle (inclusa exchange_rates)  
- Configurazione benchmark corretta  

**Prossimo Sprint (1):**  
- CRUD completo delle posizioni (inserimento, modifica, eliminazione)  
- Dashboard valore portafoglio attuale  
- Caricamento da CSV semplice
""")

# Sidebar navigazione (più robusta)
st.sidebar.title("Navigazione")
st.sidebar.markdown("### 📊 Portfolio Analyzer")

if st.sidebar.button("🏠 Home", use_container_width=True):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Sprint 0 - Setup completato")