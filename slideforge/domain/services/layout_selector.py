import re
from slideforge.application.services.content_density_analyzer import ContentDensityAnalyzer
from slideforge.domain.entities.document_section import DocumentSection
from slideforge.domain.entities.layout_decision import LayoutDecision
from slideforge.domain.enums.block_type import BlockType
from slideforge.domain.enums.slide_layout_type import SlideLayoutType


class LayoutSelector:
    def __init__(self, density_analyzer: ContentDensityAnalyzer | None = None):
        self.density_analyzer = density_analyzer or ContentDensityAnalyzer()

    def select_for_section(self, section: DocumentSection) -> SlideLayoutType:
        return self.decide_for_section(section).layout_type

    def decide_for_section(self, section: DocumentSection) -> LayoutDecision:
        text = "\n".join(block.text for block in section.blocks if block.text).lower()
        content_blocks = [block for block in section.blocks if block.type not in {BlockType.TITLE, BlockType.SUBTITLE}]
        list_items = [block for block in content_blocks if block.type == BlockType.LIST_ITEM]
        images = [block for block in content_blocks if block.type == BlockType.IMAGE]
        tables = [block for block in content_blocks if block.type == BlockType.TABLE]
        density = self.density_analyzer.analyze_blocks(content_blocks)

        if tables and len(content_blocks) <= 2:
            return LayoutDecision(SlideLayoutType.TABLE, "full_width_table", "Tabela detectada como conteúdo principal.", ["table_priority"], ["title_content"], density.level, 0.95)
        if self._has_before_after(section.title, text):
            return LayoutDecision(SlideLayoutType.COMPARISON, "two_column_comparison", "Termos Antes e Depois indicam comparação visual.", ["before_after"], ["two_columns", "bullets"], density.level, 0.96)
        if self._has_timeline_signals(text):
            return LayoutDecision(SlideLayoutType.TIMELINE, "horizontal_timeline", "Datas ou anos sequenciais indicam linha do tempo.", ["date_sequence"], ["process_flow", "bullets"], density.level, 0.92)
        if images and len(content_blocks) <= 2:
            return LayoutDecision(SlideLayoutType.IMAGE, "image_focus", "Imagem com pouco texto; slide visual dedicado.", ["image_priority"], ["image_text"], density.level, 0.98)
        if images and density.chars <= 520:
            return LayoutDecision(SlideLayoutType.IMAGE_TEXT, "image_text_60_40", "Imagem relevante combinada com texto curto.", ["image_with_context"], ["image", "title_content"], density.level, 0.9)
        if self._has_process_signals(text, list_items):
            return LayoutDecision(SlideLayoutType.PROCESS_FLOW, "step_flow", "Lista curta com sinais de processo/etapas.", ["process_words", "short_steps"], ["cards"], density.level, 0.84)
        if 1 <= len(list_items) <= 4 and all(len(item.text) <= 120 for item in list_items):
            return LayoutDecision(SlideLayoutType.CARDS, "card_grid", "Lista curta funciona melhor como cards.", ["short_list"], ["bullets"], density.level, 0.9)
        if density.chars <= 280 and not list_items:
            return LayoutDecision(SlideLayoutType.CALLOUT, "centered_callout", "Texto curto com perfil de mensagem principal.", ["short_text"], ["title_content"], density.level, 0.78)
        if len(list_items) > 4 or density.level in {"high", "critical"}:
            return LayoutDecision(SlideLayoutType.BULLETS, "chunked_bullets", "Densidade alta; conteúdo deve ser dividido em blocos seguros.", ["high_density"], ["cards", "title_content"], density.level, 0.86)
        return LayoutDecision(SlideLayoutType.TITLE_CONTENT, "title_and_content", "Conteúdo textual padrão com densidade moderada.", ["default"], ["bullets"], density.level, 0.72)

    @staticmethod
    def _has_before_after(title: str, text: str) -> bool:
        merged = f"{title}\n{text}".lower()
        return "antes" in merged and "depois" in merged

    @staticmethod
    def _has_timeline_signals(text: str) -> bool:
        years = re.findall(r"\b(20\d{2}|19\d{2})\b", text)
        date_words = ("janeiro", "fevereiro", "marco", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro")
        return len(set(years)) >= 2 or sum(1 for word in date_words if word in text) >= 2

    @staticmethod
    def _has_process_signals(text: str, list_items) -> bool:
        words = ("processo", "fluxo", "etapa", "passo", "jornada", "procedimento")
        return 2 <= len(list_items) <= 5 and any(word in text for word in words)

