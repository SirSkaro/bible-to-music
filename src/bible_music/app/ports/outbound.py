from typing import Protocol

from bible_music.domain.arrangement import Arrangement
from bible_music.domain.passage_plan import BibleEdition
from bible_music.domain.scripture import ScriptureRange
from bible_music.domain.take import AudioRevisionRef, Take


class TakeReviewLookup(Protocol):
    def load(self, audio_revision: AudioRevisionRef) -> tuple[Take, Arrangement]:
        """Read the exact take and arrangement or raise KeyError."""
        ...


class ScriptureLookup(Protocol):
    def resolve(
        self, edition_id: str, reference: str
    ) -> tuple[BibleEdition, ScriptureRange]:
        """Resolve a passage or raise KeyError for an unknown edition or reference."""
        ...
