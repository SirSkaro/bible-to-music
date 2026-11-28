"""Commands accepted by the Scripture music use cases."""

from dataclasses import dataclass

from bible_music.domain.passage_plan import SongBoundaryPolicy
from bible_music.domain.take import AudioRevisionRef
from bible_music.domain.take_review import ListenerObservation


@dataclass(frozen=True)
class ReviewTakeCommand:
    review_id: str
    audio_revision: AudioRevisionRef
    observation: ListenerObservation


@dataclass(frozen=True)
class PreviewPassageCommand:
    edition_id: str
    reference: str
    plan_id: str
    policy: SongBoundaryPolicy
    pins: frozenset[int] = frozenset()
    cuts: frozenset[int] = frozenset()
