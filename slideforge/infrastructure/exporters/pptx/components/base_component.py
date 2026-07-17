from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt
from slideforge.domain.value_objects.bounding_box import BoundingBox


ALIGNMENT = {
    "left": PP_ALIGN.LEFT,
    "center": PP_ALIGN.CENTER,
    "right": PP_ALIGN.RIGHT,
}


class BaseComponent:
    def __init__(self, theme_adapter):
        self.theme_adapter = theme_adapter
        self.theme = theme_adapter.theme

    def text_box(self, slide, box: BoundingBox, text: str, style_name: str, *, margin: float = 0.04, bullet: bool = False):
        style = self.theme_adapter.style(style_name)
        tb = slide.shapes.add_textbox(Inches(box.x), Inches(box.y), Inches(box.width), Inches(box.height))
        tf = tb.text_frame
        tf.clear()
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
        tf.margin_left = Inches(margin)
        tf.margin_right = Inches(margin)
        tf.margin_top = Inches(margin)
        tf.margin_bottom = Inches(margin)
        p = tf.paragraphs[0]
        p.text = text
        p.font.name = style.font
        p.font.size = Pt(style.size)
        p.font.bold = style.bold
        p.font.color.rgb = style.color
        p.alignment = ALIGNMENT.get(style.alignment, PP_ALIGN.LEFT)
        p.level = 0 if bullet else None
        return tb

    def paragraph(self, tf, text: str, style_name: str, *, level: int = 0, first: bool = False):
        style = self.theme_adapter.style(style_name)
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        p.text = text
        p.level = level
        p.font.name = style.font
        p.font.size = Pt(style.size)
        p.font.bold = style.bold
        p.font.color.rgb = style.color
        p.space_after = Pt(4)
        p.alignment = ALIGNMENT.get(style.alignment, PP_ALIGN.LEFT)
        return p
