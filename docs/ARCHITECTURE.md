# Arquitetura - SlideForge AI v1.0.0

Este documento descreve a arquitetura consolidada da versao 1.0.0.

## Principio central

O SlideForge AI transforma documentos em um plano intermediario rastreavel antes de publicar qualquer formato.

```text
DocumentReader
↓
SourceDocument
↓
PresentationPlanner
↓
PresentationPlan
↓
ContentAuditor
↓
PublishingEngine
↓
PPTX | PDF | HTML | DOCX | Markdown | JSON
```

## Camadas

- `domain`: entidades, enums, value objects e servicos puros.
- `application`: casos de uso, planejamento, validacao, auditoria, publicacao e contratos.
- `infrastructure`: leitores, renderizadores, temas, assets e provedores de IA.
- `presentation`: interface desktop Tkinter.
- `legacy`: copia funcional do MVP anterior.

## Dominio

O dominio nao depende de bibliotecas de infraestrutura.

Entidades principais:

- `SourceDocument`
- `DocumentSection`
- `ContentBlock`
- `PresentationPlan`
- `SlidePlan`
- `ContentAudit`
- `LayoutDecision`

Value objects:

- `BoundingBox`
- `TableData`

## Aplicacao

Responsabilidades:

- selecionar leitor adequado;
- criar plano de apresentacao;
- validar plano;
- auditar conteudo;
- publicar formatos;
- montar manifesto e pacote;
- aplicar IA opcional de forma controlada.

Casos de uso principais:

- `GeneratePresentationUseCase`
- `PublishPresentationUseCase`

## Infraestrutura

Leitores:

- DOCX
- TXT
- Markdown
- PDF sem OCR

Renderizadores:

- PPTX
- PDF
- HTML
- DOCX
- Markdown
- JSON

Outros componentes:

- `AssetManager`
- `ThemeRegistry`
- provedores de IA fake/local
- sanitizacao de caminhos em publicacoes

## Rastreabilidade

Cada slide referencia os IDs dos blocos usados. A auditoria e o manifesto permitem verificar:

- blocos utilizados;
- blocos nao utilizados;
- imagens;
- tabelas;
- densidade;
- alertas;
- consistencia entre formatos.

## IA

A IA e opcional, desativada por padrao e isolada por contratos em `slideforge/application/ai`.

A versao 1.0.0 possui:

- `FakeAIProvider` deterministico;
- `OllamaProvider` local para resumo;
- fallback;
- avaliador deterministico de qualidade de resumo.

Nenhum provedor externo real e chamado por padrao.

## Decisao arquitetural v1.0

A arquitetura esta consolidada para a versao 1.0.0. Nao ha necessidade de reescrever o nucleo antes da release.

Melhoria futura recomendada: extrair uma composition root explicita para montar leitores, renderizadores, temas e provedores fora do caso de uso principal.
