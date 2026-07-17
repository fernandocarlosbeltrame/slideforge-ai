# SlideForge AI v0.4.1 RC1

## Status

Release Candidate 1 aprovada com ressalvas documentadas.

## Destaques

- Pipeline baseado em `PresentationPlan`.
- Exportacao PPTX, PDF, HTML, DOCX, Markdown e JSON.
- Manifesto com hashes e auditoria.
- Pacote ZIP portavel.
- Sanitizacao de caminhos locais em artefatos publicados.
- PDF definido como documento executivo.

## Validacoes

- 39 testes automatizados passando.
- `compileall` sem erros.
- PPTX aberto e renderizado via PowerPoint COM.
- DOCX aberto via Word COM.
- ZIP extraido com assets relativos.

## Limitacoes conhecidas

- PDF possui capa, agenda e auditoria; portanto pode ter mais paginas que os slides do PPTX.
- DOCX possui sumario textual editavel, nao TOC nativo do Word.
- Notas nativas no PowerPoint ficam para evolucao futura.
- Hyperlinks internos nativos no PPTX ficam para evolucao futura.

## Arquivos sugeridos para release

- Pacote RC1 ZIP.
- Manifesto RC1.
- Folhas de contato visuais.
- Documentacao em `docs/`.
