from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from slideforge.application.publishing.consistency_validator import ConsistencyResult
from slideforge.domain.entities.content_audit import ContentAudit
from slideforge.domain.entities.presentation_plan import PresentationPlan
from slideforge.infrastructure.assets import AssetManager
from slideforge.infrastructure.renderers.serialization import audit_dict
from slideforge.version import SCHEMA_VERSION, SLIDEFORGE_VERSION


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass
class ManifestBuilder:
    shared_paths: bool = True

    def build(self, plan: PresentationPlan, documents: list, output_path: Path, *, audit: ContentAudit | None = None, assets: AssetManager | None = None, theme=None, consistency: ConsistencyResult | None = None) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        source_path = Path(plan.source_document.source_path)
        base_dir = output_path.parent
        generated = []
        for doc in documents:
            path = Path(doc.path)
            generated.append({
                "format": doc.format_name,
                "path": self._rel(path, base_dir),
                "size_bytes": path.stat().st_size if path.exists() else 0,
                "sha256": sha256_file(path) if path.exists() else None,
            })
        data = {
            "schema_version": SCHEMA_VERSION,
            "slideforge_version": SLIDEFORGE_VERSION,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "source_document": {
                "name": plan.source_document.name,
                "format": plan.source_document.format,
                "sha256": sha256_file(source_path) if source_path.exists() else None,
            },
            "theme": getattr(theme, "name", str(theme)) if theme else None,
            "formats": generated,
            "statistics": {
                "slide_count": len(plan.slides),
                "component_count": sum(len(slide.components) for slide in plan.slides),
                "block_reference_count": sum(len(slide.source_block_ids) for slide in plan.slides),
                "image_count": sum(1 for slide in plan.slides for c in slide.components if c.get("type") == "image"),
                "table_count": sum(1 for slide in plan.slides for c in slide.components if c.get("type") == "table"),
            },
            "audit": audit_dict(audit),
            "assets": [
                {"key": asset.key, "type": asset.asset_type, "version": asset.version, "path": Path(asset.path).name}
                for asset in assets.all()
            ] if assets else [],
            "validation": consistency.as_dict() if consistency else None,
        }
        output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return output_path

    @staticmethod
    def _rel(path: Path, base_dir: Path) -> str:
        try:
            return path.relative_to(base_dir).as_posix()
        except ValueError:
            return path.name
