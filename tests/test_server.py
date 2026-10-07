from app.models.server import Server
from app.models.table import Table, ServiceStage
from datetime import datetime

def test_server_has_own_active_tables():
    table = Table(
        table_number = 12,
        party_size = 4,
        service_stage = ServiceStage.WAITING_FOR_FOOD,
        seated_at = datetime(2026, 10, 7, 19,0)
    )
    server_1 = Server(name = "Ana", current_sales = 350.00)
    server_2 = Server(name = "Bob", current_sales = 275.00)

    server_1.active_tables.append(table)

    assert server_1.active_tables == [table]
    assert server_2.active_tables == []