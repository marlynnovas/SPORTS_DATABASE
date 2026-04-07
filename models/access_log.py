from dataclasses import dataclass
from datetime import datetime

@dataclass
class AccessLog:
    member_id: int
    result: str  # granted, denied
    access_date: datetime = None
    message: str = None
    id: int = None