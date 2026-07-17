# Integracao Ollama - SlideForge AI v1.0.0

O SlideForge AI possui integracao local opcional com Ollama apenas para resumo de conteudo.

## Escopo

- Apenas `ContentSummarizer` usa IA real local.
- Nenhum outro contrato usa modelo real nesta versao.
- A IA permanece desativada por padrao.
- `FakeAIProvider` continua disponivel para testes e fallback.
- O conteudo original nunca e substituido automaticamente.

## Instalacao manual

O SlideForge nao instala o Ollama e nao baixa modelos automaticamente.

1. Instale o Ollama pelo site oficial.
2. Baixe manualmente um modelo, por exemplo:

```bash
ollama pull llama3.1
```

## Configuracao

Arquivo:

```text
slideforge/config/ai_config.json
```

IA desligada:

```json
{
  "enabled": false,
  "provider": "fake",
  "model": "",
  "base_url": "http://localhost:11434",
  "temperature": 0.2,
  "max_tokens": 1000,
  "timeout_seconds": 60,
  "fallback_provider": "fake"
}
```

Exemplo local com Ollama:

```json
{
  "enabled": true,
  "provider": "ollama",
  "model": "llama3.1",
  "base_url": "http://localhost:11434",
  "temperature": 0.2,
  "max_tokens": 1000,
  "timeout_seconds": 60,
  "fallback_provider": "fake"
}
```

## CLI de teste

```bash
python -m slideforge.ai_summarize --text-file exemplo.txt --provider ollama --model llama3.1
```

Com fallback desativado:

```bash
python -m slideforge.ai_summarize --text-file exemplo.txt --provider ollama --model llama3.1 --no-fallback
```

## Elegibilidade

Nao sao resumidos automaticamente:

- titulos;
- subtitulos;
- tabelas;
- imagens;
- numeros isolados;
- datas isoladas;
- listas curtas;
- conteudos curtos.

Candidatos a resumo:

- paragrafos longos;
- notas longas;
- blocos densos acima dos limites definidos.

## Fallback e seguranca

Se o Ollama falhar, o sistema pode usar fallback fake ou preservar o conteudo original. Erros externos sao sanitizados para evitar caminhos locais e dados sensiveis.

Nao devem ser registrados em logs:

- texto integral do documento;
- prompt completo com conteudo corporativo;
- chaves;
- caminhos locais;
- nomes de usuarios.

## Limitacoes

- Sem OpenAI real.
- Sem Azure OpenAI real.
- Sem RAG.
- Sem embeddings.
- Sem banco vetorial.
- Qualidade depende do modelo local instalado.
