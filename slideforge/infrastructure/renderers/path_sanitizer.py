from __future__ import annotations

from pathlib import Path
import shutil
from typing import Any

SENSITIVE_MARKERS = ("C:\\Users", "C:/Users", "\\Users\\", "/Users/")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}


def is_sensitive_path(value: str) -> bool:
    text = str(value)
    return any(marker in text for marker in SENSITIVE_MARKERS) or (len(text) > 2 and text[1:3] in (":\\", ":/"))


def public_asset_path(path: str | Path, prefix: str = "assets") -> str:
    p = Path(path)
    return f"{prefix}/{p.name}"


def sanitize_public_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): sanitize_public_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize_public_value(v) for v in value]
    if isinstance(value, tuple):
        return [sanitize_public_value(v) for v in value]
    if isinstance(value, str):
        if is_sensitive_path(value):
            p = Path(value)
            if p.suffix.lower() in IMAGE_SUFFIXES:
                return public_asset_path(p)
            return p.name
        return value
    return value


def collect_component_image_paths(plan) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()
    for slide in plan.slides:
        for component in slide.components:
            if component.get("type") == "image" and component.get("path"):
                path = Path(component["path"])
                if path.exists() and path not in seen:
                    seen.add(path)
                    paths.append(path)
    return paths


def copy_public_assets(plan, target_dir: Path) -> dict[str, str]:
    target_dir.mkdir(parents=True, exist_ok=True)
    mapping: dict[str, str] = {}
    for path in collect_component_image_paths(plan):
        dest = _unique_dest(target_dir, path.name)
        if not dest.exists():
            shutil.copy2(path, dest)
        mapping[str(path)] = f"assets/{dest.name}"
    return mapping


def _unique_dest(target_dir: Path, name: str) -> Path:
    candidate = target_dir / name
    if not candidate.exists():
        return candidate
    stem = candidate.stem
    suffix = candidate.suffix
    index = 2
    while True:
        current = target_dir / f"{stem}_{index}{suffix}"
        if not current.exists():
            return current
        index += 1
