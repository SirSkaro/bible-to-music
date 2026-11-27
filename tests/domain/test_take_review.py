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
from bible_music.domain.take import AudioRevision, Take
from bible_music.domain.take_review import (
    AuditionWindow,
    EvidenceSource,
    Finding,
    ListenerObservation,
    ObservedWord,
    ReviewOutcome,
    TakeReview,
    TimeSpan,
    TimingPrecision,
)


def test_take_review_locates_a_missing_lead_word_and_accepts_the_repeated_chorus():
    song = SongPassage(
        PassagePlanRevision("plan", "1"), ScriptureRange("synthetic", 10, 16)
    )
    lead = LyricPlacement("verse", "lead", ScriptureRange("synthetic", 10, 14))
    chorus = LyricPlacement("chorus", "lead", ScriptureRange("synthetic", 14, 16))
    repeat = LyricPlacement("final chorus", "lead", chorus.source, repeat=True)
    arrangement = Arrangement(
        ArrangementRevision("arrangement", "1"),
        song,
        ("we", "sing", "with", "joy", "give", "thanks"),
        (lead, chorus, repeat),
    )
    take = Take(arrangement.revision, AudioRevision("take", "original"))
    observation = ListenerObservation(
        take.original_audio,
        "synthetic listener",
        EvidenceSource.FULL_MIX,
        (
            ObservedWord("we", TimeSpan(0, 200)),
            ObservedWord("sing", TimeSpan(220, 560)),
            ObservedWord("joy", TimeSpan(790, 1100)),
            ObservedWord("give"),
            ObservedWord("thanks"),
            ObservedWord("give"),
            ObservedWord("thanks"),
        ),
    )

    review = TakeReview.assess("review", take, arrangement, observation)

    assert review.audio_revision == take.original_audio
    assert review.arrangement_revision == arrangement.revision
    assert review.observation == observation
    assert review.outcome is ReviewOutcome.OMISSION
    assert review.findings == (
        Finding(
            ExpectedWord("with", 12, 0),
            AuditionWindow(TimeSpan(220, 1100), TimingPrecision.INFERRED),
        ),
    )


@pytest.fixture
def arrangement():
    passage = SongPassage(
        PassagePlanRevision("plan", "1"), ScriptureRange("synthetic", 300, 303)
    )
    return Arrangement(
        ArrangementRevision("arrangement", "1"),
        passage,
        ("we", "sing", "softly"),
        (LyricPlacement("verse", "lead", passage.scripture),),
    )


def assess_words(arrangement, words):
    take = Take(arrangement.revision, AudioRevision("take", "original"))
    observation = ListenerObservation(
        take.original_audio, "listener", EvidenceSource.FULL_MIX, words
    )
    return TakeReview.assess("review", take, arrangement, observation)


def test_review_accepts_both_placements_of_a_repeated_chorus(arrangement):
    first = replace(arrangement.placements[0], section="chorus")
    repeated = replace(arrangement, placements=(first, replace(first, repeat=True)))
    review = assess_words(
        repeated, tuple(ObservedWord(word) for word in repeated.scripture_words * 2)
    )
    assert (review.review_id, review.outcome, review.findings) == (
        "review",
        ReviewOutcome.MATCH,
        (),
    )


@pytest.mark.parametrize(
    ("heard", "expected"),
    [
        (("we", "sing"), ("we", "sing", b"sing".decode())),
        (("sing", "joyful"), ("we", "sing", "softly")),
        (("sing", "warmly"), ("we", "sing", "softly")),
        (("sing",), ("we", "sing", "softly")),
        (("we", "sing", "softly", "again"), ("we", "sing", "softly")),
        (("we", "sing", "quietly"), ("we", "sing", "softly")),
    ],
)
def test_review_leaves_an_ambiguous_or_more_complex_difference_inconclusive(
    arrangement, heard, expected
):
    arrangement = replace(arrangement, scripture_words=expected)
    review = assess_words(arrangement, tuple(ObservedWord(word) for word in heard))
    assert (review.outcome, review.findings) == (ReviewOutcome.INCONCLUSIVE, ())


@pytest.mark.parametrize(
    ("observed", "omission"),
    [
        ((("sing", (0, 10)), ("softly", (15, 20))), "we"),
        ((("we", (0, 10)), ("sing", (15, 20))), "softly"),
        ((("we", None), ("softly", (15, 20))), "sing"),
        ((("we", (0, 10)), ("softly", None)), "sing"),
        ((("we", (0, 16)), ("softly", (15, 20))), "sing"),
    ],
)
def test_review_preserves_an_omission_without_usable_neighbor_timing(
    arrangement, observed, omission
):
    heard = tuple(
        ObservedWord(word, TimeSpan(*timing) if timing else None)
        for word, timing in observed
    )
    review = assess_words(arrangement, heard)
    assert review.outcome is ReviewOutcome.OMISSION
    assert review.findings[0].omitted_word.text == omission
    assert review.findings[0].audition_window is None


