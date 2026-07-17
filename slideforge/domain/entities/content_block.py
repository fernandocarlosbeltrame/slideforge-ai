from dataclasses import dataclass, field
from typing import Any
from slideforge.domain.enums.block_type import BlockType


@dataclass
class ContentBlock:
    id: str
    type: BlockType
    text: str = ""
    hierarchy_level: int = 0
    order: int = 0
    source_reference: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    utilization_status: str = "unused"

    @property
    def is_textual(self) -> bool:
        return self.type in {
            BlockType.TITLE,
            BlockType.SUBTITLE,
            BlockType.PARAGRAPH,
            BlockType.LIST,
            BlockType.LIST_ITEM,
            BlockType.NOTE,
        }
