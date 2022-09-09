from typing import List

from ...exception import (
    MissingFileError,
    WrongFileTypeError,
    InvalidStateError
)
from ...model import Protocol, Attachment, FileDict
from ...repository import IStorage
from .handler import ProtocolHandler


class PlantingAnticipationHandler(ProtocolHandler):
    def __init__(self, storage: IStorage):
        self._storage = storage

    def on_create(self, protocol: Protocol, files: FileDict):
        self._validate_file('rg_cnpj', 'image/jpeg', files)
        self._validate_file('commitment', 'application/pdf', files)
        self._validate_file('sketch', 'application/pdf', files)
        self._validate_file('soy_planting', 'application/pdf', files)
        self._validate_file('art', 'application/pdf', files)
        self._validate_file('work_plan', 'application/pdf', files)
        protocol.attachments = self._save_all_files(files)

    def on_cancel(self, protocol: Protocol, files: FileDict):
        if protocol.response.message is None:
            raise InvalidStateError('Missing cancellation reason')

    # def on_complete(self, protocol: Protocol, files: FileDict):
        # self._validate_file('ordinance', 'application/pdf', files)
        # protocol.response.attachments = self._save_all_files(files)

    def _validate_file(self, name: str, mimetype: str, files: FileDict):
        if name not in files.keys():
            raise MissingFileError(name)

        file = files[name]

        if file.mimetype != mimetype:
            raise WrongFileTypeError(file.filename, file.mimetype)

    def _save_all_files(self, files: FileDict) -> List[Attachment]:
        attachments = []

        for file in files.values():
            href = self._storage.write(file)
            attachment = Attachment(file.filename, file.mimetype, href)
            attachments.append(attachment)

        return attachments
