# ADR 0002 · Compose a resumable production workflow

**Status** · Working implementation decision. Mureka supplies recordings, a selectable multimodal listener reviews them, and SoundCraft supplies local editing and rendering.

## Workflow

| Step | Operation and observable result |
| --- | --- |
| Plan | Resolve the source and [song boundary policy](0004-song-passages-and-creative-authority.md). Retain the exact edition, passage plan, producer-fixed choices and allowed creative latitude for this run. |
| Arrange | Use the artist for delegated decisions. Compile the expected sung sequence and compare its underlying coverage with the song passage. The generator receives arranged lyrics and the resolved prompt. |
| Generate or import | An existing recording can enter at review. For generation, reserve the cost and available attempts, submit the Mureka job and store its provider task ID. Download each returned choice as its own take. [Mureka generation](https://platform.mureka.ai/docs/api/operations/post-v1-song-generate.html) · [Query a task](https://platform.mureka.ai/docs/api/operations/get-v1-song-query-%7Btask_id%7D.html) |
| Listen and compare | First collect a blind audio observation. Compare with the arrangement, then run targeted audio checks for ambiguous pronunciation, endings, overlap, memorability and musical fit as appropriate. Produce a finding tied to an audio revision and playback window, or mark timing unknown. |
| Repair or retry | Route an editable problem such as an abrupt tail or a level imbalance to SoundCraft. If a phrase must be sung again, use a supported Mureka region edit or generate another take within the brief. Repeated weak results can justify a new delegated treatment. Persist the repair and its parent recording. [SoundCraft editing and rendering](https://craft.wiki/apps/soundcraft/ai-agents/) · [Mureka region editing](https://platform.mureka.ai/docs/api/operations/post-v1-song-region-edit.html) |
| Review the render | Bounce a new file. Audition the repaired phrase and join, then evaluate the complete rendered mix before giving it finalist status. Keep original audio and earlier findings addressable. A transcript of the original cannot certify the repair. |
| Rank and audition | Apply the same producer rubric to the eligible renditions for each song passage. Show up to the requested finalist count, expose why each placed and let the producer audition, select and export a keeper. |

Keep the review sequence in the application. A focused listening pass is a workflow decision. Switching between a hosted and local listener is adapter selection. Model the artist, listener and editor as responsibilities behind narrow contracts. A single process can fulfill all three.

## Paid work and recovery

- Treat the dollar cap as a run-wide limit and the attempt limit as per song passage. Display actual spend, outstanding reservations, remaining budget, attempts used and remaining. Represent money with decimal or integer units and keep the pricing assumptions used for estimates.
- Before any chargeable operation, including artist planning, generation, listening or repair, reserve a conservative upper bound atomically with its operation identity. Require spent + existing reservations + new reservation to fit the cap. A provider with no known upper bound can be used under a hard cap only after a usable bound is configured. Deduct actual cost and release the unused reservation when the operation settles.
- The initial counting convention charges one attempt per requested full-song take, including each choice in a multi-output request. Limit the number of requested choices to the remaining slots. A submitted full generation uses its allocated slots even if the recording disappoints or the provider fails after accepting it. A rejected submission with confirmed zero work releases its reservation and slots. A phrase repair belongs to the same take, consumes budget if billable, and receives a bounded repair allowance so a free local edit cannot loop forever. Return the current candidates when a limit is reached.
- Persist the operation intent before an external call, then its provider ID and disposition. Poll an existing task after a restart. A timeout after submission can mean the provider accepted the job. Retain its reservation, use provider reconciliation or documented idempotency when available, and surface an unresolved submission if its disposition cannot be established. A process restart must never by itself authorize a duplicate purchase.
- For the full workflow, use a durable local run store. SQLite plus files for audio is a reasonable workstation default. Keep one authoritative spend ledger. A graph checkpoint holds domain identifiers and step progress. For the first replay, plain Python calls suffice. Introduce a LangGraph adapter when the first paid job must survive a restart or a producer audition resumes a paused run. [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

## Producer GUI

Use one main PySide6 workspace. Put credentials and provider configuration in Settings. Store a secret reference in project data and keep tokens in the operating system's credential store or the process environment. The run screen selects the source and edition, previews legal breaks, records producer direction, and sets the QA model, dollar cap, max attempts per passage and finalist count. Show the run cost and progress alongside the current song passage. Expose findings with playable windows, compare eligible takes for the same passage, and allow the producer to select and export the chosen audio revision.

The GUI submits commands, displays validation and subscribes to progress. It can use the same generation and selection use cases as a headless acceptance driver. For the first listening UI, play a local WAV from a finding and display its actual time resolution. A provider credential or paid run is unnecessary for that slice.
