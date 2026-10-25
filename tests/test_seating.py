from app.models.server import Server
from app.models.shift import Shift
from app.models.table_session import TableSession
from app.services.seating import select_next_server
from datetime import datetime
from app.models.table import Table, ServiceStage
from app.services.seating import recommend_seating

def test_select_next_server_with_lowest_workload():
    ana = Server(name = "Ana",current_sales = 0.0)
    maria = Server(name = "Maria",current_sales = 0.0)

    selected_server = select_next_server([ana, maria])

    assert selected_server == ana

def test_select_server_with_lower_workload():
    ana = Server(name = "Ana",current_sales = 0.0)
    active_table = Table(
            table_number = 1,
            capacity = 4,
            section_id = 1
    )
    active_session = TableSession(
        table = active_table,
        party_size = 4,
        service_stage = ServiceStage.JUST_SEATED,
        seated_at = datetime(2026, 10,11,18,0)
        )

    ana.active_tables = [active_session]

    maria = Server(name = "Maria",current_sales = 0.0)

    selected_server = select_next_server([ana, maria])

    assert selected_server == maria

def test_select_server_who_waited_longer():
     ana = Server(
            name = "Ana",
            current_sales = 0.0,
            last_seated_at=datetime(2026, 10, 11, 18, 0)
        )
     maria = Server(
            name = "Maria",
            current_sales = 0.0,
            last_seated_at=datetime(2026, 10, 11, 18, 30)
        )
     selected_server = select_next_server([maria, ana])
     assert selected_server == ana

def test_server_without_previous_seating_gets_priority():
    ana = Server(
        name = "Ana",
        current_sales = 0.0,
        last_seated_at=datetime(2026, 10, 11, 18, 0)
    )

    maria = Server(
        name = "Maria",
        current_sales = 0.0,
        last_seated_at = None
    )
    selected_server = select_next_server([ana, maria])
    assert selected_server == maria

def test_new_shift_starts_without_previous_seating():
    server = Server(
        name = "Ana",
        current_sales = 0.0,
        last_seated_at = None
    )
    assert server.last_seated_at is None

def test_reset_server_for_new_shift():
    table = Table(
        table_number = 10,
        capacity = 4,
        section_id = 1,
    )

    session = TableSession(
        table = table,
        party_size=4,
        service_stage=ServiceStage.EATING,
        seated_at=datetime(2026, 10, 10, 19, 0)
    )

    server = Server(
        name="Ana",
        active_tables=[session],
        current_sales = 800.00,
        last_seated_at = datetime(2026, 10, 10, 20, 0)
    )

    server.reset_for_new_shift()

    assert server.current_sales == 0.0
    assert server.active_tables == []
    assert server.last_seated_at is None

def test_recommend_seating_balances_workload_and_capacity():
    ana = Server(
        name = "Ana",
        current_sales = 0.0
    )

    maria = Server(
        name = "Maria",
        current_sales = 0.0
    )

    table_1 = Table(table_number = 1, capacity = 4, section_id = 1)
    table_2 = Table(table_number = 2, capacity = 6, section_id = 2)

    occupied_table = Table(table_number = 3, capacity = 4, section_id = 1)

    ana.active_tables.append(
        TableSession(
            table = occupied_table,
            party_size = 4,
            service_stage = ServiceStage.EATING,
            seated_at = datetime(2026, 10, 17, 17, 0)
        )
    )

    shift = Shift(started_at = datetime(2026, 10, 17, 17, 0))
    shift.assign_section(section_id = 1, server = ana)
    shift.assign_section(section_id = 2, server = maria)

    result = recommend_seating(
        suitable_tables = [table_1, table_2],
        shift = shift,
        party_size = 4
    )

    assert result == (table_1, ana)

def test_recommend_seating_calculates_workload_automatically():
    ana = Server(
        name = "Ana",
        current_sales = 0.0
    )

    maria = Server(
        name = "Maria",
        current_sales = 0.0
    )

    table_1 = Table(table_number = 1, capacity = 4, section_id = 1)
    table_2 = Table(table_number = 2, capacity = 6, section_id = 2)

    occupied_table = Table(table_number = 3, capacity = 4, section_id = 1)

    ana.active_tables.append(
        TableSession(
            table = occupied_table,
            party_size = 4,
            service_stage = ServiceStage.JUST_SEATED,
            seated_at = datetime(2026, 10, 17, 17, 0)
        )
    )

    shift = Shift(started_at = datetime(2026, 10, 17, 17, 0))
    shift.assign_section(section_id = 1, server = ana)
    shift.assign_section(section_id = 2, server = maria)

    result = recommend_seating(
        suitable_tables = [table_1, table_2],
        shift = shift,
        party_size = 4
    )

    assert result == (table_2, maria)

def test_recommend_seating_without_assigned_servers():
    ana = Server(
        name = "Ana",
        current_sales = 0.0
    )

    table_1 = Table(table_number = 1, capacity = 4, section_id = 1)
    table_2 = Table(table_number = 2, capacity = 6, section_id = 2)

    shift = Shift(started_at = datetime(2026, 10, 17, 17, 0))

    # Ana is assigned to section 3, not sections 1 and 2
    shift.assign_section(section_id = 3, server = ana)

    result = recommend_seating(
        suitable_tables = [table_1, table_2],
        shift = shift,
        party_size = 4
    )

    assert result is None

def test_recommend_seating_with_no_suitable_tables():
    ana = Server(
        name = "Ana",
        current_sales = 0.0
    )

    shift = Shift(started_at = datetime(2026, 10, 17, 17, 0))
    shift.assign_section(section_id = 1, server = ana)

    result = recommend_seating(
        suitable_tables = [],
        shift = shift,
        party_size = 4
    )

    assert result is None

def test_recommend_seating_uses_sales_as_tiebreaker():
    ana = Server(
        name = "Ana",
        current_sales = 800.0
    )

    maria = Server(
        name = "Maria",
        current_sales = 300.0
    )

    table_1 = Table(table_number = 1, capacity = 4, section_id = 1)
    table_2 = Table(table_number = 2, capacity = 4, section_id = 2)

    shift = Shift(started_at = datetime(2026, 10, 17, 17, 0))
    shift.assign_section(section_id = 1, server = ana)
    shift.assign_section(section_id = 2, server = maria)

    result = recommend_seating(
        suitable_tables = [table_1, table_2],
        shift = shift,
        party_size = 4
    )

    assert result == (table_2, maria)

