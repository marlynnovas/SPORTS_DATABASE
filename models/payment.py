from datetime import date

@dataclass
class Payment:
    member_id: int
    membership_id: int
    amount: float
    payment_date: date = None
    payment_status: str = "paid"  # paid, pending, failed
    id: int = None