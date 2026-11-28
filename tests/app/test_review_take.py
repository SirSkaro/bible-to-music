from dataclasses import replace

import pytest

from bible_music.adapters.in_memory_take_review import InMemoryTakeReview
from bible_music.app.commands import ReviewTakeCommand
from bible_music.app.review_take import ReviewTake, TakeReviewInputNotFound
from bible_music.app.views import (
    AuditionWindowView,
    EvidenceSourceView,
    FindingView,
    ObservedWordView,
    ReviewOutcomeView,
    TakeReviewView,
    TimingPrecisionView,
)
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
from bible_music.domain.take import AudioRevisionRef, Take
from bible_music.domain.take_review import (
    EvidenceSource,
    ListenerObservation,
    ObservedWord,
    TimeSpan,
    TimingPrecision,
)


@pytest.fixture
def imported_take() -> tuple[ReviewTake, ReviewTakeCommand]:
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
    take = Take(arrangement.revision, AudioRevisionRef("imported-take", "original"))
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

    lookup = InMemoryTakeReview(
        {take.original_audio: take}, {arrangement.revision: arrangement}
    )
    return ReviewTake(lookup), ReviewTakeCommand(
        "offline-review", replace(take.original_audio), observation
    )


def test_producer_reviews_an_imported_take_and_gets_a_window_for_the_missing_word(
    imported_take: tuple[ReviewTake, ReviewTakeCommand],
) -> None:
    review_take, command = imported_take
    review = review_take(command)

    assert review == TakeReviewView(
        review_id="offline-review",
        take_id="imported-take",
        audio_revision="original",
        arrangement_id="arrangement",
        arrangement_revision="1",
        listener="recorded listener",
        evidence_source=EvidenceSourceView.FULL_MIX,
        observed_words=(
            ObservedWordView("we", None, None, TimingPrecisionView.PRECISE),
            ObservedWordView("sing", 220, 560, TimingPrecisionView.PRECISE),
            ObservedWordView("joy", 790, 1100, TimingPrecisionView.PRECISE),
            ObservedWordView("give", None, None, TimingPrecisionView.PRECISE),
            ObservedWordView("thanks", None, None, TimingPrecisionView.PRECISE),
            ObservedWordView("give", None, None, TimingPrecisionView.PRECISE),
            ObservedWordView("thanks", None, None, TimingPrecisionView.PRECISE),
        ),
        outcome=ReviewOutcomeView.OMISSION,
        findings=(
            FindingView(
                "with",
                12,
                0,
                AuditionWindowView(220, 1100, TimingPrecisionView.INFERRED),
            ),
        ),
    )


def test_producer_cannot_review_the_take_with_evidence_from_another_revision(
    imported_take: tuple[ReviewTake, ReviewTakeCommand],
) -> None:
    review_take, command = imported_take
    observation = command.observation
    wrong_revision = replace(command.audio_revision, revision="repair")

    with pytest.raises(ValueError, match="different audio revision"):
        review_take(
            replace(
                command, observation=replace(observation, audio_revision=wrong_revision)
            )
        )


def test_producer_can_inspect_an_omission_without_a_phrase_window(
    imported_take: tuple[ReviewTake, ReviewTakeCommand],
) -> None:
    review_take, command = imported_take
    observation = command.observation
    blurred_word = replace(
        observation.words[1], timing=None, precision=TimingPrecision.APPROXIMATE
    )
    observation = replace(
        observation,
        source=EvidenceSource.ISOLATED_VOCAL,
        words=(observation.words[0], blurred_word, *observation.words[2:]),
    )

    review = review_take(replace(command, observation=observation))

    assert review.evidence_source is EvidenceSourceView.ISOLATED_VOCAL
    assert review.observed_words[1] == ObservedWordView(
        "sing", None, None, TimingPrecisionView.APPROXIMATE
    )
    assert review.findings == (FindingView("with", 12, 0, None),)


@pytest.mark.parametrize(
    ("middle_words", "outcome"),
    [
        ((ObservedWord("with"), ObservedWord("joy")), ReviewOutcomeView.MATCH),
        ((), ReviewOutcomeView.INCONCLUSIVE),
    ],
)
def test_producer_can_distinguish_a_match_from_an_inconclusive_review(
    imported_take: tuple[ReviewTake, ReviewTakeCommand],
    middle_words: tuple[ObservedWord, ...],
    outcome: ReviewOutcomeView,
) -> None:
    review_take, command = imported_take
    observation = command.observation
    observation = replace(
        observation,
        words=(*observation.words[:2], *middle_words, *observation.words[3:]),
    )

    review = review_take(replace(command, observation=observation))

    assert review.outcome is outcome
    assert review.findings == ()


def test_review_reports_a_requested_revision_that_is_unavailable(
    imported_take: tuple[ReviewTake, ReviewTakeCommand],
) -> None:
    review_take, command = imported_take
    unknown = AudioRevisionRef("imported-take", "unavailable")
    command = replace(
        command,
        audio_revision=unknown,
        observation=replace(command.observation, audio_revision=unknown),
    )

    with pytest.raises(TakeReviewInputNotFound, match="unavailable"):
        review_take(command)
