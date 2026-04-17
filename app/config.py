from pathlib import Path

# Percorsi corretti
BASE_DIR = Path(__file__).parent.parent.absolute()
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "portfolio.db"

# Assicura che la cartella data esista
DATA_DIR.mkdir(parents=True, exist_ok=True)

APP_TITLE = "Portfolio Analyzer"
APP_ICON = "📊"

# Cache
CACHE_DAYS_PRICES = 1
CACHE_DAYS_HISTORICAL = 30

# Benchmark (ticker validi)
BENCHMARKS = {
    "MSCI World": "^990100-USD-STRD",
    "Euro Stoxx 50": "^STOXX50E",
    "S&P 500": "^GSPC",
    "60/40 Portfolio": None
}

RISK_FREE_RATE = 0.035