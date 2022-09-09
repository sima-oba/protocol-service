from abc import ABC, abstractmethod


class IPublisher(ABC):
    @abstractmethod
    def send(self, topic: str, payload: dict, _id: str = None) -> str:
        pass
