from app.models.table import Table
from app.models.server import Server
from app.models.shift import Shift
from app.services.seating import recommend_seating
from app.services.table_selection import find_suitable_tables

def find_seating_recommendation(
        tables: list[Table],
        party_size: int,
        shift: Shift
) -> tuple[Table, Server] | None:

    # Find tables that can accommodate the arriving party
    suitable_tables = find_suitable_tables(
        tables = tables,
        party_size = party_size
    )

    # Select the best table and server based on workload, capacity, and sales
    return recommend_seating(
        suitable_tables = suitable_tables,
        shift = shift,
        party_size = party_size
    )
