import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
from app.config import APP_TITLE, APP_ICON, RISK_FREE_RATE
from app.data.database import SessionLocal, init_db
from app.models.portfolio import PositionDB
from sqlalchemy.orm import Session
import plotly.express as px
import plotly.graph_objects as go

# Inizializzazione database robusta
init_db()

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

st.title(f"{APP_ICON} {APP_TITLE}")
st.markdown("### Sprint 4.5 - Metriche + Grafici")

pagina = st.sidebar.radio("Sezione", ["🏠 Dashboard", "📋 Gestione Posizioni", "📊 Metriche & Grafici"])

# ====================== DASHBOARD ======================
if pagina == "🏠 Dashboard":
    st.header("Dashboard Principale")

    if st.button("🔄 Aggiorna Dashboard", type="primary"):
        with st.spinner("Aggiornamento in corso..."):
            try:
                db = SessionLocal()
                positions = db.query(PositionDB).all()
                db.close()

                total_value = 0.0
                total_cost = 0.0

                for pos in positions:
                    try:
                        price = yf.Ticker(pos.ticker).history(period="1d")['Close'].iloc[-1]
                        total_value += price * pos.quantity
                        total_cost += pos.quantity * pos.cost_basis
                    except:
                        pass

                if total_cost > 0:
                    total_return = ((total_value - total_cost) / total_cost) * 100
                    st.metric("Valore Portafoglio", f"€ {total_value:,.2f}", f"{total_return:.1f}%")
                    st.metric("Rendimento Totale", f"{total_return:.2f}%")
                    st.metric("Numero Posizioni", len(positions))
                    st.success("Dashboard aggiornata")
                else:
                    st.info("Nessuna posizione nel portafoglio")

            except Exception as e:
                st.error(f"Errore: {e}")

# ====================== GESTIONE POSIZIONI ======================
elif pagina == "📋 Gestione Posizioni":
    st.header("Gestione Posizioni")

    tab1, tab2, tab3, tab4 = st.tabs(["➕ Aggiungi", "📋 Lista", "✏️ Modifica", "🗑️ Elimina"])

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

    with tab3:
        st.subheader("✏️ Modifica Posizione")
        db = SessionLocal()
        positions = db.query(PositionDB).all()
        db.close()
        if positions:
            selected_ticker = st.selectbox("Seleziona posizione da modificare", [p.ticker for p in positions])
            
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
                        p = db.query(PositionDB).filter(PositionDB.ticker == selected_ticker).first()
                        if p:
                            p.name = new_name
                            p.quantity = new_quantity
                            p.cost_basis = new_cost_basis
                            p.category = new_category if new_category.strip() else None
                            db.commit()
                            st.success(f"✅ {selected_ticker} modificata!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Errore: {e}")
                    finally:
                        db.close()
        else:
            st.info("Nessuna posizione da modificare.")

    with tab4:
        st.subheader("🗑️ Elimina Posizione")
        db = SessionLocal()
        positions = db.query(PositionDB).all()
        db.close()
        if positions:
            ticker_to_delete = st.selectbox("Seleziona da eliminare", [p.ticker for p in positions])
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

# ====================== METRICHE + GRAFICI ======================
else:
    st.header("📊 Metriche di Performance e Rischio")

    if st.button("Calcola Metriche e Grafici", type="primary"):
        with st.spinner("Calcolo e generazione grafici..."):
            try:
                db = SessionLocal()
                positions = db.query(PositionDB).all()
                db.close()

                if not positions:
                    st.warning("Nessuna posizione nel portafoglio")
                else:
                    total_value = 0.0
                    total_cost = 0.0
                    returns = []
                    history_data = {}

                    for pos in positions:
                        try:
                            data = yf.Ticker(pos.ticker).history(period="1y")
                            if not data.empty:
                                current_price = data['Close'].iloc[-1]
                                current_value = current_price * pos.quantity
                                total_value += current_value
                                total_cost += pos.quantity * pos.cost_basis

                                daily_ret = data['Close'].pct_change().dropna()
                                returns.append(daily_ret)

                                # Salva storico per grafici
                                history_data[pos.ticker] = data['Close']
                        except:
                            pass

                    if total_cost > 0:
                        total_return_pct = (total_value - total_cost) / total_cost * 100

                        if returns:
                            all_returns = pd.concat(returns)
                            volatility = all_returns.std() * np.sqrt(252) * 100
                            sharpe = ((total_return_pct / 100) - RISK_FREE_RATE) / (volatility / 100) if volatility > 0 else 0

                            # Calcolo CAGR corretto
                            start_date = max([df.index.min() for df in history_data.values()])
                            end_date = min([df.index.max() for df in history_data.values()])
                            days = (end_date - start_date).days
                            years = days / 365.25
                            cagr = (1 + total_return_pct / 100) ** (1 / years) - 1 if years > 0 else 0

                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Valore Totale Portafoglio", f"€ {total_value:,.2f}", f"{total_return_pct:.1f}%")
                            with col2:
                                st.metric("Volatilità Annualizzata", f"{volatility:.1f}%")
                            with col3:
                                st.metric("Sharpe Ratio", f"{sharpe:.2f}")

                            st.metric("CAGR (approssimativo)", f"{cagr * 100:.1f}%")

                    # ==================== GRAFICI ====================
                    st.subheader("Grafici")

                    # Grafico 1: Evoluzione valore portafoglio (approssimativo)
                    if history_data:
                        # Creiamo un indice temporale comune
                        dates = pd.date_range(start=max([df.index.min() for df in history_data.values()]),
                                              end=min([df.index.max() for df in history_data.values()]), freq='D')
                        
                        portfolio_value = pd.Series(0, index=dates)
                        for ticker, price_series in history_data.items():
                            # Trova la posizione corrispondente
                            pos = next((p for p in positions if p.ticker == ticker), None)
                            if pos:
                                portfolio_value += price_series.reindex(dates, method='ffill') * pos.quantity

                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=portfolio_value.index, y=portfolio_value.values, 
                                               mode='lines', name='Valore Portafoglio'))
                        fig.update_layout(title="Evoluzione Valore Portafoglio", xaxis_title="Data", yaxis_title="Valore (€)")
                        st.plotly_chart(fig, use_container_width=True)

                    # Grafico 2: Allocazione attuale (a torta)
                    labels = []
                    values = []
                    for p in positions:
                        try:
                            hist = yf.Ticker(p.ticker).history(period="1d")
                            price = hist['Close'].iloc[-1] if not hist.empty else None
                        except:
                            price = None
                        if price is not None:
                            labels.append(p.ticker)
                            values.append(p.quantity * price)

                    fig2 = px.pie(names=labels, values=values, title="Allocazione Portafoglio")
                    st.plotly_chart(fig2, use_container_width=True)

            except Exception as e:
                st.error(f"Errore: {e}")

st.caption("Sprint 4.5 - Metriche + Grafici completati")