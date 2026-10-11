from app.models.server import Server
from app.services.workload import calculate_workload
from datetime import datetime

def select_next_server(servers: list[Server]) -> Server:
    return min(servers,
               key = lambda server: (
                   calculate_workload(server),
                   server.last_seated_at or datetime.min
               )
               )
