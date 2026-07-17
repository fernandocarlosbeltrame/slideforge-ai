from pptx.util import Inches, Pt
from slideforge.infrastructure.exporters.pptx.components.base_component import BaseComponent


class TableComponent(BaseComponent):
    def render(self, slide, box, rows: list[list[str]]):
        if not rows:
            return None
        max_rows = min(len(rows), 10)
        max_cols = min(max(len(row) for row in rows), 6)
        table = slide.shapes.add_table(max_rows, max_cols, Inches(box.x), Inches(box.y), Inches(box.width), Inches(box.height)).table
        for r in range(max_rows):
            for c in range(max_cols):
                cell = table.cell(r, c)
                cell.text = rows[r][c] if c < len(rows[r]) else ""
                fill = cell.fill; fill.solid(); fill.fore_color.rgb = self.theme.primary if r == 0 else self.theme.white
                p = cell.text_frame.paragraphs[0]
                p.font.name = self.theme.font; p.font.size = Pt(8); p.font.color.rgb = self.theme.white if r == 0 else self.theme.dark
        return table
