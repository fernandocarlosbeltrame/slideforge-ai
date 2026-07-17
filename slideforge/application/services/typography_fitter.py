import math
from dataclasses import dataclass


@dataclass(frozen=True)
class TextFitResult:
    font_size: int
    lines: int
    adjusted: bool
    wrapped: bool


class TypographyFitter:
    def fit(self, text: str, width_inches: float, height_inches: float, max_size: int, min_size: int, max_lines: int) -> TextFitResult:
        text = text or ""
        usable_chars_per_line_at_12 = max(12, int(width_inches * 13))
        for size in range(max_size, min_size - 1, -1):
            chars_per_line = max(8, int(usable_chars_per_line_at_12 * 12 / size))
            lines = max(1, math.ceil(len(text) / chars_per_line))
            line_height = size / 72 * 1.25
            if lines <= max_lines and lines * line_height <= height_inches:
                return TextFitResult(size, lines, adjusted=size < max_size, wrapped=lines > 1)
        chars_per_line = max(8, int(usable_chars_per_line_at_12 * 12 / min_size))
        return TextFitResult(min_size, max(1, math.ceil(len(text) / chars_per_line)), True, True)
