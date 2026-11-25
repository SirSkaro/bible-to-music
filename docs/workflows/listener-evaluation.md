# Evaluating a listener

**Question.** Given several existing takes of the same arrangement, can the reviewer cut listening time while still surfacing the errors that matter for memorization?

Choose a small set of recordings you have already judged. Start with both a keeper and a reject if you still have them. For each take, record the passage and edition, the performed arrangement, a stable recording ID, and the exact audio version. Keep the producer’s judgment and the times of known defects in a separate answer key. If only an edited take survives, label it as the edited version.

| Case to include if available | What to listen for |
| --- | --- |
| The take with “foo-fillment” | Does a pronunciation check flag the missing consonant even if the transcript spells the word correctly? |
| A take with an intentional echo or round | Does the reviewer preserve a deliberate repeat while catching a genuine omission in the lead? |
| A take with an abrupt ending | Can the producer jump to the cut-off note and hear enough context to decide whether it needs repair? |
| A clean take the producer would keep | How much time do false alarms add to the review? |

## Run and compare

1. Give the transcriber the audio and a neutral take ID. Compare its transcript with the arrangement afterward. A separate musical review may see the brief when judging instruction fit.
2. Retain the listener output with its provider, model or checkpoint, prompt revision, settings, and recording ID. Identify any approximate time windows. Keep evidence from each model attributable when trying a second provider.
3. Review the flagged windows. Check the answer key and listen through the candidate you would choose. Record any defect you heard that the system missed. A missed defect on the finalist matters even when its ranking was correct.
4. Compare runs on the same takes. Count known defects missed, count clean takes needlessly flagged, and time the producer’s review including the final listen. Once there is a ranking step, also check how often a previously selected keeper appears in the requested finalists (three in the producer’s example). Keep a few song passages apart from prompt tuning for that comparison.

Record a result as a count with its denominator, such as two missed omissions out of ten known omissions. If a case lacks human labels, mark it unscored. A transcription match can support text coverage. Pronunciation, endings, genre, and ease of memorization each need their own evidence.

## Applying the producer's criteria

Use the [producer QA worksheet](../../producer/listening-rubric.md) to turn a known keeper, a known reject or a pair of near-misses into a teachable criterion. Keep teaching examples distinct from scored holdouts. Store the active rubric revision on each evidence-aware review. Report any uncalibrated criterion as such.

A useful first comparison is the same arrangement under two listeners. Hold the mix, model inputs other than the listener selection, and producer labels constant. Record which known defects each listener failed to flag and how many minutes the producer spent checking the results.
