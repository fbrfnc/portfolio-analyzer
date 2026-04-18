# ================================================
# Portfolio Analyzer - Script di Avvio Rapido
# Sprint 1.5
# ================================================

Write-Host "🚀 Avvio Portfolio Analyzer..." -ForegroundColor Cyan

# Verifica di essere nella cartella corretta
$projectPath = "C:\Users\fbrfn\Github\AnalisiPortafoglio\portfolio-analyzer"
if (-not (Test-Path $projectPath)) {
    Write-Host "❌ Cartella progetto non trovata!" -ForegroundColor Red
    pause
    exit
}

Set-Location $projectPath

# Attiva il venv
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "✅ Attivazione virtual environment..." -ForegroundColor Green
    & .\venv\Scripts\Activate.ps1
} else {
    Write-Host "❌ Virtual environment non trovato!" -ForegroundColor Red
    Write-Host "Esegui prima: py -3.12 -m venv venv" -ForegroundColor Yellow
    pause
    exit
}

# Avvia Streamlit
Write-Host "🌐 Avvio applicazione Streamlit..." -ForegroundColor Cyan
Write-Host "L'applicazione si aprirà nel browser automaticamente." -ForegroundColor Gray

streamlit run app\main.py --server.port=8501 --server.headless=true

# Se Streamlit si chiude, tieni aperta la finestra
Write-Host "`nApplicazione terminata." -ForegroundColor Yellow
pause