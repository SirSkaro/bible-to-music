from dataclasses import replace

import pytest

from bible_music.app.views import (
    AuditionWindowView,
    PassagePlanPreviewView,
    ScriptureRangeView,
    TimingPrecisionView,
)


def test_a_view_rejects_none_for_a_required_field() -> None:
    window = AuditionWindowView(0, 1100, TimingPrecisionView.INFERRED)

    with pytest.raises(TypeError, match=r"AuditionWindowView\.start_ms"):
        replace(window, **{"start_ms": None})


def test_a_view_rejects_none_in_a_collection_of_required_values() -> None:
    source = ScriptureRangeView("synthetic", 0, 5)
    preview = PassagePlanPreviewView(source, frozenset(), (), (source,), ())

    with pytest.raises(TypeError, match=r"PassagePlanPreviewView\.song_passages"):
        replace(preview, **{"song_passages": (None,)})


def test_view_construction_leaves_domain_rules_to_the_domain() -> None:
    assert AuditionWindowView(20, 10, TimingPrecisionView.INFERRED).end_ms == 10
