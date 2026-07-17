from pathlib import Path
from uuid import uuid4
from slideforge.domain.entities.content_block import ContentBlock
from slideforge.domain.entities.document_section import DocumentSection
from slideforge.domain.entities.source_document import SourceDocument
from slideforge.domain.enums.block_type import BlockType


class PDFReader:
    extensions = {".pdf"}

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in self.extensions

    def read(self, path: Path) -> SourceDocument:
        try:
            import fitz
        except ImportError as exc:
            raise RuntimeError("PyMuPDF não está instalado. Execute: pip install PyMuPDF") from exc
        document = SourceDocument(id=str(uuid4()), name=path.name, source_path=str(path), format="pdf")
        asset_dir = path.parent / ".slideforge_assets" / path.stem
        asset_dir.mkdir(parents=True, exist_ok=True)
        pdf = fitz.open(path)
        document.metadata.update({"page_count": pdf.page_count, "pdf_metadata": pdf.metadata})
        order = 1
        found_text = False
        for page_index, page in enumerate(pdf, start=1):
            section = DocumentSection(id=str(uuid4()), title=f"Página {page_index}", order=page_index, metadata={"page": page_index})
            text_blocks = page.get_text("blocks")
            text_blocks = sorted(text_blocks, key=lambda item: (item[1], item[0]))
            for block in text_blocks:
                text = (block[4] or "").strip()
                if not text:
                    continue
                found_text = True
                block_type = BlockType.SUBTITLE if len(text) < 90 and order == 1 else BlockType.PARAGRAPH
                section.blocks.append(ContentBlock(id=str(uuid4()), type=block_type, text=text, order=order, source_reference=f"page:{page_index}:block:{order}", metadata={"page": page_index, "bbox": block[:4]}))
                order += 1
            for img_index, img in enumerate(page.get_images(full=True), start=1):
                xref = img[0]
                try:
                    data = pdf.extract_image(xref)
                    ext = data.get("ext", "png")
                    target = asset_dir / f"page_{page_index}_image_{img_index}.{ext}"
                    target.write_bytes(data["image"])
                    section.blocks.append(ContentBlock(id=str(uuid4()), type=BlockType.IMAGE, text=f"Imagem PDF {page_index}.{img_index}", order=order, source_reference=f"page:{page_index}:image:{img_index}", metadata={"path": str(target), "format": ext, "page": page_index, "width_px": data.get("width", 0), "height_px": data.get("height", 0), "aspect_ratio": data.get("width", 0) / data.get("height", 1) if data.get("height", 0) else None}))
                    order += 1
                except Exception:
                    continue
            if section.blocks:
                document.sections.append(section)
        if not found_text:
            document.metadata["scanned_pdf_warning"] = "PDF sem texto extraível; OCR não é suportado nesta fase."
            document.sections.append(DocumentSection(id=str(uuid4()), title="PDF sem texto extraível", order=1, blocks=[ContentBlock(id=str(uuid4()), type=BlockType.NOTE, text="PDF sem texto extraível; OCR não é suportado nesta fase.", order=1)]))
        pdf.close()
        return document
