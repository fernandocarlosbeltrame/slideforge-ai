from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from slideforge.domain.entities.content_audit import ContentAudit
from slideforge.domain.entities.presentation_plan import PresentationPlan
from slideforge.infrastructure.renderers.serialization import plan_to_dict


@dataclass
class ConsistencyIssue:
    severity: str
    message: str
    format_name: str | None = None


@dataclass
class ConsistencyResult:
    issues: list[ConsistencyIssue] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "critica")

    @property
    def relevant_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "relevante")

    @property
    def informative_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "informativa")

    @property
    def ok(self) -> bool:
        return self.critical_count == 0

    def as_dict(self) -> dict:
        return {
            "ok": self.ok,
            "critical_count": self.critical_count,
            "relevant_count": self.relevant_count,
            "informative_count": self.informative_count,
            "issues": [issue.__dict__ for issue in self.issues],
        }


class PublishingConsistencyValidator:
    """Compara consistencia logica do pacote, sem exigir igualdade visual."""

    REQUIRED_FORMATS = {"pptx", "pdf", "html", "markdown", "docx", "json"}

    def validate(self, plan: PresentationPlan, documents: Iterable, audit: ContentAudit | None = None) -> ConsistencyResult:
        result = ConsistencyResult()
        docs = list(documents)
        formats = {doc.format_name for doc in docs}
        expected = plan_to_dict(plan, audit)
        if not plan.slides:
            result.issues.append(ConsistencyIssue("critica", "PresentationPlan sem slides."))
        if audit and audit.unused_block_ids:
            result.issues.append(ConsistencyIssue("critica", "Existem blocos nao utilizados."))
        if audit and audit.unused_image_ids:
            result.issues.append(ConsistencyIssue("critica", "Existem imagens nao utilizadas."))
        for required in sorted(self.REQUIRED_FORMATS & formats):
            doc = next(d for d in docs if d.format_name == required)
            if not Path(doc.path).exists():
                result.issues.append(ConsistencyIssue("critica", f"Arquivo nao encontrado: {doc.path}", required))
            elif Path(doc.path).stat().st_size == 0:
                result.issues.append(ConsistencyIssue("critica", f"Arquivo vazio: {doc.path}", required))
        json_doc = next((d for d in docs if d.format_name == "json"), None)
        if json_doc and Path(json_doc.path).exists():
            try:
                import json
                data = json.loads(Path(json_doc.path).read_text(encoding="utf-8"))
                if len(data.get("slides", [])) != len(expected.get("slides", [])):
                    result.issues.append(ConsistencyIssue("critica", "JSON possui quantidade divergente de slides.", "json"))
                json_titles = [s.get("title") for s in data.get("slides", [])]
                plan_titles = [s.get("title") for s in expected.get("slides", [])]
                if json_titles != plan_titles:
                    result.issues.append(ConsistencyIssue("critica", "JSON possui titulos fora de ordem.", "json"))
            except Exception as exc:
                result.issues.append(ConsistencyIssue("critica", f"JSON invalido: {exc}", "json"))
        missing = sorted(self.REQUIRED_FORMATS - formats)
        for name in missing:
            result.issues.append(ConsistencyIssue("informativa", f"Formato nao gerado nesta publicacao: {name}", name))
        return result
