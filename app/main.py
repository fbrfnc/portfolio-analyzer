import streamlit as st
import pandas as pd
from datetime import datetime
from app.config import APP_TITLE, APP_ICON
from app.data.database import SessionLocal
from app.models.portfolio import PositionDB
from sqlalchemy.orm import Session

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

st.title(f"{APP_ICON} {APP_TITLE}")
st.markdown("### Sprint 1 - Gestione Portafoglio")

# Sidebar
pagina = st.sidebar.radio("Sezione", ["🏠 Dashboard", "📋 Gestione Posizioni"])

if pagina == "🏠 Dashboard":
    st.header("Dashboard Principale")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Valore Portafoglio", "€ 0,00", "0.0%")
    with col2:
        st.metric("Rendimento Totale", "0.00%", "0.0%")
    with col3:
        st.metric("Posizioni", "0")

    st.info("Dashboard con valori reali arriverà nello Sprint 3")

elif pagina == "📋 Gestione Posizioni":
    st.header("Gestione Posizioni")

    tab1, tab2 = st.tabs(["➕ Aggiungi Posizione", "📋 Lista Posizioni"])

    # TAB 1: Aggiungi
    with tab1:
        with st.form("nuova_posizione", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                ticker = st.text_input("Ticker / ISIN *", placeholder="AAPL o IT0001234567").upper().strip()
                name = st.text_input("Nome Strumento *")
                asset_type = st.selectbox("Tipo Asset *", ["Azione", "ETF", "Fondo"])
            with col2:
                quantity = st.number_input("Quantità *", min_value=0.0001, format="%.4f", value=1.0)
                cost_basis = st.number_input("Costo Medio (€) *", min_value=0.01, format="%.4f")
                currency = st.selectbox("Valuta", ["EUR", "USD"])
                category = st.text_input("Categoria (opzionale)")

            submitted = st.form_submit_button("💾 Salva Posizione", type="primary")
            
            if submitted:
                if not ticker or not name:
                    st.error("❌ Ticker e Nome sono obbligatori")
                else:
                    try:
                        db: Session = SessionLocal()
                        nuova_pos = PositionDB(
                            ticker=ticker,
                            name=name,
                            asset_type=asset_type,
                            quantity=quantity,
                            cost_basis=cost_basis,
                            currency=currency,
                            category=category if category.strip() else None,
                            purchase_dates=str(datetime.now().date())
                        )
                        db.add(nuova_pos)
                        db.commit()
                        st.success(f"✅ Posizione {ticker} salvata correttamente!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Errore: {str(e)}")
                    finally:
                        db.close()

    # TAB 2: Lista
    with tab2:
        st.subheader("Posizioni Attuali")
        db: Session = SessionLocal()
        posizioni = db.query(PositionDB).all()
        db.close()

        if posizioni:
            df = pd.DataFrame([{
                "Ticker": p.ticker,
                "Nome": p.name,
                "Tipo": p.asset_type,
                "Quantità": round(p.quantity, 4),
                "Costo Medio": f"€ {p.cost_basis:,.2f}",
                "Valuta": p.currency,
                "Categoria": p.category or "-"
            } for p in posizioni])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nessuna posizione presente. Aggiungine una dalla scheda 'Aggiungi Posizione'.")

st.caption("Sprint 1 completato - CRUD base delle posizioni")