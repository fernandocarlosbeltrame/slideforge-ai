from dataclasses import dataclass
from pathlib import Path
from typing import List
from docx import Document

@dataclass
class Block:
    kind: str  # title, heading, paragraph, bullet
    text: str


def parse_docx(path: str) -> List[Block]:
    doc = Document(path)
    blocks: List[Block] = []
    for p in doc.paragraphs:
        text = (p.text or '').strip()
        if not text:
            continue
        style = (p.style.name or '').lower() if p.style else ''
        if 'title' in style:
            kind = 'title'
        elif 'heading' in style:
            kind = 'heading'
        elif style.startswith('list') or text.startswith(('•', '-', '▪', '○')):
            kind = 'bullet'
        else:
            kind = 'paragraph'
        blocks.append(Block(kind, text.lstrip('•-▪○ ').strip()))
    return blocks


def parse_text(path: str) -> List[Block]:
    text = Path(path).read_text(encoding='utf-8', errors='ignore')
    blocks: List[Block] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith('#'):
            blocks.append(Block('heading', line.lstrip('#').strip()))
        elif line.startswith(('-', '*', '•')):
            blocks.append(Block('bullet', line.lstrip('-*• ').strip()))
        else:
            blocks.append(Block('paragraph', line))
    return blocks


def parse_document(path: str) -> List[Block]:
    suffix = Path(path).suffix.lower()
    if suffix == '.docx':
        return parse_docx(path)
    if suffix in {'.txt', '.md'}:
        return parse_text(path)
    raise ValueError(f'Formato não suportado: {suffix}')
