from abc import ABC

from ...model import Protocol, FileDict


class ProtocolHandler(ABC):
    def on_create(self, protocol: Protocol, files: FileDict):
        pass

    def on_accept(self, protocol: Protocol):
        pass

    def on_cancel(self, protocol: Protocol, files: FileDict):
        pass

    def on_complete(self, protocol: Protocol, files: FileDict):
        pass
