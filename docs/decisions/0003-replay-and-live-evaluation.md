# ADR 0003 · Verify software and evaluate listeners

**Decision.** Deterministic tests drive public use cases using synthetic text, recorded observations and replay adapters. Each live adapter runs the same behavioral contract where applicable. The default software gate runs all offline tests, lint, formatting, import rules and per-scope mutation checks. Production listening quality is assessed separately on producer-labeled audio.

**Reason.** A replay can prove that a timestamp selects the intended phrase, that a declared repeat is accepted, or that a paid retry is idempotent. Establishing whether a listener can hear a missing consonant requires audio and an independent human judgment. The listener, evaluator and answer key must remain identifiable.

**Calibration.** The blind listener receives audio and a neutral ID only. A targeted review sees the brief, arrangement and active rubric. Withhold the adjudicated answers from both. Use held-out passages, keep the model/prompt/audio revisions and report misses, false alarms, keeper recall and producer audition time with denominators. The producer defines eligibility and weights. A rubric change requires comparable re-scoring before ranking. [Listening procedure](../workflows/listener-evaluation.md) · [Producer worksheet](../listening-rubric.md)

**Gates.** The defaults are 95% confirmed kills per covered module and cyclomatic complexity at most 10 per function. Configure justified overrides in `pyproject.toml` by repository-relative Python file path. Both full and focused commands apply the same overrides. The lint runner uses Ruff's `C901` for the configured cap and runs the other lint and formatting checks on the same scope.

**Mutation evidence.** Cosmic Ray runs the offline behavior and architecture tests in a temporary source copy. Survivors and untested mutants earn zero, and incomplete results fail at every threshold. Report a module with zero generated mutants separately. Reporting per module protects a small new policy from being hidden in a large, well-tested component. Record the reason for an override with its configuration. Keep both root documents in sync when changing a default.

## Acceptance examples to implement

| Given and when | Expected producer-visible outcome |
| --- | --- |
| A lead word is missing between two observed words with timings | Report the omission and the inferred phrase window. Keep the inference explicit. |
| The arrangement calls for a repeated Scripture chorus and the take sings it twice | Accept both placements. A duplicate finding would be a false alarm. |
| A producer fixes the prompt but delegates genre and receives a conflicting proposal | Preserve the prompt verbatim and surface the conflict before dispatch. |
| Three distinct takes in genre A outrank every take in genre B for this song | All three places go to A. Another song passage has its own list. |
| $6 is settled and $1 reserved under a $10 cap, then two workers each reserve $3 | Only one succeeds. Available budget becomes $0. |
| A paid submission times out, or the app restarts after it saved a provider job ID | Reconcile an uncertain submission or poll the existing job. A restart alone consumes no additional funds or attempts. |
| A producer repairs a suspect phrase in a finalist | The original review stays bound to the original. The new render needs its own completed review to qualify. |
