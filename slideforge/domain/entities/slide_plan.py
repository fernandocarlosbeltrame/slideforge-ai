from dataclasses import dataclass, field
from typing import Any
from slideforge.domain.enums.slide_layout_type import SlideLayoutType


@dataclass
class SlidePlan:
    sequence: int
    title: str
    layout_type: SlideLayoutType
    source_block_ids: list[str] = field(default_factory=list)
    subtitle: str | None = None
    components: list[dict[str, Any]] = field(default_factory=list)
    render_notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
