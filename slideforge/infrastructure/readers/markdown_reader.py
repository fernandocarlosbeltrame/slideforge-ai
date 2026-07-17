from pathlib import Path
from uuid import uuid4
from slideforge.domain.entities.content_block import ContentBlock
from slideforge.domain.entities.document_section import DocumentSection
from slideforge.domain.entities.source_document import SourceDocument
from slideforge.domain.enums.block_type import BlockType


class MarkdownReader:
    extensions = {".md", ".markdown"}

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in self.extensions

    def read(self, path: Path) -> SourceDocument:
        text = path.read_text(encoding="utf-8", errors="ignore")
        document = SourceDocument(id=str(uuid4()), name=path.name, source_path=str(path), format=path.suffix.lower().lstrip("."))
        current = DocumentSection(id=str(uuid4()), title=path.stem, order=1)
        document.sections.append(current)
        order = 1
        for raw in text.splitlines():
            line = raw.strip()
            if not line:
                continue
            if line.startswith("#"):
                title = line.lstrip("#").strip()
                if current.blocks:
                    current = DocumentSection(id=str(uuid4()), title=title, level=1, order=len(document.sections) + 1)
                    document.sections.append(current)
                else:
                    current.title = title
                current.blocks.append(ContentBlock(id=str(uuid4()), type=BlockType.TITLE if len(document.sections) == 1 else BlockType.SUBTITLE, text=title, hierarchy_level=line.count("#"), order=order, source_reference=f"line:{order}"))
            else:
                block_type = BlockType.LIST_ITEM if line.startswith(("-", "*", "•")) else BlockType.PARAGRAPH
                clean = line.lstrip("-*• ").strip()
                current.blocks.append(ContentBlock(id=str(uuid4()), type=block_type, text=clean, order=order, source_reference=f"line:{order}"))
            order += 1
        return document
