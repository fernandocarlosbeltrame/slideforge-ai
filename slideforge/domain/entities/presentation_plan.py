from dataclasses import dataclass, field
from typing import Any
from slideforge.domain.entities.source_document import SourceDocument
from slideforge.domain.entities.slide_plan import SlidePlan


@dataclass
class PresentationPlan:
    id: str
    title: str
    source_document: SourceDocument
    slides: list[SlidePlan] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
