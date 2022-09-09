from marshmallow import Schema, fields


class PlantingAnticipationSchema(Schema):
    farm_id = fields.String(required=True)
    notes = fields.String(missing=None)
