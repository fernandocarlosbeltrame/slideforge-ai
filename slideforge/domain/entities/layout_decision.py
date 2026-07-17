from dataclasses import dataclass, field
from slideforge.domain.enums.slide_layout_type import SlideLayoutType


@dataclass(frozen=True)
class LayoutDecision:
    layout_type: SlideLayoutType
    visual_composition: str
    reason: str
    rules_triggered: list[str] = field(default_factory=list)
    alternatives: list[str] = field(default_factory=list)
    density: str = "medium"
    score: float = 1.0

    def as_metadata(self) -> dict:
        return {
            "layout_type": self.layout_type.value,
            "visual_composition": self.visual_composition,
            "reason": self.reason,
            "rules_triggered": list(self.rules_triggered),
            "alternatives": list(self.alternatives),
            "density": self.density,
            "score": self.score,
        }
