from dataclasses import dataclass
from datetime import date

@dataclass
class Member:
    full_name: str
    phone: str = None
    email: str = None
    join_date: date = None
    id: int = None