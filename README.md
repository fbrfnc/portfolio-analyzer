# Portfolio Analyzer

Applicazione desktop per l'analisi e il monitoraggio di portafogli di investimento (Azioni, ETF, Fondi).

**Stato attuale:** Sprint 4.5 completato – Grafici aggiunti

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

# 5. Come avviare l'applicazione

### Metodo consigliato (più semplice)

1. Fai **doppio clic** sul file `start.bat` presente nella cartella del progetto.

2. La prima volta potrebbe apparire una finestra nera di comando:
   - Attende l'attivazione del virtual environment
   - Avvia automaticamente Streamlit
   - Apre il browser all'indirizzo `http://127.0.0.1:8501`

### Metodo alternativo (da PowerShell)

```powershell
cd "C:\Users\fbrfn\Github\AnalisiPortafoglio\portfolio-analyzer"
.\venv\Scripts\Activate.ps1
streamlit run app\main.py

# 6. Stato del progetto
**✅ Ecco il riepilogo chiaro e definitivo di tutti gli Sprint del progetto.**

### **Sprint 0 – Setup e Struttura** (Completato)
- Creazione della struttura cartelle (`app/`, `data/`, `build/`, ecc.)
- File di configurazione base (`config.py`)
- Modelli dati iniziali (`portfolio.py`)
- Database SQLite con SQLAlchemy (`database.py`)
- `requirements.txt` pulito e corretto
- Inizializzazione del database

### **Sprint 1.5 – Cleanup e Documentazione** (Completato)
- `.gitignore` professionale (venv, __pycache__, database.db, ecc.)
- `README.md` completo con istruzioni di installazione e roadmap
- Script di avvio rapido `start.ps1` e `start.bat`
- Miglioramento robustezza della inizializzazione DB
- Pulizia generale del repository

### **Sprint 2 – CRUD Posizioni Base** (Completato)
- Form per aggiungere nuove posizioni
- Lista delle posizioni
- Funzionalità di eliminazione
- Persistenza su SQLite

### **Sprint 3 – Valore Corrente + Miglioramento CRUD** (Completato)
- Integrazione con `yfinance` per scaricare prezzi reali
- Calcolo del **Valore Corrente** del portafoglio
- Tab "Modifica Posizione" completo
- Miglior gestione errori e messaggi utente

### **Sprint 4 – Metriche di Performance e Rischio** (Completato)
- Calcolo automatico del Valore Totale Portafoglio
- Metriche di Performance: Total Return, CAGR
- Metriche di Rischio: Volatilità annualizzata, Sharpe Ratio
- Pulsante di aggiornamento nella Dashboard
- Calcolo corretto della volatilità (ponderata per peso posizione)

### **Sprint 4.5 – Grafici** (Completato)
- Grafico evoluzione storica del valore del portafoglio (Plotly)
- Grafico a torta della allocazione attuale
- Integrazione dei grafici nella sezione Metriche

---

### Stato Finale del Progetto

**Completato al 100%:**
- Gestione completa delle posizioni (CRUD)
- Recupero prezzi da yfinance
- Calcolo valore corrente
- Metriche di performance e rischio
- Grafici interattivi
- Avvio rapido con `start.bat`
- Documentazione base

### Prossimi step

**Mancante (opzionale):**
- Packaging in .exe stabile (abbiamo provato più volte, ma Streamlit + PyInstaller è instabile)
- Test automatici
- Ottimizzazioni avanzate

---

