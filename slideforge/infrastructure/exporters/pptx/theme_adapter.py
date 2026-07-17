from dataclasses import dataclass
from pptx.dml.color import RGBColor
from slideforge.theme import Theme


@dataclass(frozen=True)
class TextStyle:
    name: str
    font: str
    size: int
    min_size: int
    max_size: int
    bold: bool
    color: RGBColor
    alignment: str = "left"
    line_spacing: float = 1.1


class ThemeAdapter:
    def __init__(self, theme: Theme):
        self.theme = theme

    def style(self, name: str) -> TextStyle:
        t = self.theme
        styles = {
            "cover_title": TextStyle("cover_title", t.font, 32, 22, 34, True, t.primary, "center"),
            "cover_subtitle": TextStyle("cover_subtitle", t.font, 17, 12, 20, False, t.dark, "center"),
            "section_title": TextStyle("section_title", t.font, 28, 20, 32, True, t.primary),
            "slide_title": TextStyle("slide_title", t.font, 23, 18, 26, True, t.dark),
            "subtitle": TextStyle("subtitle", t.font, 15, 11, 18, False, t.dark),
            "body": TextStyle("body", t.font, 14, 10, 16, False, t.dark),
            "bullet_l1": TextStyle("bullet_l1", t.font, 13, 10, 16, False, t.dark),
            "bullet_l2": TextStyle("bullet_l2", t.font, 11, 9, 13, False, t.dark),
            "caption": TextStyle("caption", t.font, 9, 8, 11, False, t.dark, "center"),
            "kpi": TextStyle("kpi", t.font, 28, 18, 32, True, t.primary, "center"),
            "callout": TextStyle("callout", t.font, 15, 11, 18, True, t.primary),
        }
        return styles.get(name, styles["body"])
