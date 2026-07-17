from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt
from slideforge.infrastructure.exporters.pptx.components.base_component import BaseComponent


class CardGrid(BaseComponent):
    def render(self, slide, boxes, items: list[str]):
        for box, item in zip(boxes, items):
            card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(box.x), Inches(box.y), Inches(box.width), Inches(box.height))
            card.fill.solid(); card.fill.fore_color.rgb = self.theme.card_fill; card.line.color.rgb = self.theme.secondary
            tf = card.text_frame
            tf.clear(); tf.word_wrap = True; tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
            tf.margin_left = Inches(0.22); tf.margin_right = Inches(0.22); tf.margin_top = Inches(0.14)
            p = tf.paragraphs[0]
            p.text = (item or "").strip().lstrip("•-*✓✗ ").strip()
            p.font.name = self.theme.font; p.font.size = Pt(13); p.font.color.rgb = self.theme.dark
            p.alignment = PP_ALIGN.LEFT
