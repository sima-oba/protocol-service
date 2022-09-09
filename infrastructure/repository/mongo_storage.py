from flask import request
from gridfs import GridFS
from pymongo.database import Database
from uuid import uuid4
from typing import Optional

from domain.model import File
from domain.repository import IStorage


class MongoStorage(IStorage):
    def __init__(self, database: Database, endpoint_path: str):
        self._fs = GridFS(database, 'files')
        self._path = endpoint_path

    def write(self, file: File, key: str = None) -> str:
        key = key or str(uuid4())

        self._fs.put(
            file.stream,
            _id=key,
            filename=file.filename,
            content_type=file.mimetype
        )

        return f'{request.root_url.rstrip("/")}{self._path}/{key}'

    def open(self, key: str) -> Optional[File]:
        grid_out = self._fs.find_one(key)
        return File(grid_out.name, grid_out.content_type, grid_out) if grid_out else None

    def remove(self, key):
        self._fs.delete(key)
