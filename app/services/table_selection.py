from app.models.table import Table
from app.models.table_session import TableSession

def find_suitable_tables(
        tables: list[Table],
        party_size: int,
        occupied_sessions: list[TableSession] | None = None,
        closed_table_numbers: set[int] | None = None,
        closed_section_ids: set[int] | None = None
) -> list[Table]:

    # If no occupied sessions are provided, use an empty list
    if occupied_sessions is None:
        occupied_sessions = []

    # If no closed tables are provided, use an empty set
    if closed_table_numbers is None:
        closed_table_numbers = set()

    # If no closed sections are provided, use an empty set
    if closed_section_ids is None:
        closed_section_ids = set()

    # Collect the table numbers that are currently occupied
    # A set automatically removes duplicates
    occupied_table_numbers = {
        session.table.table_number for session in occupied_sessions
    }

    # Check each table for enough seats and availability
    suitable_tables = []

    # Only include tables with enough seats that are not occupied or closed by the manager, or tables that are not part of closed sections
    for table in tables:
        if (table.capacity >= party_size
            and table.table_number not in occupied_table_numbers
            and table.table_number not in closed_table_numbers
            and table.section_id not in closed_section_ids):
            suitable_tables.append(table)

    # Return suitable tables sorted by capacity, smallest first
    return sorted(suitable_tables, key=lambda table: table.capacity)


