from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class AssetReference:
    key: str
    path: Path
    asset_type: str
    version: str = "1"
    metadata: dict[str, Any] = field(default_factory=dict)


class AssetManager:
    def __init__(self, roots: list[Path] | None = None):
        self.roots = roots or []
        self._assets: dict[str, AssetReference] = {}

    def register(self, key: str, path: str | Path, asset_type: str, *, version: str = "1", metadata: dict[str, Any] | None = None) -> AssetReference:
        ref = AssetReference(key=key, path=Path(path), asset_type=asset_type, version=version, metadata=metadata or {})
        self._assets[key] = ref
        return ref

    def get(self, key: str) -> AssetReference | None:
        return self._assets.get(key)

    def locate(self, key: str) -> Path | None:
        ref = self.get(key)
        if ref and ref.path.exists():
            return ref.path
        for root in self.roots:
            for candidate in root.rglob(key):
                if candidate.is_file():
                    return candidate
        return None

    def all(self) -> list[AssetReference]:
        return list(self._assets.values())

    def register_banner(self, path: str | Path) -> AssetReference:
        return self.register("banner", path, "banner")

    def register_logo(self, path: str | Path) -> AssetReference:
        return self.register("logo", path, "logo")
