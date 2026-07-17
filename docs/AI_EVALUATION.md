# AI Evaluation Report - SlideForge AI v1.0.0

O SlideForge AI inclui avaliacao deterministica para medir a qualidade de resumos gerados por `ContentSummarizer`.

Nenhuma IA e usada para avaliar.

## Objetivo

Comparar:

```text
Conteudo original
↓
Resumo produzido
↓
Conteudo utilizado na apresentacao
```

## Implementacao

Arquivo principal:

```text
slideforge/application/ai/evaluation.py
```

Classes principais:

- `AISummaryEvaluator`
- `AIEvaluationReport`
- `PreservationMetric`

## Metricas

O relatorio mede:

- tamanho do original;
- tamanho do resumo;
- tamanho do conteudo usado;
- percentual de reducao;
- provider;
- modelo;
- duracao;
- uso de fallback;
- status;
- preservacao de numeros;
- preservacao de datas;
- preservacao de percentuais;
- preservacao de listas;
- preservacao de nomes proprios;
- preservacao de referencias legais.

## Exportacao JSON

```python
from slideforge.application.ai.evaluation import AISummaryEvaluator

report = AISummaryEvaluator().evaluate(original, summary, used_content)
report.write_json("ai_evaluation.json")
```

Pela CLI:

```bash
python -m slideforge.ai_summarize --text-file exemplo.txt --provider fake --evaluation-json avaliacao.json
```

## Limitacoes

- Nomes proprios sao identificados por heuristica.
- Referencias legais dependem dos padroes conhecidos.
- A avaliacao nao mede semantica profunda.
- Revisao humana segue recomendada para conteudo critico.
