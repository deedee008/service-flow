from dataclasses import dataclass, field
from datetime import datetime

from app.models.table import Table

@dataclass
class Server:
    name: str
    current_sales: float
    active_tables: list[Table] = field(default_factory=list)
    last_seated_at: datetime | None = None

    def reset_for_new_shift(self):
       self.current_sales = 0.0
       self.active_tables.clear()
       self.last_seated_at = None