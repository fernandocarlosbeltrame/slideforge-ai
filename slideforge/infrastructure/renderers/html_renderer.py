from __future__ import annotations

import base64
from html import escape
from mimetypes import guess_type
from pathlib import Path

from slideforge.application.publishing.speaker_notes import SpeakerNotesGenerator
from slideforge.domain.entities.content_audit import ContentAudit
from slideforge.domain.entities.presentation_plan import PresentationPlan
from slideforge.infrastructure.assets import AssetManager
from slideforge.infrastructure.renderers.serialization import plan_agenda
from slideforge.version import SLIDEFORGE_VERSION


class HtmlRenderer:
    format_name = "html"
    extension = ".html"

    def render(self, plan: PresentationPlan, output_path: Path, *, audit: ContentAudit | None = None, assets: AssetManager | None = None, theme=None) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        base_theme = theme.base if hasattr(theme, "base") else None
        primary = _rgb(base_theme.primary) if base_theme else "#004a8f"
        secondary = _rgb(base_theme.secondary) if base_theme else "#009fda"
        dark = _rgb(base_theme.dark) if base_theme else "#1f2d3d"
        light = _rgb(base_theme.light) if base_theme else "#f4f8fc"
        banner = _data_uri(assets.locate("banner")) if assets and assets.locate("banner") else None
        notes = {n.slide_sequence: n for n in SpeakerNotesGenerator().generate(plan)}
        agenda = "".join(f'<li><a href="#slide-{seq}">{seq}. {escape(title)}</a></li>' for seq, title in plan_agenda(plan))
        slides = []
        for slide in plan.slides:
            comps = []
            for component in slide.components:
                ctype = component.get("type")
                if ctype == "comparison":
                    comps.append('<div class="comparison"><section><h3>Antes</h3>' + _list(component.get("before", [])) + '</section><section><h3>Depois</h3>' + _list(component.get("after", [])) + '</section></div>')
                elif ctype == "image" and component.get("path"):
                    img = _data_uri(Path(component["path"])) or escape(Path(component["path"]).as_posix())
                    caption = escape(component.get("caption", "Imagem"))
                    comps.append(f'<figure><img src="{img}" alt="{caption}"><figcaption>{caption}</figcaption></figure>')
                elif ctype == "table":
                    comps.append(_table(component.get("rows", [])))
                elif ctype == "timeline":
                    comps.append('<div class="timeline">' + ''.join(f'<div class="event"><strong>{escape(str(item))}</strong></div>' for item in component.get("items", [])) + '</div>')
                else:
                    comps.append(_list(component.get("items", [])))
            note = notes[slide.sequence]
            slides.append(
                f'<article id="slide-{slide.sequence}" class="slide" tabindex="-1" data-slide="{slide.sequence}">'
                f'<header class="slide-header"><span>Slide {slide.sequence:02d}</span><a href="#top">Agenda</a></header>'
                f'<h2>{escape(slide.title)}</h2>{"".join(comps)}'
                f'<details class="notes"><summary>Notas do apresentador</summary><p>{escape(note.summary)}</p><small>Blocos: {escape(", ".join(note.source_block_ids))}</small></details>'
                f'</article>'
            )
        audit_html = ""
        if audit:
            audit_html = f'<section class="audit"><h2>Auditoria</h2><p>Blocos não utilizados: {len(audit.unused_block_ids)} | Imagens não utilizadas: {len(audit.unused_image_ids)} | Overflows críticos: {audit.critical_overflows}</p></section>'
        banner_html = f'<img src="{banner}" alt="Banner corporativo" class="banner">' if banner else ''
        html = f'''<!doctype html><html lang="pt-br"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(plan.title)}</title>
<style>
:root{{--primary:{primary};--secondary:{secondary};--dark:{dark};--light:{light};--paper:#fff;--line:#d9e2ef}}
*{{box-sizing:border-box}}body{{font-family:Aptos,Arial,sans-serif;background:var(--light);color:var(--dark);margin:0;line-height:1.45}}a{{color:var(--primary)}}:focus-visible{{outline:3px solid var(--secondary);outline-offset:3px}}
.app{{display:grid;grid-template-columns:290px 1fr;min-height:100vh}}.sidebar{{position:sticky;top:0;height:100vh;overflow:auto;background:#0f2742;color:white;padding:24px}}.sidebar a{{color:white;text-decoration:none}}.sidebar ol{{padding-left:20px}}.sidebar li{{margin:8px 0}}.brand{{font-size:12px;text-transform:uppercase;letter-spacing:.12em;color:#9fc8f4}}.toolbar{{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}}button{{border:0;border-radius:8px;padding:10px 14px;background:var(--primary);color:white;cursor:pointer}}
main{{padding:28px;max-width:1280px}}.cover,.slide,.audit{{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:32px;margin:0 0 26px;box-shadow:0 12px 28px rgba(15,39,66,.08)}}.cover{{min-height:58vh;display:flex;flex-direction:column;justify-content:center}}.banner{{width:100%;max-height:130px;object-fit:contain;margin-bottom:32px}}
h1{{font-size:clamp(2rem,5vw,4rem);color:var(--primary);margin:.1em 0}}h2{{font-size:clamp(1.5rem,3vw,2.3rem);color:var(--primary);margin:.15em 0 .7em}}h3{{color:var(--primary)}}.slide-header{{display:flex;justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:10px;margin-bottom:18px;color:#62748a;font-size:13px}}
ul{{padding-left:1.25rem}}li{{margin:.38rem 0}}.comparison{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}.comparison section,.card{{border:1px solid var(--line);border-radius:14px;padding:18px;background:#fbfdff}}.timeline{{display:grid;gap:12px;border-left:4px solid var(--secondary);padding-left:18px}}.event{{padding:12px 14px;background:#f7fbff;border:1px solid var(--line);border-radius:12px}}figure{{margin:16px 0}}img{{max-width:100%;height:auto;border-radius:10px}}figcaption{{font-size:13px;color:#62748a;margin-top:6px}}.table-wrap{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font-size:14px}}th,td{{border:1px solid var(--line);padding:9px;vertical-align:top}}th{{background:var(--primary);color:white}}.notes{{margin-top:18px;padding:12px;background:#f4f8fc;border-radius:10px}}
.presentation-mode .slide{{min-height:calc(100vh - 56px);display:flex;flex-direction:column;justify-content:center}}.presentation-mode .sidebar{{display:none}}.presentation-mode .app{{display:block}}.presentation-mode main{{max-width:1200px;margin:auto}}
@media (max-width:900px){{.app{{display:block}}.sidebar{{position:relative;height:auto}}main{{padding:16px}}.comparison{{grid-template-columns:1fr}}}}
@media print{{.sidebar,.toolbar,.slide-header a{{display:none}}.app{{display:block}}main{{padding:0}}.slide,.cover,.audit{{break-inside:avoid;box-shadow:none}}}}
</style></head><body id="top"><div class="app"><aside class="sidebar"><div class="brand">SlideForge {SLIDEFORGE_VERSION}</div><h2>{escape(plan.title)}</h2><div class="toolbar"><button onclick="window.print()">Imprimir</button><button onclick="toggleMode()">Modo apresentação</button><button onclick="document.documentElement.requestFullscreen?.()">Tela cheia</button></div><nav aria-label="Índice"><ol>{agenda}</ol></nav></aside><main><section class="cover">{banner_html}<p class="brand">Publicação executiva</p><h1>{escape(plan.title)}</h1><p>{len(plan.slides)} slides publicados a partir do mesmo plano de apresentação.</p></section>{''.join(slides)}{audit_html}</main></div><script>
function toggleMode(){{document.body.classList.toggle('presentation-mode')}}
const slides=[...document.querySelectorAll('.slide')];let idx=0;function focusSlide(i){{idx=Math.max(0,Math.min(slides.length-1,i));slides[idx].focus();slides[idx].scrollIntoView({{behavior:'smooth',block:'start'}})}}
document.addEventListener('keydown',e=>{{if(e.key==='ArrowRight'||e.key==='PageDown')focusSlide(idx+1);if(e.key==='ArrowLeft'||e.key==='PageUp')focusSlide(idx-1);}});
</script></body></html>'''
        output_path.write_text(html, encoding="utf-8")
        return output_path


def _rgb(color) -> str:
    return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"


def _data_uri(path: Path | None) -> str | None:
    if not path or not Path(path).exists():
        return None
    mime = guess_type(str(path))[0] or "image/png"
    data = base64.b64encode(Path(path).read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def _list(items) -> str:
    return '<ul>' + ''.join(f'<li>{escape(str(item))}</li>' for item in items if item) + '</ul>' if items else ''


def _table(rows) -> str:
    if not rows:
        return ''
    head = ''.join(f'<th>{escape(str(cell))}</th>' for cell in rows[0])
    body = ''.join('<tr>' + ''.join(f'<td>{escape(str(cell))}</td>' for cell in row) + '</tr>' for row in rows[1:])
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'
