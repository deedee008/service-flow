from app.models.table import ServiceStage, Table
from app.models.server import Server
from app.models.table_session import TableSession
from datetime import datetime

SERVICE_STAGE_WEIGHTS = {
    ServiceStage.JUST_SEATED: 5,
    ServiceStage.DRINKS: 2,
    ServiceStage.DECIDING: 1,
    ServiceStage.READY_TO_ORDER: 5,
    ServiceStage.WAITING_FOR_FOOD: 1,
    ServiceStage.EATING: 1,
    ServiceStage.DESSERT_CHECK: 2,
    ServiceStage.CLOSING: 3
}

def calculate_workload(
        server: Server,
        active_sessions: list[TableSession]) -> int:
    total_workload = 0

    # Use the shared session list as the singe source of truth
    for session in active_sessions:
        # Only count sessions assigned to this server
        if session.server is not server:
            continue

        weight = SERVICE_STAGE_WEIGHTS[session.service_stage]

        if session.service_stage in (
            ServiceStage.JUST_SEATED,
            ServiceStage.READY_TO_ORDER,
        ):
            extra_guests = max(0, session.party_size - 2 )
            party_bonus = (extra_guests + 1) // 2
            weight += party_bonus

        total_workload += weight

    return total_workload

