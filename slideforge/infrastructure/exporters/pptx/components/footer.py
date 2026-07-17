from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt
from slideforge.infrastructure.exporters.pptx.components.base_component import BaseComponent


class Footer(BaseComponent):
    def render(self, slide, box, deck_title: str, number: int):
        footer = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(box.x), Inches(box.y), Inches(box.width), Inches(box.height))
        footer.fill.solid(); footer.fill.fore_color.rgb = self.theme.footer_background; footer.line.fill.background()
        tb = slide.shapes.add_textbox(Inches(box.x + 0.55), Inches(box.y + 0.08), Inches(box.width - 1.1), Inches(0.18))
        p = tb.text_frame.paragraphs[0]
        p.text = f"{deck_title} | {number}"
        p.font.name = self.theme.font; p.font.size = Pt(8); p.font.color.rgb = self.theme.white
        p.alignment = PP_ALIGN.RIGHT
