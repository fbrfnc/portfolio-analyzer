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