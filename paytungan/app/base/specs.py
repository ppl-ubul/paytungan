from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseDomain:
    id: int
    updated_at: datetime
    created_at: datetime
