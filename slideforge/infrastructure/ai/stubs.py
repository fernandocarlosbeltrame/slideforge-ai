from slideforge.application.ai.config import AIConfig
from slideforge.application.ai.models import AIProviderInfo


class StubAIProvider:
    provider_name = "stub"

    def __init__(self, config: AIConfig | None = None):
        self._config = config or AIConfig(provider=self.provider_name)

    @property
    def info(self) -> AIProviderInfo:
        return AIProviderInfo(name=self.provider_name, model=self._config.model, supports_external_calls=True, deterministic=False)

    @property
    def config(self) -> AIConfig:
        return self._config

    def _not_implemented(self):
        raise NotImplementedError(f"{self.provider_name} é apenas um stub arquitetural nesta sprint.")

    def document_analyzer(self):
        self._not_implemented()

    def presentation_planner(self):
        self._not_implemented()

    def slide_layout_advisor(self):
        self._not_implemented()

    def content_summarizer(self):
        self._not_implemented()

    def theme_advisor(self):
        self._not_implemented()

    def image_suggestion_provider(self):
        self._not_implemented()

    def speaker_notes_generator(self):
        self._not_implemented()

    def presentation_reviewer(self):
        self._not_implemented()


class OpenAIProvider(StubAIProvider):
    provider_name = "openai"


class AzureOpenAIProvider(StubAIProvider):
    provider_name = "azure_openai"


class LMStudioProvider(StubAIProvider):
    provider_name = "lmstudio"
