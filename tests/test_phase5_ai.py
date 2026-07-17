import json
from pathlib import Path

import pytest

from slideforge.application.ai import AIConfig, AIContext
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
from slideforge.application.services.content_auditor import ContentAuditor
from slideforge.application.services.presentation_planner import PresentationPlanner
from slideforge.domain.entities.content_block import ContentBlock
from slideforge.domain.entities.document_section import DocumentSection
from slideforge.domain.entities.source_document import SourceDocument
from slideforge.domain.enums.block_type import BlockType
from slideforge.infrastructure.ai import AIProviderFactory, FakeAIProvider, OpenAIProvider


def _document() -> SourceDocument:
    blocks = [
        ContentBlock(id="title", type=BlockType.TITLE, text="Plano Executivo", hierarchy_level=1, order=1, source_reference="test"),
        ContentBlock(id="item1", type=BlockType.LIST_ITEM, text="Primeiro ponto", hierarchy_level=2, order=2, source_reference="test"),
        ContentBlock(id="item2", type=BlockType.LIST_ITEM, text="Segundo ponto", hierarchy_level=2, order=3, source_reference="test"),
    ]
    section = DocumentSection(id="secao", title="Plano Executivo", order=1, blocks=blocks)
    return SourceDocument(id="doc", name="demo.docx", source_path="demo.docx", format="docx", sections=[section])


def _plan():
    return PresentationPlanner().create_plan(_document())


def test_ai_config_loads_without_api_keys(tmp_path: Path):
    config_path = tmp_path / "ai_config.json"
    config_path.write_text(json.dumps({"active_provider": "fake", "temperature": 0, "model": "fake-test", "token_limit": 1000, "timeout_seconds": 10}), encoding="utf-8")
    config = AIConfig.from_file(config_path)
    assert config.active_provider == "fake"
    assert config.model == "fake-test"
    assert "api" not in json.dumps(config.as_dict()).lower()


def test_ai_provider_factory_resolves_fake_provider():
    provider = AIProviderFactory().create(AIConfig(active_provider="fake"))
    assert isinstance(provider, FakeAIProvider)
    assert provider.info.name == "fake"
    assert provider.info.deterministic is True
    assert provider.info.supports_external_calls is False


def test_ai_provider_factory_creates_stubs_but_only_fake_executes():
    provider = AIProviderFactory().create(AIConfig(active_provider="openai", model="future-model"))
    assert isinstance(provider, OpenAIProvider)
    assert provider.info.name == "openai"
    with pytest.raises(NotImplementedError):
        provider.document_analyzer()


def test_ai_contracts_are_exposed_by_fake_provider():
    provider = FakeAIProvider()
    assert isinstance(provider.document_analyzer(), DocumentAnalyzer)
    assert isinstance(provider.presentation_planner(), PresentationPlannerAI)
    assert isinstance(provider.slide_layout_advisor(), SlideLayoutAdvisor)
    assert isinstance(provider.content_summarizer(), ContentSummarizer)
    assert isinstance(provider.theme_advisor(), ThemeAdvisor)
    assert isinstance(provider.image_suggestion_provider(), ImageSuggestionProvider)
    assert isinstance(provider.speaker_notes_generator(), SpeakerNotesGenerator)
    assert isinstance(provider.presentation_reviewer(), PresentationReviewer)


def test_fake_ai_provider_outputs_are_deterministic():
    document = _document()
    plan = _plan()
    provider = FakeAIProvider(AIConfig(model="fake-deterministic-v1"))
    context = AIContext(purpose="teste")

    insight = provider.document_analyzer().analyze_document(document, context)
    assert "demo.docx" in insight.summary
    assert insight.topics == ["Plano Executivo"]

    suggestion = provider.presentation_planner().suggest_plan(document, context)[0]
    assert suggestion.section_ids == ["secao"]

    layout = provider.slide_layout_advisor().advise_layout(plan.slides[0], plan, context)
    assert layout.recommended_layout == plan.slides[0].layout_type.value
    assert layout.confidence == 1.0

    summary = provider.content_summarizer().summarize_content("texto " * 80, context)
    assert summary.was_truncated is True
    assert summary.text.endswith("...")

    theme = provider.theme_advisor().recommend_theme(plan, context)
    assert theme.theme_name == "corporate_blue"

    images = provider.image_suggestion_provider().suggest_images(plan.slides[0], plan, context)
    assert images[0].slide_sequence == plan.slides[0].sequence
    assert "nenhuma busca externa" in images[0].rationale

    notes = provider.speaker_notes_generator().generate_speaker_notes(plan.slides[0], plan, context)
    assert notes.source_block_ids == plan.slides[0].source_block_ids

    review = provider.presentation_reviewer().review_presentation(plan, context)
    assert review.ok is True
    assert str(len(plan.slides)) in review.summary


def test_ai_layer_does_not_mutate_plan():
    plan = _plan()
    before = ContentAuditor().audit(plan).as_report()
    provider = FakeAIProvider()
    provider.presentation_reviewer().review_presentation(plan)
    provider.theme_advisor().recommend_theme(plan)
    after = ContentAuditor().audit(plan).as_report()
    assert after == before


def test_unsupported_provider_has_clear_error():
    with pytest.raises(ValueError, match="Provedor de IA não suportado"):
        AIProviderFactory().create(AIConfig(active_provider="unknown"))
