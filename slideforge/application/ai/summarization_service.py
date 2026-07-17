from dataclasses import dataclass, field
import time
from typing import Protocol

from slideforge.application.ai.config import AIConfig
from slideforge.application.ai.models import AIContext, SummaryOptions, SummaryResult
from slideforge.application.ai.summarization_policy import SummarizationEligibilityPolicy, SummaryEligibility
from slideforge.domain.entities.content_block import ContentBlock
from slideforge.application.ai.provider import AIProvider


class AIProviderResolver(Protocol):
    def create(self, config: AIConfig) -> AIProvider: ...


@dataclass(frozen=True)
class SummarizationLogEntry:
    provider: str
    model: str
    duration_ms: int
    status: str
    error_type: str | None
    approximate_chars: int
    fallback_used: bool
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class BlockSummaryResult:
    block_id: str
    original_text: str
    derived_summary: str
    eligibility: SummaryEligibility
    summary: SummaryResult
    log_entry: SummarizationLogEntry


class AISummarizationService:
    def __init__(self, config: AIConfig, provider_factory: AIProviderResolver, policy: SummarizationEligibilityPolicy | None = None):
        self.config = config
        self.provider_factory = provider_factory
        self.policy = policy or SummarizationEligibilityPolicy()

    def summarize_block(self, block: ContentBlock, context: AIContext | None = None, *, options: SummaryOptions | None = None) -> BlockSummaryResult:
        eligibility = self.policy.evaluate_block(block)
        if not self.config.enabled:
            summary = SummaryResult(text=block.text, source_length=len(block.text or ""), provider="disabled", model="", success=False, status="disabled", warnings=["IA desativada por configuração."])
            return self._result(block, eligibility, summary)
        if not eligibility.eligible:
            summary = SummaryResult(text=block.text, source_length=len(block.text or ""), provider="policy", model="", success=False, status="not_eligible", warnings=[eligibility.reason])
            return self._result(block, eligibility, summary)
        return self.summarize_text(block.text, context=context, options=options, block_id=block.id, eligibility=eligibility)

    def summarize_text(self, text: str, context: AIContext | None = None, *, options: SummaryOptions | None = None, block_id: str = "text", eligibility: SummaryEligibility | None = None) -> BlockSummaryResult:
        started = time.perf_counter()
        eligibility = eligibility or SummaryEligibility(True, "Resumo solicitado diretamente", len(text), len(text.split()))
        provider = self.provider_factory.create(self.config)
        summary = provider.content_summarizer().summarize_content(text, context, options=options)
        if not summary.success and self.config.fallback_provider == "fake":
            fallback_config = AIConfig(enabled=True, provider="fake", model="fake-deterministic-v1")
            fallback = self.provider_factory.create(fallback_config).content_summarizer().summarize_content(text, context, options=options)
            summary = SummaryResult(
                text=fallback.text,
                source_length=fallback.source_length,
                was_truncated=fallback.was_truncated,
                provider=fallback.provider,
                model=fallback.model,
                fallback_used=True,
                duration_ms=int((time.perf_counter() - started) * 1000),
                warnings=["Fallback fake utilizado; resumo real não foi produzido."] + summary.warnings,
                success=fallback.success,
                status="fallback_fake",
                error_type=summary.error_type,
            )
        elif not summary.success:
            summary = SummaryResult(
                text=text,
                source_length=len(text),
                provider=summary.provider,
                model=summary.model,
                fallback_used=False,
                duration_ms=int((time.perf_counter() - started) * 1000),
                warnings=["Resumo real falhou; conteúdo original preservado."] + summary.warnings,
                success=False,
                status="original_preserved",
                error_type=summary.error_type,
            )
        return BlockSummaryResult(
            block_id=block_id,
            original_text=text,
            derived_summary=summary.text,
            eligibility=eligibility,
            summary=summary,
            log_entry=SummarizationLogEntry(
                provider=summary.provider,
                model=summary.model,
                duration_ms=summary.duration_ms,
                status=summary.status,
                error_type=summary.error_type,
                approximate_chars=len(text),
                fallback_used=summary.fallback_used,
                warnings=list(summary.warnings),
            ),
        )

    def _result(self, block: ContentBlock, eligibility: SummaryEligibility, summary: SummaryResult) -> BlockSummaryResult:
        return BlockSummaryResult(
            block_id=block.id,
            original_text=block.text,
            derived_summary=summary.text,
            eligibility=eligibility,
            summary=summary,
            log_entry=SummarizationLogEntry(
                provider=summary.provider,
                model=summary.model,
                duration_ms=summary.duration_ms,
                status=summary.status,
                error_type=summary.error_type,
                approximate_chars=len(block.text or ""),
                fallback_used=summary.fallback_used,
                warnings=list(summary.warnings),
            ),
        )

