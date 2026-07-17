from dataclasses import dataclass, field
from slideforge.application.services.slide_geometry import SlideGeometry
from slideforge.domain.entities.presentation_plan import PresentationPlan
from slideforge.domain.enums.block_type import BlockType


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors


class PresentationValidator:
    def __init__(self, geometry: SlideGeometry | None = None):
        self.geometry = geometry or SlideGeometry()

    def validate_plan(self, plan: PresentationPlan) -> ValidationResult:
        result = ValidationResult()
        if not plan.slides:
            result.errors.append("A apresentação não possui slides.")
        used_ids = {block_id for slide in plan.slides for block_id in slide.source_block_ids}
        for section in plan.source_document.sections:
            for block in section.blocks:
                if block.id not in used_ids:
                    result.errors.append(f"Bloco obrigatório sem uso: {block.id}")
                if block.type == BlockType.IMAGE and not block.metadata.get("path"):
                    result.warnings.append(f"Imagem sem arquivo associado: {block.id}")
        layouts = [slide.layout_type.value for slide in plan.slides]
        if len(set(layouts)) < min(4, len(layouts)):
            result.warnings.append("Baixa variedade de layouts detectada.")
        for slide in plan.slides:
            if slide.sequence <= 0:
                result.errors.append("Slide com sequência inválida.")
            if len(slide.title) > 140:
                result.warnings.append(f"Título muito longo no slide {slide.sequence}.")
            density = slide.metadata.get("density", {}).get("level")
            if density == "critical":
                result.warnings.append(f"Slide {slide.sequence} possui densidade visual crítica.")
            if not slide.metadata.get("layout_decision"):
                result.warnings.append(f"Slide {slide.sequence} sem decisão visual registrada.")
        return result
