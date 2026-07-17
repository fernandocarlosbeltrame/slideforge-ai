# Arquitetura da Camada de IA - SlideForge AI v1.0.0

A camada de IA foi projetada para ser opcional, segura e desacoplada do nucleo deterministico.

## Principios

- Clean Architecture.
- Dependency Inversion.
- Providers por Strategy Pattern.
- Dominio sem SDKs ou APIs externas.
- IA nunca substitui o conteudo original automaticamente.

## Contratos

Os contratos ficam em `slideforge/application/ai/contracts.py`:

- `DocumentAnalyzer`
- `PresentationPlannerAI`
- `SlideLayoutAdvisor`
- `ContentSummarizer`
- `ThemeAdvisor`
- `ImageSuggestionProvider`
- `SpeakerNotesGenerator`
- `PresentationReviewer`

## Providers

- `FakeAIProvider`: funcional, deterministico e usado em testes.
- `OllamaProvider`: funcional apenas para `ContentSummarizer` local.
- `OpenAIProvider`: stub arquitetural.
- `AzureOpenAIProvider`: stub arquitetural.
- `LMStudioProvider`: stub arquitetural.

## Configuracao

Arquivo padrao:

```text
slideforge/config/ai_config.json
```

A IA permanece desativada por padrao. Nenhuma chave de API deve existir no repositorio.

## Fluxo do resumo local

```text
ContentBlock
↓
SummarizationEligibilityPolicy
↓
AISummarizationService
↓
AIProviderFactory
↓
OllamaProvider ou FakeAIProvider
↓
SummaryResult derivado
```

O resumo e armazenado como metadado derivado. O texto original permanece preservado.

## Avaliacao

A qualidade do resumo pode ser avaliada por `AISummaryEvaluator`, sem usar IA. O avaliador mede reducao textual e preservacao de numeros, datas, percentuais, listas, nomes proprios e referencias legais.

## Regras de seguranca

- IA e opt-in.
- Nao enviar documentos sensiveis a provedores externos sem aprovacao explicita.
- Nao gravar chaves no repositorio.
- Registrar provider, modelo, status e fallback.
- Sanitizar erros externos.
- Manter modo offline deterministico.

## Fora do escopo da v1.0

- OpenAI real.
- Azure OpenAI real.
- RAG.
- Embeddings.
- Banco vetorial.
- Geracao completa de slides por IA.
