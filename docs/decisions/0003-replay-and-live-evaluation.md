# ADR 0003 · Verify software by replay and listeners against human judgments

**Status** · Working verification strategy.

## Two kinds of evidence

A replay can prove that an omitted word becomes a finding, and that a producer can jump to the right phrase. Only a recording with an independent human judgment can tell us whether a real listener catches the omission. Preserve both feedback loops.

Drive software acceptance through the same public application boundary as the GUI. Arrange a synthetic edition, an arrangement and recorded port responses through fixtures. Exercise the use case, then assert the producer-visible result. Use a small contract suite for each real adapter, including coarse timing, missing timing and unavailable operations. Put live, potentially paid provider checks in a separately invoked suite.

For model evaluation, keep producer labels out of the blind input. Compare models on the same audio revisions and held-out passages. Record prompt, settings, model, rubric revision, and inference cost when known. Measure known defects missed, false alarms, time spent auditioning and how often a known keeper makes the requested top N. Count each with a denominator. Follow the [listening experiment](../../experiments/README.md).

## Acceptance examples for the coding agent

| Given | When | Producer-visible result |
| --- | --- | --- |
| A replay omits one expected word between two timed neighbors | Review the take | The missing word has an inferred audition window. A separately authorized repeat creates no omission or extra-word finding. |
| A valid source, an internal semicolon and a verse ending with a continuing sentence | Preview manual, artist or pinned breaks under the same policy | All three receive the same eligible positions. An illegal cut identifies the violated rule. [Synthetic boundary cases](../examples/boundary-cases.json) |
| A hand-supplied exact prompt, a fixed chorus and permission to change genre elsewhere | Generate another take | The submitted prompt is verbatim and the chorus is preserved. A suggestion conflicting with fixed instructions is surfaced before dispatch. |
| Three eligible takes of arrangement A outrank a take of B for the same song passage | Ask for three finalists | Return all three distinct takes of A in score order. The ranking for another song passage is independent. |
| A run has spent 6 dollars, reserved 1 and has a 10 dollar cap | Two workers each try to reserve 3 dollars | Exactly one reservation succeeds. The displayed remaining budget is zero. |
| Submission succeeded, its provider job ID was saved, and the app restarts | Resume the run | Poll the same job, count its takes once and settle each charge once. An ambiguous submission without an ID remains visible for reconciliation. |
| A repair produces a new WAV | Open the finalists before and after reviewing it | Earlier evidence remains tied to the original. The new revision can enter ranking after it has its own completed review. |

## Automated constraints

| What can regress | Check to build into the harness |
| --- | --- |
| Observable behavior | Use pytest for domain examples, application acceptance and adapter contracts. A narrow PySide6 smoke test exercises one real GUI action such as selecting a finding. [pytest](https://docs.pytest.org/en/stable/) |
| Boundaries and coupling | Use Import Linter to enforce inward imports and keep provider SDKs and Qt out of the core. Include external packages in the import graph when checking them. Give the composition root permission to wire real adapters. [Import Linter contracts](https://import-linter.readthedocs.io/en/stable/contract_types/) |
| Readability and branching | Run Ruff lint and format checks. Enable C901 explicitly, establish the first complexity limit in version control and inspect violations in frequently changed functions. [Ruff C901](https://docs.astral.sh/ruff/rules/complex-structure/) |
| Sensitivity of tests | Use mutmut first on boundary predicates, coverage, reservations and ranking. A survivor that changes AND to OR in the verse-end rule or lets an extra dollar through deserves a targeted assertion. Record the scoped baseline and review new survivors before tightening a threshold. Run the mutation job on a supported POSIX environment. [mutmut](https://mutmut.readthedocs.io/en/latest/) |

As the first implementation adds packages, give the regular verification job the commands `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .` and `uv run lint-imports`. Add `uv run mutmut run` as the separate mutation job for the configured pure-policy scope. Log its counts and surviving changes. A changed threshold, exclusion or expected label needs its own rationale in the change. Keep evidence about software behavior separate from claims about the ear of a particular model.
