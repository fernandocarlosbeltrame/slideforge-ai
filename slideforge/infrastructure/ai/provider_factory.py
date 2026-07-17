from slideforge.application.ai.config import AIConfig
from slideforge.application.ai.provider import AIProvider
from slideforge.infrastructure.ai.fake_provider import FakeAIProvider
from slideforge.infrastructure.ai.ollama_provider import OllamaContentSummarizer
from slideforge.infrastructure.ai.stubs import AzureOpenAIProvider, LMStudioProvider, OpenAIProvider, StubAIProvider


class OllamaProvider(StubAIProvider):
    provider_name = "ollama"

    def content_summarizer(self):
        return OllamaContentSummarizer(self._config)


class AIProviderFactory:
    _providers = {
        "fake": FakeAIProvider,
        "openai": OpenAIProvider,
        "azure_openai": AzureOpenAIProvider,
        "azure-openai": AzureOpenAIProvider,
        "ollama": OllamaProvider,
        "lmstudio": LMStudioProvider,
        "lm_studio": LMStudioProvider,
    }

    def create(self, config: AIConfig) -> AIProvider:
        provider_key = (config.provider or config.active_provider or "fake").lower()
        provider_cls = self._providers.get(provider_key)
        if provider_cls is None:
            supported = ", ".join(sorted(self._providers))
            raise ValueError(f"Provedor de IA não suportado: {provider_key}. Suportados: {supported}")
        return provider_cls(config)
