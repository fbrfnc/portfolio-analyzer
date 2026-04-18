from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
import json

Base = declarative_base()

@dataclass
class Position:
    id: Optional[int] = None
    portfolio_id: int = 1
    ticker: str = ""
    name: str = ""
    asset_type: str = "ETF"   # Azione | ETF | Fondo
    quantity: float = 0.0
    cost_basis: float = 0.0   # costo medio ponderato
    currency: str = "EUR"
    commissions: float = 0.0
    category: Optional[str] = None
    purchase_dates: List[date] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "ticker": self.ticker.upper(),
            "name": self.name,
            "asset_type": self.asset_type,
            "quantity": self.quantity,
            "cost_basis": self.cost_basis,
            "currency": self.currency,
            "commissions": self.commissions,
            "category": self.category,
            "purchase_dates": [d.isoformat() for d in self.purchase_dates]
        }

class PortfolioDB(Base):
    __tablename__ = "portfolios"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    currency = Column(String(3), default="EUR")

class PositionDB(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    ticker = Column(String(20), nullable=False)
    name = Column(String(200))
    asset_type = Column(String(20))
    quantity = Column(Float, nullable=False)
    cost_basis = Column(Float, nullable=False)
    currency = Column(String(3), default="EUR")
    commissions = Column(Float, default=0.0)
    category = Column(String(100))
    purchase_dates = Column(Text)   # JSON string di date

    def __repr__(self):
        return f"<Position {self.ticker} - {self.quantity} @ {self.cost_basis}>"