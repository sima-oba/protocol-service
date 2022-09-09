from marshmallow import Schema, fields, post_load
from uuid import uuid4


class NewUserSchema(Schema):
    _id = fields.UUID(missing=uuid4())
    username = fields.Email(required=True)
    name = fields.String(required=True)
    doc = fields.String(required=True)
    phone = fields.String(required=True)

    @post_load
    def format(self, data: dict, **_) -> dict:
        data['_id'] = str(data['_id'])
        return data
