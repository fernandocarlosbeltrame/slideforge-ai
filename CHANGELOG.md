# Changelog

## [0.2.0] - Fase 1: Base profissional

### Adicionado

- Nova arquitetura em camadas: domínio, aplicação, infraestrutura e apresentação.
- Entidades puras de domínio para documentos, blocos, seções, planos de slides e auditoria.
- Pipeline `SourceDocument -> PresentationPlan -> PPTXExporter -> ContentAudit`.
- Motor determinístico inicial de seleção de layouts.
- Leitores DOCX, TXT e Markdown na camada de infraestrutura.
- Exportador PPTX inicial com layouts de capa, bullets, cards, timeline, comparação, tabela e imagem.
- Testes automatizados com pytest.
- Documentação de arquitetura.

### Alterado

- `app.py` agora é apenas o bootstrap da interface Tkinter nova.
- Textos principais foram corrigidos para UTF-8 legível.

### Preservado

- MVP anterior copiado para `slideforge/legacy`.
- O usuário continua podendo selecionar documento, logo/banner, destino e gerar PowerPoint.

## [0.3.0] - Fase 2: Fidelidade de conteúdo e qualidade visual

### Adicionado

- Extração de imagens DOCX em ordem aproximada por XML.
- Leitura estruturada de tabelas DOCX.
- Leitor PDF inicial com PyMuPDF.
- `SlideGeometry`, `BoundingBox`, `ImageFitCalculator`, `TypographyFitter` e `PresentationValidator`.
- Tema estruturado `corporate_blue` e `usiquimica`.
- Exportador PPTX com áreas seguras, banner proporcional, rodapé fixo e imagens sem distorção.
- Auditoria expandida com imagens, títulos ajustados, alertas e overflows.
- Interface Tkinter com PDF, seleção de tema, preservação de conteúdo e relatório de auditoria.
- Testes adicionais para imagem, PDF, tabela, geometria segura, fit proporcional e geração PPTX.

### Corrigido

- Banner/logo com baixa visibilidade ou deformação.
- Títulos longos ultrapassando a página.
- Bullets desalinhados e centralizados indevidamente.
- Timeline com último item fora da área útil.
- Imagem do DOCX rastreada, mas não inserida visualmente.

### Mantido

- Arquitetura da Fase 1.
- Domínio sem dependência de bibliotecas de infraestrutura.
- Compatibilidade com o fluxo desktop do MVP.
## [0.4.0] - Fase 3: Motor visual profissional e componentes

### Adicionado

- Biblioteca de componentes PPTX reutilizáveis para título, footer, bullets, cards, comparação, timeline, imagem e tabela.
- `SlideGrid` com colunas, linhas, proporções 60/40 e áreas auxiliares.
- `LayoutDecision` para registrar motivo da escolha visual, composição, regras acionadas e alternativas.
- `ContentDensityAnalyzer` para classificar slides em baixa, média, alta ou crítica densidade.
- Preview HTML automático ao lado do PPTX gerado.
- Auditoria expandida com contagem de layouts, densidade visual e alertas visuais.
- Testes automatizados específicos da Fase 3.

### Corrigido

- Timeline longa agora separa conteúdo excedente em slides auxiliares.
- Comparações extensas agora são divididas em partes menores para evitar slides congestionados.
- Geração real do documento `O que muda.docx` sem blocos não utilizados e sem overflows críticos.

### Mantido

- Sem React, FastAPI, banco de dados, IA, OCR, exportação PDF final ou plugins externos nesta fase.
- Pipeline da Fase 1 e melhorias da Fase 2 preservados.
## [0.4.1] - Sprint 3.1: Validação e correção visual

### Validado

- Renderização de todos os slides via Microsoft PowerPoint COM.
- Geração de folha de contato com miniaturas numeradas.
- Conferência estrutural de elementos fora da página, fontes mínimas e duplicidade textual.
- Conferência textual normalizada entre Word, plano e apresentação final.

### Corrigido

- Banner do cabeçalho com presença visual insuficiente.
- Slides de comparação com coluna vazia quando sobravam itens apenas de um lado.
- Marcadores `ANTES`/`DEPOIS` com emoji e conteúdo na mesma linha vindos do Word.
- Parágrafos inline `ANTES: ... DEPOIS: ...` divididos incorretamente.
- Slide de sobra com espaço vazio excessivo em comparação longa.

### Resultado

- `O que muda_slideforge_fase3_1.pptx` gerado com 24 slides.
- Auditoria sem blocos não utilizados, sem imagens ausentes e sem overflows críticos.
- Testes automatizados ampliados para 25 casos.
## [0.5.0] - Fase 4: Publishing Engine

### Adicionado

- Porta `DocumentRenderer` para renderização independente de formato.
- `PublishingEngine` para publicar múltiplos formatos a partir do mesmo `PresentationPlan`.
- Renderizadores: `PptxRenderer`, `PdfRenderer`, `HtmlRenderer`, `MarkdownRenderer`, `DocxRenderer` e `JsonRenderer`.
- PDF nativo via ReportLab, sem conversão por PowerPoint.
- HTML navegável com índice, capítulos, imagens, tabelas e notas do apresentador.
- Markdown estruturado preservando títulos, listas, imagens e tabelas.
- DOCX reorganizado com a estrutura lógica da apresentação.
- JSON completo com metadados, slides, componentes, auditoria, rastreabilidade e estatísticas.
- `AssetManager` para centralizar banners, logotipos e recursos visuais.
- `ThemeRegistry` e `PublishingTheme` para evoluir temas sem fixar valores nos renderizadores.
- Interfaces de extensão futura: `PresentationAdvisor`, `LayoutAdvisor`, `SummaryAdvisor`, `ThemeAdvisor` e `ContentAdvisor`.
- `PublishPresentationUseCase` para geração corporativa multi-formato.
- Testes automatizados específicos dos renderizadores e da consistência entre formatos.

### Mantido

- Sem React, FastAPI, banco de dados, IA, autenticação, OCR ou multiusuário.
- Domínio sem dependência de bibliotecas de infraestrutura.
- Pipeline das fases anteriores preservado.

## Sprint 4.1 - Refinamento executivo dos formatos publicados

- Refinados PDF, HTML, DOCX e Markdown para publicacoes corporativas mais legiveis.
- Adicionado `PublishingConsistencyValidator` para validar consistencia logica entre formatos.
- Adicionado manifesto de publicacao com hashes, tamanhos, auditoria, tema e versao.
- Adicionado pacote ZIP padronizado com os arquivos publicados.
- Adicionada fonte unica de versao em `slideforge/version.py`.
- Adicionados testes para PDF 16:9, HTML navegavel, DOCX estruturado, Markdown, manifesto, ZIP e consistencia.

## RC1 - Portabilidade da primeira release publica

- Markdown, JSON, manifesto, auditoria e ZIP passaram a ser sanitizados para nao expor caminhos absolutos do sistema operacional.
- Imagens extraidas do documento sao copiadas para `assets/` e referenciadas por caminho relativo.
- O ZIP contem `presentation/assets/` com os recursos necessarios para consulta local.
- O PDF foi definido oficialmente como documento executivo, podendo conter capa, agenda e auditoria alem dos slides logicos.
- O DOCX mantem sumario textual editavel; TOC nativo fica como melhoria futura.
