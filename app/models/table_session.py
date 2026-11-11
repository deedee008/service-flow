from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from app.models.table import Table, ServiceStage

if TYPE_CHECKING:
    from app.models.server import Server

@dataclass
class TableSession:
    table: Table
    party_size: int
    service_stage: ServiceStage
    seated_at: datetime
    server: Server | None = None