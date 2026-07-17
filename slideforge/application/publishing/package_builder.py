from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from slideforge.infrastructure.renderers.path_sanitizer import collect_component_image_paths


class PublishingPackageBuilder:
    def build(self, package_path: Path, documents: list, manifest_path: Path, audit_path: Path | None = None, assets=None, plan=None) -> Path:
        package_path.parent.mkdir(parents=True, exist_ok=True)
        with ZipFile(package_path, "w", ZIP_DEFLATED) as zipf:
            for doc in documents:
                path = Path(doc.path)
                if path.exists():
                    zipf.write(path, f"presentation/presentation{path.suffix}")
            if manifest_path.exists():
                zipf.write(manifest_path, "presentation/presentation.manifest.json")
            if audit_path and audit_path.exists():
                zipf.write(audit_path, "presentation/presentation.audit.txt")
            seen: set[Path] = set()
            if assets:
                for asset in assets.all():
                    path = Path(asset.path)
                    if path.exists() and path not in seen:
                        seen.add(path)
                        zipf.write(path, f"presentation/assets/{path.name}")
            if plan:
                for path in collect_component_image_paths(plan):
                    if path.exists() and path not in seen:
                        seen.add(path)
                        zipf.write(path, f"presentation/assets/{path.name}")
        return package_path
