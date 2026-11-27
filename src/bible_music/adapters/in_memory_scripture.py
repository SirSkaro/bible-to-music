from collections.abc import Mapping

from bible_music.domain.passage_plan import BibleEdition
from bible_music.domain.scripture import ScriptureRange


class InMemoryScripture:
    """Resolve explicitly registered references in Bible editions held in memory."""

    def __init__(
        self,
        editions: Mapping[str, BibleEdition],
        passages: Mapping[tuple[str, str], ScriptureRange],
    ) -> None:
        self._editions = dict(editions)
        self._passages = dict(passages)

    def resolve(
        self, edition_id: str, reference: str
    ) -> tuple[BibleEdition, ScriptureRange]:
        return self._editions[edition_id], self._passages[edition_id, reference]
