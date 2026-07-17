from dataclasses import dataclass
from pathlib import Path

from slideforge.application.ai.config import AIConfig
from slideforge.application.ai.models import AIContext, SummaryOptions
from slideforge.application.ai.summarization_service import AISummarizationService
from slideforge.application.publishing import PublishedDocument, PublishingEngine, output_with_extension
from slideforge.application.publishing.consistency_validator import ConsistencyResult, PublishingConsistencyValidator
from slideforge.application.publishing.manifest import ManifestBuilder
from slideforge.application.publishing.package_builder import PublishingPackageBuilder
from slideforge.application.services.content_auditor import ContentAuditor
from slideforge.application.services.presentation_planner import PresentationPlanner
from slideforge.application.validation.presentation_validator import PresentationValidator
from slideforge.domain.entities.content_audit import ContentAudit
from slideforge.domain.entities.presentation_plan import PresentationPlan
from slideforge.infrastructure.ai import AIProviderFactory
from slideforge.infrastructure.assets import AssetManager
from slideforge.infrastructure.readers import DocxReader, MarkdownReader, PDFReader, TxtReader
from slideforge.infrastructure.renderers import DocxRenderer, HtmlRenderer, JsonRenderer, MarkdownRenderer, PdfRenderer, PptxRenderer
from slideforge.infrastructure.themes import ThemeRegistry
from slideforge.version import SLIDEFORGE_VERSION


@dataclass
class PublishPresentationResult:
    plan: PresentationPlan
    audit: ContentAudit
    documents: list[PublishedDocument]
    manifest_path: Path | None = None
    package_path: Path | None = None
    consistency: ConsistencyResult | None = None


class PublishPresentationUseCase:
    def __init__(self, readers=None, planner: PresentationPlanner | None = None, auditor: ContentAuditor | None = None, validator: PresentationValidator | None = None, renderers=None, asset_manager: AssetManager | None = None, theme_name: str = "corporate_blue", ai_config: AIConfig | None = None, ai_provider_factory: AIProviderFactory | None = None):
        self.readers = readers or [DocxReader(), MarkdownReader(), TxtReader(), PDFReader()]
        self.planner = planner or PresentationPlanner()
        self.auditor = auditor or ContentAuditor()
        self.validator = validator or PresentationValidator()
        self.asset_manager = asset_manager or AssetManager()
        self.theme = ThemeRegistry().get(theme_name)
        self.renderers = renderers or [PptxRenderer(self.theme.base), PdfRenderer(), HtmlRenderer(), MarkdownRenderer(), DocxRenderer(), JsonRenderer()]
        self.ai_config = ai_config or AIConfig(enabled=False)
        self.ai_provider_factory = ai_provider_factory or AIProviderFactory()

    def execute(self, source_path: str | Path, output_stem: str | Path, *, banner_path: str | None = None, logo_path: str | None = None, formats: set[str] | None = None, create_package: bool = True) -> PublishPresentationResult:
        source = Path(source_path)
        if not source.exists():
            raise FileNotFoundError(f"Documento não encontrado: {source}")
        if banner_path:
            self.asset_manager.register_banner(banner_path)
        if logo_path:
            self.asset_manager.register_logo(logo_path)
        reader = next((reader for reader in self.readers if reader.supports(source)), None)
        if reader is None:
            raise ValueError(f"Formato não suportado nesta fase: {source.suffix}")
        document = reader.read(source)
        plan = self.planner.create_plan(document)
        plan.metadata["slideforge_version"] = SLIDEFORGE_VERSION
        self._apply_optional_ai_summaries(plan)
        validation = self.validator.validate_plan(plan)
        if validation.errors:
            raise ValueError("; ".join(validation.errors))
        audit = self.auditor.audit(plan, warnings=validation.warnings)
        engine = PublishingEngine(self.renderers, assets=self.asset_manager, theme=self.theme)
        output_stem = Path(output_stem)
        docs = engine.publish(plan, output_stem, audit=audit, formats=formats)
        audit_path = output_with_extension(output_stem, ".audit.txt")
        audit_report = f"SlideForge versão: {SLIDEFORGE_VERSION}\n" + audit.as_report()
        audit_path.write_text(audit_report, encoding="utf-8")
        consistency = PublishingConsistencyValidator().validate(plan, docs, audit)
        if not consistency.ok:
            messages = "; ".join(issue.message for issue in consistency.issues if issue.severity == "critica")
            raise ValueError(f"Publicação bloqueada por divergência crítica: {messages}")
        manifest_path = ManifestBuilder().build(plan, docs, output_with_extension(output_stem, ".manifest.json"), audit=audit, assets=self.asset_manager, theme=self.theme, consistency=consistency)
        package_path = None
        if create_package:
            package_path = PublishingPackageBuilder().build(output_stem.with_name(output_stem.name + "_package.zip"), docs, manifest_path, audit_path, self.asset_manager, plan=plan)
        return PublishPresentationResult(plan=plan, audit=audit, documents=docs, manifest_path=manifest_path, package_path=package_path, consistency=consistency)
    def _apply_optional_ai_summaries(self, plan: PresentationPlan) -> None:
        if not self.ai_config.enabled:
            return
        service = AISummarizationService(self.ai_config, self.ai_provider_factory)
        context = AIContext(purpose="presentation-derived-summary")
        options = SummaryOptions(max_length=self.ai_config.max_tokens, language=context.language)
        for section in plan.source_document.sections:
            for block in section.blocks:
                result = service.summarize_block(block, context=context, options=options)
                block.metadata["ai_summary"] = {
                    "eligible": result.eligibility.eligible,
                    "reason": result.eligibility.reason,
                    "summary": result.derived_summary if result.summary.success else None,
                    "provider": result.summary.provider,
                    "model": result.summary.model,
                    "fallback_used": result.summary.fallback_used,
                    "status": result.summary.status,
                    "warnings": result.summary.warnings,
                }
