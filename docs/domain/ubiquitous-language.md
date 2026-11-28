# Bible Music · Ubiquitous language

These are the words the producer and the software use in the **Scripture music production** bounded context. They name decisions as well as things. For example, “repair this take” preserves its identity and creates a new audio revision. “Generate another take” requests another full performance and consumes a generation attempt.

## Planning a passage

| Term | Meaning in this project |
| --- | --- |
| **Producer** | The person who directs the music, sets limits, provides listening expertise and chooses the keeper. |
| **Artist** | The role that proposes song boundaries and makes or carries out the musical choices delegated by the producer. |
| **Bible edition** | A translation and a particular text edition. Reference resolution, wording, punctuation and verse anchors all belong to this edition. |
| **Scripture range** | A contiguous, edition-bound span. Endpoints can identify positions within a verse. The extent of the range is a value. |
| **Source passage** | The full Scripture range chosen for production. Titus can be the source passage. Titus 4 is an invalid range. |
| **Song passage** | The contiguous part assigned to one song. It may equal the entire source passage. An arrangement identifies it by passage-plan identity, immutable plan revision and Scripture range. |
| **Song boundary** | The position immediately after a whole word at which a song ends. The next word starts the next song passage at an internal cut. A **pinned boundary** is a cut the producer has fixed. |
| **Song boundary policy** | One choice of permitted endings, optionally intersected with a verse-end requirement. A verse end can fall in the middle of a sentence. |
| **Passage plan** · aggregate root | Owns a source passage, its boundary policy, pins and ordered song passages. Approving a revision requires exact coverage in source order and legal endings, including the fixed end of the source. Older approved revisions remain addressable. |

**In conversation.** “Let the artist divide Titus into song passages. Keep this cut fixed. Permit a semicolon only if it also ends the verse.” Both conditions apply at that cut. The same test applies when a producer draws every boundary by hand.

## Directing and recording

| Term | Meaning in this project |
| --- | --- |
| **Producer brief** | The fixed choices, guidance, delegated decisions and permissions for the artist. **Creative authority** identifies who decides structure, genre and prompt independently. **Creative latitude** is the breadth of acceptable exploration on an open choice. |
| **Arrangement** · aggregate root | A versioned specification of the expected performance for one song passage. It owns the section and voice placements and checks the origin of every intended sung word. |
| **Lyric placement** | Words assigned to a musical section and voice, with their source span or authorized additional text. It can identify repeats and overlapping parts. A **musical verse** is a section of the arrangement. A **Scripture verse** is an edition’s reference unit. |
| **Chorus / refrain** | A musical role and its placement. A **repeated Scripture chorus** reuses a declared span. A **single terminal chorus** occurs once at the end. A **shared custom refrain** adds explicitly approved words that can recur across songs. Origin, permission and placement are separate facts. |
| **Take** · aggregate root | One distinct full performance, generated or imported, linked to the arrangement revision it performed. It owns the recording lineage. |
| **Audio revision** · entity within a take | One identifiable version of that performance. The original has no parent. A local render or regenerated region has a parent in the same take. Address it through the take identity and revision key. |
| **Audio revision reference** · value object | The take identity and revision key together identify one exact audio revision. A take assessment query and its observation each carry a reference so the review can check that the evidence belongs to the requested revision. |

**In conversation.** “Use my prompt verbatim. Let the artist explore genres. Keep the chorus as written.” A wide creative latitude still leaves two of these decisions fixed. “This repair improved take two” identifies a new revision of the same performance.

## Listening and choosing

| Term | Meaning in this project |
| --- | --- |
| **Listener observation** | What a listener reports hearing in the specified audio. A blind observation uses audio and a neutral identifier. Record the model or human source, audio revision and timing precision. |
| **Finding** | A reviewable concern, its evidence and uncertainty. A dropped word can be inferred from its neighbors. Say whether the evidence came from the full mix or an isolated vocal. |
| **Audition window** | The interval to play to check a finding. Specify its bounds and precision when supported. With unknown timing, the finding remains available for a whole-take audition. |
| **Producer rubric** | Producer-authored, versioned listening criteria. It distinguishes eligibility rules from ranking preferences and records cues and acceptable counterexamples. Teaching examples and held-out answers have different uses. |
| **Take review** · aggregate root | An assessment of one exact audio revision against the expected arrangement. It owns observations and findings, and records the rubric revision, eligibility and ranking evidence when scored. |
| **Finalist list** · aggregate root | The ranked eligible revisions for one song passage under one rubric revision. It owns the shortlist and the producer’s keeper choice. The list can contain fewer than the requested N. |
| **Finalist** | A role earned by an eligible audio revision. Across all treatments, at most one revision from each distinct take may occupy a slot. |
| **Keeper** | The role of the exact finalist revision the producer selected for export. Keep the producer’s choice even when it differs from the first-ranked recording. |

**In conversation.** “The first three eligible takes were all in the same genre. I chose the second because I could hear every word.” That is a valid shortlist and a valid keeper choice.

## Running production

| Term | Meaning in this project |
| --- | --- |
| **Production run** · aggregate root | One production under a run-wide spending cap and per-song-passage generation limits. It owns the operation ledger and grants funds and generation slots atomically. |
| **Run budget** | The run’s cap, settled spend and outstanding reservations. Available budget equals the cap less spend and reservations. |
| **Paid operation** · entity within a run | A potentially billable action with an identity that survives a timeout or restart. Planning, generation, listening and region repair can all incur costs. |
| **Cost reservation** | The conservative maximum held for an operation before submission. Settlement records the actual charge and releases unused funds. Unknown submission status keeps the reservation outstanding. |
| **Generation attempt** | One requested full performance for a song passage. A request for two full performances needs two slots. An accepted attempt can yield no usable take. Importing a take uses no slot. |
| **Repair allowance** | A bound on repair iterations for a take. A region regeneration uses this allowance and any applicable budget. A fresh full performance uses another generation attempt. |

The six aggregate boundaries are a starting model for the producer’s invariants. The editable drawing shows structural references between them. Workflow branches live separately. [Editable domain model](domain-model.drawio) · [Production workflow](../workflows/production.md) · [Eric Evans, Domain-Driven Design Reference, mirrored copy](https://studylib.net/doc/26315235/ddd-reference-2015-03)
