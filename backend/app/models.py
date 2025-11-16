from sqlmodel import SQLModel, Field
from typing import Optional
import datetime

class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str  # 'buyer' or 'seller' requesting session
    buyer_address: Optional[str] = None
    seller_address: Optional[str] = None
    target_price: Optional[float] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    quantity: Optional[int] = None
    fairness_weight: Optional[float] = 0.5
    max_rounds: Optional[int] = 8
    concession_rate: Optional[float] = 0.05  # User-configurable
    aggressiveness: Optional[float] = 0.5  # User-configurable (0-1)
    market_symbol: Optional[str] = None  # Market context
    market_asset_type: Optional[str] = None  # stock|crypto|forex
    market_price: Optional[float] = None  # Cached market price
    status: str = "open"
    blockchain_tx_hash: Optional[str] = None  # Blockchain transaction hash
    blockchain_block_number: Optional[int] = None  # Block number
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class Offer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int
    round: int
    made_by: str
    price: float
    quantity: int
    fairness: float  # Simple fairness
    proportional_fairness: Optional[float] = None  # Proportional fairness
    utility: float
    explanation: Optional[str] = None  # Explainability
    tom_insights: Optional[str] = None  # Theory of Mind data (JSON string)
    payload: Optional[str] = None

class Agreement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int
    price: float
    quantity: int
    agreement_hash: str
    final_fairness: Optional[float] = None  # Simple fairness
    final_proportional_fairness: Optional[float] = None  # Proportional fairness
    buyer_utility: Optional[float] = None
    seller_utility: Optional[float] = None
    blockchain_tx_hash: Optional[str] = None  # Blockchain transaction hash
    blockchain_block_number: Optional[int] = None  # Block number
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
