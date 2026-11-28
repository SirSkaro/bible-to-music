from typing import Protocol

from bible_music.domain.passage_plan import (
    BibleEdition,
    BoundaryConflict,
    BoundaryConflictKind,
    PassagePlan,
    PassagePlanPreview,
    ScriptureWord,
    SongBoundary,
    WordEnding,
)
from bible_music.domain.scripture import ScriptureRange

from .commands import PreviewPassageCommand
from .views import (
    BoundaryConflictKindView,
    BoundaryConflictView,
    PassagePlanPreviewView,
    ScriptureRangeView,
    ScriptureWordView,
    SongBoundaryView,
    WordEndingView,
)

_ENDINGS = {
    WordEnding.OTHER: WordEndingView.OTHER,
    WordEnding.SEMICOLON: WordEndingView.SEMICOLON,
    WordEnding.SENTENCE: WordEndingView.SENTENCE,
}
_CONFLICT_KINDS = {
    BoundaryConflictKind.PIN: BoundaryConflictKindView.PIN,
    BoundaryConflictKind.PROPOSED_CUT: BoundaryConflictKindView.PROPOSED_CUT,
    BoundaryConflictKind.SOURCE_END: BoundaryConflictKindView.SOURCE_END,
}


class PassageNotFound(LookupError):
    """The requested passage could not be resolved in the selected edition."""


class ScriptureLookup(Protocol):
    def resolve(
        self, edition_id: str, reference: str
    ) -> tuple[BibleEdition, ScriptureRange]:
        """Resolve a passage or raise KeyError for an unknown edition or reference."""
        ...


class PreviewPassage:
    def __init__(self, scripture: ScriptureLookup) -> None:
        self._scripture = scripture

    def __call__(self, command: PreviewPassageCommand) -> PassagePlanPreviewView:
        """Preview a plan with cuts expressed as word positions in the selected edition."""
        try:
            edition, source = self._scripture.resolve(
                command.edition_id, command.reference
            )
        except KeyError:
            raise PassageNotFound(
                f"Passage {command.reference!r} was not found in Bible edition {command.edition_id!r}."
            ) from None
        plan = PassagePlan(command.plan_id, source, command.policy, command.pins)
        return _preview_view(plan.preview(edition, command.cuts))


def _preview_view(preview: PassagePlanPreview) -> PassagePlanPreviewView:
    return PassagePlanPreviewView(
        source=_range_view(preview.source),
        pins=frozenset(preview.pins),
        legal_cuts=tuple(_boundary_view(cut) for cut in preview.legal_cuts),
        song_passages=tuple(_range_view(passage) for passage in preview.song_passages),
        conflicts=tuple(_conflict_view(conflict) for conflict in preview.conflicts),
    )


def _range_view(passage: ScriptureRange) -> ScriptureRangeView:
    return ScriptureRangeView(passage.edition, passage.start, passage.stop)


def _word_view(word: ScriptureWord) -> ScriptureWordView:
    return ScriptureWordView(
        word.text, word.verse, _ENDINGS[word.ending], word.verse_end
    )


def _boundary_view(boundary: SongBoundary) -> SongBoundaryView:
    return SongBoundaryView(
        boundary.position,
        _word_view(boundary.before),
        _word_view(boundary.after) if boundary.after else None,
    )


def _conflict_view(conflict: BoundaryConflict) -> BoundaryConflictView:
    return BoundaryConflictView(
        _CONFLICT_KINDS[conflict.kind],
        conflict.position,
        _boundary_view(conflict.boundary) if conflict.boundary else None,
        tuple(_boundary_view(cut) for cut in conflict.legal_alternatives),
    )
