from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField

from domain.model import Priority, ProtocolType

from .protocol_type import schemas


class ProtocolSchema(Schema):
    protocol_type = EnumField(ProtocolType, required=True)
    requester = fields.UUID(required=True)
    priority = EnumField(Priority, required=True)
    content = fields.Dict(required=True)

    @post_load
    def format(self, data: dict, **_) -> dict:
        content_schema = schemas[data['protocol_type']]
        data['requester'] = str(data['requester'])
        data['content'] = content_schema.load(data['content'])

        return data
