# Publishing Engine - SlideForge AI v1.0.0

O Publishing Engine publica multiplos formatos a partir do mesmo `PresentationPlan`.

## Fluxo

```text
PresentationPlan
↓
ContentAudit
↓
PublishingEngine
↓
DocumentRenderer(s)
↓
ManifestBuilder
↓
PublishingPackageBuilder
```

## Renderizadores

Todos implementam a porta `DocumentRenderer`:

- `PptxRenderer`
- `PdfRenderer`
- `HtmlRenderer`
- `MarkdownRenderer`
- `DocxRenderer`
- `JsonRenderer`

Cada formato interpreta o mesmo plano, sem alterar o dominio.

## PDF executivo

Na versao 1.0.0, o PDF e oficialmente um documento executivo. Ele pode conter capa, agenda e auditoria, portanto pode ter mais paginas que o PPTX.

## HTML

O HTML e navegavel e local, com:

- indice;
- capitulos;
- imagens;
- tabelas;
- notas;
- suporte a pacote ZIP.

## DOCX

O DOCX e editavel, com capa, sumario textual, estilos, cabecalho/rodape e observacoes por slide.

Limitacao conhecida: o sumario ainda nao e um campo nativo atualizavel do Word.

## Markdown

O Markdown preserva hierarquia, listas, tabelas, imagens, notas e rastreabilidade discreta.

## JSON

O JSON contem metadados, slides, componentes, auditoria, rastreabilidade e estatisticas. Ele e a base para integracoes futuras.

## Manifesto e pacote

O manifesto inclui:

- versao;
- schema;
- hashes;
- tamanhos;
- estatisticas;
- auditoria;
- validacao de consistencia.

O ZIP inclui os arquivos publicados e assets relativos em estrutura portavel.

## Limitacoes conhecidas

- Notas nativas no painel do PowerPoint ficam para versao futura.
- Hyperlinks internos nativos no PPTX ficam para versao futura.
- O PDF nao e espelho 1:1 do PPTX.
