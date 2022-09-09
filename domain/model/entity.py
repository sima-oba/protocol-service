from dacite import from_dict
from dacite.config import Config
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from uuid import uuid4


@dataclass
class Entity:
    _id: str
    created_at: datetime
    updated_at: datetime

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return from_dict(cls, data, config=Config(cast=[Enum]))

    @classmethod
    def new(cls, data: dict):
        return from_dict(
            data_class=cls,
            data={
                '_id': str(uuid4()),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                **data
            }
        )
