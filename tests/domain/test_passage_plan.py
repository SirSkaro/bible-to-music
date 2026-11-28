from dataclasses import FrozenInstanceError

import pytest

from bible_music.domain.passage_plan import (
    BibleEdition,
    BoundaryConflictKind,
    PassagePlan,
    PermittedEnding,
    ScriptureWord,
    SongBoundaryPolicy,
    WordEnding,
)
from bible_music.domain.scripture import ScriptureRange


@pytest.fixture
def edition() -> BibleEdition:
    return BibleEdition(
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


def test_producer_pins_a_semicolon_at_a_verse_end(edition: BibleEdition) -> None:
    plan = PassagePlan(
        "plan",
        ScriptureRange(edition.id, 0, 21),
        SongBoundaryPolicy(
            PermittedEnding.SENTENCE_OR_SEMICOLON, require_verse_end=True
        ),
        pins=frozenset({8}),
    )

    preview = plan.preview(edition)

    assert preview.conflicts == ()
    assert preview.pins == frozenset({8})
    assert [boundary.position for boundary in preview.legal_cuts] == [8, 17]
    assert preview.song_passages == (
        ScriptureRange(edition.id, 0, 8),
        ScriptureRange(edition.id, 8, 21),
    )


def test_switching_to_sentence_endings_reports_the_pin_and_leaves_it_in_place(
    edition: BibleEdition,
) -> None:
    source = ScriptureRange(edition.id, 0, 21)
    plan = PassagePlan(
        "plan",
        source,
        SongBoundaryPolicy(PermittedEnding.SENTENCE, require_verse_end=True),
        pins=frozenset({8}),
    )
    preview = plan.preview(edition)

    assert preview.source == source
    assert plan.pins == preview.pins == frozenset({8})
    assert preview.song_passages == ()
    (conflict,) = preview.conflicts
    assert (conflict.kind, conflict.position) == (BoundaryConflictKind.PIN, 8)
    assert (conflict.boundary.before.text, conflict.boundary.before.verse) == (
        "river;",
        "1:2",
    )
    assert conflict.boundary.after.text == "then"
    assert [cut.position for cut in conflict.legal_alternatives] == [17]


@pytest.mark.parametrize("pin", [False, True])
def test_a_sentence_can_end_inside_a_verse_unless_a_verse_end_is_required(
    edition: BibleEdition, pin: bool
) -> None:
    source = ScriptureRange(edition.id, 0, 21)
    pinned = frozenset({12}) if pin else frozenset()
    proposed = frozenset() if pin else frozenset({12})
    sentence_only = PassagePlan(
        "plan", source, SongBoundaryPolicy(PermittedEnding.SENTENCE), pinned
    )
    verse_required = PassagePlan(
        "plan",
        source,
        SongBoundaryPolicy(PermittedEnding.SENTENCE, require_verse_end=True),
        pinned,
    )

    assert sentence_only.preview(edition, proposed).song_passages == (
        ScriptureRange(edition.id, 0, 12),
        ScriptureRange(edition.id, 12, 21),
    )
    preview = verse_required.preview(edition, proposed)
    assert preview.song_passages == ()
    (conflict,) = preview.conflicts
    assert conflict.kind == (
        BoundaryConflictKind.PIN if pin else BoundaryConflictKind.PROPOSED_CUT
    )
    assert (
        conflict.position,
        conflict.boundary.before.text,
        conflict.boundary.after.text,
    ) == (
        12,
        "rang.",
        "The",
    )
    assert [cut.position for cut in conflict.legal_alternatives] == [17]


def test_source_ending_mid_sentence_is_invalid_with_no_internal_cuts(
    edition: BibleEdition,
) -> None:
    plan = PassagePlan(
        "plan",
        ScriptureRange(edition.id, 0, 5),
        SongBoundaryPolicy(PermittedEnding.SENTENCE),
    )
    preview = plan.preview(edition)

    assert preview.song_passages == ()
    assert preview.legal_cuts == ()
    (conflict,) = preview.conflicts
    assert (conflict.kind, conflict.position, conflict.boundary.before.text) == (
        BoundaryConflictKind.SOURCE_END,
        5,
        "gathered",
    )
    assert [cut.position for cut in conflict.legal_alternatives] == [12]


def test_a_valid_source_fits_in_one_song_even_when_earlier_endings_are_legal(
    edition: BibleEdition,
) -> None:
    source = ScriptureRange(edition.id, 0, 17)
    plan = PassagePlan(
        "plan",
        source,
        SongBoundaryPolicy(
            PermittedEnding.SENTENCE_OR_SEMICOLON, require_verse_end=True
        ),
    )

    preview = plan.preview(edition)

    assert preview.conflicts == ()
    assert preview.song_passages == (source,)
    assert [cut.position for cut in preview.legal_cuts] == [8]


@pytest.mark.parametrize(
    ("ending", "verse_required", "positions"),
    [
        (PermittedEnding.ANY_WORD, False, list(range(1, 21))),
        (PermittedEnding.ANY_WORD, True, [5, 8, 17]),
        (PermittedEnding.SENTENCE, False, [12, 17]),
        (PermittedEnding.SENTENCE, True, [17]),
        (PermittedEnding.SENTENCE_OR_SEMICOLON, False, [8, 12, 15, 17]),
        (PermittedEnding.SENTENCE_OR_SEMICOLON, True, [8, 17]),
    ],
)
def test_preview_uses_edition_endings_including_abbreviations_and_quoted_questions(
    edition: BibleEdition,
    ending: PermittedEnding,
    verse_required: bool,
    positions: list[int],
) -> None:
    plan = PassagePlan(
        "plan",
        ScriptureRange(edition.id, 0, 21),
        SongBoundaryPolicy(ending, verse_required),
    )
    preview = plan.preview(edition)
    assert [cut.position for cut in preview.legal_cuts] == positions
    assert preview.conflicts == ()
    assert edition.boundary_at(21).before.text == "“Ready?”"
    assert edition.boundary_at(21).after is None


def test_preview_partitions_a_source_that_starts_mid_verse(
    edition: BibleEdition,
) -> None:
    source = ScriptureRange(edition.id, 6, 17)
    plan = PassagePlan(
        "plan",
        source,
        SongBoundaryPolicy(PermittedEnding.ANY_WORD),
        pins=frozenset({12}),
    )
    preview = plan.preview(edition, frozenset({12, 16, 7}))
    assert preview.conflicts == ()
    assert preview.song_passages == (
        ScriptureRange(edition.id, 6, 7),
        ScriptureRange(edition.id, 7, 12),
        ScriptureRange(edition.id, 12, 16),
        ScriptureRange(edition.id, 16, 17),
    )
    assert [cut.position for cut in preview.legal_cuts] == list(range(7, 17))


def test_preview_reports_all_out_of_range_cuts_and_the_invalid_terminal_endpoint(
    edition: BibleEdition,
) -> None:
    plan = PassagePlan(
        "plan",
        ScriptureRange(edition.id, 2, 14),
        SongBoundaryPolicy(PermittedEnding.SENTENCE),
    )
    preview = plan.preview(edition, frozenset({-1, 0, 2, 14, 22}))

    assert preview.song_passages == ()
    assert [(conflict.kind, conflict.position) for conflict in preview.conflicts] == [
        (BoundaryConflictKind.PROPOSED_CUT, -1),
        (BoundaryConflictKind.PROPOSED_CUT, 0),
        (BoundaryConflictKind.PROPOSED_CUT, 2),
        (BoundaryConflictKind.PROPOSED_CUT, 14),
        (BoundaryConflictKind.PROPOSED_CUT, 22),
        (BoundaryConflictKind.SOURCE_END, 14),
    ]
    assert [conflict.boundary is not None for conflict in preview.conflicts] == [
        False,
        False,
        True,
        True,
        False,
        True,
    ]
    assert [cut.position for cut in preview.conflicts[-1].legal_alternatives] == [
        12,
        17,
    ]


def test_invalid_end_at_the_end_of_the_loaded_edition_has_only_earlier_alternatives(
    edition: BibleEdition,
) -> None:
    edition = BibleEdition(edition.id, edition.words[:14])
    plan = PassagePlan(
        "plan",
        ScriptureRange(edition.id, 6, 14),
        SongBoundaryPolicy(PermittedEnding.SENTENCE),
    )
    (conflict,) = plan.preview(edition).conflicts
    assert [cut.position for cut in conflict.legal_alternatives] == [12]


@pytest.mark.parametrize("source", [("other", 0, 21), ("synthetic", 0, 22)])
def test_preview_requires_a_source_range_in_the_selected_edition(
    edition: BibleEdition, source: tuple[str, int, int]
) -> None:
    plan = PassagePlan(
        "plan", ScriptureRange(*source), SongBoundaryPolicy(PermittedEnding.ANY_WORD)
    )
    with pytest.raises(ValueError, match="must exist in the selected Bible edition"):
        plan.preview(edition)


def test_only_the_edition_value_needs_to_match_the_source(
    edition: BibleEdition,
) -> None:
    source = ScriptureRange(b"synthetic".decode(), 0, 21)
    plan = PassagePlan("plan", source, SongBoundaryPolicy(PermittedEnding.SENTENCE))
    assert plan.preview(edition).song_passages == (source,)
    with pytest.raises(ValueError, match="must exist in the selected Bible edition"):
        plan.preview(BibleEdition("earlier", edition.words))


def test_preview_can_suggest_the_final_word_of_an_edition_for_an_earlier_invalid_end(
    edition: BibleEdition,
) -> None:
    plan = PassagePlan(
        "plan",
        ScriptureRange(edition.id, 17, 20),
        SongBoundaryPolicy(PermittedEnding.SENTENCE),
    )
    (conflict,) = plan.preview(edition).conflicts
    (alternative,) = conflict.legal_alternatives
    assert (alternative.position, alternative.before.text, alternative.after) == (
        21,
        "“Ready?”",
        None,
    )


def test_the_first_word_has_its_own_boundary_and_adjacent_context(
    edition: BibleEdition,
) -> None:
    boundary = edition.boundary_at(1)
    assert (boundary.position, boundary.before.text, boundary.after.text) == (
        1,
        "At",
        "dawn",
    )


def test_the_final_boundary_of_a_long_edition_has_no_following_word() -> None:
    words = (ScriptureWord("word", "1:1"),) * 300
    edition = BibleEdition("synthetic", words)
    position = int("300")
    assert edition.boundary_at(position).after is None


def test_the_plan_and_preview_keep_immutable_positions_and_conflict_evidence(
    edition: BibleEdition,
) -> None:
    plan = PassagePlan(
        "plan",
        ScriptureRange(edition.id, 0, 21),
        SongBoundaryPolicy(PermittedEnding.SENTENCE),
        frozenset({8}),
    )
    preview = plan.preview(edition)
    (conflict,) = preview.conflicts
    values = (
        (plan, "pins", frozenset()),
        (plan.policy, "require_verse_end", True),
        (preview, "conflicts", ()),
        (conflict, "position", 9),
        (conflict.boundary, "position", 9),
        (conflict.boundary.before, "text", "elsewhere"),
        (edition, "id", "other"),
    )
    for value, field, alternative in values:
        with pytest.raises(FrozenInstanceError):
            setattr(value, field, alternative)
