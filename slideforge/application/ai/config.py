from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import Any


@dataclass(frozen=True)
class AIConfig:
    enabled: bool = False
    provider: str = "fake"
    model: str = ""
    base_url: str = "http://localhost:11434"
    temperature: float = 0.2
    max_tokens: int = 1000
    timeout_seconds: int = 60
    fallback_provider: str = "fake"
    extra: dict[str, Any] = field(default_factory=dict)
    active_provider: str | None = None
    token_limit: int | None = None

    def __post_init__(self) -> None:
        provider = (self.active_provider or self.provider or "fake").lower()
        object.__setattr__(self, "provider", provider)
        object.__setattr__(self, "active_provider", provider)
        if self.token_limit is not None:
            object.__setattr__(self, "max_tokens", int(self.token_limit))
        object.__setattr__(self, "fallback_provider", (self.fallback_provider or "fake").lower())
        if not self.model:
            default_model = "fake-deterministic-v1" if provider == "fake" else ""
            object.__setattr__(self, "model", default_model)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AIConfig":
        provider = str(data.get("provider", data.get("active_provider", "fake"))).lower()
        max_tokens = int(data.get("max_tokens", data.get("token_limit", 1000)))
        return cls(
            enabled=bool(data.get("enabled", False)),
            provider=provider,
            active_provider=provider,
            temperature=float(data.get("temperature", 0.2)),
            model=str(data.get("model", "fake-deterministic-v1" if provider == "fake" else "")),
            base_url=str(data.get("base_url", "http://localhost:11434")),
            max_tokens=max_tokens,
            token_limit=max_tokens,
            timeout_seconds=int(data.get("timeout_seconds", 60)),
            fallback_provider=str(data.get("fallback_provider", "fake")).lower(),
            extra=dict(data.get("extra", {})),
        )

    @classmethod
    def from_file(cls, path: str | Path) -> "AIConfig":
        config_path = Path(path)
        data = json.loads(config_path.read_text(encoding="utf-8"))
        return cls.from_dict(data)

    def as_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "provider": self.provider,
            "active_provider": self.active_provider,
            "model": self.model,
            "base_url": self.base_url,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "token_limit": self.max_tokens,
            "timeout_seconds": self.timeout_seconds,
            "fallback_provider": self.fallback_provider,
            "extra": self.extra,
        }
