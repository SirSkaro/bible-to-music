# Engineering Bible Music

Bible Music is a local Scripture music production workbench. Its producer directs an artist, auditions recordings and chooses the performance people will use to memorize the passage. Build an offline, inspectable path through each use case. An imported recording and a replayed observation are valid inputs from the first slice.

## Atomic and GitHub

Use Atomic for agent repository operations and let trusted Codex hooks record changes with provenance. Use the local Vault to recover project context across sessions. Keep enduring engineering decisions in the checked-in ADRs and glossary.

GitHub remains the collaboration remote. The Git shim maps the shared Atomic view to the Git branch for the maintainer to publish. Work from the main checkout and use `atomic git shim status` to inspect the mapping. Run `atomic git shim reconcile` after the maintainer moves the Git branch, then `atomic git shim verify` to check agreement. Keep Atomic Storage publishing opt-in. See the [Atomic setup skill](.agents/skills/atomic-setup/SKILL.md) and [Git shim guide](https://docs.atomic.dev/getting-started/git-shim).

## Workflow and product rules

1. **Plan the passages.** Resolve the producer’s source passage in the chosen translation and edition. Reject nonexistent ranges such as Titus 4. Validate fixed, partially pinned and artist-proposed cuts identically. Song passages must cover the source once, contiguously and in order. Choose sentence ends, sentence ends or semicolons, or any whole word. Intersect this with an optional verse-end requirement. Validate the final source endpoint too. Expose the offending position and legal alternatives when there is a conflict.
2. **Arrange the expected performance.** For each song passage the producer independently fixes, guides or delegates structure, genre and prompt. Latitude varies choices still open to the artist. A fixed prompt passes verbatim. Surface conflicts between fixed directions before submission. Preserve source-span provenance, section placement and voice. Support repeated Scripture choruses, a single terminal chorus, and an explicitly authorized shared custom refrain. Mark intentional repeats, echoes and simultaneous lines. Account for source coverage before generation.
3. **Generate or import.** An imported take includes its arrangement. Each new full performance is a distinct take. Atomically reserve the maximum cost of any billable operation against the run and the requested generation slots against the song passage. Count each full-song choice as an attempt. Settle confirmed costs, release unused amounts and reconcile uncertain submissions under the original operation identity. Preserve caps and producer-fixed inputs across retries.
4. **Hear, compare and repair.** Give the blind listener only a neutral identifier and the audio. Compare its observation to the arranged performance. Give a targeted listener the exact revision, arrangement, brief and active producer rubric. Distinguish full-mix and isolated-vocal evidence. A finding identifies what the producer should audition and may have precise, approximate, inferred or unknown timing. A local edit or region regeneration creates another audio revision of that take. Review the whole new mix and the joins before ranking.
5. **Rank and audition.** Pool eligible revisions for the same song passage across arrangements and genres under the same rubric version. Return the strongest N, default three, at most one revision per distinct take. The producer may hear three takes from one genre. Preserve the chosen keeper’s exact audio revision for WAV export. In the main desktop workspace show progress, spend/reservations, attempts, QA model, playback and selection. Keep credentials in Settings via secret references.

## Domain-driven design

Use Eric Evans’s ubiquitous language in use cases, examples, tests and producer-facing controls. Use *source passage* for the full selection and *song passage* for one song’s portion. A *take* survives a repair. An *audio revision* is the particular performance file under review. A *keeper* is the revision the producer actually chose. “A producer repairs a take and auditions its new audio revision” is a useful acceptance test name in prose.

An aggregate root owns the invariants that must hold in a single change. The **passage plan** validates the partition. The **arrangement** validates lyric origins and permitted placements. The **production run** grants budget and attempt reservations together. The **take** preserves its revision lineage. A **take review** binds evidence to an exact version. The **finalist list** enforces common passage, comparable rubric and distinct takes. Refer across these boundaries by root identity and immutable version or range values. Use a value object when equality is determined by its contents. Keep storage rows, SDK objects and Qt types outside the model. Update the glossary, single-canvas drawing, preview and affected acceptance examples when a term, boundary or invariant changes. [Domain model](docs/domain/domain-model.drawio) · [Glossary](docs/domain/ubiquitous-language.md) · [Eric Evans, DDD Reference, mirrored copy](https://studylib.net/doc/26315235/ddd-reference-2015-03)

## Architecture and design standards

Use a Python modular monolith. The domain makes decisions. Application use cases orchestrate them and own the ports they call. PySide6 is a driving adapter. Mureka, the listener, local SoundCraft editing, SQLite, file storage and credentials are driven adapters. The composition root wires implementations. Source dependencies point inward even when runtime control flows out to an injected provider.

Kent Beck’s **features and futures** both matter in review. After the feature passes, inspect the next concrete change it makes likely. For example, ask what a second listening model would force you to edit. If a provider field leaks into omission policy, translate it at the adapter now and rerun the same acceptance example. Defer general extension machinery until a real second use warrants it. [Kent Beck, Features Versus Futures, 13:45](https://www.youtube.com/watch?v=AZn7JZiNetA&t=825s) · [Why Does Development Slow?](https://newsletter.kentbeck.com/p/why-does-development-slow)

| SOLID principle | Apply it in a change |
| --- | --- |
| **Single Responsibility Principle (SRP)** | Separate the publisher’s text parser from the producer’s cut-eligibility policy. Ask whose decision would cause each to change. |
| **Open/Closed Principle (OCP)** | Add a new listener behind the current review port. The same comparison examples should pass without a new provider branch in the use case. |
| **Liskov Substitution Principle (LSP)** | Run the same consumer contract against replay and live adapters. Both accept the same valid input and honor revision identity, timing precision and failure semantics. |
| **Interface Segregation Principle (ISP)** | Define the smallest useful contract for each caller. Playback needs seek/play. A repair client needs render. Split a broad audio interface when callers use different capabilities. |
| **Dependency Inversion Principle (DIP)** | Define the listener protocol and its observation at the application boundary. Inject the implementation. Keep SDK imports and response translation inside the adapter. |

| Component Cohesion + Coupling Principles | Apply it in a change |
| --- | --- |
| **Reuse/Release Equivalence Principle (REP)** · cohesion | If consumers reuse an extracted review contract, version its mutually required types as one release. Keep the monolith’s release unit until extraction has a consumer. |
| **Common Closure Principle (CCP)** · cohesion | Put rules that change for one producer decision together. A new permitted ending should be implemented once and used by both manual and artist planning. |
| **Common Reuse Principle (CRP)** · cohesion | Keep the review contract usable by a headless replay. An import of that contract should never require installing desktop or editing tools. |
| **Acyclic Dependencies Principle (ADP)** · coupling | Break a GUI ↔ review import cycle by returning a finding or using an application-owned port. Verify the direction through Import Linter. |
| **Stable Dependencies Principle (SDP)** · coupling | Make replaceable providers depend on the policy and contracts relied on by many callers. Aim dependency arrows toward components with greater responsibility to dependents. |
| **Stable Abstractions Principle (SAP)** · coupling | At stable extension seams, let consumers depend on an abstraction that admits the needed variation. Keep ordinary immutable values concrete. |

Use these principles to explain a consequential design choice in terms of the behavior and the likely next change. [Robert C. Martin, Clean Architecture, chapters 7–11, 13–14](https://www.pearson.com/en-us/subject-catalog/p/clean-architecture/P200000009528/9780134494326) · [The Dependency Rule](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

## Modules and verification

All tests must pass. Lint, complexity, architectural dependency checks, and mutation testing must meet the project’s thresholds. 
Document the full-suite and per-module commands when the build is established.

## When to open another file

| If the change involves… | Open this file for… |
| --- | --- |
| Naming, identity, versioning or transaction ownership | [Glossary](docs/domain/ubiquitous-language.md) and [editable domain model](docs/domain/domain-model.drawio) for meanings, root boundaries and invariants. |
| A module, port, adapter, cross-layer import or new dependency | [ADR 0001](docs/decisions/0001-python-modular-monolith.md) for dependency direction and the cost of introducing a boundary. |
| Billable work, retry, repair, resumption, persistence or a new workflow branch | [ADR 0002](docs/decisions/0002-replaceable-workflow-steps.md) and [production workflow](docs/workflows/production.md) for operation identity, limits and routing. |
| A change in a test gate, listener inputs, rubric or evaluation method | [ADR 0003](docs/decisions/0003-replay-and-live-evaluation.md) for the boundary between software evidence and listening evidence. |
| Cut positions, creative authority, authorized lyrics or finalist eligibility | [ADR 0004](docs/decisions/0004-song-passages-and-creative-authority.md) for conflicts, fixed choices and selection. |
| Implementing or repairing an observable behavior | [Local TDD skill](.agents/skills/tdd/SKILL.md). Use a public use case, aggregate or adapter contract. Take one failing example through green and refactor. |
| Implementing a durable LangGraph adapter | [Local LangChain skill](.agents/skills/langchain-build-agent/SKILL.md). Verify APIs against the installed, locked package. The application owns business transitions. |
| Changing what a runtime reviewer listens for or comparing actual listeners | [Producer’s rubric](docs/listening-rubric.md) and [evaluation procedure](docs/workflows/listener-evaluation.md). Pass the chosen rubric explicitly to targeted review. Keep held-out answers out of model inputs. The producer supplies judgments, weights and eligibility cutoffs. |

**First product change.** Implement the smallest offline take review. Use synthetic lyrics, one genuinely omitted word with evidence from its neighboring words, and one authorized chorus repeat. Return the audition window through the use case and accept the repeat. Follow it with a passage-boundary preview using the [worked examples in ADR 0004](docs/decisions/0004-song-passages-and-creative-authority.md#worked-examples-of-song-boundaries), including conflicting pins and an invalid terminal endpoint.
