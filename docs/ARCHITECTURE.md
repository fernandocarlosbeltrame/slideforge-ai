# Arquitetura - SlideForge AI

A Fase 1 implementa uma base limpa para transformar documentos em apresentações rastreáveis.

## Camadas

- `domain`: entidades e regras puras, sem dependência de bibliotecas externas.
- `application`: casos de uso, planejamento e auditoria.
- `infrastructure`: leitores de arquivo e exportadores.
- `presentation`: interface desktop Tkinter.
- `legacy`: cópia funcional do MVP anterior.

## Pipeline

```text
SourceDocument
↓
DocumentSection / ContentBlock
↓
PresentationPlan / SlidePlan
↓
LayoutSelector
↓
PPTXExporter
↓
ContentAudit
```

## Rastreabilidade

Cada `SlidePlan` mantém `source_block_ids`, permitindo identificar:

- blocos utilizados;
- blocos parcialmente utilizados;
- blocos divididos;
- blocos não utilizados.

## Limitações da Fase 1

- Sem FastAPI.
- Sem React.
- Sem banco de dados.
- Sem PDF.
- Sem IA.
- Sem sistema externo de plugins.
- Extração de imagem DOCX é básica e salva mídia em `.slideforge_assets`.

## Fase 2 - Fidelidade visual

A Fase 2 adiciona serviços de apoio à renderização sem mover regras de negócio para o exportador.

Novos serviços:

- `SlideGeometry`: dimensões 16:9, cabeçalho, rodapé e área segura.
- `BoundingBox`: validação de coordenadas e dimensões.
- `ImageFitCalculator`: cálculo proporcional para `contain`, `cover`, `original`, `fit_width` e `fit_height`.
- `TypographyFitter`: estimativa inicial de ajuste de títulos e textos.
- `PresentationValidator`: validação do plano antes da exportação.

O domínio continua livre de dependências como `python-pptx`, `python-docx`, `Pillow` e `PyMuPDF`.

## Fase 4 - Publishing Engine

A Fase 4 adiciona uma camada de publicação sem alterar o domínio.

Fluxo:

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
DocumentRenderer(s)
↓
PPTX • PDF • HTML • Markdown • DOCX • JSON
```

Cada renderizador consome o mesmo `PresentationPlan`. O domínio permanece livre de dependências como `python-pptx`, `ReportLab` ou `python-docx`.

Novos pontos de infraestrutura:

- `slideforge/application/ports/document_renderer.py`
- `slideforge/application/publishing/publishing_engine.py`
- `slideforge/infrastructure/renderers/`
- `slideforge/infrastructure/assets/`
- `slideforge/infrastructure/themes/`

Interfaces para IA futura ficam em `slideforge/application/advisors`, sem implementação concreta nesta fase.

## Sprint 4.1 - Publishing Package

A camada de publicacao ganhou tres componentes de aplicacao:

- `PublishingConsistencyValidator`: compara a consistencia logica dos formatos gerados.
- `ManifestBuilder`: gera manifesto com hashes, tamanhos, versao, auditoria e validacao.
- `PublishingPackageBuilder`: cria ZIP padronizado em `presentation/`.

O dominio permanece isolado. Todos os renderizadores continuam consumindo o mesmo `PresentationPlan`.
