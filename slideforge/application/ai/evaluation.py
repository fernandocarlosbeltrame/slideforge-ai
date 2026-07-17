from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
import re
from pathlib import Path
from typing import Iterable

from slideforge.application.ai.models import SummaryResult


@dataclass(frozen=True)
class PreservationMetric:
    name: str
    original_items: list[str]
    summary_items: list[str]
    used_items: list[str]

    @property
    def original_count(self) -> int:
        return len(self.original_items)

    @property
    def summary_preserved_count(self) -> int:
        return len(_intersection(self.original_items, self.summary_items))

    @property
    def used_preserved_count(self) -> int:
        return len(_intersection(self.original_items, self.used_items))

    @property
    def summary_preservation_rate(self) -> float:
        return _rate(self.summary_preserved_count, self.original_count)

    @property
    def used_preservation_rate(self) -> float:
        return _rate(self.used_preserved_count, self.original_count)

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "original_count": self.original_count,
            "summary_preserved_count": self.summary_preserved_count,
            "used_preserved_count": self.used_preserved_count,
            "summary_preservation_rate": self.summary_preservation_rate,
            "used_preservation_rate": self.used_preservation_rate,
            "original_items": self.original_items,
            "summary_items": self.summary_items,
            "used_items": self.used_items,
        }


@dataclass(frozen=True)
class AIEvaluationReport:
    original_length: int
    summary_length: int
    used_content_length: int
    reduction_percent: float
    provider: str
    model: str
    fallback_used: bool
    duration_ms: int
    success: bool
    status: str
    metrics: dict[str, PreservationMetric] = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            "original_length": self.original_length,
            "summary_length": self.summary_length,
            "used_content_length": self.used_content_length,
            "reduction_percent": self.reduction_percent,
            "provider": self.provider,
            "model": self.model,
            "fallback_used": self.fallback_used,
            "duration_ms": self.duration_ms,
            "success": self.success,
            "status": self.status,
            "metrics": {name: metric.as_dict() for name, metric in self.metrics.items()},
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.as_dict(), ensure_ascii=False, indent=indent)

    def write_json(self, path: str | Path) -> Path:
        output = Path(path)
        output.write_text(self.to_json(), encoding="utf-8")
        return output


class AISummaryEvaluator:
    def evaluate(self, original: str, summary: str, used_content: str | None = None, *, summary_result: SummaryResult | None = None) -> AIEvaluationReport:
        used_content = summary if used_content is None else used_content
        original = original or ""
        summary = summary or ""
        used_content = used_content or ""
        result = summary_result or SummaryResult(text=summary, source_length=len(original), provider="unknown", model="", success=True)
        metrics = {
            "numbers": self._metric("numbers", original, summary, used_content, _extract_numbers),
            "dates": self._metric("dates", original, summary, used_content, _extract_dates),
            "percentages": self._metric("percentages", original, summary, used_content, _extract_percentages),
            "lists": self._metric("lists", original, summary, used_content, _extract_list_items),
            "proper_names": self._metric("proper_names", original, summary, used_content, _extract_proper_names),
            "legal_references": self._metric("legal_references", original, summary, used_content, _extract_legal_references),
        }
        return AIEvaluationReport(
            original_length=len(original),
            summary_length=len(summary),
            used_content_length=len(used_content),
            reduction_percent=_reduction_percent(len(original), len(summary)),
            provider=result.provider,
            model=result.model,
            fallback_used=result.fallback_used,
            duration_ms=result.duration_ms,
            success=result.success,
            status=result.status,
            metrics=metrics,
        )

    def _metric(self, name: str, original: str, summary: str, used_content: str, extractor) -> PreservationMetric:
        return PreservationMetric(
            name=name,
            original_items=extractor(original),
            summary_items=extractor(summary),
            used_items=extractor(used_content),
        )


def _normalize_item(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().strip(".,;:()[]{}" )).casefold()


def _unique(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        clean = re.sub(r"\s+", " ", item.strip())
        if not clean:
            continue
        key = _normalize_item(clean)
        if key not in seen:
            seen.add(key)
            result.append(clean)
    return result


def _intersection(left: list[str], right: list[str]) -> set[str]:
    right_norm = {_normalize_item(item) for item in right}
    return {_normalize_item(item) for item in left if _normalize_item(item) in right_norm}


def _rate(part: int, total: int) -> float:
    if total == 0:
        return 1.0
    return round(part / total, 4)


def _reduction_percent(original_len: int, summary_len: int) -> float:
    if original_len <= 0:
        return 0.0
    return round(max(0.0, (1 - (summary_len / original_len)) * 100), 2)


def _extract_percentages(text: str) -> list[str]:
    return _unique(re.findall(r"\b\d{1,3}(?:[\.,]\d+)?\s?%", text))


def _extract_dates(text: str) -> list[str]:
    patterns = [
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\b(?:jan(?:eiro)?|fev(?:ereiro)?|mar(?:ço|co)?|abr(?:il)?|mai(?:o)?|jun(?:ho)?|jul(?:ho)?|ago(?:sto)?|set(?:embro)?|out(?:ubro)?|nov(?:embro)?|dez(?:embro)?)\s+de\s+\d{4}\b",
    ]
    found: list[str] = []
    for pattern in patterns:
        found.extend(re.findall(pattern, text, flags=re.IGNORECASE))
    return _unique(found)


def _extract_numbers(text: str) -> list[str]:
    without_percentages = re.sub(r"\b\d{1,3}(?:[\.,]\d+)?\s?%", " ", text)
    return _unique(re.findall(r"(?:R\$\s*)?\b\d{1,3}(?:\.\d{3})*(?:,\d+)?\b|\b\d+(?:\.\d+)?\b", without_percentages))


def _extract_list_items(text: str) -> list[str]:
    items: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^\s*(?:[-*•]|\d+[.)])\s+(.+?)\s*$", line)
        if match:
            items.append(match.group(1))
    return _unique(items)


def _extract_proper_names(text: str) -> list[str]:
    candidates = re.findall(r"\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][\wÁÉÍÓÚÂÊÔÃÕÇáéíóúâêôãõç-]+(?:\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ][\wÁÉÍÓÚÂÊÔÃÕÇáéíóúâêôãõç-]+)+", text)
    ignored = {"Em", "O", "A", "Os", "As", "No", "Na", "Nos", "Nas"}
    return _unique(item for item in candidates if item.split()[0] not in ignored)


def _extract_legal_references(text: str) -> list[str]:
    patterns = [
        r"\bLei(?:\s+Complementar)?\s+n?[ºo°]?\s*\d+[\d./-]*",
        r"\bDecreto\s+n?[ºo°]?\s*\d+[\d./-]*",
        r"\bPortaria\s+n?[ºo°]?\s*\d+[\d./-]*",
        r"\bIN\s+RFB\s+n?[ºo°]?\s*\d+[\d./-]*",
        r"\bart\.\s*\d+[A-Za-zº°]*",
    ]
    found: list[str] = []
    for pattern in patterns:
        found.extend(re.findall(pattern, text, flags=re.IGNORECASE))
    return _unique(found)

