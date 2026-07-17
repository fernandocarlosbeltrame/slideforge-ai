from pathlib import Path
from typing import Protocol
from slideforge.domain.entities.presentation_plan import PresentationPlan


class PresentationExporter(Protocol):
    def export(self, plan: PresentationPlan, output_path: Path, *, banner_path: str | None = None, logo_path: str | None = None) -> Path:
        ...
