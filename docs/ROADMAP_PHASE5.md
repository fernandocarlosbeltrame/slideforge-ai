# Roadmap da Camada de IA - Pos v1.0

A versao 1.0.0 entrega a arquitetura de IA, FakeAIProvider, Ollama local para resumo e avaliacao deterministica de qualidade.

## Ja entregue

- Contratos neutros de IA.
- `AIProvider` como ponto unico de entrada.
- `FakeAIProvider` deterministico.
- Stubs para provedores futuros.
- `OllamaProvider` funcional apenas para resumo local.
- Politica de elegibilidade para resumo.
- Fallback seguro.
- CLI de resumo.
- Avaliador deterministico de qualidade.
- Documentacao de IA e Ollama.

## Regras permanentes

- O pipeline deterministico continua sendo a fonte segura da verdade.
- IA permanece opcional.
- IA nao remove nem substitui conteudo original automaticamente.
- Provedores externos reais exigem revisao de privacidade e consentimento.

## Recomendado para v1.1

- Tela simples para configurar IA local.
- Health check do Ollama.
- Melhor exibicao dos metadados de resumo.
- Relatorio de avaliacao integrado ao fluxo de publicacao.

## Futuro 2.x

- OpenAI ou Azure OpenAI com opt-in explicito.
- RAG.
- Embeddings.
- Banco vetorial.
- Layout advisor real.
- Reviewer de apresentacao com aprovacao humana.
- Sugestoes de tema por IA.

## Nao recomendado antes da v1.0

- Geracao completa por IA.
- Reescrita automatica sem aprovacao.
- Envio silencioso de documentos para provedores externos.
