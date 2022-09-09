from dataclasses import dataclass
from typing import List, Optional

from .attachment import Attachment


@dataclass
class ProtocolResponse:
    message: Optional[str]
    attachments: List[Attachment]
