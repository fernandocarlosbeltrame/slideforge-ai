from dataclasses import dataclass, field


@dataclass
class ContentAudit:
    used_block_ids: set[str] = field(default_factory=set)
    partially_used_block_ids: set[str] = field(default_factory=set)
    unused_block_ids: set[str] = field(default_factory=set)
    split_block_ids: set[str] = field(default_factory=set)
    used_image_ids: set[str] = field(default_factory=set)
    unused_image_ids: set[str] = field(default_factory=set)
    resized_image_ids: set[str] = field(default_factory=set)
    adjusted_title_ids: set[str] = field(default_factory=set)
    wrapped_title_ids: set[str] = field(default_factory=set)
    split_table_ids: set[str] = field(default_factory=set)
    repositioned_element_ids: set[str] = field(default_factory=set)
    warnings: list[str] = field(default_factory=list)
    visual_warnings: list[str] = field(default_factory=list)
    layout_counts: dict[str, int] = field(default_factory=dict)
    density_counts: dict[str, int] = field(default_factory=dict)
    critical_overflows: int = 0
    slide_count: int = 0

    @property
    def all_tracked_ids(self) -> set[str]:
        return self.used_block_ids | self.partially_used_block_ids | self.unused_block_ids | self.split_block_ids

    def as_report(self) -> str:
        layout_text = ", ".join(f"{k}: {v}" for k, v in sorted(self.layout_counts.items())) or "-"
        density_text = ", ".join(f"{k}: {v}" for k, v in sorted(self.density_counts.items())) or "-"
        return "\n".join([
            f"Slides gerados: {self.slide_count}",
            f"Blocos utilizados: {len(self.used_block_ids)}",
            f"Blocos divididos: {len(self.split_block_ids)}",
            f"Blocos não utilizados: {len(self.unused_block_ids)}",
            f"Imagens utilizadas: {len(self.used_image_ids)}",
            f"Imagens não utilizadas: {len(self.unused_image_ids)}",
            f"Imagens redimensionadas: {len(self.resized_image_ids)}",
            f"Títulos ajustados: {len(self.adjusted_title_ids)}",
            f"Tabelas divididas: {len(self.split_table_ids)}",
            f"Layouts usados: {layout_text}",
            f"Densidade visual: {density_text}",
            f"Overflows críticos: {self.critical_overflows}",
            f"Alertas: {len(self.warnings)}",
            f"Alertas visuais: {len(self.visual_warnings)}",
        ])
