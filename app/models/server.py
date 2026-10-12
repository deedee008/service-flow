from dataclasses import dataclass, field
from datetime import datetime

from app.models.table_session import TableSession

@dataclass
class Server:
    name: str
    current_sales: float
    active_tables: list[TableSession] = field(default_factory=list)
    last_seated_at: datetime | None = None

    def reset_for_new_shift(self):
       self.current_sales = 0.0
       self.active_tables.clear()
       self.last_seated_at = None