from app.models.table import Table
from app.models.section import Section
from app.models.server import Server
from datetime import datetime
from app.models.shift import Shift

section_1 = Section(
    section_id = 1,
    tables = [
        Table(table_number = 1, capacity = 4, section_id = 1),
        Table(table_number = 2, capacity = 2, section_id = 1),
        Table(table_number = 3, capacity = 4, section_id = 1),
        Table(table_number = 4, capacity = 6, section_id = 1),
        Table(table_number = 5, capacity = 4, section_id = 1),
        Table(table_number = 6, capacity = 2, section_id = 1)
    ]
)

section_2 = Section(
    section_id =2,
    tables = [
        Table(table_number = 7, capacity = 2, section_id = 2),
        Table(table_number = 8, capacity = 6, section_id = 2),
        Table(table_number = 9, capacity = 4, section_id = 2),
        Table(table_number = 10, capacity = 8, section_id = 2),
        Table(table_number = 11, capacity = 2, section_id = 2),
        Table(table_number = 12, capacity = 4, section_id = 2)
    ]
)

section_3 = Section(
    section_id =3,
    tables = [
        Table(table_number = 13, capacity = 2, section_id = 3),
        Table(table_number = 14, capacity = 6, section_id = 3),
        Table(table_number = 15, capacity = 4, section_id = 3),
        Table(table_number = 16, capacity = 2, section_id = 3),
        Table(table_number = 17, capacity = 6, section_id = 3),
        Table(table_number = 18, capacity = 4, section_id = 3)
    ]
)

section_4 = Section(
    section_id =4,
    tables = [
        Table(table_number = 19, capacity = 2, section_id = 4),
        Table(table_number = 20, capacity = 6, section_id = 4),
        Table(table_number = 21, capacity = 4, section_id = 4),
        Table(table_number = 22, capacity = 2, section_id = 4),
        Table(table_number = 23, capacity = 6, section_id = 4),
        Table(table_number = 24, capacity = 4, section_id = 4)
    ]
)

section_5 = Section(
    section_id =5,
    tables = [
        Table(table_number = 25, capacity = 2, section_id = 5),
        Table(table_number = 26, capacity = 4, section_id = 5),
        Table(table_number = 27, capacity = 6, section_id = 5),
        Table(table_number = 28, capacity = 2, section_id = 5),
        Table(table_number = 29, capacity = 4, section_id = 5),
        Table(table_number = 30, capacity = 2, section_id = 5)
    ]
)

# Group all restaurant sections into a single collection
restaurant_sections = [section_1, section_2, section_3, section_4, section_5]

# Combine tables from all sections into a single list for API access
restaurant_tables = []

for section in restaurant_sections:
    restaurant_tables.extend(section.tables)

# Demo servers for testing seating recommendations
demo_servers = [
    Server(name = "Ana", current_sales = 0),
    Server(name = "Bob", current_sales = 0),
    Server(name = "Charlie", current_sales = 0),
    Server(name = "David", current_sales = 0),
    Server(name = "Eve", current_sales = 0)
]

# Create a demo shift
demo_shift = Shift(started_at = datetime.now())

# Assign each demo server to a restaurant section
for section_id, server in enumerate(demo_servers, start=1):
    demo_shift.assign_section(section_id, server)
