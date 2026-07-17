from enum import Enum


class SlideLayoutType(str, Enum):
    COVER = "cover"
    TITLE_CONTENT = "title_content"
    BULLETS = "bullets"
    CARDS = "cards"
    TIMELINE = "timeline"
    COMPARISON = "comparison"
    TABLE = "table"
    IMAGE = "image"
    IMAGE_TEXT = "image_text"
    TWO_COLUMNS = "two_columns"
    PROCESS_FLOW = "process_flow"
    CALLOUT = "callout"
    SECTION_DIVIDER = "section_divider"
