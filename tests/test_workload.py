from datetime import datetime

from app.models.server import Server
from app.models.table import Table, ServiceStage
from app.services.workload import calculate_workload

import pytest

def test_calculate_workload():
    table_1 = Table(
        table_number = 12,
        party_size = 4,
        service_stage = ServiceStage.JUST_SEATED,
        seated_at = datetime(2026, 10, 7, 19, 0)
    )
    table_2 = Table(
        table_number = 15,
        party_size = 2,
        service_stage = ServiceStage.WAITING_FOR_FOOD,
        seated_at = datetime(2026, 10, 7, 18, 30)
    )

    server = Server(
        name = "Ana",
        current_sales = 350.00,
        active_tables = [table_1, table_2]
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
        party_size = 10,
        service_stage = ServiceStage.DECIDING,
        seated_at = datetime(2026, 10, 7, 19, 0)
    )

    server = Server(
        name = "Ana",
        current_sales = 400.00,
        active_tables = [table]
    )
    assert calculate_workload(server) == 1

def test_party_size_affects_just_seated_workload():
    small_table = Table(
        table_number = 10,
        party_size = 2,
        service_stage = ServiceStage.JUST_SEATED,
        seated_at = datetime(2026, 10, 7, 19, 0)
    )

    large_table = Table(
        table_number = 20,
        party_size = 8,
        service_stage = ServiceStage.JUST_SEATED,
        seated_at = datetime(2026, 10, 7, 19, 0)
    )

    server_1 = Server(
        name = "Ana",
        current_sales = 0.0,
        active_tables = [small_table]
    )

    server_2 = Server(
        name = "Bob",
        current_sales = 0.0,
        active_tables = [large_table]
    )

    assert calculate_workload(server_1) == 5
    assert calculate_workload(server_2) == 8

def test_party_size_affects_ready_to_order():
    table = Table(
        table_number = 25,
        party_size = 10,
        service_stage = ServiceStage.READY_TO_ORDER,
        seated_at = datetime(2026, 10, 7, 19, 0)
    )

    server = Server(
        name = "Ana",
        current_sales = 0.0,
        active_tables = [table]
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
        party_size = party_size,
        service_stage = ServiceStage.JUST_SEATED,
        seated_at = datetime(2026, 10, 7, 19, 0)
    )

    server = Server(
        name = "Ana",
        current_sales = 0.0,
        active_tables = [table]
    )

    assert calculate_workload(server) == expected_workload