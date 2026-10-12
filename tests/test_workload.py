from datetime import datetime

from app.models.server import Server
from app.models.table import Table, ServiceStage
from app.services.workload import calculate_workload
from app.models.table_session import TableSession

import pytest

def test_calculate_workload():
    table_1 = Table(
        table_number = 12,
        capacity = 4,
        section_id = 1
    )
    session_1 = TableSession(
        table = table_1,
        party_size = 4,
        service_stage = ServiceStage.JUST_SEATED,
        seated_at = datetime(2026, 10, 7, 19, 0)
    )
    table_2 = Table(
        table_number = 15,
        capacity = 4,
        section_id = 1
    )

    session_2 = TableSession(
        table = table_2,
        party_size = 2,
        service_stage = ServiceStage.WAITING_FOR_FOOD,
        seated_at = datetime(2026, 10, 7, 18, 30)
    )

    server = Server(
        name="Ana",
        current_sales=350.00,
        active_tables=[session_1, session_2]
    )

    assert calculate_workload(server) == 7

def test_workload_with_no_active_tables():
    server = Server(
        name = "Bob",
        current_sales = 0.0
    )
    assert calculate_workload(server) == 0

def test_workload_deciding_stage():
    table = Table(
        table_number = 20,
        capacity = 10,
        section_id = 1
    )
    session = TableSession(
        table = table,
        party_size = 10,
        service_stage = ServiceStage.DECIDING,
        seated_at = datetime(2026, 10, 7, 19, 0)
    )

    server = Server(
        name="Ana",
        current_sales=400.00,
        active_tables=[session]
    )
    assert calculate_workload(server) == 1

def test_party_size_affects_just_seated_workload():
    small_table = Table(
        table_number = 10,
        capacity = 2,
        section_id = 1
    )

    small_session = TableSession(
        table = small_table,
        party_size = 2,
        service_stage = ServiceStage.JUST_SEATED,
        seated_at = datetime(2026, 10, 7, 19, 0)
    )

    large_table = Table(
        table_number=20,
        capacity = 8,
        section_id = 1
    )

    large_session = TableSession(
        table = large_table,
        party_size=8,
        service_stage=ServiceStage.JUST_SEATED,
        seated_at = datetime(2026, 10, 7, 19, 0)
    )

    server_1 = Server(
        name="Ana",
        current_sales=0.0,
        active_tables=[small_session]
    )

    server_2 = Server(
        name = "Bob",
        current_sales = 0.0,
        active_tables = [large_session]
    )

    assert calculate_workload(server_1) == 5
    assert calculate_workload(server_2) == 8

def test_party_size_affects_ready_to_order():
    table = Table(
        table_number = 25,
        capacity = 2,
        section_id = 1
    )

    session = TableSession(
        table = table,
        party_size = 10,
        service_stage = ServiceStage.READY_TO_ORDER,
        seated_at = datetime(2026, 10, 7, 19, 0)
    )

    server = Server(
        name="Ana",
        current_sales=0.0,
        active_tables=[session]
    )

    assert calculate_workload(server) == 9

@pytest.mark.parametrize(
    "party_size, expected_workload",
    [
        (1,5),
        (2, 5),
        (3,6),
        (4, 6),
    ]
)
def test_party_size_boundaries(party_size, expected_workload):
    table = Table(
        table_number = 30,
        capacity = 2,
        section_id = 1
    )

    session = TableSession(
        table = table,
        party_size = party_size,
        service_stage = ServiceStage.JUST_SEATED,
        seated_at = datetime(2026, 10, 7, 19, 0)
    )

    server = Server(
        name="Ana",
        current_sales=0.0,
        active_tables=[session]
    )

    assert calculate_workload(server) == expected_workload