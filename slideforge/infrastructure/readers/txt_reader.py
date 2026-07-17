from pathlib import Path
from uuid import uuid4
from slideforge.domain.entities.content_block import ContentBlock
from slideforge.domain.entities.document_section import DocumentSection
from slideforge.domain.entities.source_document import SourceDocument
from slideforge.domain.enums.block_type import BlockType


class TxtReader:
    extensions = {".txt"}

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in self.extensions

    def read(self, path: Path) -> SourceDocument:
        text = path.read_text(encoding="utf-8", errors="ignore")
        document = SourceDocument(id=str(uuid4()), name=path.name, source_path=str(path), format=path.suffix.lower().lstrip("."))
        section = DocumentSection(id=str(uuid4()), title=path.stem, order=1)
        order = 1
        for raw in text.splitlines():
            line = raw.strip()
            if not line:
                continue
            block_type = BlockType.LIST_ITEM if line.startswith(("-", "*", "•")) else BlockType.PARAGRAPH
            clean = line.lstrip("-*• ").strip()
            section.blocks.append(ContentBlock(id=str(uuid4()), type=block_type, text=clean, order=order, source_reference=f"line:{order}"))
            order += 1
        if not section.blocks:
            section.blocks.append(ContentBlock(id=str(uuid4()), type=BlockType.NOTE, text="Documento sem conteúdo textual identificável.", order=1))
        document.sections.append(section)
        return document
