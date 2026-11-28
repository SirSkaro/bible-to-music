from bible_music.domain.passage_plan import (
    BoundaryConflict,
    BoundaryConflictKind,
    PassagePlanPreview,
    ScriptureWord,
    SongBoundary,
    WordEnding,
)
from bible_music.domain.scripture import ScriptureRange

from ..views import (
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


def to_passage_plan_preview_view(preview: PassagePlanPreview) -> PassagePlanPreviewView:
    """Project the song passages and the boundary evidence behind the preview."""
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
