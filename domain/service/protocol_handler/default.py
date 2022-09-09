from typing import List

from ...model import Attachment, Protocol, FileDict
from ...repository import IStorage
from .handler import ProtocolHandler


class DefaultHandler(ProtocolHandler):
    def __init__(self, storage: IStorage):
        self._storage = storage

    def on_create(self, protocol: Protocol, files: FileDict):
        protocol.attachments = self._save_files(files)

    def on_cancel(self, protocol: Protocol, files: FileDict):
        protocol.response.attachments = self._save_files(files)

    def on_complete(self, protocol: Protocol, files: FileDict):
        protocol.response.attachments = self._save_files(files)

    def _save_files(self, files: FileDict) -> List[Attachment]:
        attachments = []

        for file in files.values():
            href = self._storage.write(file)
            attachment = Attachment(file.filename, file.mimetype, href)
            attachments.append(attachment)

        return attachments
