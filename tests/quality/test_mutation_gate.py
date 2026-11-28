import json
import runpy
from collections.abc import Callable, Iterable, Set
from functools import partial
from pathlib import Path
from typing import Protocol

import pytest

type MutationResult = dict[str, str]


class ScoreReport(Protocol):
    def __call__(
        self,
        report: str,
        expected_modules: Set[Path],
        may_have_no_mutants: Set[Path] = frozenset(),
        *,
        minimum_for: Callable[[Path], int] = ...,
    ) -> bool: ...


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


@pytest.fixture
def score_report(monkeypatch: pytest.MonkeyPatch) -> ScoreReport:
    script = Path(__file__).resolve().parents[2] / "scripts" / "check_mutations.py"
    monkeypatch.syspath_prepend(str(script.parent))
    return partial(
        runpy.run_path(str(script))["score_report"], minimum_for=lambda _: 95
    )


def session_report(results: Iterable[tuple[Path, MutationResult | None]]) -> str:
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
    score_report: ScoreReport, nonkill: MutationResult
) -> None:
    at_threshold = session_report([(REVIEW, CONFIRMED)] * 19 + [(REVIEW, nonkill)])
    below_threshold = session_report([(REVIEW, CONFIRMED)] * 18 + [(REVIEW, nonkill)])
    assert score_report(at_threshold, {REVIEW})
    assert not score_report(below_threshold, {REVIEW})


@pytest.mark.parametrize("partial", [None, {**CONFIRMED, "output": "timeout"}])
def test_incomplete_mutation_runs_fail_even_with_enough_confirmed_kills(
    score_report: ScoreReport, partial: MutationResult | None
) -> None:
    report = session_report([(REVIEW, CONFIRMED)] * 30 + [(REVIEW, partial)])
    assert not score_report(report, {REVIEW})


def test_mutation_gate_does_not_average_modules(score_report: ScoreReport) -> None:
    report = session_report(
        [(REVIEW, CONFIRMED)] * 40 + [(PLAN, CONFIRMED), (PLAN, SURVIVOR)]
    )
    assert not score_report(report, {REVIEW, PLAN})


def test_each_module_is_scored_against_its_own_floor(score_report: ScoreReport) -> None:
    report = session_report(
        [(REVIEW, CONFIRMED)] * 9
        + [(REVIEW, SURVIVOR)]
        + [(PLAN, CONFIRMED)] * 19
        + [(PLAN, UNTESTED)]
    )
    assert score_report(
        report, {REVIEW, PLAN}, minimum_for={REVIEW: 90, PLAN: 95}.__getitem__
    )
    assert not score_report(
        report, {REVIEW, PLAN}, minimum_for={REVIEW: 90, PLAN: 96}.__getitem__
    )


def test_gate_requires_results_for_the_selected_module(
    score_report: ScoreReport,
) -> None:
    assert not score_report("", {REVIEW})


def test_a_module_without_mutable_operators_can_have_an_empty_report(
    score_report: ScoreReport,
) -> None:
    wrapper = Path("src/bible_music/adapters/in_memory_scripture.py")
    assert score_report("", {wrapper}, {wrapper})
    assert not score_report(session_report([(wrapper, None)]), {wrapper}, {wrapper})
