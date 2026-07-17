from dataclasses import dataclass, field
from typing import Any
from slideforge.domain.entities.document_section import DocumentSection


@dataclass
class SourceDocument:
    id: str
    name: str
    source_path: str
    format: str
    sections: list[DocumentSection] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
