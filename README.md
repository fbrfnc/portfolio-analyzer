# Portfolio Analyzer

Applicazione desktop per l'analisi e il monitoraggio di portafogli di investimento (Azioni, ETF, Fondi).

**Stato attuale:** Sprint 1.5 completato

## Requisiti

- Python 3.12
- Windows 11 (testato)

## Installazione

```powershell
# 1. Clona il repository
git clone https://github.com/fbrfnc/portfolio-analyzer.git
cd portfolio-analyzer

# 2. Crea virtual environment
py -3.12 -m venv venv

# 3. Attiva il venv
.\venv\Scripts\Activate.ps1

# 4. Installa dipendenze
pip install -r requirements.txt

# 5. Avvia l'applicazione
streamlit run app/main.py

# 6. Stato del progetto
**✅ Ecco il riepilogo chiaro e dettagliato dei 4 Sprint.**

### Sprint 0 – Setup e Struttura (Completato)
- Creazione struttura cartelle (`app/`, `data/`, ecc.)
- `requirements.txt` pulito e corretto
- Configurazione base (`config.py`)
- Modelli base (`portfolio.py`)
- Database SQLite con tabelle (`portfolios`, `positions`)
- Inizializzazione DB
- `start.ps1` per avvio rapido
- `.gitignore` corretto

### Sprint 1.5 – Cleanup e Documentazione (Completato)
- `.gitignore` professionale (ignora venv, pycache, database.db, ecc.)
- `README.md` completo con istruzioni di installazione e roadmap
- Inizializzazione DB resa più robusta
- Creazione script `start.ps1` per doppio clic
- Pulizia generale del repository

### Sprint 2 – CRUD Posizioni Base (Completato)
- Inserimento nuova posizione (form completo)
- Visualizzazione lista posizioni
- Eliminazione posizione
- Persistenza su SQLite con SQLAlchemy

### Sprint 3 – Valore Corrente + Miglioramento CRUD (Completato)
- Integrazione `yfinance` per scaricare prezzi reali
- Calcolo **Valore Corrente** del portafoglio
- Tab "Modifica Posizione" completo
- Miglior gestione errori
- Pulsante "Aggiorna Prezzi"

### Sprint 4 – Metriche di Performance e Rischio (Completato)
- Calcolo automatico del **Valore Totale Portafoglio** nella sezione Metriche
- Metriche di Performance:
  - Rendimento Totale
  - CAGR (approssimativo)
- Metriche di Rischio:
  - Volatilità Annualizzata
  - Sharpe Ratio (con risk-free rate)
- Pulsante "Ricalcola Metriche"
- Dashboard con aggiornamento manuale

---

### Stato Attuale del Progetto

**Completato:**
- Gestione completa delle posizioni (Aggiungi, Lista, Modifica, Elimina)
- Recupero prezzi reali da yfinance
- Calcolo Valore Corrente
- Metriche di Performance e Rischio (Valore Totale, Volatilità, Sharpe, CAGR)
- Dashboard base
- Avvio rapido con `start.ps1`
- Documentazione base

**Mancante (opzionale per MVP):**
- Grafici Plotly (evoluzione nel tempo)
- Packaging in .exe con PyInstaller
- Cache per yfinance (per velocizzare)
- Gestione multi-portafoglio avanzata
- Test automatici

---
