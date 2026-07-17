from html import escape
from pathlib import Path
from slideforge.domain.entities.content_audit import ContentAudit
from slideforge.domain.entities.presentation_plan import PresentationPlan


class HTMLPreviewGenerator:
    def generate(self, plan: PresentationPlan, audit: ContentAudit, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        rows = []
        for slide in plan.slides:
            decision = slide.metadata.get("layout_decision", {})
            density = slide.metadata.get("density", {})
            rows.append(
                "<tr>"
                f"<td>{slide.sequence}</td>"
                f"<td>{escape(slide.title)}</td>"
                f"<td>{escape(slide.layout_type.value)}</td>"
                f"<td>{escape(decision.get('visual_composition', '-'))}</td>"
                f"<td>{escape(density.get('level', '-'))}</td>"
                f"<td>{len(slide.source_block_ids)}</td>"
                f"<td>{escape(decision.get('reason', '-'))}</td>"
                "</tr>"
            )
        html = f"""<!doctype html>
<html lang=\"pt-br\">
<head>
<meta charset=\"utf-8\">
<title>SlideForge Preview - {escape(plan.title)}</title>
<style>
body {{ font-family: Aptos, Arial, sans-serif; background:#f4f7fb; color:#172033; margin:32px; }}
header {{ background:white; border:1px solid #d9e2ef; border-radius:12px; padding:22px 26px; margin-bottom:18px; }}
h1 {{ margin:0 0 8px; color:#004a8f; }}
.grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:18px 0; }}
.card {{ background:white; border:1px solid #d9e2ef; border-radius:10px; padding:16px; }}
.card strong {{ display:block; font-size:24px; color:#004a8f; }}
table {{ width:100%; border-collapse:collapse; background:white; border-radius:12px; overflow:hidden; }}
th,td {{ padding:10px 12px; border-bottom:1px solid #e7edf5; text-align:left; vertical-align:top; }}
th {{ background:#004a8f; color:white; }}
</style>
</head>
<body>
<header>
<h1>{escape(plan.title)}</h1>
<p>Preview estrutural gerado automaticamente. Use este arquivo para revisar layouts, densidade e rastreabilidade antes de abrir o PPTX.</p>
</header>
<section class=\"grid\">
<div class=\"card\"><span>Slides</span><strong>{audit.slide_count}</strong></div>
<div class=\"card\"><span>Layouts usados</span><strong>{len(audit.layout_counts)}</strong></div>
<div class=\"card\"><span>Blocos usados</span><strong>{len(audit.used_block_ids)}</strong></div>
<div class=\"card\"><span>Alertas</span><strong>{len(audit.warnings)}</strong></div>
</section>
<table>
<thead><tr><th>#</th><th>Título</th><th>Layout</th><th>Composição</th><th>Densidade</th><th>Blocos</th><th>Motivo</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
</body>
</html>"""
        output_path.write_text(html, encoding="utf-8")
        return output_path
