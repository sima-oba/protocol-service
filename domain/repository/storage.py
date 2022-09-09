from abc import ABC, abstractmethod
from typing import Optional

from ..model import File


class IStorage(ABC):
    @abstractmethod
    def write(self, file: File, key: Optional[str]) -> str:
        pass

    @abstractmethod
    def open(self, key: str) -> Optional[File]:
        pass

    @abstractmethod
    def remove(self, key):
        pass
