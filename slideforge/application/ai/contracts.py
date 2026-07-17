from typing import Protocol, runtime_checkable

from slideforge.application.ai.models import (
    AIContext,
    DocumentInsight,
    ImageSuggestion,
    LayoutSuggestion,
    PlanSuggestion,
    ReviewResult,
    SpeakerNotes,
    SummaryOptions,
    SummaryResult,
    ThemeSuggestion,
)
from slideforge.domain.entities.presentation_plan import PresentationPlan
from slideforge.domain.entities.slide_plan import SlidePlan
from slideforge.domain.entities.source_document import SourceDocument


@runtime_checkable
class DocumentAnalyzer(Protocol):
    def analyze_document(self, document: SourceDocument, context: AIContext | None = None) -> DocumentInsight: ...


@runtime_checkable
class PresentationPlannerAI(Protocol):
    def suggest_plan(self, document: SourceDocument, context: AIContext | None = None) -> list[PlanSuggestion]: ...


@runtime_checkable
class SlideLayoutAdvisor(Protocol):
    def advise_layout(self, slide: SlidePlan, plan: PresentationPlan, context: AIContext | None = None) -> LayoutSuggestion: ...


@runtime_checkable
class ContentSummarizer(Protocol):
    def summarize_content(self, text: str, context: AIContext | None = None, *, options: SummaryOptions | None = None) -> SummaryResult: ...


@runtime_checkable
class ThemeAdvisor(Protocol):
    def recommend_theme(self, plan: PresentationPlan, context: AIContext | None = None) -> ThemeSuggestion: ...


@runtime_checkable
class ImageSuggestionProvider(Protocol):
    def suggest_images(self, slide: SlidePlan, plan: PresentationPlan, context: AIContext | None = None) -> list[ImageSuggestion]: ...


@runtime_checkable
class SpeakerNotesGenerator(Protocol):
    def generate_speaker_notes(self, slide: SlidePlan, plan: PresentationPlan, context: AIContext | None = None) -> SpeakerNotes: ...


@runtime_checkable
class PresentationReviewer(Protocol):
    def review_presentation(self, plan: PresentationPlan, context: AIContext | None = None) -> ReviewResult: ...
