from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional, Dict
import json

@dataclass
class Position:
    id: Optional[int] = None
    portfolio_id: int = 1
    ticker: str = ""                    # ISIN o Ticker
    name: str = ""
    asset_type: str = "ETF"             # Azione | ETF | Fondo
    quantity: float = 0.0
    cost_basis: float = 0.0             # costo medio
    currency: str = "EUR"
    purchase_dates: List[date] = field(default_factory=list)
    commissions: float = 0.0
    category: Optional[str] = None      # settore, regione, stile

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "ticker": self.ticker,
            "name": self.name,
            "asset_type": self.asset_type,
            "quantity": self.quantity,
            "cost_basis": self.cost_basis,
            "currency": self.currency,
            "purchase_dates": [d.isoformat() for d in self.purchase_dates],
            "commissions": self.commissions,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        data["purchase_dates"] = [date.fromisoformat(d) for d in data.get("purchase_dates", [])]
        return cls(**data)


@dataclass
class Portfolio:
    id: int = 1
    name: str = "Principale"
    currency: str = "EUR"
    positions: List[Position] = field(default_factory=list)