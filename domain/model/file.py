from dataclasses import dataclass
from typing import IO, Dict


@dataclass
class File:
    filename: str
    mimetype: str
    stream: IO


FileDict = Dict[str, File]
