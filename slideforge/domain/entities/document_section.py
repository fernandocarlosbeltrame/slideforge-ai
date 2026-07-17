from dataclasses import dataclass, field
from typing import Any
from slideforge.domain.entities.content_block import ContentBlock


@dataclass
class DocumentSection:
    id: str
    title: str
    level: int = 1
    order: int = 0
    blocks: list[ContentBlock] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
