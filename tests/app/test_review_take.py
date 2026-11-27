from dataclasses import replace

import pytest

from bible_music.app.review_take import review_take
from bible_music.domain.arrangement import (
    Arrangement,
    ArrangementRevision,
    LyricPlacement,
)
from bible_music.domain.scripture import (
    PassagePlanRevision,
    ScriptureRange,
    SongPassage,
)
from bible_music.domain.take import AudioRevision, Take
from bible_music.domain.take_review import (
    AuditionWindow,
    EvidenceSource,
    ListenerObservation,
    ObservedWord,
    ReviewOutcome,
    TimeSpan,
    TimingPrecision,
)


@pytest.fixture
def imported_take():
    song = SongPassage(
        PassagePlanRevision("plan", "1"), ScriptureRange("synthetic", 10, 16)
    )
    lead = LyricPlacement("verse", "lead", ScriptureRange("synthetic", 10, 14))
    chorus = LyricPlacement("chorus", "lead", ScriptureRange("synthetic", 14, 16))
    arrangement = Arrangement(
        ArrangementRevision("arrangement", "1"),
        song,
        ("we", "sing", "with", "joy", "give", "thanks"),
        (
            lead,
            chorus,
            LyricPlacement("final chorus", "lead", chorus.source, repeat=True),
        ),
    )
    take = Take(arrangement.revision, AudioRevision("imported-take", "original"))
    observation = ListenerObservation(
        take.original_audio,
        "recorded listener",
        EvidenceSource.FULL_MIX,
        (
            ObservedWord("we"),
            ObservedWord("sing", TimeSpan(220, 560)),
            ObservedWord("joy", TimeSpan(790, 1100)),
            ObservedWord("give"),
            ObservedWord("thanks"),
            ObservedWord("give"),
            ObservedWord("thanks"),
        ),
    )

    return take, arrangement, observation


def test_producer_reviews_an_imported_take_and_gets_a_window_for_the_missing_word(
    imported_take,
):
    take, arrangement, observation = imported_take
    review = review_take("offline-review", take, arrangement, observation)

    assert review.review_id == "offline-review"
    assert review.audio_revision == take.original_audio
    assert review.arrangement_revision == arrangement.revision
    assert review.observation == observation
    assert review.outcome is ReviewOutcome.OMISSION
    (finding,) = review.findings
    assert finding.omitted_word.text == "with"
    assert finding.audition_window == AuditionWindow(
        TimeSpan(220, 1100), TimingPrecision.INFERRED
    )


def test_producer_cannot_review_the_take_with_evidence_from_another_revision(
    imported_take,
):
    take, arrangement, observation = imported_take
    wrong_revision = replace(take.original_audio, revision="repair")

    with pytest.raises(ValueError, match="different audio revision"):
        review_take(
            "offline-review",
            take,
            arrangement,
            replace(observation, audio_revision=wrong_revision),
        )
