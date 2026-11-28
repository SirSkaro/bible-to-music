from bible_music.domain.passage_plan import PassagePlan

from .mapping.passage_preview import to_passage_plan_preview_view
from .ports.outbound import ScriptureLookup
from .queries import PreviewPassageQuery
from .views import PassagePlanPreviewView


class PassageNotFound(LookupError):
    """The requested passage could not be resolved in the selected edition."""


class PreviewPassage:
    def __init__(self, scripture: ScriptureLookup) -> None:
        self._scripture = scripture

    def __call__(self, query: PreviewPassageQuery) -> PassagePlanPreviewView:
        """Preview a plan with cuts expressed as word positions in the selected edition."""
        try:
            edition, source = self._scripture.resolve(query.edition_id, query.reference)
        except KeyError:
            raise PassageNotFound(
                f"Passage {query.reference!r} was not found in Bible edition {query.edition_id!r}."
            ) from None
        plan = PassagePlan(query.plan_id, source, query.policy, query.pins)
        return to_passage_plan_preview_view(plan.preview(edition, query.cuts))
