from uuid import uuid4
from slideforge.application.services.content_density_analyzer import ContentDensityAnalyzer
from slideforge.domain.entities.content_block import ContentBlock
from slideforge.domain.entities.document_section import DocumentSection
from slideforge.domain.entities.layout_decision import LayoutDecision
from slideforge.domain.entities.presentation_plan import PresentationPlan
from slideforge.domain.entities.slide_plan import SlidePlan
from slideforge.domain.entities.source_document import SourceDocument
from slideforge.domain.enums.block_type import BlockType
from slideforge.domain.enums.slide_layout_type import SlideLayoutType
from slideforge.domain.services.layout_selector import LayoutSelector


class PresentationPlanner:
    def __init__(self, layout_selector: LayoutSelector | None = None, density_analyzer: ContentDensityAnalyzer | None = None):
        self.density_analyzer = density_analyzer or ContentDensityAnalyzer()
        self.layout_selector = layout_selector or LayoutSelector(self.density_analyzer)

    def create_plan(self, document: SourceDocument) -> PresentationPlan:
        title = self._document_title(document)
        plan = PresentationPlan(id=str(uuid4()), title=title, source_document=document)
        sequence = 1
        cover_ids = self._cover_block_ids(document)
        cover = SlidePlan(sequence=sequence, title=title, subtitle=document.metadata.get("subtitle"), layout_type=SlideLayoutType.COVER, source_block_ids=cover_ids)
        cover.metadata["layout_decision"] = LayoutDecision(SlideLayoutType.COVER, "branded_cover", "Primeiro título do documento usado como capa.", ["document_title"], [], "low", 1.0).as_metadata()
        cover.metadata["density"] = self.density_analyzer.analyze_slide(cover).as_dict()
        plan.slides.append(cover)
        sequence += 1

        for section in document.sections:
            if self._is_title_only_section(section):
                continue
            decision = self.layout_selector.decide_for_section(section)
            slides = self._slides_for_section(section, decision.layout_type, sequence)
            self._decorate_slides(slides, decision)
            plan.slides.extend(slides)
            sequence += len(slides)

        self._mark_utilization(document, plan)
        return plan

    def _decorate_slides(self, slides: list[SlidePlan], decision: LayoutDecision) -> None:
        for slide in slides:
            slide.metadata["layout_decision"] = decision.as_metadata()
            slide.metadata["density"] = self.density_analyzer.analyze_slide(slide).as_dict()
            if slide.metadata["density"].get("level") == "critical":
                slide.render_notes.append("critical_density")

    def _slides_for_section(self, section: DocumentSection, layout: SlideLayoutType, start_sequence: int) -> list[SlidePlan]:
        if layout == SlideLayoutType.COMPARISON:
            slides = self._comparison_slides(section, start_sequence)
            slides.extend(self._image_slides_for_section(section, start_sequence + len(slides)))
            return slides
        if layout == SlideLayoutType.TIMELINE:
            content_blocks = [block for block in self._content_blocks(section) if block.type != BlockType.IMAGE]
            slides = [self._timeline_slide(section, start_sequence, content_blocks[:6])]
            if len(content_blocks) > 6:
                slides.extend(self._chunked_slides_from_blocks(section, SlideLayoutType.BULLETS, start_sequence + len(slides), content_blocks[6:]))
            slides.extend(self._image_slides_for_section(section, start_sequence + len(slides)))
            return slides
        if layout in {SlideLayoutType.CARDS, SlideLayoutType.PROCESS_FLOW, SlideLayoutType.CALLOUT, SlideLayoutType.IMAGE_TEXT}:
            slides = [self._single_slide(section, layout, start_sequence)]
            slides.extend(self._image_slides_for_section(section, start_sequence + len(slides)))
            return slides
        if layout == SlideLayoutType.IMAGE:
            return [self._image_slide(section, start_sequence)]
        if layout == SlideLayoutType.TABLE:
            return [self._single_slide(section, layout, start_sequence)]
        return self._chunked_slides(section, layout, start_sequence)

    def _single_slide(self, section: DocumentSection, layout: SlideLayoutType, sequence: int) -> SlidePlan:
        blocks = self._content_blocks(section)
        return SlidePlan(sequence=sequence, title=section.title, layout_type=layout, source_block_ids=self._section_title_block_ids(section) + [block.id for block in blocks], components=self._components_for_blocks(blocks))

    def _image_slide(self, section: DocumentSection, sequence: int) -> SlidePlan:
        blocks = self._content_blocks(section)
        return SlidePlan(sequence=sequence, title=section.title, layout_type=SlideLayoutType.IMAGE, source_block_ids=self._section_title_block_ids(section) + [block.id for block in blocks], components=self._components_for_blocks(blocks))

    def _image_slides_for_section(self, section: DocumentSection, start_sequence: int) -> list[SlidePlan]:
        slides: list[SlidePlan] = []
        title_ids = self._section_title_block_ids(section)
        for block in self._content_blocks(section):
            if block.type != BlockType.IMAGE:
                continue
            slides.append(SlidePlan(
                sequence=start_sequence + len(slides),
                title=section.title,
                layout_type=SlideLayoutType.IMAGE,
                source_block_ids=title_ids + [block.id],
                components=[{"type": "image", "path": block.metadata.get("path"), "caption": block.text, "fit_mode": "contain", "position": "related"}],
            ))
        return slides

    def _comparison_slides(self, section: DocumentSection, start_sequence: int) -> list[SlidePlan]:
        before: list[tuple[str, str]] = []
        after: list[tuple[str, str]] = []
        side = "before"
        marker_ids: list[str] = []
        for block in self._content_blocks(section):
            if block.type == BlockType.IMAGE:
                continue
            text = block.text.strip()
            if not text:
                continue
            split_pair = self._split_inline_before_after(block.id, text)
            if split_pair:
                before.extend(split_pair[0])
                after.extend(split_pair[1])
                continue
            marker_side, remainder = self._comparison_marker(text)
            if marker_side:
                side = marker_side
                marker_ids.append(block.id)
                if remainder:
                    (before if side == "before" else after).append((block.id, remainder))
                continue
            (before if side == "before" else after).append((block.id, text))

        slides: list[SlidePlan] = []
        max_items_per_side = 5
        total_parts = max(1, (max(len(before), len(after)) + max_items_per_side - 1) // max_items_per_side)
        title_ids = self._section_title_block_ids(section)
        for part in range(total_parts):
            b_chunk = before[part * max_items_per_side:(part + 1) * max_items_per_side]
            a_chunk = after[part * max_items_per_side:(part + 1) * max_items_per_side]
            title = self._part_title(section.title, part + 1) if total_parts > 1 else section.title
            ids = title_ids + (marker_ids if part == 0 else []) + [item_id for item_id, _ in b_chunk + a_chunk]
            if b_chunk and a_chunk:
                slides.append(SlidePlan(
                    sequence=start_sequence + len(slides),
                    title=title,
                    layout_type=SlideLayoutType.COMPARISON,
                    source_block_ids=ids,
                    components=[{"type": "comparison", "before": [text for _, text in b_chunk], "after": [text for _, text in a_chunk]}],
                ))
                continue
            side_label = "ANTES" if b_chunk else "DEPOIS"
            items = [text for _, text in (b_chunk or a_chunk)]
            if len(items) <= 2 and slides and "comparison_overflow" in slides[-1].render_notes:
                text_component = next((component for component in slides[-1].components if component.get("type") == "text"), None)
                if text_component and len(text_component.get("items", [])) + len(items) <= 6:
                    text_component["items"].extend(items)
                    slides[-1].source_block_ids.extend(block_id for block_id in ids if block_id not in slides[-1].source_block_ids)
                    continue
            slides.append(SlidePlan(
                sequence=start_sequence + len(slides),
                title=f"{title} - {side_label}",
                layout_type=SlideLayoutType.BULLETS,
                source_block_ids=ids,
                components=[{"type": "text", "items": items}],
                render_notes=["comparison_overflow"],
            ))
        return slides

    @staticmethod
    def _comparison_marker(text: str) -> tuple[str | None, str]:
        normalized = (text or "").replace("\r", "").strip()
        normalized = normalized.lstrip("•-*✓✗🔴🟢✅❌ ").strip()
        lowered = normalized.lower()
        for label, side in (("antes", "before"), ("depois", "after")):
            if lowered == label:
                return side, ""
            if lowered.startswith(label + ":"):
                return side, normalized.split(":", 1)[1].strip()
            if lowered.startswith(label + "\n"):
                return side, normalized.split("\n", 1)[1].strip()
            if lowered.startswith(label + " -"):
                return side, normalized.split("-", 1)[1].strip()
        return None, ""

    @staticmethod
    def _split_inline_before_after(block_id: str, text: str) -> tuple[list[tuple[str, str]], list[tuple[str, str]]] | None:
        lowered = (text or "").lower()
        if "antes:" not in lowered or "depois:" not in lowered:
            return None
        before_text = text
        after_text = ""
        parts = text.split("DEPOIS:", 1) if "DEPOIS:" in text else text.split("Depois:", 1)
        if len(parts) == 2:
            before_text, after_text = parts
        before_text = before_text.split("ANTES:", 1)[-1] if "ANTES:" in before_text else before_text.split("Antes:", 1)[-1]
        before_text = before_text.strip().lstrip("•-*✓✗🔴🟢✅❌ ").strip()
        after_text = after_text.strip().lstrip("•-*✓✗🔴🟢✅❌ ").strip()
        before_items = [(block_id, before_text)] if before_text else []
        after_items = [(block_id, after_text)] if after_text else []
        return before_items, after_items

    def _timeline_slide(self, section: DocumentSection, sequence: int, blocks: list[ContentBlock] | None = None) -> SlidePlan:
        selected_blocks = blocks if blocks is not None else self._content_blocks(section)
        return SlidePlan(sequence=sequence, title=section.title, layout_type=SlideLayoutType.TIMELINE, source_block_ids=self._section_title_block_ids(section) + [block.id for block in selected_blocks], components=self._components_for_blocks(selected_blocks))

    def _chunked_slides(self, section: DocumentSection, layout: SlideLayoutType, start_sequence: int) -> list[SlidePlan]:
        slides: list[SlidePlan] = []
        chunk: list[ContentBlock] = []
        chars = 0
        max_items = 5
        max_chars = 620
        for block in self._content_blocks(section):
            if block.type == BlockType.IMAGE:
                large = self._is_large_image(block)
                if large:
                    if chunk:
                        slides.append(self._build_chunk_slide(section, layout, start_sequence + len(slides), chunk, len(slides) + 1))
                        chunk = []
                        chars = 0
                    slides.append(SlidePlan(sequence=start_sequence + len(slides), title=section.title, layout_type=SlideLayoutType.IMAGE, source_block_ids=self._section_title_block_ids(section) + [block.id], components=[{"type": "image", "path": block.metadata.get("path"), "caption": block.text, "fit_mode": "contain", "position": "exclusive"}]))
                    continue
                chunk.append(block)
                continue
            text_len = len(block.text or "")
            if chunk and (len(chunk) >= max_items or chars + text_len > max_chars):
                slides.append(self._build_chunk_slide(section, layout, start_sequence + len(slides), chunk, len(slides) + 1))
                chunk = []
                chars = 0
            if text_len > max_chars:
                parts = self._split_long_text(block.text, max_chars)
                for part in parts:
                    proxy = ContentBlock(id=block.id, type=block.type, text=part, hierarchy_level=block.hierarchy_level, order=block.order, source_reference=block.source_reference, metadata=block.metadata)
                    slides.append(SlidePlan(sequence=start_sequence + len(slides), title=self._part_title(section.title, len(slides) + 1), layout_type=SlideLayoutType.BULLETS, source_block_ids=self._section_title_block_ids(section) + [block.id], components=[{"type": "text", "items": [proxy.text]}], render_notes=["partial"]))
                continue
            chunk.append(block)
            chars += text_len
        if chunk:
            slides.append(self._build_chunk_slide(section, layout, start_sequence + len(slides), chunk, len(slides) + 1))
        return slides

    def _chunked_slides_from_blocks(self, section: DocumentSection, layout: SlideLayoutType, start_sequence: int, blocks: list[ContentBlock]) -> list[SlidePlan]:
        slides: list[SlidePlan] = []
        chunk: list[ContentBlock] = []
        chars = 0
        max_items = 5
        max_chars = 620
        for block in blocks:
            text_len = len(block.text or "")
            if chunk and (len(chunk) >= max_items or chars + text_len > max_chars):
                slides.append(self._build_chunk_slide(section, layout, start_sequence + len(slides), chunk, len(slides) + 2))
                chunk = []
                chars = 0
            chunk.append(block)
            chars += text_len
        if chunk:
            slides.append(self._build_chunk_slide(section, layout, start_sequence + len(slides), chunk, len(slides) + 2))
        return slides

    def _build_chunk_slide(self, section: DocumentSection, layout: SlideLayoutType, sequence: int, blocks: list[ContentBlock], part: int) -> SlidePlan:
        title = self._part_title(section.title, part) if part > 1 else section.title
        return SlidePlan(sequence=sequence, title=title, layout_type=layout, source_block_ids=self._section_title_block_ids(section) + [block.id for block in blocks], components=self._components_for_blocks(blocks))

    @staticmethod
    def _is_large_image(block: ContentBlock) -> bool:
        width = block.metadata.get("width_px") or 0
        height = block.metadata.get("height_px") or 0
        return width >= 420 or height >= 260

    @staticmethod
    def _split_long_text(text: str, max_chars: int) -> list[str]:
        words = text.split()
        parts: list[str] = []
        current: list[str] = []
        size = 0
        for word in words:
            if current and size + len(word) + 1 > max_chars:
                parts.append(" ".join(current))
                current = []
                size = 0
            current.append(word)
            size += len(word) + 1
        if current:
            parts.append(" ".join(current))
        return parts

    @staticmethod
    def _components_for_blocks(blocks: list[ContentBlock]) -> list[dict]:
        components: list[dict] = []
        text_items = [block.text for block in blocks if block.is_textual and block.text]
        images = [block for block in blocks if block.type == BlockType.IMAGE]
        tables = [block for block in blocks if block.type == BlockType.TABLE]
        if text_items:
            components.append({"type": "text", "items": text_items})
        for image in images:
            components.append({"type": "image", "path": image.metadata.get("path"), "caption": image.text})
        for table in tables:
            components.append({"type": "table", "rows": table.metadata.get("rows", [])})
        return components

    @staticmethod
    def _section_title_block_ids(section: DocumentSection) -> list[str]:
        return [block.id for block in section.blocks if block.type in {BlockType.TITLE, BlockType.SUBTITLE}]

    @staticmethod
    def _content_blocks(section: DocumentSection) -> list[ContentBlock]:
        return [block for block in section.blocks if block.type not in {BlockType.TITLE, BlockType.SUBTITLE}]

    @staticmethod
    def _part_title(title: str, part: int) -> str:
        return f"{title} - Parte {part}"

    @staticmethod
    def _document_title(document: SourceDocument) -> str:
        for section in document.sections:
            for block in section.blocks:
                if block.type == BlockType.TITLE and block.text:
                    return block.text
        return document.name.rsplit(".", 1)[0]

    @staticmethod
    def _cover_block_ids(document: SourceDocument) -> list[str]:
        ids: list[str] = []
        for section in document.sections:
            for block in section.blocks:
                if block.type in {BlockType.TITLE, BlockType.SUBTITLE}:
                    ids.append(block.id)
            if ids:
                return ids
        return []

    @staticmethod
    def _is_title_only_section(section: DocumentSection) -> bool:
        return all(block.type in {BlockType.TITLE, BlockType.SUBTITLE} for block in section.blocks)

    @staticmethod
    def _mark_utilization(document: SourceDocument, plan: PresentationPlan) -> None:
        used_ids = {block_id for slide in plan.slides for block_id in slide.source_block_ids}
        split_ids = {block_id for block_id in used_ids if sum(block_id in slide.source_block_ids for slide in plan.slides) > 1}
        for section in document.sections:
            for block in section.blocks:
                if block.id in split_ids:
                    block.utilization_status = "split"
                elif block.id in used_ids:
                    block.utilization_status = "used"
                else:
                    block.utilization_status = "unused"






