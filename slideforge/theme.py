from dataclasses import dataclass, field
from pptx.dml.color import RGBColor


@dataclass
class Theme:
    name: str = "corporate_blue"
    primary: RGBColor = RGBColor(15, 70, 140)
    secondary: RGBColor = RGBColor(33, 150, 243)
    dark: RGBColor = RGBColor(45, 55, 72)
    light: RGBColor = RGBColor(242, 247, 252)
    white: RGBColor = RGBColor(255, 255, 255)
    accent: RGBColor = RGBColor(0, 151, 167)
    danger: RGBColor = RGBColor(205, 64, 64)
    success: RGBColor = RGBColor(32, 136, 88)
    font: str = "Aptos"
    title_font_size: int = 24
    body_font_size: int = 15
    min_body_font_size: int = 10
    header_background: RGBColor = RGBColor(255, 255, 255)
    header_border: RGBColor = RGBColor(210, 220, 232)
    footer_background: RGBColor = RGBColor(15, 70, 140)
    card_fill: RGBColor = RGBColor(255, 255, 255)
    comparison_before_fill: RGBColor = RGBColor(252, 238, 238)
    comparison_after_fill: RGBColor = RGBColor(235, 248, 241)
    metadata: dict = field(default_factory=dict)


def get_theme(name: str | None = None) -> Theme:
    return Theme()
