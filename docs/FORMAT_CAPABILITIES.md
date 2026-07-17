# Matriz de Capacidades dos Formatos

| Recurso | PPTX | PDF | HTML | DOCX | Markdown | JSON |
|---|---|---|---|---|---|---|
| Imagens | Sim | Sim | Sim, embutidas quando possivel | Sim | Referencia ao arquivo | Metadados e caminhos |
| Tabelas | Sim | Sim, com cabecalho repetivel | Sim, responsivas | Sim | Sim | Dados estruturados |
| Notas | Externas/JSON | Texto por pagina | Painel recolhivel | Observacoes por slide | Bloco recolhivel | Estruturadas |
| Links internos | Parcial | Nao aplicavel | Sim | Parcial | Sim | Metadados |
| Tema | Sim | Sim | Sim | Parcial via estilos | Metadados | Metadados |
| Rastreabilidade | Sim | Notas resumidas | Notas e blocos | Observacoes | Comentarios HTML | Completa |
| Pacote ZIP | Sim | Sim | Sim | Sim | Sim | Sim |
| Manifesto | Sim | Sim | Sim | Sim | Sim | Sim |

## Observacao

Os formatos nao tentam ser clones visuais. Cada renderizador respeita a linguagem do seu formato, usando o mesmo `PresentationPlan` como fonte unica da verdade.
