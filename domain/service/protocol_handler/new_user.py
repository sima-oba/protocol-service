import logging
from dataclasses import asdict

from ...messaging import IPublisher
from ...model import Protocol
from .handler import ProtocolHandler


class NewUserHandler(ProtocolHandler):
    def __init__(self, publisher: IPublisher):
        self._publisher = publisher
        self._log = logging.getLogger(self.__class__.__name__)

    def on_complete(self, protocol: Protocol):
        owner = asdict(protocol.content)
        self._publisher.send('NEW_OWNER', owner, owner['_id'])
        self._log.debug(f'Sent new owner {owner["_id"]}')
