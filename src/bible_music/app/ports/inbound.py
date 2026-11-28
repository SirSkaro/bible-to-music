from typing import Protocol

from ..queries import AssessTakeQuery, PreviewPassageQuery
from ..views import PassagePlanPreviewView, TakeReviewView


class AssessTakePort(Protocol):
    def __call__(self, query: AssessTakeQuery) -> TakeReviewView:
        """Assess recorded evidence for an exact audio revision."""
        ...


class PreviewPassagePort(Protocol):
    def __call__(self, query: PreviewPassageQuery) -> PassagePlanPreviewView:
        """Preview boundaries for a source passage in the selected edition."""
        ...
