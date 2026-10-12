from datetime import datetime

from _pytest.main import Session

from app.models.table import ServiceStage, Table
from app.models.table_session import TableSession


def test_create_table():
    seated_time = datetime(2026, 10, 7, 19,0)

    table = Table(
        table_number = 12,
        capacity = 4,
        section_id = 1
    )

    session = TableSession(
        table = table,
        party_size = 4,
        service_stage = ServiceStage.WAITING_FOR_FOOD,
        seated_at = seated_time
    )

    assert table.table_number == 12
    assert session.party_size == 4
    assert session.service_stage == ServiceStage.WAITING_FOR_FOOD
    assert session.seated_at == seated_time

def test_table_capacity_and_section():
    table = Table(
        table_number = 12,
        capacity = 6,
        section_id = 2
    )

    session = TableSession(
        table = table,
        party_size = 4,
        service_stage = ServiceStage.JUST_SEATED,
        seated_at = datetime(2026, 10, 11, 18, 0),
    )
    assert table.capacity == 6
    assert table.section_id == 2
