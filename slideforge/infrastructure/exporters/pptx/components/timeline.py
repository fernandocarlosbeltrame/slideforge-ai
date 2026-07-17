from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt
from slideforge.infrastructure.exporters.pptx.components.base_component import BaseComponent


class TimelineComponent(BaseComponent):
    def render(self, slide, box, items: list[str]):
        items = items[:6]
        count = max(1, len(items))
        x0 = box.x + 0.45
        width = box.width - 0.9
        y = box.y + box.height * 0.48
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x0), Inches(y), Inches(width), Inches(0.055))
        line.fill.solid(); line.fill.fore_color.rgb = self.theme.secondary; line.line.fill.background()
        step = width / max(1, count - 1)
        for i, item in enumerate(items):
            x = min(x0 + i * step, x0 + width - 0.12)
            dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x - 0.12), Inches(y - 0.12), Inches(0.24), Inches(0.24))
            dot.fill.solid(); dot.fill.fore_color.rgb = self.theme.primary; dot.line.fill.background()
            tb_x = max(box.x, min(x - 0.75, box.x + box.width - 1.5))
            tb_y = box.y + 0.35 if i % 2 == 0 else y + 0.35
            tb = slide.shapes.add_textbox(Inches(tb_x), Inches(tb_y), Inches(1.7), Inches(1.15))
            tf = tb.text_frame; tf.word_wrap = True; tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
            p = tf.paragraphs[0]
            p.text = item
            p.font.name = self.theme.font; p.font.size = Pt(9); p.font.color.rgb = self.theme.dark; p.alignment = PP_ALIGN.CENTER
