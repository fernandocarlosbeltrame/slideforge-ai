# Changelog

## [1.0.0] - Release oficial

### Consolidado

- Pipeline completo de geracao e publicacao a partir de documentos.
- Clean Architecture com dominio, aplicacao, infraestrutura, apresentacao e legado separados.
- Leitura de DOCX, TXT, Markdown e PDF.
- Extracao de imagens e tabelas de DOCX.
- Planejamento rastreavel com `PresentationPlan` e `SlidePlan`.
- Renderizadores independentes para PPTX, PDF, HTML, DOCX, Markdown e JSON.
- Manifesto de publicacao com hashes, versao, auditoria e validacao.
- Pacote ZIP portavel com assets relativos.
- Asset Manager e Theme Registry.
- Auditoria de conteudo, imagens, densidade visual e rastreabilidade.
- Interface desktop Tkinter preservada.
- Camada de IA desacoplada e opcional.
- `FakeAIProvider` deterministico.
- `OllamaProvider` funcional apenas para resumo local.
- Framework deterministico de avaliacao de resumos por IA.
- Documentacao de arquitetura, publicacao, IA, Ollama, avaliacao e plano 1.0.

### Validado

- `python -m pytest`: 65 testes passando.
- `python -m compileall slideforge tests`: sem erros.
- `git diff --check`: sem problemas apos a estabilizacao final.

### Limitacoes conhecidas

- Sem React, FastAPI, banco de dados, OCR, RAG, embeddings, multiusuario ou editor web.
- PDF e documento executivo e pode ter estrutura diferente do PPTX.
- DOCX usa sumario textual editavel, nao TOC nativo.
- IA e opcional, local e desativada por padrao.

## [0.5.0] - Fase 4: Publishing Engine

### Adicionado

- Porta `DocumentRenderer` para renderizacao independente de formato.
- `PublishingEngine` para publicar multiplos formatos a partir do mesmo `PresentationPlan`.
- Renderizadores: `PptxRenderer`, `PdfRenderer`, `HtmlRenderer`, `MarkdownRenderer`, `DocxRenderer` e `JsonRenderer`.
- PDF nativo via ReportLab.
- HTML navegavel.
- Markdown estruturado.
- DOCX reorganizado.
- JSON completo com metadados, slides, componentes, auditoria e rastreabilidade.
- `AssetManager`, `ThemeRegistry`, manifesto e pacote ZIP.

## [0.4.1] - Sprint 3.1: Validacao visual

### Corrigido

- Banner com baixa visibilidade.
- Comparacoes extensas com desequilibrio visual.
- Marcadores `ANTES`/`DEPOIS` vindos do Word.
- Slides com espaco vazio excessivo ou overflows criticos.

### Resultado

- Apresentacao real validada com 24 slides.
- Auditoria sem blocos nao utilizados e sem imagens ausentes.

## [0.4.0] - Fase 3: Motor visual profissional

### Adicionado

- Componentes PPTX reutilizaveis.
- Grid visual.
- `LayoutDecision`.
- `ContentDensityAnalyzer`.
- Preview HTML estrutural.
- Auditoria visual ampliada.

## [0.3.0] - Fase 2: Fidelidade de conteudo e qualidade visual

### Adicionado

- Extracao de imagens DOCX.
- Leitura estruturada de tabelas DOCX.
- Leitor PDF inicial.
- Geometria segura, ajuste tipografico e redimensionamento proporcional de imagens.

## [0.2.0] - Fase 1: Base profissional

### Adicionado

- Arquitetura em camadas.
- Entidades de dominio.
- Pipeline `SourceDocument -> PresentationPlan -> PPTXExporter -> ContentAudit`.
- Leitores DOCX, TXT e Markdown.
- Exportador PPTX inicial.
- Testes automatizados.
- MVP anterior preservado em `slideforge/legacy`.
