from datetime import datetime

from app.models.server import Server
from app.models.table import Table, ServiceStage
from app.models.shift import Shift
from app.services.seating_flow import find_seating_recommendation
from app.models.table_session import TableSession

def test_seating_flow_recommends_available_table():
    ana = Server(name = "Ana", current_sales = 0.0)
    maria = Server(name = "Maria", current_sales = 0.0)

    table_1 = Table(table_number = 1, capacity = 2, section_id = 1)
    table_2 = Table(table_number = 2, capacity = 4, section_id = 2)

    shift = Shift(started_at = datetime(2026, 10, 24, 17, 0 ))
    shift.assign_section(section_id = 1, server = ana)
    shift.assign_section(section_id = 2, server = maria)

    result =  find_seating_recommendation(
        tables = [table_1, table_2],
        shift = shift,
        party_size = 4
    )

    assert result == (table_2,maria)

def test_seating_flow_excludes_occupied_tables():
    ana = Server(name = "Ana", current_sales = 0.0)

    table_1 = Table(table_number = 1, capacity = 4, section_id = 1)
    table_2 = Table(table_number = 2, capacity = 4, section_id = 1)

    shift = Shift(started_at = datetime(2026, 10, 24, 17, 0 ))
    shift.assign_section(section_id = 1, server = ana)

    occupied_session = TableSession(
        table = table_1,
        party_size = 4,
        service_stage = ServiceStage.EATING,
        seated_at = datetime(2026, 10, 24, 17, 30 )
    )

    result = find_seating_recommendation(
        tables = [table_1, table_2],
        party_size = 4,
        shift = shift,
        occupied_sessions = [occupied_session]
    )

    assert result == (table_2,ana)

def test_seating_flow_excludes_tables_closed_by_manager():
    ana = Server(name = "Ana", current_sales = 0.0)

    table_1 = Table(table_number = 1, capacity = 4, section_id = 1)
    table_2 = Table(table_number = 2, capacity = 4, section_id = 1)

    shift = Shift(started_at = datetime(2026, 10, 24, 17, 0 ))
    shift.assign_section(section_id = 1, server = ana)

    result = find_seating_recommendation(
        tables = [table_1, table_2],
        party_size = 4,
        shift = shift,
        closed_table_numbers = {1}
    )

    assert result == (table_2,ana)

def test_seating_flow_excludes_sections_closed_by_manager():
    ana = Server(name = "Ana", current_sales = 0.0)
    maria = Server(name = "Maria", current_sales = 0.0)

    table_1 = Table(table_number = 1, capacity = 4, section_id = 1)
    table_2 = Table(table_number = 2, capacity = 4, section_id = 2)

    shift = Shift(started_at = datetime(2026, 10, 24, 17, 0 ))
    shift.assign_section(section_id = 1, server = ana)
    shift.assign_section(section_id = 2, server = maria)

    result = find_seating_recommendation(
        tables = [table_1, table_2],
        party_size = 4,
        shift = shift,
        closed_section_ids = {1}
    )

    assert result == (table_2, maria)

def test_seating_flow_applies_all_availability_filters():
    ana = Server(name = "Ana", current_sales = 0.0)
    maria = Server(name = "Maria", current_sales = 0.0)

    tables = [
        Table(table_number = 1, capacity = 4, section_id = 1),
        Table(table_number = 2, capacity = 4, section_id = 1),
        Table(table_number = 3, capacity = 4, section_id = 2),
        Table(table_number = 4, capacity = 4, section_id = 2),
        Table(table_number = 5, capacity = 4, section_id = 3)
    ]

    shift = Shift(started_at = datetime(2026, 10, 24, 17, 0 ))
    shift.assign_section(section_id = 1, server = ana)
    shift.assign_section(section_id= 2, server = ana)
    shift.assign_section(section_id = 3, server = maria)

    occupied_session = TableSession(
        table = tables[0],
        party_size = 4,
        service_stage = ServiceStage.EATING,
        seated_at = datetime(2026, 10, 24, 17, 30 )
    )

    result = find_seating_recommendation(
        tables = tables,
        party_size = 4,
        shift = shift,
        occupied_sessions = [occupied_session],
        closed_table_numbers = {2},
        closed_section_ids = {2}
    )

    assert result == (tables[4], maria)

def test_seating_flow_returns_none_when_all_tables_unavailable():
    ana = Server(name = "Ana", current_sales = 0.0)

    table_1 = Table(table_number = 1, capacity = 4, section_id = 1)
    table_2 = Table(table_number = 2, capacity = 4, section_id = 1)

    shift = Shift(started_at = datetime(2026, 10, 24, 17, 0 ))
    shift.assign_section(section_id = 1, server = ana)

    occupied_session = TableSession(
         table = table_1,
         party_size = 4,
         service_stage = ServiceStage.EATING,
         seated_at = datetime(2026, 10, 24, 17, 30 )
        )

    result = find_seating_recommendation(
            tables = [table_1, table_2],
            party_size = 4,
            shift = shift,
            occupied_sessions = [occupied_session],
            closed_table_numbers = {2}
    )

    assert result is None