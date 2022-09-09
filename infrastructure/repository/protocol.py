from pymongo.database import Database
from typing import List, Optional

from domain.model import Protocol
from domain.repository import IProtocolRepository


class ProtocolRepository(IProtocolRepository):
    def __init__(self, database: Database):
        self._collection = database.get_collection('protocols')

    def _to_doc(self, protocol: Protocol) -> dict:
        doc = protocol.to_dict()
        doc['protocol_type'] = doc['protocol_type'].value
        doc['priority'] = doc['priority'].value
        doc['status'] = doc['status'].value
        return doc

    def find_by_id(self, _id) -> Optional[Protocol]:
        doc = self._collection.find_one({'_id': _id})
        return Protocol.from_dict(doc) if doc else None

    def find_all(self) -> List[Protocol]:
        docs = self._collection.find()
        return [Protocol.from_dict(doc) for doc in docs]

    def search(self, filter: dict) -> List[Protocol]:
        docs = self._collection.find(filter)
        return [Protocol.from_dict(doc) for doc in docs]

    def add(self, protocol: Protocol) -> Protocol:
        doc = self._to_doc(protocol)
        self._collection.insert_one(doc)
        return protocol

    def update(self, protocol: Protocol) -> Protocol:
        doc = self._to_doc(protocol)
        self._collection.replace_one({'_id': protocol._id}, doc)
        return protocol
