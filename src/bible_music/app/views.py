"""Immutable results for callers of the application use cases."""

from dataclasses import dataclass, fields
from enum import StrEnum
from types import NoneType
from typing import cast, get_args, get_origin, get_type_hints


class _View:
    def __post_init__(self) -> None:
        annotations = get_type_hints(type(self))
        for field in fields(type(self)):
            _require_value(
                getattr(self, field.name),
                annotations[field.name],
                f"{type(self).__name__}.{field.name}",
            )


def _require_value(value: object, annotation: object, field_path: str) -> None:
    if isinstance(value, NoneType):
        if NoneType not in get_args(annotation):
            raise TypeError(f"{field_path} requires a value")
    elif get_origin(annotation) in (tuple, frozenset):
        item_type = next(iter(get_args(annotation)))
        for item in cast(tuple[object, ...] | frozenset[object], value):
            _require_value(item, item_type, field_path)


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
class AuditionWindowView(_View):
    start_ms: int
    end_ms: int
    precision: TimingPrecisionView


@dataclass(frozen=True)
class FindingView(_View):
    omitted_word: str
    source_word_index: int
    placement_index: int
    audition_window: AuditionWindowView | None


@dataclass(frozen=True)
class ObservedWordView(_View):
    text: str
    start_ms: int | None
    end_ms: int | None
    precision: TimingPrecisionView


@dataclass(frozen=True)
class TakeReviewView(_View):
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
class ScriptureRangeView(_View):
    """An edition and its half-open range of word positions."""

    edition: str
    start: int
    stop: int


@dataclass(frozen=True)
class ScriptureWordView(_View):
    text: str
    verse: str
    ending: WordEndingView
    verse_end: bool


@dataclass(frozen=True)
class SongBoundaryView(_View):
    position: int
    before: ScriptureWordView
    after: ScriptureWordView | None


@dataclass(frozen=True)
class BoundaryConflictView(_View):
    kind: BoundaryConflictKindView
    position: int
    boundary: SongBoundaryView | None
    legal_alternatives: tuple[SongBoundaryView, ...]


@dataclass(frozen=True)
class PassagePlanPreviewView(_View):
    source: ScriptureRangeView
    pins: frozenset[int]
    legal_cuts: tuple[SongBoundaryView, ...]
    song_passages: tuple[ScriptureRangeView, ...]
    conflicts: tuple[BoundaryConflictView, ...]
