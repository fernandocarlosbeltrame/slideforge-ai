from __future__ import annotations

from pathlib import Path

from slideforge.application.publishing.speaker_notes import SpeakerNotesGenerator
from slideforge.domain.entities.content_audit import ContentAudit
from slideforge.domain.entities.presentation_plan import PresentationPlan
from slideforge.infrastructure.assets import AssetManager
from slideforge.infrastructure.renderers.path_sanitizer import copy_public_assets, public_asset_path
from slideforge.infrastructure.renderers.serialization import plan_agenda
from slideforge.version import SLIDEFORGE_VERSION


class MarkdownRenderer:
    format_name = "markdown"
    extension = ".md"

    def render(self, plan: PresentationPlan, output_path: Path, *, audit: ContentAudit | None = None, assets: AssetManager | None = None, theme=None) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        asset_map = copy_public_assets(plan, output_path.parent / "assets")
        notes = {n.slide_sequence: n for n in SpeakerNotesGenerator().generate(plan)}
        theme_name = getattr(theme, "name", "corporate_blue") if theme else "corporate_blue"
        lines = ["---", f"title: {plan.title}", f"slideforge_version: {SLIDEFORGE_VERSION}", f"theme: {theme_name}", f"slides: {len(plan.slides)}", "---", "", f"# {plan.title}", "", "## ?ndice", ""]
        for seq, title in plan_agenda(plan):
            lines.append(f"- [{seq}. {title}](#slide-{seq})")
        for slide in plan.slides:
            lines.extend(["", "---", "", f'<a id="slide-{slide.sequence}"></a>', f"## Slide {slide.sequence}: {slide.title}", "", f"<!-- layout: {slide.layout_type.value}; blocks: {', '.join(slide.source_block_ids)} -->", ""])
            if slide.subtitle:
                lines.extend([f"_{slide.subtitle}_", ""])
            for component in slide.components:
                ctype = component.get("type")
                if ctype == "comparison":
                    lines.extend(["### Antes", *[f"- {item}" for item in component.get("before", [])], "", "### Depois", *[f"- {item}" for item in component.get("after", [])], ""])
                elif ctype == "image" and component.get("path"):
                    alt = component.get("caption", "Imagem")
                    path = asset_map.get(str(Path(component["path"])), public_asset_path(component["path"]))
                    lines.extend([f"![{alt}]({path})", ""])
                elif ctype == "table":
                    lines.extend(_markdown_table(component.get("rows", [])))
                    lines.append("")
                elif ctype == "timeline":
                    lines.extend([f"1. {item}" for item in component.get("items", []) if item])
                else:
                    lines.extend(f"- {item}" for item in component.get("items", []) if item)
            note = notes[slide.sequence]
            lines.extend(["", "<details>", "<summary>Notas do apresentador</summary>", "", note.summary, "", f"Blocos: {', '.join(note.source_block_ids)}", "", "</details>"])
        if audit:
            lines.extend(["", "---", "", "## Auditoria", "", f"- Blocos n?o utilizados: {len(audit.unused_block_ids)}", f"- Imagens n?o utilizadas: {len(audit.unused_image_ids)}", f"- Overflows cr?ticos: {audit.critical_overflows}"])
        output_path.write_text("\n".join(lines), encoding="utf-8")
        return output_path


def _markdown_table(rows):
    if not rows:
        return []
    width = max(len(row) for row in rows)
    normalized = [list(row) + [""] * (width - len(row)) for row in rows]
    lines = ["| " + " | ".join(_cell(cell) for cell in normalized[0]) + " |", "| " + " | ".join("---" for _ in range(width)) + " |"]
    for row in normalized[1:]:
        lines.append("| " + " | ".join(_cell(cell) for cell in row) + " |")
    return lines


def _cell(value) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")
