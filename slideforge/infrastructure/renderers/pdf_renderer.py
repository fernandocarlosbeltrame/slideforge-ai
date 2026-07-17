from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image as RLImage, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, KeepTogether

from slideforge.application.publishing.speaker_notes import SpeakerNotesGenerator
from slideforge.domain.entities.content_audit import ContentAudit
from slideforge.domain.entities.presentation_plan import PresentationPlan
from slideforge.infrastructure.assets import AssetManager
from slideforge.infrastructure.renderers.serialization import plan_agenda
from slideforge.version import SLIDEFORGE_VERSION

PAGE_16_9 = (13.333 * inch, 7.5 * inch)


class PdfRenderer:
    format_name = "pdf"
    extension = ".pdf"

    def render(self, plan: PresentationPlan, output_path: Path, *, audit: ContentAudit | None = None, assets: AssetManager | None = None, theme=None) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        base_theme = theme.base if hasattr(theme, "base") else None
        primary = _color(base_theme.primary) if base_theme else colors.HexColor("#004a8f")
        secondary = _color(base_theme.secondary) if base_theme else colors.HexColor("#009fda")
        dark = _color(base_theme.dark) if base_theme else colors.HexColor("#2d3748")
        light = _color(base_theme.light) if base_theme else colors.HexColor("#f4f8fc")
        banner = assets.locate("banner") if assets else None
        doc = SimpleDocTemplate(str(output_path), pagesize=PAGE_16_9, rightMargin=0.5 * inch, leftMargin=0.5 * inch, topMargin=0.65 * inch, bottomMargin=0.55 * inch)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle("DeckTitle", parent=styles["Title"], textColor=primary, fontSize=28, leading=33, spaceAfter=14))
        styles.add(ParagraphStyle("SlideTitle", parent=styles["Heading1"], textColor=primary, fontSize=20, leading=24, spaceAfter=12))
        styles.add(ParagraphStyle("BodyExec", parent=styles["BodyText"], textColor=dark, fontSize=10.5, leading=13.5, spaceAfter=5))
        styles.add(ParagraphStyle("SmallExec", parent=styles["BodyText"], textColor=colors.HexColor("#62748a"), fontSize=8.5, leading=10.5))
        story = []
        if banner and Path(banner).exists():
            story.append(RLImage(str(banner), width=6.6 * inch, height=0.95 * inch, kind="proportional"))
            story.append(Spacer(1, 0.2 * inch))
        story.extend([Paragraph(plan.title, styles["DeckTitle"]), Paragraph("Publicação executiva gerada pelo SlideForge", styles["BodyExec"]), Spacer(1, 0.4 * inch), Paragraph(f"Versão {SLIDEFORGE_VERSION} | {len(plan.slides)} slides", styles["SmallExec"]), PageBreak()])
        story.append(Paragraph("Agenda", styles["SlideTitle"]))
        agenda_rows = [[Paragraph(str(seq), styles["BodyExec"]), Paragraph(title, styles["BodyExec"])] for seq, title in plan_agenda(plan)]
        agenda = Table(agenda_rows, colWidths=[0.45 * inch, 10.8 * inch], repeatRows=0)
        agenda.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#d9e2ef")), ("TEXTCOLOR", (0, 0), (0, -1), secondary)]))
        story.extend([agenda, PageBreak()])
        notes = {n.slide_sequence: n for n in SpeakerNotesGenerator().generate(plan)}
        for slide in plan.slides:
            flow = [Paragraph(f"{slide.sequence:02d}. {slide.title}", styles["SlideTitle"])]
            for component in slide.components:
                flow.extend(_component_flow(component, styles, primary, secondary, light))
            note = notes[slide.sequence]
            flow.append(Spacer(1, 0.08 * inch))
            flow.append(Paragraph(f"Notas: {note.summary}", styles["SmallExec"]))
            story.extend(flow)
            story.append(PageBreak())
        if audit:
            story.extend([Paragraph("Auditoria", styles["SlideTitle"]), Paragraph(audit.as_report().replace("\n", "<br/>"), styles["BodyExec"])])
        doc.build(story, onFirstPage=_page_decorator(plan.title, primary, banner), onLaterPages=_page_decorator(plan.title, primary, banner))
        return output_path


def _component_flow(component: dict, styles, primary, secondary, light) -> list:
    ctype = component.get("type")
    if ctype == "comparison":
        rows = [[Paragraph("Antes", styles["BodyExec"]), Paragraph("Depois", styles["BodyExec"])], [Paragraph(_breaks(component.get("before", [])), styles["BodyExec"]), Paragraph(_breaks(component.get("after", [])), styles["BodyExec"])]]
        table = Table(rows, colWidths=[5.55 * inch, 5.55 * inch], splitByRow=True)
        table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#c9d7e8")), ("BACKGROUND", (0, 0), (-1, 0), light), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10)]))
        return [table, Spacer(1, 0.12 * inch)]
    if ctype == "image" and component.get("path") and Path(component["path"]).exists():
        flow = [RLImage(component["path"], width=7.2 * inch, height=3.45 * inch, kind="proportional")]
        if component.get("caption"):
            flow.append(Paragraph(component["caption"], styles["SmallExec"]))
        return flow + [Spacer(1, 0.1 * inch)]
    if ctype == "table":
        rows = component.get("rows", [])
        if not rows:
            return []
        clean = [[Paragraph(str(cell), styles["SmallExec"] if r else styles["BodyExec"]) for cell in row] for r, row in enumerate(rows)]
        width = max(len(row) for row in rows)
        table = Table(clean, colWidths=[11.1 * inch / max(width, 1)] * width, repeatRows=1, splitByRow=True)
        table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#ccd6e2")), ("BACKGROUND", (0, 0), (-1, 0), primary), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        return [table, Spacer(1, 0.1 * inch)]
    items = component.get("items", [])
    if ctype == "timeline":
        rows = [[Paragraph(str(item), styles["BodyExec"])] for item in items if item]
        table = Table(rows, colWidths=[11.1 * inch], splitByRow=True)
        table.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.4, secondary), ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#d9e2ef")), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fbfdff"))]))
        return [table, Spacer(1, 0.1 * inch)]
    if len(items) <= 4 and items:
        rows = []
        for i in range(0, len(items), 2):
            rows.append([Paragraph(str(item), styles["BodyExec"]) for item in items[i:i + 2]])
            if len(rows[-1]) == 1:
                rows[-1].append("")
        table = Table(rows, colWidths=[5.45 * inch, 5.45 * inch], splitByRow=True)
        table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#d9e2ef")), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fbfdff")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10)]))
        return [table, Spacer(1, 0.1 * inch)]
    return [Paragraph(f"• {item}", styles["BodyExec"]) for item in items if item]


def _page_decorator(title: str, primary, banner: Path | None):
    def draw(canvas, doc):
        canvas.saveState()
        width, height = PAGE_16_9
        canvas.setFillColor(primary)
        canvas.rect(0, 0, width, 0.18 * inch, fill=1, stroke=0)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#62748a"))
        canvas.drawString(0.5 * inch, 0.28 * inch, title[:90])
        canvas.drawRightString(width - 0.5 * inch, 0.28 * inch, f"{doc.page}")
        canvas.restoreState()
    return draw


def _breaks(items: list) -> str:
    return "<br/>".join(f"• {item}" for item in items if item)


def _color(rgb) -> colors.Color:
    return colors.Color(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
