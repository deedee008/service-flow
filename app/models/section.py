from dataclasses import dataclass, field
from app.models.table import Table

@dataclass
class Section:
    section_id: int
    tables: list[Table] = field(default_factory=list)