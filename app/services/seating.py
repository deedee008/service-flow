from app.models.server import Server
from app.services.workload import calculate_workload
from datetime import datetime
from app.models.table import Table
from app.models.shift import Shift

def select_next_server(servers: list[Server]) -> Server:
    return min(servers,
               key = lambda server: (
                   calculate_workload(server),
                   server.last_seated_at or datetime.min
               )
               )

def recommend_seating(
        suitable_tables: list[Table],
        shift: Shift,
        party_size: int
) -> tuple[Table, Server] | None:

    # Start with no recommendation and the highest possible score
    best_recommendation = None
    best_score = float("inf")

    # Check each suitable table and find its assigned server
    for table in suitable_tables:
        server = shift.get_server_for_section(table.section_id)

        # Skip tables in sections without an assigned server
        if server is None:
            continue

        # Calculate unused seats and the server's workload from active tables
        unused_seats = table.capacity - party_size
        workload = calculate_workload(server)

        # Combine workload and unused seats into one score
        # A lower score means a better seating option
        score = workload + unused_seats

        # Prefer the lowest score, then the lowest sales if scores are equal
        if (
                score < best_score
                or
                (score == best_score
                    and (
                            best_recommendation is None
                            or server.current_sales < best_recommendation[1].current_sales
                    )
                )
        ):

            best_score = score
            best_recommendation = (table, server)

    # Return the best option, or None if no valid option was found
    return best_recommendation
