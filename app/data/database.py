from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from app.config import DB_PATH
from app.models.portfolio import Base, PortfolioDB

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Crea tutte le tabelle"""
    Base.metadata.create_all(bind=engine)
    
    # Crea portafoglio di default se non esiste
    with SessionLocal() as session:
        if not session.query(PortfolioDB).first():
            default_portfolio = PortfolioDB(name="Principale", currency="EUR")
            session.add(default_portfolio)
            session.commit()
    
    print("✅ Database inizializzato con successo (Sprint 1)")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()