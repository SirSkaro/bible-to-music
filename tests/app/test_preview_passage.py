import pytest

from bible_music.adapters.in_memory_scripture import InMemoryScripture
from bible_music.app.preview_passage import PassageNotFound, preview_passage
from bible_music.app.views import (
    BoundaryConflictKindView,
    BoundaryConflictView,
    PassagePlanPreviewView,
    ScriptureRangeView,
    ScriptureWordView,
    SongBoundaryView,
    WordEndingView,
)
from bible_music.domain.passage_plan import (
    BibleEdition,
    PermittedEnding,
    ScriptureWord,
    SongBoundaryPolicy,
    WordEnding,
)
from bible_music.domain.scripture import ScriptureRange


@pytest.fixture
def scripture():
    # ADR 0004's synthetic edition, with sentence and verse endings marked.
    edition = BibleEdition(
        "synthetic",
        (
            ScriptureWord("At", "1:1"),
            ScriptureWord("dawn", "1:1"),
            ScriptureWord("the", "1:1"),
            ScriptureWord("singers", "1:1"),
            ScriptureWord("gathered", "1:1", verse_end=True),
            ScriptureWord("beside", "1:2"),
            ScriptureWord("the", "1:2"),
            ScriptureWord("river;", "1:2", WordEnding.SEMICOLON, verse_end=True),
            ScriptureWord("then", "1:3"),
            ScriptureWord("the", "1:3"),
            ScriptureWord("bells", "1:3"),
            ScriptureWord("rang.", "1:3", WordEnding.SENTENCE),
            ScriptureWord("The", "1:3"),
            ScriptureWord("choir", "1:3"),
            ScriptureWord("waited;", "1:3", WordEnding.SEMICOLON),
            ScriptureWord("everyone", "1:3"),
            ScriptureWord("listened.", "1:3", WordEnding.SENTENCE, verse_end=True),
            ScriptureWord("Dr.", "1:4"),
            ScriptureWord("Vale", "1:4"),
            ScriptureWord("called,", "1:4"),
            ScriptureWord("“Ready?”", "1:4", WordEnding.SENTENCE, verse_end=True),
        ),
    )
    return InMemoryScripture(
        {edition.id: edition},
        {
            (edition.id, "1:1–1:4"): ScriptureRange(edition.id, 0, 21),
            (edition.id, "1:1"): ScriptureRange(edition.id, 0, 5),
        },
    )


def test_producer_previews_a_source_passage_pinned_at_a_semicolon(scripture):
    preview = preview_passage(
        scripture,
        edition_id="synthetic",
        reference="1:1–1:4",
        plan_id="plan",
        policy=SongBoundaryPolicy(
            PermittedEnding.SENTENCE_OR_SEMICOLON, require_verse_end=True
        ),
        pins=frozenset({8}),
    )

    assert preview == PassagePlanPreviewView(
        source=ScriptureRangeView("synthetic", 0, 21),
        pins=frozenset({8}),
        legal_cuts=(
            SongBoundaryView(
                8,
                ScriptureWordView("river;", "1:2", WordEndingView.SEMICOLON, True),
                ScriptureWordView("then", "1:3", WordEndingView.OTHER, False),
            ),
            SongBoundaryView(
                17,
                ScriptureWordView("listened.", "1:3", WordEndingView.SENTENCE, True),
                ScriptureWordView("Dr.", "1:4", WordEndingView.OTHER, False),
            ),
        ),
        song_passages=(
            ScriptureRangeView("synthetic", 0, 8),
            ScriptureRangeView("synthetic", 8, 21),
        ),
        conflicts=(),
    )


def test_producer_sees_a_conflicting_pin_and_can_keep_it_for_revision(scripture):
    preview = preview_passage(
        scripture,
        edition_id="synthetic",
        reference="1:1–1:4",
        plan_id="plan",
        policy=SongBoundaryPolicy(PermittedEnding.SENTENCE, require_verse_end=True),
        pins=frozenset({8}),
    )

    assert preview.pins == frozenset({8})
    assert preview.song_passages == ()
    assert preview.conflicts == (
        BoundaryConflictView(
            BoundaryConflictKindView.PIN,
            8,
            SongBoundaryView(
                8,
                ScriptureWordView("river;", "1:2", WordEndingView.SEMICOLON, True),
                ScriptureWordView("then", "1:3", WordEndingView.OTHER, False),
            ),
            (
                SongBoundaryView(
                    17,
                    ScriptureWordView(
                        "listened.", "1:3", WordEndingView.SENTENCE, True
                    ),
                    ScriptureWordView("Dr.", "1:4", WordEndingView.OTHER, False),
                ),
            ),
        ),
    )


def test_producer_sees_an_illegal_source_endpoint_even_without_any_cuts(scripture):
    preview = preview_passage(
        scripture,
        edition_id="synthetic",
        reference="1:1",
        plan_id="plan",
        policy=SongBoundaryPolicy(PermittedEnding.SENTENCE),
    )

    assert preview.song_passages == ()
    (conflict,) = preview.conflicts
    assert (conflict.kind, conflict.position) == (
        BoundaryConflictKindView.SOURCE_END,
        5,
    )
    assert conflict.boundary.before.text == "gathered"
    assert [boundary.position for boundary in conflict.legal_alternatives] == [12]


@pytest.mark.parametrize(
    ("edition_id", "reference"),
    [("synthetic", "Titus 4"), ("unloaded", "1:1")],
)
def test_producer_cannot_preview_an_unresolvable_passage(
    scripture, edition_id, reference
):
    with pytest.raises(PassageNotFound) as error:
        preview_passage(
            scripture,
            edition_id=edition_id,
            reference=reference,
            plan_id="plan",
            policy=SongBoundaryPolicy(PermittedEnding.ANY_WORD),
        )

    assert str(error.value) == (
        f"Passage {reference!r} was not found in Bible edition {edition_id!r}."
    )


def test_producer_previews_an_artists_proposed_cut_alongside_a_pin(scripture):
    preview = preview_passage(
        scripture,
        edition_id="synthetic",
        reference="1:1–1:4",
        plan_id="plan",
        policy=SongBoundaryPolicy(PermittedEnding.SENTENCE_OR_SEMICOLON),
        pins=frozenset({8}),
        cuts=frozenset({12}),
    )

    assert preview.conflicts == ()
    assert preview.song_passages == (
        ScriptureRangeView("synthetic", 0, 8),
        ScriptureRangeView("synthetic", 8, 12),
        ScriptureRangeView("synthetic", 12, 21),
    )


def test_producer_can_see_conflicts_with_partial_or_missing_boundary_context(scripture):
    preview = preview_passage(
        scripture,
        edition_id="synthetic",
        reference="1:1–1:4",
        plan_id="plan",
        policy=SongBoundaryPolicy(PermittedEnding.SENTENCE, require_verse_end=True),
        cuts=frozenset({0, 21}),
    )

    assert preview.conflicts == (
        BoundaryConflictView(
            BoundaryConflictKindView.PROPOSED_CUT, 0, None, preview.legal_cuts
        ),
        BoundaryConflictView(
            BoundaryConflictKindView.PROPOSED_CUT,
            21,
            SongBoundaryView(
                21,
                ScriptureWordView("“Ready?”", "1:4", WordEndingView.SENTENCE, True),
                None,
            ),
            preview.legal_cuts,
        ),
    )
