# SlideForge AI

Aplicacao para transformar documentos Word (`.docx`), PDF, Markdown e TXT em apresentacoes profissionais e pacotes de publicacao corporativa.

O SlideForge AI interpreta o conteudo, cria um plano rastreavel de apresentacao e publica os mesmos dados em multiplos formatos: PPTX, PDF, HTML, DOCX, Markdown, JSON, manifesto e pacote ZIP.

## Status

Versao preparada: **1.0.0**.

A versao 1.0.0 consolida o pipeline deterministico, a arquitetura limpa, os renderizadores multi-formato, auditoria, rastreabilidade, empacotamento e a camada opcional de IA local para resumo via Ollama.

## Principais funcionalidades

- Leitura de DOCX, TXT, Markdown e PDF.
- Extracao de imagens embutidas em DOCX.
- Leitura estruturada de tabelas DOCX.
- Planejamento rastreavel com `SourceDocument`, `ContentBlock`, `PresentationPlan` e `SlidePlan`.
- Selecao deterministica de layouts: capa, bullets, cards, timeline, comparacao, tabela e imagem.
- Exportacao PPTX editavel em widescreen 16:9.
- Exportacao PDF executiva nativa via ReportLab.
- Exportacao HTML navegavel e portavel.
- Exportacao DOCX reorganizada.
- Exportacao Markdown estruturada.
- Exportacao JSON com metadados, slides, componentes, auditoria e rastreabilidade.
- Manifesto com hashes e validacao.
- Pacote ZIP com assets relativos.
- Asset Manager para banners, logos e imagens.
- Theme Registry para temas visuais.
- Auditoria de conteudo, imagens, densidade, rastreabilidade e consistencia.
- Camada de IA desacoplada, com `FakeAIProvider` e `OllamaProvider` opcional para resumo.
- Avaliacao deterministica da qualidade de resumos por IA.
- Interface desktop Tkinter.
- MVP anterior preservado em `slideforge/legacy`.

## Executar

```bash
pip install -r requirements.txt
python app.py
```

## Rodar testes

```bash
python -m pytest
python -m compileall slideforge tests
```

## Gerar publicacao por codigo

```python
from pathlib import Path
from slideforge.application.use_cases.publish_presentation import PublishPresentationUseCase

result = PublishPresentationUseCase(theme_name="corporate_blue").execute(
    Path("entrada.docx"),
    Path("saida/Minha_Apresentacao"),
    banner_path="banner.jpg",
)
```

## Arquitetura

O projeto segue Clean Architecture:

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

Camadas principais:

- `slideforge/domain`: entidades e regras puras.
- `slideforge/application`: casos de uso, auditoria, validacao, publicacao e contratos.
- `slideforge/infrastructure`: leitores, renderizadores, temas, assets e provedores de IA.
- `slideforge/presentation`: interface desktop.
- `slideforge/legacy`: MVP preservado.

## Inteligencia artificial

A IA e opcional e fica desativada por padrao.

Recursos atuais:

- Contratos neutros para provedores.
- `FakeAIProvider` deterministico.
- `OllamaProvider` local para `ContentSummarizer`.
- Fallback seguro.
- Avaliacao deterministica de resumos.

Nao ha chamadas reais para OpenAI, Azure OpenAI ou servicos externos nesta versao.

## Documentacao

- `docs/ARCHITECTURE.md`
- `docs/PUBLISHING_ENGINE.md`
- `docs/AI_ARCHITECTURE.md`
- `docs/OLLAMA_INTEGRATION.md`
- `docs/AI_EVALUATION.md`
- `docs/V1_RELEASE_PLAN.md`
- `docs/RELEASE_NOTES_1.0.0.md`
- `docs/RELEASE_CHECKLIST_1.0.md`
- `docs/FINAL_RELEASE_REPORT.md`

## Limitacoes conhecidas

- PDF escaneado nao possui OCR.
- PDF e documento executivo, nao espelho 1:1 do PPTX.
- DOCX possui sumario textual editavel; TOC nativo do Word fica para evolucao futura.
- Notas nativas no painel do PowerPoint e hyperlinks internos nativos no PPTX ficam para evolucao futura.
- IA local com Ollama e opcional e depende de ambiente local configurado.
- A revisao visual fina ainda deve ser feita por uma pessoa antes de uso externo critico.

## Roadmap futuro

- Melhorias de UX na interface desktop.
- Composition root mais explicita.
- Mais temas visuais.
- Testes visuais automatizados mais robustos.
- UI para configuracao de IA local.
- Versao web futura com React/FastAPI.
- OCR, RAG, embeddings e provedores externos apenas em versoes futuras.
