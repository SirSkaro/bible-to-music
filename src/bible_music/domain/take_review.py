from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from .arrangement import Arrangement, ArrangementRevision, ExpectedWord
from .take import AudioRevision, Take


class EvidenceSource(Enum):
    FULL_MIX = auto()
    ISOLATED_VOCAL = auto()


class TimingPrecision(Enum):
    PRECISE = auto()
    APPROXIMATE = auto()
    INFERRED = auto()


class ReviewOutcome(Enum):
    MATCH = auto()
    OMISSION = auto()
    INCONCLUSIVE = auto()


@dataclass(frozen=True)
class TimeSpan:
    start_ms: int
    end_ms: int

    def __post_init__(self) -> None:
        if not 0 <= self.start_ms < self.end_ms:
            raise ValueError("A time span needs ordered nonnegative bounds.")


@dataclass(frozen=True)
class ObservedWord:
    """A normalized word. Precision describes the reported timing when present."""

    text: str
    timing: TimeSpan | None = None
    precision: TimingPrecision = TimingPrecision.PRECISE


@dataclass(frozen=True)
class ListenerObservation:
    audio_revision: AudioRevision
    listener: str
    source: EvidenceSource
    words: tuple[ObservedWord, ...]


@dataclass(frozen=True)
class AuditionWindow:
    timing: TimeSpan
    precision: TimingPrecision


@dataclass(frozen=True)
class Finding:
    omitted_word: ExpectedWord
    audition_window: AuditionWindow | None


@dataclass(frozen=True)
class TakeReview:
    review_id: str
    arrangement_revision: ArrangementRevision
    observation: ListenerObservation
    outcome: ReviewOutcome
    findings: tuple[Finding, ...]

    @property
    def audio_revision(self) -> AudioRevision:
        return self.observation.audio_revision

    @classmethod
    def assess(
        cls,
        review_id: str,
        take: Take,
        arrangement: Arrangement,
        observation: ListenerObservation,
    ) -> "TakeReview":
        if take.arrangement_revision != arrangement.revision:
            raise ValueError(
                "The review needs the arrangement revision performed by the take."
            )
        if take.original_audio != observation.audio_revision:
            raise ValueError("The observation belongs to a different audio revision.")

        expected_words = arrangement.expected_words()
        expected = tuple(word.text for word in expected_words)
        observed = tuple(word.text for word in observation.words)
        if expected == observed:
            return cls(
                review_id, arrangement.revision, observation, ReviewOutcome.MATCH, ()
            )

        index = _omission_index(expected, observed)
        if index is None:
            return cls(
                review_id,
                arrangement.revision,
                observation,
                ReviewOutcome.INCONCLUSIVE,
                (),
            )

        finding = Finding(
            expected_words[index], _audition_window(observation.words, index)
        )
        return cls(
            review_id,
            arrangement.revision,
            observation,
            ReviewOutcome.OMISSION,
            (finding,),
        )


def _omission_index(
    expected: tuple[str, ...], observed: tuple[str, ...]
) -> Optional[int]:
    if len(expected) != len(observed) + 1:
        return None
    index = next(
        (
            i
            for i, (wanted, heard) in enumerate(zip(expected, observed, strict=False))
            if wanted != heard
        ),
        len(observed),
    )
    if expected[index + 1 :] != observed[index:]:
        return None
    if index and expected[index - 1] == expected[index]:
        # Any word in this run of identical words could have been omitted.
        return None
    return index


def _audition_window(
    words: tuple[ObservedWord, ...], index: int
) -> Optional[AuditionWindow]:
    if index in (0, len(words)):
        return None
    before = words[index - 1].timing
    after = words[index].timing
    if before is None or after is None or before.end_ms > after.start_ms:
        return None
    return AuditionWindow(
        TimeSpan(before.start_ms, after.end_ms), TimingPrecision.INFERRED
    )
