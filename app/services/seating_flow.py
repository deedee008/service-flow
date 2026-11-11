from app.models.table import Table
from app.models.server import Server
from app.models.shift import Shift
from app.services.seating import recommend_seating
from app.services.table_selection import find_suitable_tables
from app.models.table_session import TableSession

def find_seating_recommendation(
        tables: list[Table],
        party_size: int,
        shift: Shift,
        occupied_sessions: list[TableSession] | None = None,
        closed_table_numbers: set[int] | None = None,
        closed_section_ids: set[int] | None = None
) -> tuple[Table, Server] | None:

    # Find tables that can accommodate the arriving party
    suitable_tables = find_suitable_tables(
        tables = tables,
        party_size = party_size,
        occupied_sessions = occupied_sessions,
        closed_table_numbers = closed_table_numbers,
        closed_section_ids = closed_section_ids
    )

    # Select the best table and server based on workload, capacity, and sales
    return recommend_seating(
        suitable_tables = suitable_tables,
        shift = shift,
        party_size = party_size,
        active_sessions = occupied_sessions or []
    )
