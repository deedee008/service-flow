from dataclasses import dataclass, field
from datetime import datetime

from app.models.server import Server

@dataclass
class Shift:
    started_at: datetime

    # Creates a separate dictionary for each shift to store section assignments
    section_assignments: dict[int, Server] = field(default_factory=dict)

    # Assign a server to a section for the current shift
    # Section assignments can change between shifts
    def assign_section(self, section_id: int, server: Server):
        self.section_assignments[section_id] = server

    def get_server_for_section(self, section_id: int) -> Server | None:
        return self.section_assignments.get(section_id)