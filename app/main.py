import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
from app.config import APP_TITLE, APP_ICON
from app.data.database import SessionLocal
from app.models.portfolio import PositionDB
from sqlalchemy.orm import Session

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

st.title(f"{APP_ICON} {APP_TITLE}")
st.markdown("### Sprint 3 - Valore Corrente + CRUD Completo")

pagina = st.sidebar.radio("Sezione", ["🏠 Dashboard", "📋 Gestione Posizioni", "📈 Valore Corrente"])

if pagina == "🏠 Dashboard":
    st.header("Dashboard Principale")
    st.info("Valori reali e metriche nello Sprint 4")

elif pagina == "📋 Gestione Posizioni":
    st.header("Gestione Posizioni")

    tab1, tab2, tab3, tab4 = st.tabs(["➕ Aggiungi", "📋 Lista", "✏️ Modifica", "🗑️ Elimina"])

    # 1. Aggiungi
    with tab1:
        with st.form("add_position", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                ticker = st.text_input("Ticker / ISIN *").upper().strip()
                name = st.text_input("Nome Strumento *")
                asset_type = st.selectbox("Tipo Asset *", ["Azione", "ETF", "Fondo"])
            with col2:
                quantity = st.number_input("Quantità *", min_value=0.0001, format="%.4f")
                cost_basis = st.number_input("Costo Medio (€) *", min_value=0.01, format="%.4f")
                currency = st.selectbox("Valuta", ["EUR", "USD"])
                category = st.text_input("Categoria (opzionale)")

            if st.form_submit_button("💾 Salva Posizione", type="primary"):
                if not ticker or not name:
                    st.error("Ticker e Nome obbligatori")
                else:
                    try:
                        db = SessionLocal()
                        pos = PositionDB(
                            ticker=ticker, name=name, asset_type=asset_type,
                            quantity=quantity, cost_basis=cost_basis,
                            currency=currency, category=category or None,
                            purchase_dates=str(datetime.now().date())
                        )
                        db.add(pos)
                        db.commit()
                        st.success(f"✅ {ticker} salvata")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Errore: {e}")
                    finally:
                        db.close()

    # 2. Lista
    with tab2:
        st.subheader("Lista Posizioni")
        db = SessionLocal()
        positions = db.query(PositionDB).all()
        db.close()
        if positions:
            df = pd.DataFrame([{
                "ID": p.id,
                "Ticker": p.ticker,
                "Nome": p.name,
                "Tipo": p.asset_type,
                "Quantità": p.quantity,
                "Costo Medio": f"€ {p.cost_basis:.2f}",
                "Valuta": p.currency
            } for p in positions])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nessuna posizione presente.")

    # 3. Modifica (NUOVA)
    with tab3:
        st.subheader("✏️ Modifica Posizione")
        db = SessionLocal()
        positions = db.query(PositionDB).all()
        db.close()

        if positions:
            selected_ticker = st.selectbox("Seleziona posizione da modificare", [p.ticker for p in positions])
            
            # Carica i dati attuali
            db = SessionLocal()
            pos = db.query(PositionDB).filter(PositionDB.ticker == selected_ticker).first()
            db.close()

            with st.form("edit_position"):
                new_name = st.text_input("Nome Strumento", value=pos.name)
                new_quantity = st.number_input("Quantità", value=pos.quantity, format="%.4f")
                new_cost_basis = st.number_input("Costo Medio (€)", value=pos.cost_basis, format="%.4f")
                new_category = st.text_input("Categoria", value=pos.category or "")

                if st.form_submit_button("💾 Salva Modifiche", type="primary"):
                    try:
                        db = SessionLocal()
                        pos_to_update = db.query(PositionDB).filter(PositionDB.ticker == selected_ticker).first()
                        if pos_to_update:
                            pos_to_update.name = new_name
                            pos_to_update.quantity = new_quantity
                            pos_to_update.cost_basis = new_cost_basis
                            pos_to_update.category = new_category if new_category else None
                            db.commit()
                            st.success(f"✅ {selected_ticker} modificata con successo!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Errore modifica: {e}")
                    finally:
                        db.close()
        else:
            st.info("Nessuna posizione da modificare.")

    # 4. Elimina
    with tab4:
        st.subheader("🗑️ Elimina Posizione")
        db = SessionLocal()
        positions = db.query(PositionDB).all()
        db.close()

        if positions:
            ticker_to_delete = st.selectbox("Seleziona posizione da eliminare", [p.ticker for p in positions])
            if st.button("🗑️ Elimina Posizione", type="secondary"):
                try:
                    db = SessionLocal()
                    pos = db.query(PositionDB).filter(PositionDB.ticker == ticker_to_delete).first()
                    if pos:
                        db.delete(pos)
                        db.commit()
                        st.success(f"✅ {ticker_to_delete} eliminata")
                        st.rerun()
                except Exception as e:
                    st.error(f"Errore: {e}")
                finally:
                    db.close()
        else:
            st.info("Nessuna posizione da eliminare.")

# ====================== VALORE CORRENTE ======================
else:
    st.header("📈 Valore Corrente del Portafoglio")

    if st.button("🔄 Aggiorna Prezzi", type="primary"):
        with st.spinner("Scaricamento prezzi da yfinance..."):
            try:
                db = SessionLocal()
                positions = db.query(PositionDB).all()
                total_value = 0.0
                rows = []

                for pos in positions:
                    try:
                        ticker_data = yf.Ticker(pos.ticker)
                        price = ticker_data.history(period="1d")['Close'].iloc[-1]
                        current_value = price * pos.quantity
                        total_value += current_value

                        rows.append({
                            "Ticker": pos.ticker,
                            "Nome": pos.name,
                            "Quantità": pos.quantity,
                            "Prezzo Attuale": round(price, 4),
                            "Valore Corrente (€)": round(current_value, 2),
                            "Costo Medio": pos.cost_basis,
                            "Guadagno/Perdita (€)": round(current_value - pos.quantity * pos.cost_basis, 2)
                        })
                    except:
                        rows.append({"Ticker": pos.ticker, "Errore": "Prezzo non disponibile"})

                st.success(f"Valore Totale Portafoglio: **€ {total_value:,.2f}**")
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

            except Exception as e:
                st.error(f"Errore: {e}")

st.caption("Sprint 3 - Valore Corrente + CRUD completo con modifica")