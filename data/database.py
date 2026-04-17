import sqlite3
from sqlalchemy import create_engine, text
from pathlib import Path
from app.config import DB_PATH

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

def init_db():
    """Crea tutte le tabelle se non esistono"""
    with engine.connect() as conn:
        # Portafogli
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS portfolios (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                currency TEXT DEFAULT 'EUR'
            )
        """))
        
        # Posizioni
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY,
                portfolio_id INTEGER,
                ticker TEXT NOT NULL,
                name TEXT,
                asset_type TEXT CHECK(asset_type IN ('Azione', 'ETF', 'Fondo')),
                quantity REAL NOT NULL,
                cost_basis REAL NOT NULL,
                currency TEXT DEFAULT 'EUR',
                commissions REAL DEFAULT 0,
                category TEXT,
                purchase_dates TEXT,   -- JSON array di date ISO
                FOREIGN KEY(portfolio_id) REFERENCES portfolios(id)
            )
        """))
        
        # Cache prezzi
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS price_history (
                ticker TEXT NOT NULL,
                date TEXT NOT NULL,
                close_price REAL NOT NULL,
                dividend REAL DEFAULT 0,
                currency TEXT DEFAULT 'EUR',
                PRIMARY KEY (ticker, date)
            )
        """))
        
        # Tassi di cambio ECB (multi-valuta)
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS exchange_rates (
                date TEXT NOT NULL,
                from_currency TEXT NOT NULL,
                to_currency TEXT NOT NULL,
                rate REAL NOT NULL,
                PRIMARY KEY (date, from_currency, to_currency)
            )
        """))
        
        conn.commit()
    
    print("✅ Database inizializzato correttamente con tutte le tabelle previste nelle specifiche.")

if __name__ == "__main__":
    init_db()