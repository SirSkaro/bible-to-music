import json
import runpy
from pathlib import Path

import pytest

REVIEW = Path("src/bible_music/domain/take_review.py")
PLAN = Path("src/bible_music/domain/passage_plan.py")
CONFIRMED = {
    "worker_outcome": "normal",
    "test_outcome": "killed",
    "output": "PYTEST_EXIT=1\n",
}
SURVIVOR = {
    "worker_outcome": "normal",
    "test_outcome": "survived",
    "output": "PYTEST_EXIT=0\n",
}
UNTESTED = {**CONFIRMED, "output": "PYTEST_EXIT=5\n"}


@pytest.fixture(scope="module")
def score_report():
    script = Path(__file__).resolve().parents[2] / "scripts" / "check_mutations.py"
    return runpy.run_path(str(script))["score_report"]


def session_report(results):
    return "\n".join(
        json.dumps(
            [
                {
                    "mutations": [
                        {
                            "module_path": str(module),
                            "start_pos": [1, 0],
                            "operator_name": "sample operator",
                        }
                    ]
                },
                result,
            ]
        )
        for module, result in results
    )


@pytest.mark.parametrize("nonkill", [SURVIVOR, UNTESTED])
def test_gate_counts_a_survivor_or_untested_mutant_in_the_denominator(
    score_report, nonkill
):
    at_threshold = session_report([(REVIEW, CONFIRMED)] * 19 + [(REVIEW, nonkill)])
    below_threshold = session_report([(REVIEW, CONFIRMED)] * 18 + [(REVIEW, nonkill)])
    assert score_report(at_threshold, {REVIEW})
    assert not score_report(below_threshold, {REVIEW})


@pytest.mark.parametrize("partial", [None, {**CONFIRMED, "output": "timeout"}])
def test_incomplete_mutation_runs_fail_even_with_enough_confirmed_kills(
    score_report, partial
):
    report = session_report([(REVIEW, CONFIRMED)] * 30 + [(REVIEW, partial)])
    assert not score_report(report, {REVIEW})


def test_mutation_gate_does_not_average_modules(score_report):
    report = session_report(
        [(REVIEW, CONFIRMED)] * 40 + [(PLAN, CONFIRMED), (PLAN, SURVIVOR)]
    )
    assert not score_report(report, {REVIEW, PLAN})


def test_gate_requires_results_for_the_selected_module(score_report):
    assert not score_report("", {REVIEW})


def test_a_module_without_mutable_operators_can_have_an_empty_report(score_report):
    wrapper = Path("src/bible_music/app/review_take.py")
    assert score_report("", {wrapper}, {wrapper})
    assert not score_report(session_report([(wrapper, None)]), {wrapper}, {wrapper})
