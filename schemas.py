from pydantic import BaseModel
from datetime import date
from enum import Enum

class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class UserCreate(BaseModel):
    name: str
    email: str

class TransactionCreate(BaseModel):
    user_id: int
    symbol: str
    type: TransactionType
    units: float
    price: float
    date: date

class PortfolioHolding(BaseModel):
    symbol: str
    units: float
    avg_cost: float
    current_price: float
    unrealized_pl: float

class PortfolioSummary(BaseModel):
    user_id: int
    holdings: list[PortfolioHolding]
    total_value: float
    total_gain: float
