# Bible Music

Bible Music helps a producer turn Scripture into songs that people can memorize word for word. Psalm 119 took seven months to produce. An audition queue that pinpoints a missing consonant or a cut-off ending is valuable even before the application can generate its first song.

## Domain model and language

The [domain model](docs/domain/Bible-Music-Domain-Model.drawio) has four editable views covering song passages, arrangements and takes, review and selection, and production limits. The [ubiquitous language glossary](GLOSSARY.md) defines the terms used in the model, producer controls and acceptance examples.

## Engineering decisions

| When working on… | Read |
| --- | --- |
| Application structure, GUI, imports and ports | [ADR 0001 · Python modular monolith](docs/decisions/0001-python-modular-monolith.md) |
| Generation, paid retries, editing, resumption or producer controls | [ADR 0002 · Production workflow](docs/decisions/0002-replaceable-workflow-steps.md) |
| Software verification or listening experiments | [ADR 0003 · Verification and evaluation](docs/decisions/0003-replay-and-live-evaluation.md) |
| Song boundaries, creative authority or finalist selection | [ADR 0004 · Passages and creative authority](docs/decisions/0004-song-passages-and-creative-authority.md) |
| Skills for Codex and the producer's listening criteria | [Skill selection](docs/development/skills.md) |

The [root agent instructions](AGENTS.md) apply throughout the project. The first implementation slice takes a replayed listener observation and returns a phrase the producer can audition. The [development guide](docs/development/README.md) includes the task for the PyCharm checkout. An independent [listening experiment](experiments/README.md) measures whether a real reviewer can hear what the producer hears.
