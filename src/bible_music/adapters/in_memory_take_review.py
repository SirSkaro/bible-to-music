from collections.abc import Mapping

from bible_music.domain.arrangement import Arrangement, ArrangementRevision
from bible_music.domain.take import AudioRevisionRef, Take


class InMemoryTakeReview:
    """Read imported takes and their exact arrangement revisions from memory."""

    def __init__(
        self,
        takes: Mapping[AudioRevisionRef, Take],
        arrangements: Mapping[ArrangementRevision, Arrangement],
    ) -> None:
        self._takes = dict(takes)
        self._arrangements = dict(arrangements)

    def load(self, audio_revision: AudioRevisionRef) -> tuple[Take, Arrangement]:
        take = self._takes[audio_revision]
        return take, self._arrangements[take.arrangement_revision]
