"""Immutable results for callers of the application use cases."""

from dataclasses import dataclass
from enum import StrEnum


class ReviewOutcomeView(StrEnum):
    MATCH = "match"
    OMISSION = "omission"
    INCONCLUSIVE = "inconclusive"


class EvidenceSourceView(StrEnum):
    FULL_MIX = "full_mix"
    ISOLATED_VOCAL = "isolated_vocal"


class TimingPrecisionView(StrEnum):
    PRECISE = "precise"
    APPROXIMATE = "approximate"
    INFERRED = "inferred"


@dataclass(frozen=True)
class AuditionWindowView:
    start_ms: int
    end_ms: int
    precision: TimingPrecisionView


@dataclass(frozen=True)
class FindingView:
    omitted_word: str
    source_word_index: int
    placement_index: int
    audition_window: AuditionWindowView | None


@dataclass(frozen=True)
class ObservedWordView:
    text: str
    start_ms: int | None
    end_ms: int | None
    precision: TimingPrecisionView


@dataclass(frozen=True)
class TakeReviewView:
    review_id: str
    take_id: str
    audio_revision: str
    arrangement_id: str
    arrangement_revision: str
    listener: str
    evidence_source: EvidenceSourceView
    observed_words: tuple[ObservedWordView, ...]
    outcome: ReviewOutcomeView
    findings: tuple[FindingView, ...]


class WordEndingView(StrEnum):
    OTHER = "other"
    SEMICOLON = "semicolon"
    SENTENCE = "sentence"


class BoundaryConflictKindView(StrEnum):
    PIN = "pin"
    PROPOSED_CUT = "proposed_cut"
    SOURCE_END = "source_end"


@dataclass(frozen=True)
class ScriptureRangeView:
    """An edition and its half-open range of word positions."""

    edition: str
    start: int
    stop: int


@dataclass(frozen=True)
class ScriptureWordView:
    text: str
    verse: str
    ending: WordEndingView
    verse_end: bool


@dataclass(frozen=True)
class SongBoundaryView:
    position: int
    before: ScriptureWordView
    after: ScriptureWordView | None


@dataclass(frozen=True)
class BoundaryConflictView:
    kind: BoundaryConflictKindView
    position: int
    boundary: SongBoundaryView | None
    legal_alternatives: tuple[SongBoundaryView, ...]


@dataclass(frozen=True)
class PassagePlanPreviewView:
    source: ScriptureRangeView
    pins: frozenset[int]
    legal_cuts: tuple[SongBoundaryView, ...]
    song_passages: tuple[ScriptureRangeView, ...]
    conflicts: tuple[BoundaryConflictView, ...]
