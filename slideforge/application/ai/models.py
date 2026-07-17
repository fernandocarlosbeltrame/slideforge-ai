from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AIContext:
    purpose: str
    language: str = "pt-BR"
    audience: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SummaryOptions:
    objective: str = "Criar resumo fiel e seguro para apoio à apresentação."
    max_length: int = 1000
    language: str = "pt-BR"
    context: str | None = None


@dataclass(frozen=True)
class AIProviderInfo:
    name: str
    model: str
    supports_external_calls: bool
    deterministic: bool


@dataclass(frozen=True)
class DocumentInsight:
    summary: str
    topics: list[str]
    risks: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class PlanSuggestion:
    title: str
    rationale: str
    section_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class LayoutSuggestion:
    slide_sequence: int
    recommended_layout: str
    confidence: float
    rationale: str


@dataclass(frozen=True)
class SummaryResult:
    text: str
    source_length: int
    was_truncated: bool = False
    provider: str = "fake"
    model: str = ""
    fallback_used: bool = False
    duration_ms: int = 0
    warnings: list[str] = field(default_factory=list)
    success: bool = True
    status: str = "ok"
    error_type: str | None = None


@dataclass(frozen=True)
class ThemeSuggestion:
    theme_name: str
    rationale: str


@dataclass(frozen=True)
class ImageSuggestion:
    slide_sequence: int
    query: str
    rationale: str


@dataclass(frozen=True)
class SpeakerNotes:
    slide_sequence: int
    notes: str
    source_block_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ReviewIssue:
    severity: str
    slide_sequence: int | None
    message: str
    recommendation: str


@dataclass(frozen=True)
class ReviewResult:
    summary: str
    issues: list[ReviewIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not any(issue.severity.lower() in {"critical", "critica", "bloqueador"} for issue in self.issues)
