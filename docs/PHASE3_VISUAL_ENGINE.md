# Fase 3 - Motor Visual Profissional

A Fase 3 adiciona uma camada visual reutilizável ao SlideForge AI sem alterar o domínio nem introduzir React, FastAPI, banco de dados, IA ou exportação PDF final.

## Componentes PPTX

Foram criados componentes em `slideforge/infrastructure/exporters/pptx/components`:

- `TitleBlock`
- `Footer`
- `BulletList`
- `CardGrid`
- `ComparisonComponent`
- `TimelineComponent`
- `ImagePanel`
- `TableComponent`

O `PPTXExporter` usa esses componentes para renderizar os layouts atuais.

## Grid

O `SlideGrid` cria colunas, linhas e divisões proporcionais dentro da área segura do slide.

Exemplos suportados:

- cards 2x2 ou 2x3;
- comparação 50/50;
- imagem + texto 45/55;
- divisão por linhas para componentes futuros.

## Decisão Visual

O `LayoutSelector` agora gera `LayoutDecision`, contendo:

- layout escolhido;
- composição visual;
- motivo da decisão;
- regras acionadas;
- alternativas consideradas;
- densidade.

Esses dados são armazenados em `SlidePlan.metadata`.

## Densidade Visual

O `ContentDensityAnalyzer` classifica cada slide como:

- `low`;
- `medium`;
- `high`;
- `critical`.

Slides críticos entram na auditoria como risco visual. Na regressão real da Fase 3, o documento de teste ficou com zero overflows críticos.

## Preview HTML

Ao gerar o PPTX, o sistema também cria:

```text
<nome_do_arquivo>_preview.html
```

Esse arquivo mostra:

- número do slide;
- título;
- layout;
- composição visual;
- densidade;
- quantidade de blocos;
- motivo da decisão.

## Como Validar

1. Rode os testes:

```bash
python -m pytest
```

2. Gere uma apresentação real pelo app ou pelo caso de uso.

3. Confira os arquivos gerados:

- `.pptx`;
- `.audit.txt`;
- `_preview.html`.

4. No relatório de auditoria, confirme:

- `Blocos não utilizados: 0`;
- `Overflows críticos: 0`;
- variedade de layouts;
- imagens utilizadas quando existirem no documento.

## Limitações

- O preview HTML é estrutural, não uma renderização fiel do PowerPoint.
- A inspeção estética final ainda deve ser feita no PowerPoint.
- A IA visual fica reservada para fase futura.
