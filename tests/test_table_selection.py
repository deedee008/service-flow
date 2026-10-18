import pytest

from app.models.server import Server
from app.models.table import Table
from app.services.table_selection import find_suitable_tables
from datetime import datetime
from app.models.table import ServiceStage
from app.models.table_session import TableSession
from app.services.workload import calculate_workload


def suitable_tables():
    suitable_tables = []

def test_find_suitable_tables_by_capacity():
    tables = [
        Table( table_number = 1, capacity = 2, section_id = 1 ),
        Table( table_number = 2, capacity = 4, section_id = 1 ),
        Table( table_number = 3, capacity = 6, section_id = 2),
        Table( table_number = 4, capacity = 10, section_id = 2)
    ]

    result = find_suitable_tables(tables, party_size = 4)

    assert [table.table_number for table in result] == [2, 3, 4]

def test_no_suitable_tables():
    tables = [
        Table( table_number = 1, capacity = 2, section_id = 1 ),
        Table( table_number = 2, capacity = 4, section_id = 1 ),
        Table( table_number = 3, capacity = 6, section_id = 2 ),
    ]

    result = find_suitable_tables(tables, party_size = 8)
    assert result == []

def test_exclude_occupied_tables():
    table_1 = Table( table_number = 1, capacity = 2, section_id = 1 )
    table_2 = Table( table_number = 2, capacity = 4, section_id = 1 )
    table_3 = Table( table_number = 3, capacity = 4, section_id = 1 )
    table_4 = Table( table_number = 4, capacity = 6, section_id = 2 )

    tables = [table_1, table_2, table_3, table_4]

    occupied_session = TableSession(
        table = table_2,
        party_size = 4,
        service_stage = ServiceStage.EATING,
        seated_at = datetime(2026, 10, 11, 18, 0)
    )

    result = find_suitable_tables(tables, party_size = 4, occupied_sessions = [occupied_session])

    assert [table.table_number for table in result] == [3, 4]

def test_exclude_closed_tables():
    tables = [
        Table( table_number = 1, capacity = 2, section_id = 1 ),
        Table( table_number = 2, capacity = 4, section_id = 1 ),
        Table( table_number = 3, capacity = 4, section_id = 1 ),
        Table( table_number = 4, capacity = 6, section_id = 2 )
    ]

    result = find_suitable_tables(tables, party_size = 4, closed_table_numbers = {2})
    assert [table.table_number for table in result] == [3, 4]

def test_exclude_tables_from_closed_sections():
    tables = [
        Table( table_number = 1, capacity = 4, section_id = 1 ),
        Table( table_number = 2, capacity = 4, section_id = 2 ),
        Table( table_number = 3, capacity = 6, section_id = 2 ),
        Table( table_number = 4, capacity = 4, section_id = 1 )
    ]
    result = find_suitable_tables(tables, party_size = 4, closed_section_ids = {2})
    assert [table.table_number for table in result] == [1, 4]

def test_closing_section_preserves_active_session_and_workload():
    patio_table = Table( table_number = 5, capacity = 4, section_id = 2 )
    dining_table = Table( table_number = 6, capacity = 4, section_id = 1 )

    session = TableSession(
        table = patio_table,
        party_size = 4,
        service_stage = ServiceStage.EATING,
        seated_at = datetime(2026, 10, 17, 18, 0)
    )

    server = Server(
        name = "Ana",
        current_sales = 0.0,
        active_tables = [session]
    )

    workload_before = calculate_workload(server)

    result = find_suitable_tables(
        tables = [patio_table, dining_table],
        party_size = 4,
        occupied_sessions = server.active_tables,
        closed_section_ids = {2}
    )

    workload_after = calculate_workload(server)

    assert [ table.table_number for table in result ] == [6]
    assert server.active_tables == [session]
    assert workload_after == workload_before