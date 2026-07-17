from dataclasses import dataclass
from slideforge.domain.value_objects.bounding_box import BoundingBox


@dataclass(frozen=True)
class SlideGeometry:
    slide_width: float = 13.333
    slide_height: float = 7.5
    margin_left: float = 0.62
    margin_right: float = 0.62
    margin_top: float = 0.25
    margin_bottom: float = 0.28
    header_height: float = 0.78
    footer_height: float = 0.34
    title_top: float = 0.92
    title_height: float = 0.62

    @property
    def content_top(self) -> float:
        return 1.62

    @property
    def content_bottom(self) -> float:
        return self.slide_height - self.footer_height - 0.28

    @property
    def content_height(self) -> float:
        return self.content_bottom - self.content_top

    @property
    def content_width(self) -> float:
        return self.slide_width - self.margin_left - self.margin_right

    @property
    def safe_content_box(self) -> BoundingBox:
        return BoundingBox(self.margin_left, self.content_top, self.content_width, self.content_height)

    @property
    def title_box(self) -> BoundingBox:
        return BoundingBox(self.margin_left, self.title_top, self.content_width, self.title_height)

    @property
    def header_box(self) -> BoundingBox:
        return BoundingBox(0.0, 0.0, self.slide_width, self.header_height)

    @property
    def footer_box(self) -> BoundingBox:
        return BoundingBox(0.0, self.slide_height - self.footer_height, self.slide_width, self.footer_height)
