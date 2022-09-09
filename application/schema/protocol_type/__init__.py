from marshmallow import Schema
from typing import Dict

from domain.model import ProtocolType

from .new_user import NewUserSchema
from .plain_text import PlainTextSchema
from .planting_anticipation import PlantingAnticipationSchema

schemas: Dict[ProtocolType, Schema] = {
    ProtocolType.NEW_USER: NewUserSchema(),
    ProtocolType.OTHER: PlainTextSchema(),
    ProtocolType.PLANTING_ANTICIPATION: PlantingAnticipationSchema()
}
