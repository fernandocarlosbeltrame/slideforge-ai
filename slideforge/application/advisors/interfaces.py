from typing import Protocol
from slideforge.application.ai.contracts import (
    ContentSummarizer,
    PresentationReviewer,
    SlideLayoutAdvisor,
    ThemeAdvisor,
)
from slideforge.domain.entities.presentation_plan import PresentationPlan


class PresentationAdvisor(Protocol):
    def advise(self, plan: PresentationPlan) -> list[str]: ...


class LayoutAdvisor(SlideLayoutAdvisor, Protocol):
    pass


class SummaryAdvisor(ContentSummarizer, Protocol):
    pass


class ThemeAdvisorProtocol(ThemeAdvisor, Protocol):
    pass


class ContentAdvisor(PresentationReviewer, Protocol):
    pass


ThemeAdvisor = ThemeAdvisorProtocol
