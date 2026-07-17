from pathlib import Path
from dataclasses import dataclass
from slideforge.application.ports.document_renderer import DocumentRenderer
from slideforge.domain.entities.content_audit import ContentAudit
from slideforge.domain.entities.presentation_plan import PresentationPlan


@dataclass
class PublishedDocument:
    format_name: str
    path: Path


class PublishingEngine:
    def __init__(self, renderers: list[DocumentRenderer], assets=None, theme=None):
        self.renderers = renderers
        self.assets = assets
        self.theme = theme

    def publish(self, plan: PresentationPlan, output_stem: Path, *, audit: ContentAudit | None = None, formats: set[str] | None = None) -> list[PublishedDocument]:
        output_stem.parent.mkdir(parents=True, exist_ok=True)
        selected = formats or {renderer.format_name for renderer in self.renderers}
        documents: list[PublishedDocument] = []
        for renderer in self.renderers:
            if renderer.format_name not in selected:
                continue
            output = output_stem.with_suffix(renderer.extension)
            documents.append(PublishedDocument(renderer.format_name, renderer.render(plan, output, audit=audit, assets=self.assets, theme=self.theme)))
        return documents
