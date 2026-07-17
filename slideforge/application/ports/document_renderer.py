from pathlib import Path
from typing import Protocol
from slideforge.domain.entities.content_audit import ContentAudit
from slideforge.domain.entities.presentation_plan import PresentationPlan


class DocumentRenderer(Protocol):
    format_name: str
    extension: str

    def render(self, plan: PresentationPlan, output_path: Path, *, audit: ContentAudit | None = None, assets=None, theme=None) -> Path:
        ...