def test_review_can_infer_a_phrase_window_when_the_observed_intervals_touch(
    arrangement,
):
    review = assess_words(
        arrangement,
        (ObservedWord("we", TimeSpan(0, 10)), ObservedWord("softly", TimeSpan(10, 20))),
    )
    assert review.findings[0].audition_window == AuditionWindow(
        TimeSpan(0, 20), TimingPrecision.INFERRED
    )


@pytest.mark.parametrize("bounds", [(-1, 1), (1, 1), (2, 1)])
def test_word_timing_requires_a_positive_interval_from_a_nonnegative_start(bounds):
    with pytest.raises(ValueError, match="ordered nonnegative bounds"):
        TimeSpan(*bounds)


def test_review_rejects_an_observation_for_a_different_audio_revision(arrangement):
    take = Take(arrangement.revision, AudioRevision("take", "original"))
    observation = ListenerObservation(
        AudioRevision("take", "repair"),
        "listener",
        EvidenceSource.ISOLATED_VOCAL,
        (),
    )
    with pytest.raises(ValueError, match="different audio revision"):
        TakeReview.assess("review", take, arrangement, observation)


def test_review_rejects_a_different_arrangement_revision(arrangement):
    take = Take(
        ArrangementRevision(arrangement.revision.arrangement_id, "2"),
        AudioRevision("take", "original"),
    )
    observation = ListenerObservation(
        take.original_audio, "listener", EvidenceSource.FULL_MIX, ()
    )
    with pytest.raises(ValueError, match="arrangement revision"):
        TakeReview.assess("review", take, arrangement, observation)


def test_review_uses_value_equality_for_evidence_and_revision_references(arrangement):
    audio = AudioRevision("take", "original")
    take = Take(replace(arrangement.revision), audio)
    observation = ListenerObservation(
        replace(audio),
        "listener",
        EvidenceSource.ISOLATED_VOCAL,
        (
            ObservedWord(b"we".decode(), TimeSpan(0, 20)),
            ObservedWord("softly", TimeSpan(35, 41)),
        ),
    )
    review = TakeReview.assess("review", take, arrangement, observation)
    assert review.outcome is ReviewOutcome.OMISSION
    assert review.observation.source is EvidenceSource.ISOLATED_VOCAL


def test_review_finds_the_neighbors_of_a_word_late_in_a_long_take(arrangement):
    prelude = ("sing",) * 260
    scripture = ScriptureRange("synthetic", 300, 563)
    arrangement = replace(
        arrangement,
        song_passage=replace(arrangement.song_passage, scripture=scripture),
        scripture_words=(*prelude, "with", "great", "joy"),
        placements=(LyricPlacement("verse", "lead", scripture),),
    )
    heard = (
        *(ObservedWord(word) for word in prelude),
        ObservedWord("with", TimeSpan(500, 520)),
        ObservedWord("joy", TimeSpan(630, 680)),
    )
    review = assess_words(arrangement, heard)
    assert review.findings == (
        Finding(
            ExpectedWord("great", 561, 0),
            AuditionWindow(TimeSpan(500, 680), TimingPrecision.INFERRED),
        ),
    )


def test_the_take_and_its_review_keep_immutable_evidence(arrangement):
    take = Take(arrangement.revision, AudioRevision("take", "original"))
    words = (
        ObservedWord("we", TimeSpan(0, 10)),
        ObservedWord("softly", TimeSpan(20, 30)),
    )
    observation = ListenerObservation(
        take.original_audio, "listener", EvidenceSource.FULL_MIX, words
    )
    review = TakeReview.assess("review", take, arrangement, observation)
    (finding,) = review.findings
    values = (
        (take, "original_audio", AudioRevision("take", "repair")),
        (take.original_audio, "revision", "repair"),
        (observation, "listener", "other listener"),
        (words[0], "text", "you"),
        (words[0].timing, "start_ms", 5),
        (review, "review_id", "other review"),
        (finding, "audition_window", None),
        (finding.audition_window, "precision", TimingPrecision.PRECISE),
    )
    for value, field, alternative in values:
        with pytest.raises(FrozenInstanceError):
            setattr(value, field, alternative)
