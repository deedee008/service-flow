from datetime import datetime

from app.models import table
from app.models.server import Server
from app.models.table import Table, ServiceStage
from app.services.workload import calculate_workload
from app.models.table_session import TableSession

import pytest

def test_calculate_workload():
    server = Server(
        name="Ana",
        current_sales=350.00
    )

    table_1 = Table(
        table_number = 12,
        capacity = 4,
        section_id = 1
    )
    session_1 = TableSession(
        table = table_1,
        party_size = 4,
        service_stage = ServiceStage.JUST_SEATED,
        seated_at = datetime(2026, 10, 7, 19, 0),
        server = server
    )
    table_2 = Table(
        table_number = 15,
        capacity = 4,
        section_id = 1
    )

    session_2 = TableSession(
        table = table_2,
        party_size = 2,
        service_stage = ServiceStage.WAITING_FOR_FOOD,
        seated_at = datetime(2026, 10, 7, 18, 30),
        server = server
    )
    active_sessions = [session_1, session_2]

    assert calculate_workload(server, active_sessions) == 7

def test_workload_with_no_active_sessions():
    server = Server(
        name = "Bob",
        current_sales = 0.0
    )
    active_sessions = []
    assert calculate_workload(server, active_sessions) == 0

def test_workload_deciding_stage():
    table = Table(
        table_number = 20,
        capacity = 10,
        section_id = 1
    )
    server = Server(
        name="Ana",
        current_sales=400.00
    )

    session = TableSession(
        table = table,
        party_size = 10,
        service_stage = ServiceStage.DECIDING,
        seated_at = datetime(2026, 10, 7, 19, 0),
        server = server
    )
    active_sessions = [session]
    assert calculate_workload(server, active_sessions) == 1

def test_party_size_affects_just_seated_workload():
    server_1 = Server(
        name="Ana",
        current_sales=0.0
    )

    server_2 = Server(
        name="Bob",
        current_sales=0.0
    )

    small_table = Table(
        table_number = 10,
        capacity = 2,
        section_id = 1
    )

    small_session = TableSession(
        table = small_table,
        party_size = 2,
        service_stage = ServiceStage.JUST_SEATED,
        seated_at = datetime(2026, 10, 7, 19, 0),
        server = server_1
    )

    large_table = Table(
        table_number=20,
        capacity = 8,
        section_id = 1
    )

    large_session = TableSession(
        table = large_table,
        party_size=8,
        service_stage=ServiceStage.JUST_SEATED,
        seated_at = datetime(2026, 10, 7, 19, 0),
        server = server_2
    )

    active_sessions = [small_session, large_session]

    assert calculate_workload(server_1, active_sessions) == 5
    assert calculate_workload(server_2, active_sessions) == 8

def test_party_size_affects_ready_to_order():
    table = Table(
        table_number = 25,
        capacity = 10,
        section_id = 1
    )
    server = Server(
        name="Ana",
        current_sales=0.0
    )

    session = TableSession(
        table = table,
        party_size = 10,
        service_stage = ServiceStage.READY_TO_ORDER,
        seated_at = datetime(2026, 10, 7, 19, 0),
        server = server
    )

    active_sessions = [session]
    assert calculate_workload(server, active_sessions) == 9

@pytest.mark.parametrize(
    "party_size, expected_workload",
    [
        (1,5),
        (2, 5),
        (3,6),
        (4, 6)
    ]
)
def test_party_size_boundaries(party_size, expected_workload):
    table = Table(
        table_number = 30,
        capacity = 4,
        section_id = 1
    )

    server = Server(
        name="Ana",
        current_sales=0.0
    )

    session = TableSession(
        table = table,
        party_size = party_size,
        service_stage = ServiceStage.JUST_SEATED,
        seated_at = datetime(2026, 10, 7, 19, 0),
        server = server
    )

    active_sessions = [session]
    assert calculate_workload(server, active_sessions) == expected_workload

def test_table_session_tracks_assigned_server():
    ana = Server(
        name = "Ana",
        current_sales = 0.0
    )

    maria = Server(
        name = "Maria",
        current_sales = 0.0
    )

    table = Table(
        table_number = 12,
        capacity = 4,
        section_id = 1
    )

    session = TableSession(
        table = table,
        party_size = 4,
        service_stage = ServiceStage.JUST_SEATED,
        seated_at = datetime.now(),
        server = ana
    )

    assert session.server is ana

    session.server = maria

    assert session.server is maria

def test_workload_only_counts_sessions_assigned_to_server():
    ana = Server(
        name = "Ana",
        current_sales = 0.0
    )

    maria = Server(
        name = "Maria",
        current_sales = 0.0
    )

    active_sessions = [
        TableSession(
            table = Table(
                table_number = 1,
                capacity = 2,
                section_id = 1
            ),
            party_size = 2,
            service_stage = ServiceStage.JUST_SEATED,
            seated_at = datetime.now(),
            server = ana
        ),

        TableSession(
            table = Table(
                table_number = 2,
                capacity = 4,
                section_id = 1
            ),
            party_size = 4,
            service_stage = ServiceStage.EATING,
            seated_at = datetime.now(),
            server = ana
        ),

        TableSession(
            table = Table(
                table_number = 3,
                capacity = 4,
                section_id = 2
            ),
            party_size = 4,
            service_stage = ServiceStage.READY_TO_ORDER,
            seated_at = datetime.now(),
            server = maria
        ),

        TableSession(
            table = Table(
                table_number = 4,
                capacity = 2,
                section_id = 2
            ),
            party_size = 2,
            service_stage = ServiceStage.DRINKS,
            seated_at = datetime.now(),
            server = maria
        )
    ]

    assert calculate_workload(ana, active_sessions) == 6
    assert calculate_workload(maria, active_sessions) == 8

