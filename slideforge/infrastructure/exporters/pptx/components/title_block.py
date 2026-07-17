from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt
from slideforge.application.services.typography_fitter import TypographyFitter
from slideforge.infrastructure.exporters.pptx.components.base_component import BaseComponent


class TitleBlock(BaseComponent):
    def __init__(self, theme_adapter):
        super().__init__(theme_adapter)
        self.text_fit = TypographyFitter()

    def render(self, slide, box, title: str, style_name: str = "slide_title"):
        style = self.theme_adapter.style(style_name)
        fit = self.text_fit.fit(title, box.width, box.height, style.size, style.min_size, 3)
        tb = slide.shapes.add_textbox(Inches(box.x), Inches(box.y), Inches(box.width), Inches(box.height))
        tf = tb.text_frame
        tf.clear(); tf.word_wrap = True; tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = style.font
        p.font.size = Pt(fit.font_size)
        p.font.bold = style.bold
        p.font.color.rgb = style.color
        p.alignment = PP_ALIGN.CENTER if style.alignment == "center" else PP_ALIGN.LEFT
        return tb
