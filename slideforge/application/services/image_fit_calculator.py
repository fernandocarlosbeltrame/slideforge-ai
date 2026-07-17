from dataclasses import dataclass
from slideforge.domain.value_objects.bounding_box import BoundingBox


@dataclass(frozen=True)
class ImageFit:
    x: float
    y: float
    width: float
    height: float
    mode: str
    resized: bool = True


class ImageFitCalculator:
    def calculate(self, image_width: float, image_height: float, box: BoundingBox, mode: str = "contain", padding: float = 0.0) -> ImageFit:
        safe = box.inset(max(0.0, padding))
        if image_width <= 0 or image_height <= 0 or safe.width <= 0 or safe.height <= 0:
            return ImageFit(safe.x, safe.y, max(0.01, safe.width), max(0.01, safe.height), mode)
        ratio = image_width / image_height
        box_ratio = safe.width / safe.height
        if mode == "fit_width":
            width = safe.width
            height = width / ratio
        elif mode == "fit_height":
            height = safe.height
            width = height * ratio
        elif mode == "original":
            width = min(image_width / 96.0, safe.width)
            height = width / ratio
            if height > safe.height:
                height = safe.height
                width = height * ratio
        elif mode == "cover":
            if ratio > box_ratio:
                height = safe.height
                width = height * ratio
            else:
                width = safe.width
                height = width / ratio
        else:
            if ratio > box_ratio:
                width = safe.width
                height = width / ratio
            else:
                height = safe.height
                width = height * ratio
        width = max(0.01, min(width, safe.width if mode != "cover" else width))
        height = max(0.01, min(height, safe.height if mode != "cover" else height))
        x = safe.x + (safe.width - width) / 2
        y = safe.y + (safe.height - height) / 2
        return ImageFit(x, y, width, height, mode, resized=(width != image_width or height != image_height))
