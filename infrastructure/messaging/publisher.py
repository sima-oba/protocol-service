import json
from confluent_kafka import Producer
from uuid import uuid4

from domain.messaging import IPublisher


class KafkaPublisher(IPublisher):
    def __init__(self, config: dict):
        self._producer = Producer(config)

    def send(self, topic: str, payload: dict, _id: str = None) -> str:
        key = _id or str(uuid4())
        payload = json.dumps(payload, ensure_ascii=False)
        self._producer.produce(topic, key=key, value=payload)
        self._producer.flush()
