from collections import Counter
from slideforge.domain.entities.content_audit import ContentAudit
from slideforge.domain.entities.presentation_plan import PresentationPlan
from slideforge.domain.enums.block_type import BlockType


class ContentAuditor:
    def audit(self, plan: PresentationPlan, warnings: list[str] | None = None, critical_overflows: int = 0) -> ContentAudit:
        all_ids = {block.id for section in plan.source_document.sections for block in section.blocks}
        image_ids = {block.id for section in plan.source_document.sections for block in section.blocks if block.type == BlockType.IMAGE}
        usage_counter = Counter(block_id for slide in plan.slides for block_id in slide.source_block_ids)
        used = {block_id for block_id, count in usage_counter.items() if count == 1}
        split = {block_id for block_id, count in usage_counter.items() if count > 1}
        unused = all_ids - set(usage_counter.keys())
        partial = {block_id for slide in plan.slides for block_id in slide.source_block_ids if "partial" in slide.render_notes}
        used_images = image_ids & set(usage_counter.keys())
        unused_images = image_ids - used_images
        resized_images = set()
        adjusted_titles = set()
        wrapped_titles = set()
        split_tables = set()
        visual_warnings: list[str] = []
        layout_counts: Counter[str] = Counter()
        density_counts: Counter[str] = Counter()
        for slide in plan.slides:
            layout_counts[slide.layout_type.value] += 1
            density = slide.metadata.get("density", {}).get("level", "unknown")
            density_counts[density] += 1
            if density == "critical":
                visual_warnings.append(f"Slide {slide.sequence} com densidade crítica: {slide.title}")
            decision = slide.metadata.get("layout_decision", {})
            if not decision:
                visual_warnings.append(f"Slide {slide.sequence} sem decisão visual registrada.")
            for component in slide.components:
                if component.get("type") == "image" and component.get("path"):
                    resized_images.update(block_id for block_id in slide.source_block_ids if block_id in image_ids)
            if len(slide.title) > 72:
                adjusted_titles.update(slide.source_block_ids[:1])
            if len(slide.title) > 42:
                wrapped_titles.update(slide.source_block_ids[:1])
            if "table_split" in slide.render_notes:
                split_tables.update(slide.source_block_ids)
        return ContentAudit(
            used_block_ids=used,
            partially_used_block_ids=partial,
            unused_block_ids=unused,
            split_block_ids=split,
            used_image_ids=used_images,
            unused_image_ids=unused_images,
            resized_image_ids=resized_images,
            adjusted_title_ids=adjusted_titles,
            wrapped_title_ids=wrapped_titles,
            split_table_ids=split_tables,
            warnings=warnings or [],
            visual_warnings=visual_warnings,
            layout_counts=dict(layout_counts),
            density_counts=dict(density_counts),
            critical_overflows=critical_overflows + density_counts.get("critical", 0),
            slide_count=len(plan.slides),
        )
