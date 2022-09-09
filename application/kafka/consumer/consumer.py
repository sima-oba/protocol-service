
from typing import Callable, Any
from marshmallow import Schema

from .base import BaseConsumer
from .error import error_handler


class Consumer(BaseConsumer):
    def __init__(self, schema: Schema, callback: Callable[[dict], Any]):
        super().__init__()
        self._schema = schema
        self._callback = callback

    @error_handler
    def process(self, msg: any):
        data = self._schema.loads(msg.value())
        self._callback(data)
