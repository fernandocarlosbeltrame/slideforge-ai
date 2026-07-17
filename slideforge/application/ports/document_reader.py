from pathlib import Path
from typing import Protocol
from slideforge.domain.entities.source_document import SourceDocument


class DocumentReader(Protocol):
    def supports(self, path: Path) -> bool:
        ...

    def read(self, path: Path) -> SourceDocument:
        ...
