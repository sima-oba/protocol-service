from dataclasses import dataclass
from typing import Optional


@dataclass
class NewUser:
    _id: str
    username: str
    name: str
    doc: str
    phone: str


@dataclass
class PlainText:
    text: str


@dataclass
class PlantingAnticipation:
    farm_id: str
    notes: Optional[str]
