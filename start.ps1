# start.ps1 (root del repo)
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
cd $scriptPath

if (-not (Test-Path "venv")) {
    py -3.12 -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
} else {
    .\venv\Scripts\Activate.ps1
}

# init DB
python -c "from app.data.database import init_db; init_db()"

streamlit run app/main.py --server.headless true