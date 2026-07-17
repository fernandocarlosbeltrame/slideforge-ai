from dataclasses import dataclass
from pathlib import Path
from slideforge.application.preview import HTMLPreviewGenerator
from slideforge.application.services.content_auditor import ContentAuditor
from slideforge.application.services.presentation_planner import PresentationPlanner
from slideforge.application.validation.presentation_validator import PresentationValidator
from slideforge.domain.entities.content_audit import ContentAudit
from slideforge.domain.entities.presentation_plan import PresentationPlan
from slideforge.infrastructure.exporters.pptx_exporter import PPTXExporter
from slideforge.infrastructure.readers import DocxReader, MarkdownReader, PDFReader, TxtReader


@dataclass
class GeneratePresentationResult:
    output_path: Path
    plan: PresentationPlan
    audit: ContentAudit


class GeneratePresentationUseCase:
    def __init__(self, readers=None, planner: PresentationPlanner | None = None, exporter: PPTXExporter | None = None, auditor: ContentAuditor | None = None, validator: PresentationValidator | None = None, preview_generator: HTMLPreviewGenerator | None = None):
        self.readers = readers or [DocxReader(), MarkdownReader(), TxtReader(), PDFReader()]
        self.planner = planner or PresentationPlanner()
        self.exporter = exporter or PPTXExporter()
        self.auditor = auditor or ContentAuditor()
        self.validator = validator or PresentationValidator()
        self.preview_generator = preview_generator or HTMLPreviewGenerator()

    def execute(self, source_path: str | Path, output_path: str | Path, *, banner_path: str | None = None, logo_path: str | None = None) -> GeneratePresentationResult:
        source = Path(source_path)
        output = Path(output_path)
        if not source.exists():
            raise FileNotFoundError(f"Documento não encontrado: {source}")
        reader = next((reader for reader in self.readers if reader.supports(source)), None)
        if reader is None:
            raise ValueError(f"Formato não suportado nesta fase: {source.suffix}")
        document = reader.read(source)
        plan = self.planner.create_plan(document)
        validation = self.validator.validate_plan(plan)
        if validation.errors:
            raise ValueError("; ".join(validation.errors))
        self.exporter.export(plan, output, banner_path=banner_path, logo_path=logo_path)
        audit = self.auditor.audit(plan, warnings=validation.warnings)
        preview_path = output.with_name(output.stem + "_preview.html")
        self.preview_generator.generate(plan, audit, preview_path)
        audit_path = output.with_name(output.stem + ".audit.txt")
        audit_path.write_text(audit.as_report(), encoding="utf-8")
        plan.metadata["audit"] = {
            "used": len(audit.used_block_ids),
            "partial": len(audit.partially_used_block_ids),
            "split": len(audit.split_block_ids),
            "unused": len(audit.unused_block_ids),
            "images_used": len(audit.used_image_ids),
            "overflows": audit.critical_overflows,
            "layouts": audit.layout_counts,
            "density": audit.density_counts,
            "preview_path": str(preview_path),
            "audit_path": str(audit_path),
        }
        return GeneratePresentationResult(output_path=output, plan=plan, audit=audit)
