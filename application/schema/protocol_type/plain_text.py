from marshmallow import Schema, fields


class PlainTextSchema(Schema):
    text = fields.String(required=True)
