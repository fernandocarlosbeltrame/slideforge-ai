from __future__ import annotations

import argparse
from pathlib import Path

from slideforge.application.ai import AIConfig, AIContext, AISummarizationService, AISummaryEvaluator, SummaryOptions
from slideforge.infrastructure.ai import AIProviderFactory


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Testa o resumo assistido por IA local do SlideForge.")
    parser.add_argument("--text-file", required=True, help="Arquivo TXT com o conteúdo a resumir.")
    parser.add_argument("--provider", choices=["fake", "ollama"], default="fake")
    parser.add_argument("--model", default="", help="Modelo local. Ex.: llama3.1, mistral, phi3.")
    parser.add_argument("--base-url", default="http://localhost:11434")
    parser.add_argument("--max-length", type=int, default=1000)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--no-fallback", action="store_true", help="Não usar fallback fake em caso de falha.")
    parser.add_argument("--evaluation-json", help="Caminho para salvar relatório JSON determinístico de avaliação do resumo.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    text_path = Path(args.text_file)
    text = text_path.read_text(encoding="utf-8")
    config = AIConfig(
        enabled=True,
        provider=args.provider,
        model=args.model or ("fake-deterministic-v1" if args.provider == "fake" else ""),
        base_url=args.base_url,
        max_tokens=args.max_length,
        timeout_seconds=args.timeout,
        fallback_provider="" if args.no_fallback else "fake",
    )
    service = AISummarizationService(config, AIProviderFactory())
    result = service.summarize_text(
        text,
        context=AIContext(purpose="cli-summary"),
        options=SummaryOptions(max_length=args.max_length, language="pt-BR"),
    )
    print("Status:", result.summary.status)
    print("Provider:", result.summary.provider)
    print("Modelo:", result.summary.model or "-")
    print("Fallback:", "sim" if result.summary.fallback_used else "não")
    print("Avisos:", "; ".join(result.summary.warnings) if result.summary.warnings else "-")
    print("\nResumo:\n")
    print(result.derived_summary)
    if args.evaluation_json:
        report = AISummaryEvaluator().evaluate(result.original_text, result.derived_summary, result.derived_summary, summary_result=result.summary)
        report.write_json(args.evaluation_json)
        print("\nRelatório de avaliação:", args.evaluation_json)
    return 0 if result.summary.success else 2


if __name__ == "__main__":
    raise SystemExit(main())

