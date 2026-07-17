from dataclasses import dataclass, field


@dataclass
class TableCell:
    text: str = ""
    row_span: int = 1
    col_span: int = 1


@dataclass
class TableRow:
    cells: list[TableCell] = field(default_factory=list)


@dataclass
class TableData:
    rows: list[TableRow] = field(default_factory=list)
    has_header: bool = False

    def as_matrix(self) -> list[list[str]]:
        return [[cell.text for cell in row.cells] for row in self.rows]
