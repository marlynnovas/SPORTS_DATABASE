from dataclasses import dataclass
from datetime import datetime

@dataclass
class Member:
    first_name: str
    last_name: str
    email: str
    phone: str = None
    id: int = None
    created_at: datetime = None
