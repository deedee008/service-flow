from datetime import datetime

from app.models.table import ServiceStage, Table

def test_create_table():
    seated_time = datetime(2026, 10, 7, 19,0)

    table = Table(
        table_number = 12,
        party_size = 4,
        service_stage = ServiceStage.WAITING_FOR_FOOD,
        seated_at = seated_time
    )

    assert table.table_number == 12
    assert table.party_size == 4
    assert table.service_stage == ServiceStage.WAITING_FOR_FOOD
    assert table.seated_at == seated_time
