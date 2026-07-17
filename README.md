# SlideForge AI

Aplicação para transformar documentos Word (`.docx`), PDF, Markdown e TXT em apresentações PowerPoint profissionais, preservando o conteúdo e criando um plano rastreável antes da geração do arquivo.

## Status

Fase 4 concluída: Publishing Engine com renderização PPTX, PDF, HTML, Markdown, DOCX e JSON a partir do mesmo PresentationPlan.

## Funcionalidades atuais

- Leitura de DOCX, TXT, Markdown e PDF.
- Extração de imagens embutidas em DOCX preservando a ordem do documento.
- Extração inicial de texto e imagens em PDF com PyMuPDF, sem OCR.
- Leitura estruturada de tabelas DOCX.
- Criação de `SourceDocument`, `DocumentSection`, `ContentBlock`, `PresentationPlan` e `SlidePlan`.
- Seleção determinística de layouts: capa, bullets, cards, timeline, comparação, tabela e imagem.
- Exportação para PPTX editável em widescreen 16:9.
- Cabeçalho/banner proporcional, sem deformação.
- Rodapé fixo e consistente.
- Ajuste inicial de títulos longos e corpo do slide.
- Redimensionamento proporcional de imagens por `contain`.
- Validação de plano antes da exportação.
- Auditoria de conteúdo, imagens, títulos, overflows e densidade visual.
- Biblioteca de componentes PPTX: título, footer, bullets, cards, comparação, timeline, imagem e tabela.
- Sistema de grid reutilizável para colunas, linhas, proporções 60/40 e áreas seguras.
- Decisão visual rastreável por slide, com motivo, regras acionadas, alternativas e densidade.
- Análise de densidade de conteúdo para evitar slides congestionados.
- Preview HTML estrutural com layout, composição, densidade e blocos utilizados.
- Publishing Engine com renderizadores independentes: PPTX, PDF, HTML, Markdown, DOCX e JSON.
- PDF nativo via ReportLab, sem depender de conversão do PowerPoint.
- HTML navegável com índice, capítulos, imagens, tabelas e notas.
- Markdown estruturado com hierarquia, listas, tabelas e imagens.
- DOCX reorganizado a partir da estrutura lógica da apresentação.
- JSON completo com metadados, slides, componentes, auditoria e rastreabilidade.
- Asset Manager para banners, logos e recursos visuais.
- Theme Registry para centralizar tokens visuais por tema.
- Interfaces de extensão para IA futura, sem implementação concreta.
- Interface Tkinter com seleção de tema e auditoria.
- MVP anterior preservado em `slideforge/legacy`.

## Executar

```bash
pip install -r requirements.txt
python app.py
```

## Rodar testes

```bash
pytest
```

## Arquitetura

Consulte `docs/ARCHITECTURE.md`, `docs/PHASE3_VISUAL_ENGINE.md` e `docs/PUBLISHING_ENGINE.md`.

Pipeline principal:

```text
DocumentReader
↓
SourceDocument
↓
ContentBlock
↓
PresentationPlanner
↓
SlidePlan
↓
PPTXExporter
↓
ContentAudit
```

## Limitações atuais

- Ainda não há React.
- Ainda não há FastAPI.
- Ainda não há banco de dados.
- Ainda não há IA.
- Exportação PDF nativa disponível na Fase 4.
- PDF escaneado é identificado como limitação, sem OCR.
- A inspeção visual fina ainda depende de abertura no PowerPoint pelo usuário, mas a Fase 3 gera preview HTML para revisão estrutural.



## Sprint 4.1 - Refinamento Executivo

O SlideForge agora gera um pacote de publicacao mais completo:

- PDF executivo em proporcao 16:9.
- HTML local, responsivo e navegavel.
- DOCX editavel com capa, sumario e estilos.
- Markdown com metadados, indice e rastreabilidade discreta.
- JSON com versao do sistema.
- Manifesto `.manifest.json` com hashes e auditoria.
- Pacote ZIP padronizado com todos os formatos.

Documentacao complementar:

- `docs/PUBLISHING_PACKAGE.md`
- `docs/FORMAT_CAPABILITIES.md`
