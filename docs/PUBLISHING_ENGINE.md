# Publishing Engine

A Fase 4 transforma o SlideForge AI em um motor de publicação corporativa multi-formato.

## Princípio central

Todos os formatos são gerados a partir do mesmo `PresentationPlan`.

Nenhum renderizador altera o domínio. Cada um apenas interpreta o plano e escreve seu próprio formato.

## Renderizadores

A porta principal é:

```python
DocumentRenderer.render(plan, output_path, audit=None, assets=None, theme=None)
```

Implementações atuais:

- `PptxRenderer`
- `PdfRenderer`
- `HtmlRenderer`
- `MarkdownRenderer`
- `DocxRenderer`
- `JsonRenderer`

## PDF nativo

O `PdfRenderer` usa ReportLab. Ele não converte PowerPoint para PDF.

## HTML

O `HtmlRenderer` gera uma apresentação navegável com:

- índice;
- capítulos;
- slides como seções;
- imagens;
- tabelas;
- notas do apresentador;
- links internos.

## Markdown

O `MarkdownRenderer` preserva:

- hierarquia;
- títulos;
- listas;
- tabelas;
- imagens;
- notas.

## DOCX

O `DocxRenderer` reorganiza o `PresentationPlan` como documento Word, preservando a lógica da apresentação.

## JSON

O `JsonRenderer` exporta:

- metadados;
- slides;
- componentes;
- layouts;
- auditoria;
- rastreabilidade;
- estatísticas;
- assets.

Esse JSON é a base para integrações futuras.

## Asset Manager

O `AssetManager` centraliza recursos como:

- banners;
- logos;
- imagens;
- placeholders;
- ícones e recursos futuros.

## Temas

O `ThemeRegistry` empacota tokens visuais em `PublishingTheme`.

Cada tema pode definir:

- paleta;
- cards;
- tabelas;
- timelines;
- callouts;
- cabeçalho;
- rodapé.

## Pontos de extensão para IA

Foram criadas apenas interfaces, sem implementação:

- `PresentationAdvisor`
- `LayoutAdvisor`
- `SummaryAdvisor`
- `ThemeAdvisor`
- `ContentAdvisor`

## Como usar via código

```python
from pathlib import Path
from slideforge.application.use_cases.publish_presentation import PublishPresentationUseCase

result = PublishPresentationUseCase(theme_name="usiquimica").execute(
    Path("entrada.docx"),
    Path("saida"),
    banner_path="banner.jpg",
)
```

Arquivos gerados:

- `saida.pptx`
- `saida.pdf`
- `saida.html`
- `saida.md`
- `saida.docx`
- `saida.json`
- `saida.audit.txt`

## Sprint 4.1

O Publishing Engine agora possui refinamento executivo dos formatos publicados, manifesto e pacote ZIP.

Fluxo atualizado:

`PresentationPlan -> DocumentRenderers -> ConsistencyValidator -> ManifestBuilder -> PackageBuilder`

Notas nativas de PowerPoint e hyperlinks internos nativos no PPTX foram mantidos como evolucao futura por nao haver API publica segura em `python-pptx` para aplicar sem risco de corromper arquivos.

## RC1 - Decisao oficial de publicacao

### PDF executivo

A partir da RC1, o PDF e tratado oficialmente como **documento executivo**, nao como espelho 1:1 do PowerPoint.

Portanto, ele pode incluir:

- capa;
- agenda;
- paginas de conteudo;
- auditoria.

A quantidade de paginas do PDF pode ser maior que a quantidade de slides do PPTX. O `PresentationPlan` continua sendo a fonte unica da verdade; paginas extras representam elementos editoriais do pacote de publicacao.

### DOCX

O DOCX possui sumario textual editavel. Um sumario nativo atualizavel do Word nao foi implementado nesta release para evitar manipulacao fragil de campos XML/COM. Essa melhoria fica registrada para evolucao futura.
