from dataclasses import dataclass


@dataclass(frozen=True)
class ScriptureRange:
    """A nonempty half-open range of word offsets in a particular Bible edition."""

    edition: str
    start: int
    stop: int

    def __post_init__(self) -> None:
        if not 0 <= self.start < self.stop:
            raise ValueError(
                "A Scripture range needs ordered nonnegative word offsets."
            )

    def contains(self, other: "ScriptureRange") -> bool:
        return (
            self.edition == other.edition
            and self.start <= other.start
            and other.stop <= self.stop
        )


@dataclass(frozen=True)
class PassagePlanRevision:
    plan_id: str
    revision: str


@dataclass(frozen=True)
class SongPassage:
    plan_revision: PassagePlanRevision
    scripture: ScriptureRange
