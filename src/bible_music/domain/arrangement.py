from dataclasses import dataclass

from .scripture import ScriptureRange, SongPassage


@dataclass(frozen=True)
class ArrangementRevision:
    arrangement_id: str
    revision: str


@dataclass(frozen=True)
class LyricPlacement:
    section: str
    voice: str
    source: ScriptureRange
    repeat: bool = False


@dataclass(frozen=True)
class ExpectedWord:
    text: str
    source_word_index: int
    placement_index: int


@dataclass(frozen=True)
class Arrangement:
    """The Scripture words and ordered lyric placements for one song passage."""

    revision: ArrangementRevision
    song_passage: SongPassage
    scripture_words: tuple[str, ...]
    placements: tuple[LyricPlacement, ...]

    def __post_init__(self) -> None:
        scripture = self.song_passage.scripture
        if len(self.scripture_words) != scripture.stop - scripture.start:
            raise ValueError(
                "Supply one normalized word for each position in the song passage."
            )

        remaining = set(range(scripture.start, scripture.stop))
        placed: set[ScriptureRange] = set()
        for placement in self.placements:
            source = placement.source
            if not scripture.contains(source):
                raise ValueError("A lyric placement must be inside its song passage.")
            if placement.repeat:
                if source not in placed:
                    raise ValueError(
                        "A repeated placement needs an earlier placement of that span."
                    )
                continue
            positions = set(range(source.start, source.stop))
            if not positions.issubset(remaining):
                raise ValueError("Reused Scripture needs an authorized repeat.")
            remaining.difference_update(positions)
            placed.add(source)
        if remaining:
            raise ValueError("Lyric placements must cover the complete song passage.")

    def expected_words(self) -> tuple[ExpectedWord, ...]:
        start = self.song_passage.scripture.start
        return tuple(
            ExpectedWord(self.scripture_words[index - start], index, placement_index)
            for placement_index, placement in enumerate(self.placements)
            for index in range(placement.source.start, placement.source.stop)
        )
