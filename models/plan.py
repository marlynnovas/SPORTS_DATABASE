from dataclasses import dataclass

@dataclass
class Plan:
    name: str
    price: float
    duration_months: int
    id: int = None
