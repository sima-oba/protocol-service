
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from .attachment import Attachment
from .entity import Entity
from .protocol_content import NewUser, PlainText, PlantingAnticipation
from .protocol_response import ProtocolResponse


class ProtocolType(Enum):
    OTHER = 'OTHER'
    NEW_USER = 'NEW_USER'
    PLANTING_ANTICIPATION = 'PLANTING_ANTICIPATION'


class Priority(Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    VERY_HIGH = 'VERY_HIGH'


class Status(Enum):
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    CANCELED = 'CANCELED'
    COMPLETED = 'COMPLETED'


@dataclass
class Protocol(Entity):
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    protocol_type: ProtocolType
    requester: str
    priority: Priority
    status: Status
    attachments: List[Attachment]
    content: Union[NewUser, PlainText, PlantingAnticipation]
    response: Optional[ProtocolResponse]
