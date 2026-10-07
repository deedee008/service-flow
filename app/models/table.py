from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class ServiceStage(Enum):
    JUST_SEATED = 'just_seated'
    DRINKS = 'drinks'
    READY_TO_ORDER = 'ready_to_order'
    WAITING_FOR_FOOD = 'waiting_for_food'
    EATING = 'eating'
    DESSERT_CHECK = 'dessert_check'
    CLOSING = 'closing'

@dataclass
class Table:
    table_number: int
    party_size: int
    service_stage: ServiceStage
    seated_at: datetime
