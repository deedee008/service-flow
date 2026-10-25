from datetime import datetime

from app.models.server import Server
from app.models.table import Table
from app.models.shift import Shift
from app.services.seating_flow import find_seating_recommendation

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