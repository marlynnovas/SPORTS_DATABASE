@dataclass
class Plan:
    name: str
    duration_days: int
    price: float
    id: int = None