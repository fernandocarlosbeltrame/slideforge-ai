from typing import Protocol
from slideforge.domain.entities.presentation_plan import PresentationPlan


class PresentationAdvisor(Protocol):
    def advise(self, plan: PresentationPlan) -> list[str]: ...


class LayoutAdvisor(Protocol):
    def advise_layouts(self, plan: PresentationPlan) -> list[str]: ...


class SummaryAdvisor(Protocol):
    def summarize(self, plan: PresentationPlan) -> str: ...


class ThemeAdvisor(Protocol):
    def recommend_theme(self, plan: PresentationPlan) -> str: ...


class ContentAdvisor(Protocol):
    def review_content(self, plan: PresentationPlan) -> list[str]: ...
