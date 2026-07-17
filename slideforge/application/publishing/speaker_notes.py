from dataclasses import dataclass
from slideforge.domain.entities.presentation_plan import PresentationPlan
from slideforge.domain.entities.slide_plan import SlidePlan


@dataclass(frozen=True)
class SpeakerNote:
    slide_sequence: int
    summary: str
    source_block_ids: list[str]
    audit_notes: list[str]


class SpeakerNotesGenerator:
    def generate_for_slide(self, plan: PresentationPlan, slide: SlidePlan) -> SpeakerNote:
        summary = slide.title
        text_items: list[str] = []
        for component in slide.components:
            text_items.extend(component.get("items", []))
            text_items.extend(component.get("before", []))
            text_items.extend(component.get("after", []))
            if component.get("caption"):
                text_items.append(component["caption"])
        if text_items:
            summary = f"{slide.title}: " + " ".join(text_items)[:240]
        audit_notes = []
        density = slide.metadata.get("density", {}).get("level")
        if density:
            audit_notes.append(f"Densidade visual: {density}")
        decision = slide.metadata.get("layout_decision", {}).get("reason")
        if decision:
            audit_notes.append(f"Layout: {decision}")
        return SpeakerNote(slide.sequence, summary, list(slide.source_block_ids), audit_notes)

    def generate(self, plan: PresentationPlan) -> list[SpeakerNote]:
        return [self.generate_for_slide(plan, slide) for slide in plan.slides]
