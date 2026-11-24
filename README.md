# Bible Music

Bible Music helps a producer turn Scripture into songs that people can memorize word for word. Psalm 119 took seven months to produce. An audition queue that pinpoints a missing consonant or a cut-off ending is valuable even before the application can generate its first song.

## Production vocabulary

| Term | Meaning |
| --- | --- |
| Source passage | The text selected for a production run, identified by reference, translation and edition. Titus is a possible source passage. |
| Song passage | The contiguous part of the source assigned to one song. One song can also cover the entire source. |
| Arrangement | The expected performance of a song passage, including sections, repeats, overlapping parts and any explicitly authorized custom refrain. |
| Take | A recording of one arrangement. A repair creates a new audio revision of that take. |
| Finding | Something the listener or comparison step observed, with the recording and enough evidence for the producer to audition it. |
| Finalists | The strongest recordings for one song passage across all the arrangements, genres and takes tried. The producer chooses the keeper. |

## Engineering decisions

| When working on… | Read |
| --- | --- |
| Application structure, GUI, imports and ports | [ADR 0001 · Python modular monolith](docs/decisions/0001-python-modular-monolith.md) |
| Generation, paid retries, editing, resumption or producer controls | [ADR 0002 · Production workflow](docs/decisions/0002-replaceable-workflow-steps.md) |
| Software verification or listening experiments | [ADR 0003 · Verification and evaluation](docs/decisions/0003-replay-and-live-evaluation.md) |
| Song boundaries, creative authority or finalist selection | [ADR 0004 · Passages and creative authority](docs/decisions/0004-song-passages-and-creative-authority.md) |
| Skills for Codex and the producer's listening criteria | [Skill selection](docs/development/skills.md) |

The [root agent instructions](AGENTS.md) apply throughout the project. The first implementation slice takes a replayed listener observation and returns a phrase the producer can audition. The [development guide](docs/development/README.md) includes the task for the PyCharm checkout. An independent [listening experiment](experiments/README.md) measures whether a real reviewer can hear what the producer hears.
