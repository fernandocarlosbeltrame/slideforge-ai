# SlideForge AI v1.0.0 - Release Notes

## Visao geral

A versao 1.0.0 consolida o SlideForge AI como motor local de geracao e publicacao corporativa a partir de documentos.

O sistema le documentos Word, PDF, Markdown e TXT, cria um plano de apresentacao rastreavel e publica o mesmo conteudo em multiplos formatos.

## Principais funcionalidades

- Pipeline deterministico com `PresentationPlan`.
- Exportacao PPTX editavel.
- Exportacao PDF executiva nativa.
- Exportacao HTML navegavel.
- Exportacao DOCX editavel.
- Exportacao Markdown estruturada.
- Exportacao JSON com rastreabilidade.
- Manifesto com hashes e estatisticas.
- Pacote ZIP portavel.
- Auditoria de conteudo, imagens, tabelas, densidade e rastreabilidade.
- Asset Manager.
- Theme Registry.
- Interface desktop Tkinter.
- Camada de IA opcional.
- Resumo local via Ollama opcional.
- Avaliacao deterministica de qualidade de resumo.

## Arquitetura

A arquitetura segue Clean Architecture:

- `domain`: entidades e regras puras.
- `application`: casos de uso, validacao, auditoria, publicacao e contratos.
- `infrastructure`: leitores, renderizadores, temas, assets e provedores.
- `presentation`: interface desktop.
- `legacy`: MVP preservado.

O dominio nao depende de bibliotecas de infraestrutura nem de provedores de IA.

## IA

A IA permanece opcional e desativada por padrao.

Disponivel na v1.0.0:

- `FakeAIProvider` deterministico.
- `OllamaProvider` local para resumo.
- Fallback.
- Avaliacao deterministica de resumo.

Fora do escopo:

- OpenAI real.
- Azure OpenAI real.
- RAG.
- Embeddings.
- Banco vetorial.
- Geracao completa de slides por IA.

## Validacoes da release

- 65 testes automatizados passando.
- `compileall` sem erros.
- `git diff --check` sem problemas.
- Artefatos v1.0.0 gerados a partir de documento real.
- Manifesto em versao 1.0.0.
- ZIP sem caminhos absolutos em conteudo textual.

## Limitacoes conhecidas

- PDF e documento executivo, nao espelho 1:1 do PPTX.
- DOCX possui sumario textual editavel, nao TOC nativo atualizavel.
- PDF escaneado nao possui OCR.
- Revisao visual humana ainda e recomendada antes de uso externo critico.
- Tema publico demonstrativo neutralizado como `corporate_blue`.

## Roadmap futuro

- Melhorias de UX.
- Mais temas.
- Composition root explicita.
- Testes visuais automatizados.
- Configuracao de IA pela interface.
- Versao web futura.
- OCR e IA externa apenas em versoes futuras.

## Agradecimentos

Esta release consolida as fases de arquitetura, visual engine, publishing engine e camada opcional de IA em uma base unica, testavel e publicavel.



## Artefatos demonstrativos

A release publica utiliza uma amostra neutra sem dados reais de empresas:

- `slideforge_ai_demo_v1.0.0_package.zip`
- `slideforge_ai_demo_v1.0.0_pptx_contact_sheet.png`
- `slideforge_ai_demo_v1.0.0_pdf_contact_sheet.png`

A amostra foi gerada com tema `corporate_blue` e manifesto `1.0.0`.
