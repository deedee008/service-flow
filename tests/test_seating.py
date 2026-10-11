from app.models.server import Server
from app.services.seating import select_next_server
from datetime import datetime
from app.models.table import Table, ServiceStage

def test_select_next_server_with_lowest_workload():
    ana = Server(name = "Ana",current_sales = 0.0)
    maria = Server(name = "Maria",current_sales = 0.0)

    selected_server = select_next_server([ana, maria])

    assert selected_server == ana

def test_select_server_with_lower_workload():
    ana = Server(name = "Ana",current_sales = 0.0,
                 active_tables = [
                     Table(
                         table_number = 10,
                         party_size = 4,
                         service_stage = ServiceStage.JUST_SEATED,
                         seated_at = datetime(2026, 10,11,18,0)
                     )
                 ])
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
         table_number=10,
         party_size=4,
         service_stage=ServiceStage.EATING,
         seated_at=datetime(2026, 10, 10, 19, 0)
    )


    server = Server(
        name = "Ana",
        active_tables = [table],
        current_sales = 800.00,
        last_seated_at = datetime(2026, 10, 10, 20, 0)
    )

    server.reset_for_new_shift()

    assert server.current_sales == 0.0
    assert server.active_tables == []
    assert server.last_seated_at is None