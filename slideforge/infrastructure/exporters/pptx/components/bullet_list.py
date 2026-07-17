from pptx.enum.text import MSO_AUTO_SIZE
from pptx.util import Inches, Pt
from slideforge.infrastructure.exporters.pptx.components.base_component import BaseComponent


class BulletList(BaseComponent):
    def render(self, shape, items: list[str], font_size: int | None = None):
        tf = shape.text_frame
        tf.clear(); tf.word_wrap = True; tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
        tf.margin_left = Inches(0.38); tf.margin_right = Inches(0.32); tf.margin_top = Inches(0.24); tf.margin_bottom = Inches(0.18)
        size = font_size or self._font_size(items)
        first = True
        for item in items:
            clean = self.clean(item)
            if not clean:
                continue
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.text = clean
            p.level = 0
            p.font.name = self.theme.font; p.font.size = Pt(size); p.font.color.rgb = self.theme.dark
            p.space_after = Pt(5)

    @staticmethod
    def clean(text: str) -> str:
        return (text or "").strip().lstrip("•-*✓✗ ").strip()

    @staticmethod
    def _font_size(items: list[str]) -> int:
        total = sum(len(item or "") for item in items)
        if len(items) <= 4 and total < 420:
            return 16
        if len(items) <= 7 and total < 760:
            return 13
        return 10
