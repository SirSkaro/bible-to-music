from typing import Protocol

from bible_music.domain.arrangement import Arrangement
from bible_music.domain.take import AudioRevisionRef, Take
from bible_music.domain.take_review import (
    EvidenceSource,
    Finding,
    ObservedWord,
    ReviewOutcome,
    TakeReview,
    TimingPrecision,
)

from .commands import ReviewTakeCommand
from .views import (
    AuditionWindowView,
    EvidenceSourceView,
    FindingView,
    ObservedWordView,
    ReviewOutcomeView,
    TakeReviewView,
    TimingPrecisionView,
)

_OUTCOMES = {
    ReviewOutcome.MATCH: ReviewOutcomeView.MATCH,
    ReviewOutcome.OMISSION: ReviewOutcomeView.OMISSION,
    ReviewOutcome.INCONCLUSIVE: ReviewOutcomeView.INCONCLUSIVE,
}
_EVIDENCE_SOURCES = {
    EvidenceSource.FULL_MIX: EvidenceSourceView.FULL_MIX,
    EvidenceSource.ISOLATED_VOCAL: EvidenceSourceView.ISOLATED_VOCAL,
}
_PRECISIONS = {
    TimingPrecision.PRECISE: TimingPrecisionView.PRECISE,
    TimingPrecision.APPROXIMATE: TimingPrecisionView.APPROXIMATE,
    TimingPrecision.INFERRED: TimingPrecisionView.INFERRED,
}


class TakeReviewInputNotFound(LookupError):
    """The requested take or its arrangement revision is unavailable."""


class TakeReviewLookup(Protocol):
    def load(self, audio_revision: AudioRevisionRef) -> tuple[Take, Arrangement]:
        """Read the exact take and arrangement or raise KeyError."""
        ...


class ReviewTake:
    def __init__(self, lookup: TakeReviewLookup) -> None:
        self._lookup = lookup

    def __call__(self, command: ReviewTakeCommand) -> TakeReviewView:
        """Review an imported take using a recorded listener observation."""
        revision = command.audio_revision
        if revision != command.observation.audio_revision:
            raise ValueError("The observation belongs to a different audio revision.")
        try:
            take, arrangement = self._lookup.load(revision)
        except KeyError:
            raise TakeReviewInputNotFound(
                f"Take {revision.take_id!r}, audio revision {revision.revision!r}, "
                "or its arrangement is unavailable."
            ) from None
        return _review_view(
            TakeReview.assess(command.review_id, take, arrangement, command.observation)
        )


def _review_view(review: TakeReview) -> TakeReviewView:
    return TakeReviewView(
        review_id=review.review_id,
        take_id=review.audio_revision.take_id,
        audio_revision=review.audio_revision.revision,
        arrangement_id=review.arrangement_revision.arrangement_id,
        arrangement_revision=review.arrangement_revision.revision,
        listener=review.observation.listener,
        evidence_source=_EVIDENCE_SOURCES[review.observation.source],
        observed_words=tuple(
            _observed_word_view(word) for word in review.observation.words
        ),
        outcome=_OUTCOMES[review.outcome],
        findings=tuple(_finding_view(finding) for finding in review.findings),
    )


def _observed_word_view(word: ObservedWord) -> ObservedWordView:
    timing = word.timing
    start_ms, end_ms = (timing.start_ms, timing.end_ms) if timing else (None, None)
    return ObservedWordView(word.text, start_ms, end_ms, _PRECISIONS[word.precision])


def _finding_view(finding: Finding) -> FindingView:
    window = finding.audition_window
    return FindingView(
        finding.omitted_word.text,
        finding.omitted_word.source_word_index,
        finding.omitted_word.placement_index,
        AuditionWindowView(
            window.timing.start_ms,
            window.timing.end_ms,
            _PRECISIONS[window.precision],
        )
        if window
        else None,
    )
