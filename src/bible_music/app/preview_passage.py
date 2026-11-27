from typing import Protocol

from bible_music.domain.passage_plan import (
    BibleEdition,
    PassagePlan,
    PassagePlanPreview,
    SongBoundaryPolicy,
)
from bible_music.domain.scripture import ScriptureRange


class PassageNotFound(LookupError):
    """The requested passage could not be resolved in the selected edition."""


class ScriptureLookup(Protocol):
    def resolve(
        self, edition_id: str, reference: str
    ) -> tuple[BibleEdition, ScriptureRange]:
        """Resolve a passage or raise KeyError for an unknown edition or reference."""
        ...


def preview_passage(
    scripture: ScriptureLookup,
    edition_id: str,
    reference: str,
    plan_id: str,
    policy: SongBoundaryPolicy,
    pins: frozenset[int] = frozenset(),
    cuts: frozenset[int] = frozenset(),
) -> PassagePlanPreview:
    """Preview a plan with cuts expressed as word positions in the selected edition."""
    try:
        edition, source = scripture.resolve(edition_id, reference)
    except KeyError:
        raise PassageNotFound(
            f"Passage {reference!r} was not found in Bible edition {edition_id!r}."
        ) from None
    return PassagePlan(plan_id, source, policy, pins).preview(edition, cuts)
