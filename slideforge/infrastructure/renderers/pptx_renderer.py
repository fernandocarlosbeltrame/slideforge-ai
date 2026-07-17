from pathlib import Path
from slideforge.domain.entities.content_audit import ContentAudit
from slideforge.domain.entities.presentation_plan import PresentationPlan
from slideforge.infrastructure.exporters.pptx_exporter import PPTXExporter
from slideforge.infrastructure.assets import AssetManager
from slideforge.theme import Theme, get_theme


class PptxRenderer:
    format_name = "pptx"
    extension = ".pptx"

    def __init__(self, theme: Theme | None = None):
        self.theme = theme or get_theme("corporate_blue")

    def render(self, plan: PresentationPlan, output_path: Path, *, audit: ContentAudit | None = None, assets: AssetManager | None = None, theme=None) -> Path:
        active_theme = theme.base if hasattr(theme, "base") else self.theme
        banner = assets.locate("banner") if assets else None
        logo = assets.locate("logo") if assets else None
        return PPTXExporter(theme=active_theme).export(plan, output_path, banner_path=str(banner) if banner else None, logo_path=str(logo) if logo else None)
