from datetime import datetime
from app.models.table import Table, ServiceStage
from app.models.section import Section

def test_create_section_with_tables():
    table_1 = Table(
        table_number = 1,
        capacity = 4,
        section_id = 1
    )

    table_2 = Table(
        table_number = 2,
        capacity = 6,
        section_id = 1
    )

    section = Section(
        section_id = 1,
        tables = [table_1, table_2]
    )

    assert section.section_id == 1
    assert len(section.tables) == 2
    assert table_1 in section.tables
    assert table_2 in section.tables