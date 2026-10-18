from datetime import datetime

from app.models.server import Server
from app.models.shift import Shift

def test_assign_section_to_server():
    ana = Server(
        name="Ana",
        current_sales=0.0
    )

    shift = Shift(
        started_at = datetime(2026, 10, 11, 17, 0)
    )

    shift.assign_section(section_id = 1, server = ana)

    assert shift.section_assignments[1] == ana

def test_section_assignments_are_independent_between_shifts():
    ana = Server(
        name="Ana",
        current_sales=0.0
    )

    morning_shift = Shift(
        started_at = datetime(2026, 10, 12, 8, 0)
    )

    evening_shift = Shift(
        started_at = datetime(2026, 10, 12, 17, 0)
    )

    morning_shift.assign_section(section_id = 1, server = ana)

    assert morning_shift.section_assignments[1] == ana
    assert evening_shift.section_assignments == {}

def test_reassign_section_to_another_server():
    ana = Server(
        name="Ana",
        current_sales=0.0
    )

    maria = Server(
        name="Maria",
        current_sales=0.0
    )

    shift = Shift(
        started_at = datetime(2026, 10, 11, 17, 0)
    )

    # In Python, assigning a new value to an existing dictionary key
    # replaces the previous value instead of creating a duplicate
    shift.assign_section(section_id = 1, server = ana)
    shift.assign_section(section_id = 1, server = maria)

    assert shift.section_assignments[1] == maria

def test_get_server_for_section():
    ana = Server(
        name="Ana",
        current_sales=0.0
    )
    maria = Server(
        name="Maria",
        current_sales=0.0
    )
    shift = Shift(
        started_at = datetime(2026, 10, 11, 17, 0)
    )
    shift.assign_section(section_id = 1, server = ana)
    shift.assign_section(section_id = 2, server = maria)

    result = shift.get_server_for_section(section_id = 2)
    assert result == maria

def test_get_server_for_unassigned_section():
    shift = Shift(
        started_at = datetime(2026, 10, 11, 17, 0)
    )
    result = shift.get_server_for_section(section_id = 3)
    assert result is None