from dataclasses import dataclass
import re

from slideforge.domain.entities.content_block import ContentBlock
from slideforge.domain.enums.block_type import BlockType


@dataclass(frozen=True)
class SummaryEligibility:
    eligible: bool
    reason: str
    char_count: int
    word_count: int


class SummarizationEligibilityPolicy:
    def __init__(self, min_chars: int = 700, min_words: int = 100):
        self.min_chars = min_chars
        self.min_words = min_words
        self._blocked_types = {BlockType.TITLE, BlockType.SUBTITLE, BlockType.TABLE, BlockType.IMAGE}

    def evaluate_block(self, block: ContentBlock) -> SummaryEligibility:
        text = (block.text or "").strip()
        char_count = len(text)
        word_count = len(re.findall(r"\w+", text, flags=re.UNICODE))
        if block.type in self._blocked_types:
            return SummaryEligibility(False, f"Tipo de bloco não resumível: {block.type.value}", char_count, word_count)
        if self._looks_like_isolated_number_or_date(text):
            return SummaryEligibility(False, "Conteúdo numérico ou data isolada", char_count, word_count)
        if block.type in {BlockType.LIST, BlockType.LIST_ITEM} and word_count < self.min_words:
            return SummaryEligibility(False, "Lista curta já adequada ao slide", char_count, word_count)
        if char_count < self.min_chars and word_count < self.min_words:
            return SummaryEligibility(False, "Conteúdo curto já adequado ao slide", char_count, word_count)
        return SummaryEligibility(True, "Conteúdo longo elegível para resumo assistido", char_count, word_count)

    def _looks_like_isolated_number_or_date(self, text: str) -> bool:
        if not text:
            return True
        number_or_date = re.fullmatch(r"[\d\s.,/%\-]+", text)
        return bool(number_or_date and len(text) <= 32)
