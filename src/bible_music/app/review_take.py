from bible_music.domain.arrangement import Arrangement
from bible_music.domain.take import Take
from bible_music.domain.take_review import ListenerObservation, TakeReview


def review_take(
    review_id: str,
    take: Take,
    arrangement: Arrangement,
    observation: ListenerObservation,
) -> TakeReview:
    """Review an imported take using a recorded listener observation."""
    return TakeReview.assess(review_id, take, arrangement, observation)
