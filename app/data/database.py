from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import logging
from app.config import DB_PATH
from app.models.portfolio import Base, PortfolioDB

# Assicura che la cartella data esista
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Inizializzazione robusta del database"""
    try:
        Base.metadata.create_all(bind=engine)
        
        with SessionLocal() as session:
            if not session.query(PortfolioDB).first():
                default = PortfolioDB(name="Principale", currency="EUR")
                session.add(default)
                session.commit()
        
        print("Database inizializzato con successo (Sprint 1.5)")
        return True
    except Exception as e:
        print(f"Errore inizializzazione database: {e}")
        logging.error(str(e))
        return False

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()