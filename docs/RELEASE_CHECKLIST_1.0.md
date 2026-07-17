# Release Checklist - SlideForge AI v1.0.0

## Testes

- [x] `python -m pytest`
- [x] `python -m compileall slideforge tests`
- [x] `git diff --check`
- [x] Geracao real de artefatos v1.0.0

## Documentacao

- [x] README revisado
- [x] CHANGELOG revisado
- [x] ARCHITECTURE revisado
- [x] AI_ARCHITECTURE revisado
- [x] PUBLISHING_ENGINE revisado
- [x] OLLAMA_INTEGRATION revisado
- [x] AI_EVALUATION revisado
- [x] ROADMAP_PHASE5 revisado
- [x] V1_RELEASE_PLAN criado
- [x] RELEASE_NOTES_1.0.0 criado
- [x] FINAL_RELEASE_REPORT criado

## Seguranca

- [x] Busca por caminhos absolutos
- [x] Busca por nomes locais
- [x] Busca por tokens e credenciais
- [x] Busca por segredos
- [x] Busca por dados corporativos
- [x] Busca por arquivos temporarios
- [x] Validacao de ZIP sem caminhos absolutos em textos publicados

## Revisao visual e estrutural

- [x] PPTX gerado e inspecionado estruturalmente
- [x] PDF gerado e inspecionado estruturalmente
- [x] HTML gerado e inspecionado estruturalmente
- [x] DOCX gerado e inspecionado estruturalmente
- [x] Markdown gerado
- [x] JSON gerado
- [x] Manifesto gerado
- [x] ZIP gerado

## Empacotamento

- [x] Pacote ZIP gerado
- [x] Manifesto com hashes
- [x] Assets relativos
- [x] Sem arquivos temporarios no pacote

## GitHub

- [x] Revisao automatizada assistida concluida; revisao humana visual final recomendada
- [ ] Commit da sprint final
- [ ] Tag `v1.0.0`
- [ ] Release GitHub
- [ ] Upload de artefatos demonstrativos

## Validacao final antes de publicar

- [ ] Abrir PPTX manualmente pelo usuario antes da publicacao final
- [ ] Abrir PDF manualmente pelo usuario antes da publicacao final
- [ ] Abrir DOCX manualmente pelo usuario antes da publicacao final
- [x] Validar HTML/ZIP estruturalmente; abertura visual em navegador recomendada pelo usuario
- [ ] Revisar screenshots/folha de contato, se desejado
- [ ] Confirmar que nenhum exemplo contem dados sensiveis

## Amostra publica neutra

- [x] Documento demonstrativo sem empresa real
- [x] Banner demonstrativo neutro
- [x] Artefatos `slideforge_ai_demo_v1.0.0.*`
- [x] Manifesto versao 1.0.0
- [x] Tema `corporate_blue`
- [x] ZIP portavel sem caminhos absolutos em textos
- [x] Folhas de contato PPTX e PDF geradas
