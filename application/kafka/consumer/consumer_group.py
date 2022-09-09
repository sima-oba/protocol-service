import signal

from .base import BaseConsumer


class ConsumerGroup:
    def __init__(self, config: dict) -> None:
        self._config = config
        self._consumers = []

    def add(self, consumer: BaseConsumer, topic: str):
        consumer.start(self._config, topic)
        self._consumers.append(consumer)

    def wait(self):
        def shutdown(*_):
            self.shutdown()

        signal.signal(signal.SIGHUP, shutdown)
        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

        for consumer in self._consumers:
            consumer.wait()

    def shutdown(self):
        for consumer in self._consumers:
            consumer.shutdown()
