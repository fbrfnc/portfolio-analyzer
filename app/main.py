import streamlit as st
import logging
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

@st.cache_resource(show_spinner=False)
def initialize_db():
    init_db()

# Inizializzazione database robusta (chiamata una volta per sessione)
initialize_db()

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
                    except (yf.YFinanceError, ValueError) as e:
                        st.error(str(e))

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
                logging.error(str(e))

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

# ====================== METRICHE + GRAFICI MIGLIORATI ======================
else:
    st.header("📊 Metriche di Performance e Rischio")

    if st.button("Calcola Metriche e Grafici", type="primary"):
        with st.spinner("Calcolo metriche e generazione grafici..."):
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
                                # Rimuoviamo timezone per evitare errori
                                data.index = data.index.tz_localize(None)
                                
                                current_price = data['Close'].iloc[-1]
                                current_value = current_price * pos.quantity
                                total_value += current_value
                                total_cost += pos.quantity * pos.cost_basis

                                daily_ret = data['Close'].pct_change().dropna()
                                returns.append(daily_ret)

                                history_data[pos.ticker] = data['Close']
                        except:
                            pass

                    if total_cost > 0:
                        total_return_pct = (total_value - total_cost) / total_cost * 100

                        if returns:
                            all_returns = pd.concat(returns)
                            volatility = all_returns.std() * np.sqrt(252) * 100
                            sharpe = ((total_return_pct / 100) - RISK_FREE_RATE) / (volatility / 100) if volatility > 0 else 0

                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Valore Totale Portafoglio", f"€ {total_value:,.2f}", f"{total_return_pct:.1f}%")
                            with col2:
                                st.metric("Volatilità Annualizzata", f"{volatility:.1f}%")
                            with col3:
                                st.metric("Sharpe Ratio", f"{sharpe:.2f}")

                            st.metric("CAGR (approssimativo)", f"{total_return_pct:.1f}%")

                    # ==================== GRAFICI MIGLIORATI ====================

                    st.subheader("Grafici")

                    # Grafico 1: Evoluzione Valore Portafoglio
                    if history_data:
                        all_dates = pd.Index([])
                        for series in history_data.values():
                            all_dates = all_dates.union(series.index)

                        portfolio_value = pd.Series(0.0, index=all_dates)

                        for ticker, price_series in history_data.items():
                            pos = next((p for p in positions if p.ticker == ticker), None)
                            if pos:
                                aligned = price_series.reindex(all_dates, method='ffill')
                                portfolio_value += aligned * pos.quantity

                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=portfolio_value.index, 
                            y=portfolio_value.values,
                            mode='lines',
                            name='Valore Portafoglio',
                            line=dict(color='#00ff88', width=2.5)
                        ))
                        fig.update_layout(
                            title="Evoluzione Valore del Portafoglio nel Tempo",
                            xaxis_title="Data",
                            yaxis_title="Valore (€)",
                            template="plotly_dark",
                            height=500
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    # Grafico 2: Allocazione a Torta (migliorato)
                    if history_data:
                        labels = []
                        values = []
                        colors = ['#00ff88', '#ff0088', '#0088ff', '#ffff00', '#ff8800']

                        for pos in positions:
                            try:
                                current_price = yf.Ticker(pos.ticker).history(period="1d")['Close'].iloc[-1]
                                values.append(current_price * pos.quantity)
                                labels.append(f"{pos.ticker} ({pos.asset_type})")
                            except:
                                pass

                        if values:
                            fig2 = px.pie(
                                names=labels, 
                                values=values, 
                                title="Allocazione Attuale del Portafoglio",
                                color_discrete_sequence=colors
                            )
                            fig2.update_traces(textinfo='percent+label', textfont_size=14)
                            fig2.update_layout(height=500, template="plotly_dark")
                            st.plotly_chart(fig2, use_container_width=True)

                    # Grafico 3: Rendimento vs Volatilità (scatter semplice)
                    st.subheader("Rendimento vs Volatilità")
                    if len(positions) > 1:
                        tickers = [p.ticker for p in positions]
                        rets = []
                        vols = []
                        for t in tickers:
                            try:
                                data = yf.Ticker(t).history(period="1y")['Close']
                                ret = (data.iloc[-1] / data.iloc[0] - 1) * 100
                                vol = data.pct_change().std() * np.sqrt(252) * 100
                                rets.append(ret)
                                vols.append(vol)
                            except:
                                pass
                        
                        fig3 = px.scatter(
                            x=vols, y=rets,
                            text=tickers,
                            title="Rendimento vs Volatilità (1 anno)",
                            labels={"x": "Volatilità (%)", "y": "Rendimento (%)"}
                        )
                        fig3.update_layout(template="plotly_dark", height=400)
                        st.plotly_chart(fig3, use_container_width=True)

            except Exception as e:
                st.error(f"Errore durante il calcolo: {e}")

st.caption("Sprint 4.5 - Metriche + Grafici migliorati")