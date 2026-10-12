from dataclasses import dataclass
from datetime import datetime


from app.models.table import Table, ServiceStage

@dataclass
class TableSession:
    table: Table
    party_size: int
    service_stage: ServiceStage
    seated_at: datetime
