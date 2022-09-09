from abc import ABC, abstractmethod
from typing import List, Optional

from ..model import Protocol


class IProtocolRepository(ABC):
    @abstractmethod
    def find_all(self) -> List[Protocol]:
        pass

    @abstractmethod
    def search(self, filter: dict) -> List[Protocol]:
        pass

    @abstractmethod
    def find_by_id(self, _id) -> Optional[Protocol]:
        pass

    @abstractmethod
    def add(self, protocol: Protocol) -> Protocol:
        pass

    @abstractmethod
    def update(self, protocol: Protocol) -> Protocol:
        pass
