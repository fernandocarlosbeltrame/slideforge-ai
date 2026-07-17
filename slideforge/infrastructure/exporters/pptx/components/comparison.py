from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt
from slideforge.infrastructure.exporters.pptx.components.base_component import BaseComponent


class ComparisonComponent(BaseComponent):
    def render(self, slide, left_box, right_box, before: list[str], after: list[str]):
        for box, label, items, fill in [(left_box, "ANTES", before, self.theme.comparison_before_fill), (right_box, "DEPOIS", after, self.theme.comparison_after_fill)]:
            panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(box.x), Inches(box.y), Inches(box.width), Inches(box.height))
            panel.fill.solid(); panel.fill.fore_color.rgb = fill; panel.line.color.rgb = self.theme.primary
            tf = panel.text_frame
            tf.clear(); tf.word_wrap = True; tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
            tf.margin_left = Inches(0.22); tf.margin_right = Inches(0.22)
            p = tf.paragraphs[0]
            p.text = label; p.font.name = self.theme.font; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = self.theme.primary; p.alignment = PP_ALIGN.CENTER
            for item in items:
                q = tf.add_paragraph()
                q.text = (item or "").strip().lstrip("•-*✓✗ ").strip()
                q.font.name = self.theme.font; q.font.size = Pt(10 if len(items) > 9 else 12); q.font.color.rgb = self.theme.dark; q.alignment = PP_ALIGN.LEFT
