from dataclasses import dataclass
from datetime import datetime

@dataclass
class Payment:
    membership_id: int
    amount: float
    payment_date: datetime = None
    status: str = 'pending'
    id: int = None
