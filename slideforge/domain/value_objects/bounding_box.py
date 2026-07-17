from dataclasses import dataclass


@dataclass(frozen=True)
class BoundingBox:
    x: float
    y: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    def inset(self, margin: float) -> "BoundingBox":
        return BoundingBox(self.x + margin, self.y + margin, max(0.0, self.width - margin * 2), max(0.0, self.height - margin * 2))

    def validate(self, slide_width: float, slide_height: float) -> list[str]:
        errors: list[str] = []
        if self.width <= 0 or self.height <= 0:
            errors.append("Elemento com largura ou altura inválida.")
        if self.x < 0 or self.y < 0:
            errors.append("Elemento com coordenada negativa.")
        if self.right > slide_width:
            errors.append("Elemento ultrapassa a largura do slide.")
        if self.bottom > slide_height:
            errors.append("Elemento ultrapassa a altura do slide.")
        return errors
