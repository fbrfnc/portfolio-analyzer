# start.ps1 (nella root)
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Attiva venv (crea se non esiste)
if (-not (Test-Path "venv")) {
    py -3.12 -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
} else {
    .\venv\Scripts\Activate.ps1
}

# Inizializza DB esplicitamente
python -c "
import sys
sys.path.insert(0, '.')
from app.data.db import init_db
init_db()
print('Database inizializzato.')
"

# Avvia Streamlit
streamlit run app/main.py --server.headless true --server.port 8501