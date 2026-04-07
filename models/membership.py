from dataclasses import dataclass
from datetime import date

@dataclass
class Membership:
    member_id: int
    plan_id: int
    start_date: date
    end_date: date
    status: str = 'active'
    id: int = None
