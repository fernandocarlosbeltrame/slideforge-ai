from dataclasses import dataclass, field
from pptx.dml.color import RGBColor
from slideforge.theme import Theme, get_theme


@dataclass(frozen=True)
class ComponentStyle:
    fill: RGBColor
    border: RGBColor
    text: RGBColor
    radius: float = 0.12
    metadata: dict = field(default_factory=dict)


@dataclass(frozen=True)
class PublishingTheme:
    name: str
    base: Theme
    icons: dict[str, str] = field(default_factory=dict)
    card: ComponentStyle | None = None
    table_header: ComponentStyle | None = None
    timeline: ComponentStyle | None = None
    callout: ComponentStyle | None = None


class ThemeRegistry:
    def __init__(self):
        self._themes: dict[str, PublishingTheme] = {}
        self.register(self._from_base(get_theme("corporate_blue")))
        self.register(self._from_base(get_theme("usiquimica")))

    def register(self, theme: PublishingTheme) -> None:
        self._themes[theme.name] = theme

    def get(self, name: str | None = None) -> PublishingTheme:
        key = name or "corporate_blue"
        return self._themes.get(key, self._themes["corporate_blue"])

    def names(self) -> list[str]:
        return sorted(self._themes)

    @staticmethod
    def _from_base(base: Theme) -> PublishingTheme:
        card = ComponentStyle(base.card_fill, base.secondary, base.dark)
        table = ComponentStyle(base.primary, base.primary, base.white)
        timeline = ComponentStyle(base.secondary, base.primary, base.dark)
        callout = ComponentStyle(base.white, base.secondary, base.primary)
        return PublishingTheme(name=base.name, base=base, card=card, table_header=table, timeline=timeline, callout=callout)
