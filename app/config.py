"""Configurazione globale del Portfolio Analyzer"""

import os
from pathlib import Path

# Percorsi
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "portfolio.db"

# Config Streamlit
APP_TITLE = "Portfolio Analyzer"
APP_ICON = "📊"

# Cache
CACHE_DAYS_PRICES = 1
CACHE_DAYS_HISTORICAL = 30

# Benchmark predefiniti con ticker validi per yfinance (aprile 2026)
BENCHMARKS = {
    "MSCI World": "^990100-USD-STRD",      # Indice MSCI World ufficiale
    "Euro Stoxx 50": "^STOXX50E",
    "S&P 500": "^GSPC",
    "60/40 Portfolio": None               # Placeholder per calcolo custom futuro
}

# Risk-free rate di default (da aggiornare dinamicamente con ECB)
RISK_FREE_RATE = 0.035  # 3.5% placeholder