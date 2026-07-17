# Release Acceptance - RC1

## Versao

- Produto: SlideForge AI
- Base: 0.4.1
- Release Candidate: RC1
- Data da revisao: 2026-07-17
- Decisao: APROVADA COM RESSALVAS

## Arquivos avaliados

- `<pasta-local>/Downloads/O que muda_slideforge_RC1.pptx`
- `<pasta-local>/Downloads/O que muda_slideforge_RC1.pdf`
- `<pasta-local>/Downloads/O que muda_slideforge_RC1.html`
- `<pasta-local>/Downloads/O que muda_slideforge_RC1.docx`
- `<pasta-local>/Downloads/O que muda_slideforge_RC1.md`
- `<pasta-local>/Downloads/O que muda_slideforge_RC1.json`
- `<pasta-local>/Downloads/O que muda_slideforge_RC1.audit.txt`
- `<pasta-local>/Downloads/O que muda_slideforge_RC1.manifest.json`
- `<pasta-local>/Downloads/O que muda_slideforge_RC1_package.zip`

## Metodos utilizados

- Testes automatizados com `pytest`.
- Compilacao com `compileall`.
- PowerPoint COM para abertura e renderizacao do PPTX.
- Word COM para abertura do DOCX.
- PyMuPDF para inspecao do PDF.
- Parser JSON para JSON e manifesto.
- `zipfile` para extracao e validacao do pacote.
- Busca automatica por caminhos sensiveis em HTML, Markdown, JSON, manifesto, auditoria e ZIP.

## Resultados estruturais

- PPTX: abriu via PowerPoint COM; 24 slides; 24 PNGs renderizados.
- PDF: 28 paginas; proporcao 16:9; texto selecionavel.
- HTML: sem caminhos absolutos; imagem embutida; navegacao presente.
- DOCX: abriu via Word COM; 285 paragrafos; 11 tabelas; sem reparo observado.
- Markdown: sem caminhos absolutos; imagem referenciada como `assets/rId5_image1.png`.
- JSON: versao 0.4.1; 24 slides; sem caminhos absolutos.
- Manifesto: validacao `ok`; 24 slides logicos; caminhos relativos.
- ZIP: estrutura `presentation/`; assets incluidos; sem caminhos absolutos em conteudo textual.

## Problemas por severidade

### BLOQUEADOR

Nenhum.

### RELEVANTE

Nenhum bloqueante para release publica.

### COSMETICO

1. Alguns slides PPTX ainda possuem bastante espaco em branco e texto pequeno. Nao afeta uso nem seguranca.

### LIMITACAO CONHECIDA

1. PDF e documento executivo, nao espelho 1:1 do PPTX. Por isso possui 28 paginas, com capa, agenda e auditoria.
2. DOCX possui sumario textual editavel, nao campo nativo atualizavel do Word.
3. Notas nativas no painel do PowerPoint nao foram implementadas por falta de API publica segura em `python-pptx`.
4. Hyperlinks internos nativos no PPTX permanecem como evolucao futura.

## Seguranca e portabilidade

- `<caminho-local>`: nao encontrado nos arquivos publicados textuais nem dentro do ZIP.
- `<caminho-local>`: nao encontrado.
- `<usuario-local>`: nao encontrado nos arquivos publicados textuais nem dentro do ZIP.
- Arquivos temporarios: nao encontrados no ZIP.
- HTML apos extracao: presente e com assets disponiveis.
- Manifesto: sem caminhos absolutos.

## Testes

- `python -m pytest`: 39 testes passaram.
- `python -m compileall slideforge tests`: sem erros.

## Decisao final

APROVADA COM RESSALVAS.

A RC1 esta apta para ser considerada primeira release publica desde que as limitacoes conhecidas sejam aceitas e documentadas.

## Recomendacao

- Criar release RC1/publica demonstrativa.
- Nao iniciar Fase 5 antes de uma revisao visual humana final dos arquivos publicados.
