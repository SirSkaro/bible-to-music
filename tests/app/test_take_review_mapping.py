import pytest

from bible_music.app.mapping.take_review_view import to_take_review_view
from bible_music.app.views import (
    AuditionWindowView,
    EvidenceSourceView,
    FindingView,
    ObservedWordView,
    ReviewOutcomeView,
    TakeReviewView,
    TimingPrecisionView,
)
from bible_music.domain.arrangement import ArrangementRevision, ExpectedWord
from bible_music.domain.take import AudioRevisionRef
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


@pytest.mark.parametrize(
    ("window", "expected_window"),
    [
        (
            AuditionWindow(TimeSpan(0, 760), TimingPrecision.INFERRED),
            AuditionWindowView(0, 760, TimingPrecisionView.INFERRED),
        ),
        (None, None),
    ],
)
def test_review_projection_preserves_revision_and_observation_evidence(
    window: AuditionWindow | None, expected_window: AuditionWindowView | None
) -> None:
    review = TakeReview(
        "review-2",
        ArrangementRevision("arrangement-a", "arrangement-v3"),
        ListenerObservation(
            AudioRevisionRef("take-b", "audio-v2"),
            "replayed listener",
            EvidenceSource.ISOLATED_VOCAL,
            (
                ObservedWord("we", TimeSpan(0, 110), TimingPrecision.APPROXIMATE),
                ObservedWord("today"),
            ),
        ),
        ReviewOutcome.OMISSION,
        (Finding(ExpectedWord("sing", 15, 2), window),),
    )

    assert to_take_review_view(review) == TakeReviewView(
        review_id="review-2",
        take_id="take-b",
        audio_revision="audio-v2",
        arrangement_id="arrangement-a",
        arrangement_revision="arrangement-v3",
        listener="replayed listener",
        evidence_source=EvidenceSourceView.ISOLATED_VOCAL,
        observed_words=(
            ObservedWordView("we", 0, 110, TimingPrecisionView.APPROXIMATE),
            ObservedWordView("today", None, None, TimingPrecisionView.PRECISE),
        ),
        outcome=ReviewOutcomeView.OMISSION,
        findings=(FindingView("sing", 15, 2, expected_window),),
    )
