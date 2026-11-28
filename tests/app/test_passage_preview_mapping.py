from bible_music.app.mapping.passage_preview import to_passage_plan_preview_view
from bible_music.app.views import (
    BoundaryConflictKindView,
    BoundaryConflictView,
    PassagePlanPreviewView,
    ScriptureRangeView,
    ScriptureWordView,
    SongBoundaryView,
    WordEndingView,
)
from bible_music.domain.passage_plan import (
    BoundaryConflict,
    BoundaryConflictKind,
    PassagePlanPreview,
    ScriptureWord,
    SongBoundary,
    WordEnding,
)
from bible_music.domain.scripture import ScriptureRange


def test_passage_preview_projection_preserves_conflicts_and_word_context() -> None:
    earlier = SongBoundary(
        12,
        ScriptureWord("rang.", "1:3", WordEnding.SENTENCE),
        ScriptureWord("Then", "1:3"),
    )
    ready = ScriptureWord("“Ready?”", "1:4", WordEnding.SENTENCE, verse_end=True)
    source_end = SongBoundary(14, ScriptureWord("called,", "1:4"), ready)
    later = SongBoundary(15, ready, None)
    preview = PassagePlanPreview(
        source=ScriptureRange("synthetic", 0, 14),
        pins=frozenset({12}),
        legal_cuts=(earlier,),
        song_passages=(),
        conflicts=(
            BoundaryConflict(BoundaryConflictKind.PROPOSED_CUT, 0, None, (earlier,)),
            BoundaryConflict(
                BoundaryConflictKind.SOURCE_END, 14, source_end, (earlier, later)
            ),
        ),
    )

    earlier_view = SongBoundaryView(
        12,
        ScriptureWordView("rang.", "1:3", WordEndingView.SENTENCE, False),
        ScriptureWordView("Then", "1:3", WordEndingView.OTHER, False),
    )
    ready_view = ScriptureWordView("“Ready?”", "1:4", WordEndingView.SENTENCE, True)
    assert to_passage_plan_preview_view(preview) == PassagePlanPreviewView(
        source=ScriptureRangeView("synthetic", 0, 14),
        pins=frozenset({12}),
        legal_cuts=(earlier_view,),
        song_passages=(),
        conflicts=(
            BoundaryConflictView(
                BoundaryConflictKindView.PROPOSED_CUT, 0, None, (earlier_view,)
            ),
            BoundaryConflictView(
                BoundaryConflictKindView.SOURCE_END,
                14,
                SongBoundaryView(
                    14,
                    ScriptureWordView("called,", "1:4", WordEndingView.OTHER, False),
                    ready_view,
                ),
                (earlier_view, SongBoundaryView(15, ready_view, None)),
            ),
        ),
    )
