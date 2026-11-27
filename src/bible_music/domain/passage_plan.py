from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum, auto
from itertools import pairwise

from .scripture import ScriptureRange


class WordEnding(Enum):
    OTHER = auto()
    SEMICOLON = auto()
    SENTENCE = auto()


class PermittedEnding(Enum):
    ANY_WORD = auto()
    SENTENCE_OR_SEMICOLON = auto()
    SENTENCE = auto()


@dataclass(frozen=True)
class ScriptureWord:
    """One display word with ending facts supplied by the edition."""

    text: str
    verse: str
    ending: WordEnding = WordEnding.OTHER
    verse_end: bool = False


@dataclass(frozen=True)
class SongBoundary:
    position: int
    before: ScriptureWord
    after: ScriptureWord | None


@dataclass(frozen=True)
class BibleEdition:
    id: str
    words: tuple[ScriptureWord, ...]

    def boundary_at(self, position: int) -> SongBoundary | None:
        if not 0 < position <= len(self.words):
            return None
        return _boundary_at(self.words, position)


@dataclass(frozen=True)
class SongBoundaryPolicy:
    ending: PermittedEnding
    require_verse_end: bool = False

    def allows(self, word: ScriptureWord) -> bool:
        if self.require_verse_end and not word.verse_end:
            return False
        return (
            self.ending is PermittedEnding.ANY_WORD
            or word.ending is WordEnding.SENTENCE
            or (
                self.ending is PermittedEnding.SENTENCE_OR_SEMICOLON
                and word.ending is WordEnding.SEMICOLON
            )
        )


class BoundaryConflictKind(Enum):
    PIN = auto()
    PROPOSED_CUT = auto()
    SOURCE_END = auto()


@dataclass(frozen=True)
class BoundaryConflict:
    kind: BoundaryConflictKind
    position: int
    boundary: SongBoundary | None
    legal_alternatives: tuple[SongBoundary, ...]


@dataclass(frozen=True)
class PassagePlanPreview:
    source: ScriptureRange
    pins: frozenset[int]
    legal_cuts: tuple[SongBoundary, ...]
    song_passages: tuple[ScriptureRange, ...]
    conflicts: tuple[BoundaryConflict, ...]


@dataclass(frozen=True)
class PassagePlan:
    plan_id: str
    source: ScriptureRange
    policy: SongBoundaryPolicy
    pins: frozenset[int] = frozenset()

    def preview(
        self, edition: BibleEdition, cuts: frozenset[int] = frozenset()
    ) -> PassagePlanPreview:
        source = self.source
        if source.edition != edition.id or source.stop > len(edition.words):
            raise ValueError(
                "The source passage must exist in the selected Bible edition."
            )

        internal_words = range(source.start, source.stop - 1)
        legal_cuts = tuple(self._legal_ends(edition, internal_words))
        legal_positions = {boundary.position for boundary in legal_cuts}
        positions = sorted(self.pins | cuts)
        conflicts = [
            BoundaryConflict(
                BoundaryConflictKind.PIN
                if position in self.pins
                else BoundaryConflictKind.PROPOSED_CUT,
                position,
                edition.boundary_at(position),
                legal_cuts,
            )
            for position in positions
            if position not in legal_positions
        ]
        terminal = _boundary_at(edition.words, source.stop)
        if not self.policy.allows(terminal.before):
            later_words = range(source.stop, len(edition.words))
            later_end = next(self._legal_ends(edition, later_words), None)
            alternatives = legal_cuts if later_end is None else (*legal_cuts, later_end)
            conflicts.append(
                BoundaryConflict(
                    BoundaryConflictKind.SOURCE_END, source.stop, terminal, alternatives
                )
            )
        if conflicts:
            return PassagePlanPreview(
                source, self.pins, legal_cuts, (), tuple(conflicts)
            )

        ends = (source.start, *positions, source.stop)
        song_passages = tuple(
            ScriptureRange(edition.id, start, stop) for start, stop in pairwise(ends)
        )
        return PassagePlanPreview(source, self.pins, legal_cuts, song_passages, ())

    def _legal_ends(
        self, edition: BibleEdition, word_indices: range
    ) -> Iterator[SongBoundary]:
        return (
            _boundary_at(edition.words, index + 1)
            for index in word_indices
            if self.policy.allows(edition.words[index])
        )


def _boundary_at(words: tuple[ScriptureWord, ...], position: int) -> SongBoundary:
    following = words[position] if position < len(words) else None
    return SongBoundary(position, words[position - 1], following)
