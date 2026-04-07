from dataclasses import dataclass
from datetime import datetime

@dataclass
class AccessLog:
    member_id: int
    granted: bool
    access_time: datetime = None
    message: str = None
    id: int = None
