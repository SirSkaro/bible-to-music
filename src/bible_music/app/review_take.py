from bible_music.domain.take_review import TakeReview

from .mapping.take_review_view import to_take_review_view
from .ports.outbound import TakeReviewLookup
from .queries import AssessTakeQuery
from .views import TakeReviewView


class TakeReviewInputNotFound(LookupError):
    """The requested take or its arrangement revision is unavailable."""


class ReviewTake:
    def __init__(self, lookup: TakeReviewLookup) -> None:
        self._lookup = lookup

    def __call__(self, query: AssessTakeQuery) -> TakeReviewView:
        """Assess an imported take using a recorded listener observation."""
        revision = query.audio_revision
        if revision != query.observation.audio_revision:
            raise ValueError("The observation belongs to a different audio revision.")
        try:
            take, arrangement = self._lookup.load(revision)
        except KeyError:
            raise TakeReviewInputNotFound(
                f"Take {revision.take_id!r}, audio revision {revision.revision!r}, "
                "or its arrangement is unavailable."
            ) from None
        return to_take_review_view(
            TakeReview.assess(query.review_id, take, arrangement, query.observation)
        )
