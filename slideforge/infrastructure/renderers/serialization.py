from __future__ import annotations
from dataclasses import asdict, is_dataclass
from typing import Any
from slideforge.application.publishing.speaker_notes import SpeakerNotesGenerator
from slideforge.domain.entities.content_audit import ContentAudit
from slideforge.domain.entities.presentation_plan import PresentationPlan
from slideforge.domain.entities.slide_plan import SlidePlan


def component_text_items(component: dict) -> list[str]:
    items: list[str] = []
    items.extend(str(item) for item in component.get("items", []) if item)
    items.extend(str(item) for item in component.get("before", []) if item)
    items.extend(str(item) for item in component.get("after", []) if item)
    if component.get("caption"):
        items.append(str(component["caption"]))
    rows = component.get("rows", [])
    for row in rows:
        items.append(" | ".join(str(cell) for cell in row))
    return items


def slide_text(slide: SlidePlan) -> str:
    parts = [slide.title]
    if slide.subtitle:
        parts.append(slide.subtitle)
    for component in slide.components:
        parts.extend(component_text_items(component))
    return "\n".join(part for part in parts if part)


def plan_agenda(plan: PresentationPlan) -> list[tuple[int, str]]:
    return [(slide.sequence, slide.title) for slide in plan.slides if slide.layout_type.value != "cover"]


def audit_dict(audit: ContentAudit | None) -> dict[str, Any]:
    if audit is None:
        return {}
    return {
        "used_block_ids": sorted(audit.used_block_ids),
        "partially_used_block_ids": sorted(audit.partially_used_block_ids),
        "unused_block_ids": sorted(audit.unused_block_ids),
        "split_block_ids": sorted(audit.split_block_ids),
        "used_image_ids": sorted(audit.used_image_ids),
        "unused_image_ids": sorted(audit.unused_image_ids),
        "warnings": list(audit.warnings),
        "visual_warnings": list(audit.visual_warnings),
        "layout_counts": dict(audit.layout_counts),
        "density_counts": dict(audit.density_counts),
        "critical_overflows": audit.critical_overflows,
        "slide_count": audit.slide_count,
    }


def plan_to_dict(plan: PresentationPlan, audit: ContentAudit | None = None) -> dict[str, Any]:
    notes = {note.slide_sequence: note for note in SpeakerNotesGenerator().generate(plan)}
    return {
        "id": plan.id,
        "title": plan.title,
        "metadata": _safe(plan.metadata),
        "source_document": {
            "id": plan.source_document.id,
            "name": plan.source_document.name,
            "source_path": plan.source_document.source_path,
            "format": plan.source_document.format,
            "metadata": _safe(plan.source_document.metadata),
        },
        "slides": [
            {
                "sequence": slide.sequence,
                "title": slide.title,
                "subtitle": slide.subtitle,
                "layout_type": slide.layout_type.value,
                "source_block_ids": list(slide.source_block_ids),
                "components": _safe(slide.components),
                "render_notes": list(slide.render_notes),
                "metadata": _safe(slide.metadata),
                "speaker_notes": _safe(notes[slide.sequence]),
            }
            for slide in plan.slides
        ],
        "agenda": plan_agenda(plan),
        "audit": audit_dict(audit),
        "statistics": {
            "slide_count": len(plan.slides),
            "component_count": sum(len(slide.components) for slide in plan.slides),
            "block_reference_count": sum(len(slide.source_block_ids) for slide in plan.slides),
        },
    }


def _safe(value: Any) -> Any:
    if is_dataclass(value):
        return _safe(asdict(value))
    if isinstance(value, dict):
        return {str(k): _safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_safe(item) for item in value]
    if hasattr(value, "value"):
        return value.value
    if hasattr(value, "__fspath__"):
        return str(value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)
