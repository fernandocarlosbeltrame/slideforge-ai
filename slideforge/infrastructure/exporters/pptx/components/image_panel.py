from pathlib import Path
from PIL import Image
from pptx.util import Inches
from slideforge.application.services.image_fit_calculator import ImageFitCalculator
from slideforge.infrastructure.exporters.pptx.components.base_component import BaseComponent


class ImagePanel(BaseComponent):
    def __init__(self, theme_adapter):
        super().__init__(theme_adapter)
        self.image_fit = ImageFitCalculator()

    def render(self, slide, path: str, box, fit_mode: str = "contain") -> bool:
        if not path or not Path(path).exists():
            return False
        try:
            with Image.open(path) as img:
                fit = self.image_fit.calculate(img.width, img.height, box, fit_mode, padding=0.1)
            slide.shapes.add_picture(path, Inches(fit.x), Inches(fit.y), width=Inches(fit.width), height=Inches(fit.height))
            return True
        except Exception:
            return False
