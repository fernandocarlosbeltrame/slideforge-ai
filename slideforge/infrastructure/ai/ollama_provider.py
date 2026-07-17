from __future__ import annotations

import json
import time
from urllib import error, request

from slideforge.application.ai.config import AIConfig
from slideforge.application.ai.contracts import ContentSummarizer
from slideforge.application.ai.models import AIContext, SummaryOptions, SummaryResult


class OllamaError(Exception):
    error_type = "ollama_error"


class OllamaUnavailableError(OllamaError):
    error_type = "connection_unavailable"


class OllamaTimeoutError(OllamaError):
    error_type = "timeout"


class OllamaModelNotFoundError(OllamaError):
    error_type = "model_not_found"


class OllamaInvalidResponseError(OllamaError):
    error_type = "invalid_response"


class OllamaEmptyResponseError(OllamaError):
    error_type = "empty_response"


class OllamaContentSummarizer(ContentSummarizer):
    def __init__(self, config: AIConfig):
        self.config = config

    def summarize_content(self, text: str, context: AIContext | None = None, *, options: SummaryOptions | None = None) -> SummaryResult:
        started = time.perf_counter()
        options = options or SummaryOptions(language=context.language if context else "pt-BR", max_length=self.config.max_tokens)
        prompt = self._build_prompt(text, context, options)
        try:
            response_text = self._call_ollama(prompt)
            duration_ms = int((time.perf_counter() - started) * 1000)
            return SummaryResult(
                text=response_text,
                source_length=len(text),
                was_truncated=False,
                provider="ollama",
                model=self.config.model,
                fallback_used=False,
                duration_ms=duration_ms,
                warnings=[],
                success=True,
                status="ok",
            )
        except OllamaError as exc:
            duration_ms = int((time.perf_counter() - started) * 1000)
            return SummaryResult(
                text=text,
                source_length=len(text),
                provider="ollama",
                model=self.config.model,
                fallback_used=False,
                duration_ms=duration_ms,
                warnings=[sanitize_external_error(str(exc))],
                success=False,
                status="failed",
                error_type=getattr(exc, "error_type", "ollama_error"),
            )

    def _build_prompt(self, text: str, context: AIContext | None, options: SummaryOptions) -> str:
        objective = options.objective or "Criar resumo fiel e seguro para apresentação."
        language = options.language or (context.language if context else "pt-BR")
        extra_context = f"\nContexto opcional: {options.context}" if options.context else ""
        return (
            "Você é um assistente de apoio editorial corporativo.\n"
            "Tarefa: resumir o conteúdo abaixo somente quando for seguro.\n"
            f"Objetivo: {objective}\n"
            f"Idioma de saída: {language}.\n"
            f"Tamanho máximo desejado: {options.max_length} caracteres.\n"
            "Regras obrigatórias:\n"
            "- Não invente informações.\n"
            "- Preserve números, datas, percentuais, nomes de tributos e referências legais.\n"
            "- Não altere o sentido do texto.\n"
            "- Não trate tabelas estruturadas como texto comum.\n"
            "- Se não for seguro resumir, responda: NÃO_RESUMIR_COM_SEGURANÇA.\n"
            f"{extra_context}\n\n"
            "Conteúdo:\n"
            f"{text}\n"
        )

    def _call_ollama(self, prompt: str) -> str:
        if not self.config.model:
            raise OllamaModelNotFoundError("Modelo Ollama não informado.")
        base_url = self.config.base_url.rstrip("/")
        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens,
            },
        }
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(f"{base_url}/api/generate", data=data, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with request.urlopen(req, timeout=self.config.timeout_seconds) as response:
                raw = response.read().decode("utf-8")
        except TimeoutError as exc:
            raise OllamaTimeoutError("Timeout ao consultar o Ollama local.") from exc
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            if exc.code == 404 or "not found" in body.lower() or "model" in body.lower():
                raise OllamaModelNotFoundError("Modelo não encontrado no Ollama local.") from exc
            raise OllamaUnavailableError(f"Erro HTTP do Ollama: {exc.code}.") from exc
        except error.URLError as exc:
            reason = str(getattr(exc, "reason", exc))
            if "timed out" in reason.lower():
                raise OllamaTimeoutError("Timeout ao conectar no Ollama local.") from exc
            raise OllamaUnavailableError("Ollama local indisponível ou conexão recusada.") from exc
        except OSError as exc:
            raise OllamaUnavailableError("Falha de conexão com o Ollama local.") from exc

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise OllamaInvalidResponseError("Resposta JSON inválida do Ollama.") from exc
        if not isinstance(parsed, dict):
            raise OllamaInvalidResponseError("Resposta do Ollama não é um objeto JSON.")
        if parsed.get("error"):
            error_message = str(parsed.get("error"))
            if "not found" in error_message.lower() or "model" in error_message.lower():
                raise OllamaModelNotFoundError("Modelo não encontrado no Ollama local.")
            raise OllamaInvalidResponseError("Ollama retornou erro na resposta.")
        response_text = str(parsed.get("response", "")).strip()
        if not response_text:
            raise OllamaEmptyResponseError("Ollama retornou resposta vazia.")
        return response_text


def sanitize_external_error(message: str) -> str:
    sanitized = message.replace("\\", "/")
    markers = ["/Users/", "C:/Users/"]
    for marker in markers:
        if marker in sanitized:
            before, _, after = sanitized.partition(marker)
            tail = after.split("/", 1)[1] if "/" in after else ""
            sanitized = before + marker + "<usuario>/" + tail
    if len(sanitized) > 180:
        sanitized = sanitized[:177].rstrip() + "..."
    return sanitized
