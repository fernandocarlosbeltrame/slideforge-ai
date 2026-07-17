# Roadmap da Fase 5 - Camada de IA

A Fase 5 ainda nao deve ser implementada. Este documento define o escopo antes de qualquer codigo.

## Objetivo

Adicionar IA como camada de recomendacao e assistencia, mantendo o pipeline deterministico como fonte segura e auditavel.

## Onde a IA entra

A IA deve entrar somente por interfaces ja previstas:

- `PresentationAdvisor`: avalia a apresentacao completa e sugere melhorias.
- `LayoutAdvisor`: sugere layout alternativo para secoes complexas.
- `SummaryAdvisor`: cria resumos de apoio, sem descartar conteudo original.
- `ThemeAdvisor`: sugere tema visual com base no publico e no contexto.
- `ContentAdvisor`: aponta excesso de densidade, repeticoes e riscos de legibilidade.

## O que permanece deterministico

- Leitura dos documentos.
- Criacao de `SourceDocument`, `DocumentSection` e `ContentBlock`.
- Rastreabilidade dos blocos.
- Auditoria de conteudo.
- Exportacao PPTX, PDF, HTML, DOCX, Markdown e JSON.
- Manifesto, hashes e pacote ZIP.

## Recursos candidatos a IA

1. Sugestao de layout por secao.
2. Reescrita opcional de titulos longos.
3. Sugestao de quebra de slides densos.
4. Resumo para notas do apresentador.
5. Sugestao de tom visual e tema.
6. Classificacao de publico-alvo.
7. Checklist de qualidade visual e textual.

## Modelos suportados futuramente

A arquitetura deve ser agnostica. Possiveis provedores:

- OpenAI.
- Azure OpenAI.
- Modelos locais via adaptadores futuros.

Nenhum provedor deve entrar diretamente no dominio.

## Contratos necessarios

- Entrada: `PresentationPlan`, contexto do usuario e politicas de seguranca.
- Saida: sugestoes estruturadas, nunca alteracao direta do plano sem aprovacao.
- Auditoria: toda sugestao deve ser registrada.

## Regras de seguranca

- Nao enviar documentos sensiveis para IA sem confirmacao explicita.
- Permitir modo offline/deterministico.
- Registrar prompts, decisoes e versoes de modelo quando IA for usada.

## Entrega sugerida da Fase 5

1. Definir contratos das sugestoes.
2. Criar implementacao fake/local para testes.
3. Adicionar opt-in de IA.
4. Criar primeiro advisor real somente apos validacao.
