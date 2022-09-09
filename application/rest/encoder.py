from datetime import datetime
from enum import Enum
from flask.json import JSONEncoder


class CustomJsonEncoder(JSONEncoder):
    def default(self, obj: any) -> str:
        if isinstance(obj, datetime):
            return obj.isoformat()

        if isinstance(obj, Enum):
            return obj.value

        return super().default(obj)
