from enum import Enum


class BlockType(str, Enum):
    TITLE = "title"
    SUBTITLE = "subtitle"
    PARAGRAPH = "paragraph"
    LIST = "list"
    LIST_ITEM = "list_item"
    TABLE = "table"
    IMAGE = "image"
    NOTE = "note"
