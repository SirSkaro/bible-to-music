from dataclasses import FrozenInstanceError, replace

import pytest

from bible_music.domain.arrangement import (
    Arrangement,
    ArrangementRevision,
    ExpectedWord,
    LyricPlacement,
)
from bible_music.domain.scripture import (
    PassagePlanRevision,
    ScriptureRange,
    SongPassage,
)


@pytest.fixture
def arrangement() -> Arrangement:
    song = SongPassage(
        PassagePlanRevision("plan", "1"), ScriptureRange("edition", 5, 9)
    )
    placements = (
        LyricPlacement("musical verse", "lead", ScriptureRange("edition", 5, 7)),
        LyricPlacement("chorus", "lead", ScriptureRange("edition", 7, 9)),
    )
    return Arrangement(
        ArrangementRevision("arrangement", "1"),
        song,
        ("we", "sing", "for", "joy"),
        placements,
    )


def test_arrangement_preserves_source_word_positions_and_performance_order(
    arrangement: Arrangement,
) -> None:
    verse, chorus = arrangement.placements
    arrangement = replace(
        arrangement, placements=(chorus, replace(chorus, repeat=True), verse)
    )

    assert arrangement.expected_words() == (
        ExpectedWord("for", 7, 0),
        ExpectedWord("joy", 8, 0),
        ExpectedWord("for", 7, 1),
        ExpectedWord("joy", 8, 1),
        ExpectedWord("we", 5, 2),
        ExpectedWord("sing", 6, 2),
    )


@pytest.mark.parametrize(
    "words", [("we", "sing", "for"), ("we", "sing", "for", "great", "joy")]
)
def test_arrangement_requires_the_words_of_the_complete_song_passage(
    arrangement: Arrangement, words: tuple[str, ...]
) -> None:
    with pytest.raises(ValueError, match="one normalized word for each position"):
        replace(arrangement, scripture_words=words)


@pytest.mark.parametrize(
    "span", [("other", 5, 7), ("edition", 4, 7), ("edition", 5, 10)]
)
def test_arrangement_rejects_placements_outside_the_song_passage(
    arrangement: Arrangement, span: tuple[str, int, int]
) -> None:
    verse, chorus = arrangement.placements
    with pytest.raises(ValueError, match="inside its song passage"):
        replace(
            arrangement,
            placements=(replace(verse, source=ScriptureRange(*span)), chorus),
        )


def test_arrangement_accounts_for_every_source_word(arrangement: Arrangement) -> None:
    with pytest.raises(ValueError, match="cover the complete song passage"):
        replace(arrangement, placements=arrangement.placements[:1])


def test_arrangement_requires_authorization_before_reusing_scripture(
    arrangement: Arrangement,
) -> None:
    verse, chorus = arrangement.placements
    with pytest.raises(ValueError, match="authorized repeat"):
        replace(arrangement, placements=(verse, chorus, chorus))


def test_arrangement_requires_a_previous_placement_for_an_authorized_repeat(
    arrangement: Arrangement,
) -> None:
    verse, chorus = arrangement.placements
    with pytest.raises(ValueError, match="earlier placement"):
        replace(arrangement, placements=(verse, replace(chorus, repeat=True), chorus))


def test_arrangement_accepts_a_long_song_passage(arrangement: Arrangement) -> None:
    words = ("sing",) * 259 + ("well",)
    scripture = ScriptureRange("edition", 5, 265)
    arranged = replace(
        arrangement,
        song_passage=replace(arrangement.song_passage, scripture=scripture),
        scripture_words=words,
        placements=(LyricPlacement("musical verse", "lead", scripture),),
    )
    assert arranged.expected_words()[-1] == ExpectedWord("well", 264, 0)


def test_an_arrangement_and_its_cited_values_are_immutable(
    arrangement: Arrangement,
) -> None:
    values = (
        (arrangement, "placements", ()),
        (arrangement.revision, "revision", "2"),
        (arrangement.placements[0], "voice", "backup"),
        (arrangement.expected_words()[0], "text", "new"),
        (arrangement.song_passage, "scripture", ScriptureRange("edition", 5, 6)),
        (arrangement.song_passage.plan_revision, "revision", "2"),
    )
    for value, field, alternative in values:
        with pytest.raises(FrozenInstanceError):
            setattr(value, field, alternative)
