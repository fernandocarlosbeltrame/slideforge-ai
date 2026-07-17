from dataclasses import dataclass
from slideforge.domain.entities.content_block import ContentBlock
from slideforge.domain.entities.slide_plan import SlidePlan
from slideforge.domain.enums.block_type import BlockType


@dataclass(frozen=True)
class ContentDensity:
    chars: int
    words: int
    bullets: int
    images: int
    tables: int
    level: str

    def as_dict(self) -> dict:
        return {
            "chars": self.chars,
            "words": self.words,
            "bullets": self.bullets,
            "images": self.images,
            "tables": self.tables,
            "level": self.level,
        }


class ContentDensityAnalyzer:
    def analyze_blocks(self, blocks: list[ContentBlock]) -> ContentDensity:
        texts = [block.text or "" for block in blocks if block.text]
        chars = sum(len(text) for text in texts)
        words = sum(len(text.split()) for text in texts)
        bullets = sum(1 for block in blocks if block.type == BlockType.LIST_ITEM)
        images = sum(1 for block in blocks if block.type == BlockType.IMAGE)
        tables = sum(1 for block in blocks if block.type == BlockType.TABLE)
        return ContentDensity(chars=chars, words=words, bullets=bullets, images=images, tables=tables, level=self._level(chars, bullets, images, tables))

    def analyze_slide(self, slide: SlidePlan) -> ContentDensity:
        texts: list[str] = []
        images = 0
        tables = 0
        bullets = 0
        for component in slide.components:
            ctype = component.get("type")
            if ctype == "text":
                items = component.get("items", [])
                texts.extend(items)
                bullets += len(items)
            elif ctype == "comparison":
                before = component.get("before", [])
                after = component.get("after", [])
                texts.extend(before + after)
                bullets += len(before) + len(after)
            elif ctype == "image":
                images += 1
                if component.get("caption"):
                    texts.append(component["caption"])
            elif ctype == "table":
                tables += 1
                for row in component.get("rows", []):
                    texts.extend(str(cell) for cell in row)
        chars = sum(len(text or "") for text in texts)
        words = sum(len((text or "").split()) for text in texts)
        return ContentDensity(chars=chars, words=words, bullets=bullets, images=images, tables=tables, level=self._level(chars, bullets, images, tables))

    @staticmethod
    def _level(chars: int, bullets: int, images: int, tables: int) -> str:
        if tables or images:
            chars_limit = 750
        else:
            chars_limit = 900
        if chars <= 350 and bullets <= 3:
            return "low"
        if chars <= chars_limit and bullets <= 8:
            return "medium"
        if chars <= 1500 and bullets <= 14:
            return "high"
        return "critical"
