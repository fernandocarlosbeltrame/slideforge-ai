from dataclasses import dataclass
from slideforge.domain.value_objects.bounding_box import BoundingBox


@dataclass(frozen=True)
class GridGap:
    horizontal: float = 0.28
    vertical: float = 0.28


@dataclass(frozen=True)
class GridColumn:
    box: BoundingBox
    index: int


@dataclass(frozen=True)
class GridRow:
    box: BoundingBox
    index: int


class SlideGrid:
    def __init__(self, box: BoundingBox, gap: GridGap | None = None):
        self.box = box
        self.gap = gap or GridGap()

    def columns(self, count: int) -> list[GridColumn]:
        count = max(1, count)
        width = (self.box.width - self.gap.horizontal * (count - 1)) / count
        return [GridColumn(BoundingBox(self.box.x + i * (width + self.gap.horizontal), self.box.y, width, self.box.height), i) for i in range(count)]

    def rows(self, count: int) -> list[GridRow]:
        count = max(1, count)
        height = (self.box.height - self.gap.vertical * (count - 1)) / count
        return [GridRow(BoundingBox(self.box.x, self.box.y + i * (height + self.gap.vertical), self.box.width, height), i) for i in range(count)]

    def split_ratio(self, left_ratio: float) -> tuple[BoundingBox, BoundingBox]:
        left_ratio = min(0.8, max(0.2, left_ratio))
        left_w = (self.box.width - self.gap.horizontal) * left_ratio
        right_w = self.box.width - self.gap.horizontal - left_w
        return (
            BoundingBox(self.box.x, self.box.y, left_w, self.box.height),
            BoundingBox(self.box.x + left_w + self.gap.horizontal, self.box.y, right_w, self.box.height),
        )

    def band_top(self, height: float) -> BoundingBox:
        return BoundingBox(self.box.x, self.box.y, self.box.width, min(height, self.box.height))

    def band_bottom(self, height: float) -> BoundingBox:
        h = min(height, self.box.height)
        return BoundingBox(self.box.x, self.box.bottom - h, self.box.width, h)

    def main_with_sidebar(self, sidebar_ratio: float = 0.32, sidebar_on_right: bool = True) -> tuple[BoundingBox, BoundingBox]:
        main, side = self.split_ratio(1 - sidebar_ratio)
        return (main, side) if sidebar_on_right else (side, main)
