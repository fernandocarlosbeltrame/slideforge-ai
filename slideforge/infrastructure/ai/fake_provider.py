from slideforge.application.ai.config import AIConfig
from slideforge.application.ai.contracts import (
    ContentSummarizer,
    DocumentAnalyzer,
    ImageSuggestionProvider,
    PresentationPlannerAI,
    PresentationReviewer,
    SlideLayoutAdvisor,
    SpeakerNotesGenerator,
    ThemeAdvisor,
)
from slideforge.application.ai.models import (
    AIContext,
    AIProviderInfo,
    DocumentInsight,
    ImageSuggestion,
    LayoutSuggestion,
    PlanSuggestion,
    ReviewIssue,
    ReviewResult,
    SpeakerNotes,
    SummaryOptions,
    SummaryResult,
    ThemeSuggestion,
)
from slideforge.domain.entities.presentation_plan import PresentationPlan
from slideforge.domain.entities.slide_plan import SlidePlan
from slideforge.domain.entities.source_document import SourceDocument


class FakeDocumentAnalyzer(DocumentAnalyzer):
    def analyze_document(self, document: SourceDocument, context: AIContext | None = None) -> DocumentInsight:
        topics = [section.title for section in document.sections if section.title]
        summary = f"Documento '{document.name}' com {len(document.sections)} seções e {sum(len(s.blocks) for s in document.sections)} blocos."
        return DocumentInsight(summary=summary, topics=topics[:8], risks=[])


class FakePresentationPlannerAI(PresentationPlannerAI):
    def suggest_plan(self, document: SourceDocument, context: AIContext | None = None) -> list[PlanSuggestion]:
        return [PlanSuggestion(title="Usar pipeline determinístico", rationale="FakeAIProvider não altera o plano; apenas registra sugestão previsível.", section_ids=[s.id for s in document.sections])]


class FakeSlideLayoutAdvisor(SlideLayoutAdvisor):
    def advise_layout(self, slide: SlidePlan, plan: PresentationPlan, context: AIContext | None = None) -> LayoutSuggestion:
        return LayoutSuggestion(slide_sequence=slide.sequence, recommended_layout=slide.layout_type.value, confidence=1.0, rationale="Mantém o layout determinístico definido pelo SlideForge.")


class FakeContentSummarizer(ContentSummarizer):
    def __init__(self, config: AIConfig | None = None):
        self.config = config or AIConfig()

    def summarize_content(self, text: str, context: AIContext | None = None, *, options: SummaryOptions | None = None) -> SummaryResult:
        normalized = " ".join(text.split())
        limit = min((options.max_length if options else 160), 160)
        truncated = len(normalized) > limit
        return SummaryResult(
            text=normalized[:limit].rstrip() + ("..." if truncated else ""),
            source_length=len(text),
            was_truncated=truncated,
            provider="fake",
            model=self.config.model,
            fallback_used=False,
            status="fake_summary",
        )


class FakeThemeAdvisor(ThemeAdvisor):
    def recommend_theme(self, plan: PresentationPlan, context: AIContext | None = None) -> ThemeSuggestion:
        return ThemeSuggestion(theme_name="corporate_blue", rationale="Tema padrão seguro para uso corporativo.")


class FakeImageSuggestionProvider(ImageSuggestionProvider):
    def suggest_images(self, slide: SlidePlan, plan: PresentationPlan, context: AIContext | None = None) -> list[ImageSuggestion]:
        return [ImageSuggestion(slide_sequence=slide.sequence, query=f"imagem corporativa para {slide.title}", rationale="Sugestão determinística para testes; nenhuma busca externa é executada.")]


class FakeSpeakerNotesGenerator(SpeakerNotesGenerator):
    def generate_speaker_notes(self, slide: SlidePlan, plan: PresentationPlan, context: AIContext | None = None) -> SpeakerNotes:
        blocks = ", ".join(slide.source_block_ids) or "sem blocos"
        notes = f"Slide {slide.sequence}: apresentar '{slide.title}'. Blocos de origem: {blocks}."
        return SpeakerNotes(slide_sequence=slide.sequence, notes=notes, source_block_ids=list(slide.source_block_ids))


class FakePresentationReviewer(PresentationReviewer):
    def review_presentation(self, plan: PresentationPlan, context: AIContext | None = None) -> ReviewResult:
        issues: list[ReviewIssue] = []
        for slide in plan.slides:
            if not slide.title.strip():
                issues.append(ReviewIssue("warning", slide.sequence, "Slide sem título.", "Revisar título antes da publicação."))
        return ReviewResult(summary=f"Revisão fake concluída para {len(plan.slides)} slides.", issues=issues)


class FakeAIProvider:
    def __init__(self, config: AIConfig | None = None):
        self._config = config or AIConfig()
        self._document_analyzer = FakeDocumentAnalyzer()
        self._presentation_planner = FakePresentationPlannerAI()
        self._slide_layout_advisor = FakeSlideLayoutAdvisor()
        self._content_summarizer = FakeContentSummarizer(self._config)
        self._theme_advisor = FakeThemeAdvisor()
        self._image_suggestion_provider = FakeImageSuggestionProvider()
        self._speaker_notes_generator = FakeSpeakerNotesGenerator()
        self._presentation_reviewer = FakePresentationReviewer()

    @property
    def info(self) -> AIProviderInfo:
        return AIProviderInfo(name="fake", model=self._config.model, supports_external_calls=False, deterministic=True)

    @property
    def config(self) -> AIConfig:
        return self._config

    def document_analyzer(self) -> DocumentAnalyzer:
        return self._document_analyzer

    def presentation_planner(self) -> PresentationPlannerAI:
        return self._presentation_planner

    def slide_layout_advisor(self) -> SlideLayoutAdvisor:
        return self._slide_layout_advisor

    def content_summarizer(self) -> ContentSummarizer:
        return self._content_summarizer

    def theme_advisor(self) -> ThemeAdvisor:
        return self._theme_advisor

    def image_suggestion_provider(self) -> ImageSuggestionProvider:
        return self._image_suggestion_provider

    def speaker_notes_generator(self) -> SpeakerNotesGenerator:
        return self._speaker_notes_generator

    def presentation_reviewer(self) -> PresentationReviewer:
        return self._presentation_reviewer
