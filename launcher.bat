@echo off
title Portfolio Analyzer

echo ================================================
echo    Portfolio Analyzer - Avvio
echo ================================================
echo.

:: Vai nella cartella del progetto
cd /d "%~dp0"

:: Attiva il virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo ✓ Virtual environment attivato
) else (
    echo ERRORE: Virtual environment non trovato!
    echo Esegui prima: py -3.12 -m venv venv
    pause
    exit /b 1
)

:: Imposta PYTHONPATH (importante per riconoscere il package 'app')
set PYTHONPATH=.

echo.
echo Avvio applicazione Streamlit...
echo (si aprirà automaticamente nel browser)
echo.

:: Avvia Streamlit
streamlit run app\main.py ^
    --server.headless=true ^
    --server.port=8501 ^
    --server.address=127.0.0.1 ^
    --logger.level=error

pause