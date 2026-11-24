# Working on Bible Music

Use the [project vocabulary](README.md) in commands, tests and the GUI. Read the ADR for the behavior you are changing. Treat producer decisions as product requirements. The implementation choices in the ADRs give a starting design.

Note that all readmes and ADRs in this project are _not final_. They can be appealed, amended, or otherwise augmented as the problem and solution space are better understood. But ALWAYS check with me before making such a change unless it is correcting out-of-date information.

## Implement one observable behavior

- Drive the change through an application use case or an actual adapter contract. Express the outcome in producer language. For example, “the final word is missing” yields a playable phrase window when the listener supplied timing.
- Put the policy in Python code that the desktop GUI, a replay test, and the production workflow can all call. Introduce a port when the application needs an outside capability. Test the same contract against each adapter.
- Keep canonical Scripture, the arranged performance, and the observed performance distinct. Preserve edition, source spans, and authorized repeats. A transcription can spell a word correctly even when the recording audibly mangles it.
- Validate all proposed cuts and arrangements, including model suggestions, through the same domain rules. Run local validation before requesting generation. Hold producer-fixed choices across retries.
- Every paid operation goes through the application's budget and attempt policy. Preserve its operation identity, result and audio revision across restarts. A GUI click and a background retry use the same application entry point.
- Use the [verification guidance](docs/decisions/0003-replay-and-live-evaluation.md) for acceptance, mutation, import and complexity checks. Report the command actually run, its result and the behavior it exercised.
- Use the [skill selections](docs/development/skills.md) where relevant. When changing a listener, its rubric or a calibration case, also follow [the experiment instructions](experiments/AGENTS.md).

Keep each change small enough that the producer can understand the behavior it buys. When a feature makes the next change costly, identify the dependency causing that cost and make a focused structural improvement.
