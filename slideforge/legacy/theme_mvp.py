from dataclasses import dataclass
from pptx.dml.color import RGBColor

@dataclass
class Theme:
    primary: RGBColor = RGBColor(15, 70, 140)
    secondary: RGBColor = RGBColor(33, 150, 243)
    dark: RGBColor = RGBColor(45, 55, 72)
    light: RGBColor = RGBColor(242, 247, 252)
    white: RGBColor = RGBColor(255, 255, 255)
    accent: RGBColor = RGBColor(0, 151, 167)
    font: str = 'Aptos'
