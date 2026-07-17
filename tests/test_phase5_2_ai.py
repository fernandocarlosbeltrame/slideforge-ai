import json

from slideforge.application.ai import AISummaryEvaluator, SummaryResult


ORIGINAL = """
A Reforma Tributária do Consumo entra em transição em 2026.
- Revisar contratos com fornecedores.
- Conferir base de cálculo mensal.
A alíquota estimada é 12,5% e o impacto inicial é de R$ 1.234,56.
A Companhia Alfa Beta deve observar a Lei Complementar nº 214/2025 e a Portaria nº 549/2025.
Em maio de 2026, o Comitê Gestor do IBS divulgará novas orientações.
"""


SUMMARY = """
A Reforma Tributária do Consumo inicia transição em maio de 2026, com alíquota estimada de 12,5% e impacto de R$ 1.234,56.
- Revisar contratos com fornecedores.
- Conferir base de cálculo mensal.
A Companhia Alfa Beta deve observar a Lei Complementar nº 214/2025.
"""


USED = """
A Reforma Tributária do Consumo inicia transição em 2026.
- Revisar contratos com fornecedores.
A Companhia Alfa Beta deve observar a Lei Complementar nº 214/2025.
"""


def test_ai_summary_evaluation_measures_lengths_and_provider_metadata():
    summary_result = SummaryResult(text=SUMMARY, source_length=len(ORIGINAL), provider="ollama", model="llama3", fallback_used=False, duration_ms=321, status="ok")
    report = AISummaryEvaluator().evaluate(ORIGINAL, SUMMARY, USED, summary_result=summary_result)
    assert report.original_length == len(ORIGINAL)
    assert report.summary_length == len(SUMMARY)
    assert report.used_content_length == len(USED)
    assert report.reduction_percent > 0
    assert report.provider == "ollama"
    assert report.model == "llama3"
    assert report.fallback_used is False
    assert report.duration_ms == 321


def test_ai_summary_evaluation_preserves_numbers_dates_percentages_and_legal_refs():
    report = AISummaryEvaluator().evaluate(ORIGINAL, SUMMARY, USED)
    assert "2026" in report.metrics["numbers"].original_items
    assert report.metrics["percentages"].summary_preservation_rate == 1.0
    assert report.metrics["dates"].original_count >= 1
    assert report.metrics["dates"].summary_preserved_count >= 1
    assert report.metrics["legal_references"].original_count == 2
    assert report.metrics["legal_references"].summary_preserved_count == 1
    assert report.metrics["legal_references"].used_preserved_count == 1


def test_ai_summary_evaluation_preserves_lists_and_proper_names():
    report = AISummaryEvaluator().evaluate(ORIGINAL, SUMMARY, USED)
    assert report.metrics["lists"].original_count == 2
    assert report.metrics["lists"].summary_preserved_count == 2
    assert report.metrics["lists"].used_preserved_count == 1
    assert "Reforma Tributária" in " ".join(report.metrics["proper_names"].original_items)
    assert report.metrics["proper_names"].summary_preserved_count >= 1


def test_ai_summary_evaluation_compares_original_summary_and_used_content():
    report = AISummaryEvaluator().evaluate(ORIGINAL, SUMMARY, USED)
    assert report.metrics["lists"].summary_preservation_rate > report.metrics["lists"].used_preservation_rate
    assert report.metrics["legal_references"].summary_preservation_rate == report.metrics["legal_references"].used_preservation_rate


def test_ai_summary_evaluation_exports_json(tmp_path):
    report = AISummaryEvaluator().evaluate(ORIGINAL, SUMMARY, USED, summary_result=SummaryResult(text=SUMMARY, source_length=len(ORIGINAL), provider="fake", model="fake-deterministic-v1", fallback_used=True, duration_ms=5, status="fallback_fake"))
    output = report.write_json(tmp_path / "evaluation.json")
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["provider"] == "fake"
    assert data["fallback_used"] is True
    assert data["metrics"]["numbers"]["original_count"] >= 1
    assert "original_items" in data["metrics"]["dates"]


def test_ai_summary_evaluation_empty_original_is_safe():
    report = AISummaryEvaluator().evaluate("", "Resumo", "Resumo")
    assert report.reduction_percent == 0.0
    assert report.metrics["numbers"].summary_preservation_rate == 1.0

