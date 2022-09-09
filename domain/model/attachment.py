from dataclasses import dataclass


@dataclass
class Attachment:
    filename: str
    mimetype: str
    href: str
