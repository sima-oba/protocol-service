import logging
from datetime import datetime
from typing import List, Optional

from ..exception import EntityNotFoundError, InvalidStateError
from ..model import Protocol, ProtocolType, ProtocolResponse, Status, FileDict
from ..repository import IProtocolRepository
from .protocol_handler import ProtocolHandler


class ProtocolService:
    def __init__(self, repo: IProtocolRepository):
        self._repo = repo
        self._handlers = {}
        self._log = logging.getLogger(self.__class__.__name__)

    def add_handler(self, _type: ProtocolType, handler: ProtocolHandler):
        self._handlers[_type] = handler

    def get_handler(self, _type: ProtocolType) -> ProtocolHandler:
        if _type not in self._handlers.keys():
            raise ValueError(f'No handler suitable for type {_type.name}')

        return self._handlers[_type]

    def get_protocol(self, protocol_id: str) -> Protocol:
        protocol = self._repo.find_by_id(protocol_id)

        if protocol is None:
            raise EntityNotFoundError(Protocol, protocol_id)

        return protocol

    def _get_protocol_if_active(self, protocol_id: str) -> Protocol:
        protocol = self.get_protocol(protocol_id)

        if protocol.status in [Status.COMPLETED, Status.CANCELED]:
            raise InvalidStateError(
                f'Protocol {protocol._id} is no longer active'
            )

        return protocol

    def get_all_protocols(self) -> List[Protocol]:
        return self._repo.find_all()

    def search_protocols(self, filter: dict) -> List[Protocol]:
        return self._repo.search(filter)

    def create(self, data: dict, files: FileDict = {}) -> Protocol:
        protocol = Protocol.new({
            'status':           Status.PENDING,
            'started_at':       None,
            'finished_at':      None,
            'protocol_type':    data['protocol_type'],
            'requester':        data['requester'],
            'priority':         data['priority'],
            'content':          data['content'],
            'response':         None,
            'attachments':      [],
        })

        handler = self.get_handler(protocol.protocol_type)
        handler.on_create(protocol, files)
        self._repo.add(protocol)
        self._log.debug(f'Submitted protocol {protocol._id}')

        return protocol

    def accept(self, protocol_id: str) -> Protocol:
        now = datetime.utcnow()

        protocol = self._get_protocol_if_active(protocol_id)
        protocol.status = Status.IN_PROGRESS
        protocol.updated_at = now
        protocol.started_at = now

        handler = self.get_handler(protocol.protocol_type)
        handler.on_accept(protocol)
        self._repo.update(protocol)
        self._log.debug(f'Accepted protocol {protocol._id}')

        return protocol

    def cancel(
        self,
        protocol_id: str,
        message: Optional[str],
        files: FileDict
    ) -> Protocol:
        now = datetime.utcnow()

        protocol = self._get_protocol_if_active(protocol_id)
        protocol.status = Status.CANCELED
        protocol.updated_at = now
        protocol.finished_at = now
        protocol.response = ProtocolResponse(message, [])

        if protocol.started_at is None:
            protocol.started_at = now

        handler = self.get_handler(protocol.protocol_type)
        handler.on_cancel(protocol, files)
        self._repo.update(protocol)
        self._log.debug(f'Canceled protocol {protocol._id}')

        return protocol

    def complete(
        self,
        protocol_id: str,
        message: Optional[str],
        files: FileDict
    ) -> Protocol:
        now = datetime.utcnow()

        protocol = self._get_protocol_if_active(protocol_id)
        protocol.status = Status.COMPLETED
        protocol.updated_at = now
        protocol.finished_at = now
        protocol.response = ProtocolResponse(message, [])

        if protocol.started_at is None:
            protocol.started_at = now

        handler = self.get_handler(protocol.protocol_type)
        handler.on_complete(protocol, files)
        self._repo.update(protocol)
        self._log.debug(f'Completed protocol {protocol._id}')

        return protocol
