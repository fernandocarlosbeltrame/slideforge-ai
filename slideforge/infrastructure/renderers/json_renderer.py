from __future__ import annotations

import json
from pathlib import Path

from slideforge.domain.entities.content_audit import ContentAudit
from slideforge.domain.entities.presentation_plan import PresentationPlan
from slideforge.infrastructure.assets import AssetManager
from slideforge.infrastructure.renderers.path_sanitizer import sanitize_public_value
from slideforge.infrastructure.renderers.serialization import plan_to_dict
from slideforge.version import SLIDEFORGE_VERSION


class JsonRenderer:
    format_name = "json"
    extension = ".json"

    def render(self, plan: PresentationPlan, output_path: Path, *, audit: ContentAudit | None = None, assets: AssetManager | None = None, theme=None) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        data = sanitize_public_value(plan_to_dict(plan, audit))
        data["slideforge_version"] = SLIDEFORGE_VERSION
        if assets:
            data["assets"] = [{"key": asset.key, "path": f"assets/{Path(asset.path).name}", "asset_type": asset.asset_type, "version": asset.version, "metadata": sanitize_public_value(asset.metadata)} for asset in assets.all()]
        if theme:
            data["theme"] = {"name": theme.name if hasattr(theme, "name") else str(theme)}
        output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return output_path
