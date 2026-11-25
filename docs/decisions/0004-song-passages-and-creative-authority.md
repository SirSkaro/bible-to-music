# ADR 0004 · Song passages, creative authority and finalist selection

**Decision.** Use the producer's terms *source passage* and *song passage*. A song passage can equal its source. Boundaries between them are edition-specific word positions. A complete plan covers the selected source exactly once in order. Manual, pinned and delegated cuts all use the same validator.

**Ending policy.** Choose sentence endings, sentence endings or semicolons, or any whole word. Intersect that choice with the optional verse-end requirement. A period in an abbreviation is insufficient evidence of a sentence end. Closing quotation marks can follow the terminal punctuation. Validate the fixed end of the source as well as each internal cut. Keep display and normalized word offsets traceable to the original edition. Distinguish headings, verse numbers and footnotes from sung text. Compute eligible positions before asking the artist to propose a plan. Show the reference and neighboring words when restrictions cannot be satisfied. A producer must be able to inspect and revise the choice before submission.

**Authority.** Fixed, guided and delegated decisions apply independently to structure, genre and generation prompt. Default a finished producer-supplied value to fixed. A fixed prompt reaches the generator verbatim. Guided decisions can carry free text, such as “let EDM lead and experiment with brass.” Creative latitude controls the breadth of choices left open. A provider temperature can help implement that intent. It has no authority over fixed choices. Keep permission for extra lyrical text explicit regardless of latitude. A chorus can repeat source spans, appear only once at the end, or contain an authorized shared custom refrain. Retain the origin and placement of each line and voice.

**Ranking.** A genre quota could displace a stronger recording. When genre is delegated, poor results can reduce future attempts in that genre. Every eligible take still competes on its merits. Rank up to the requested number of eligible distinct takes for one song passage across all treatments under one rubric revision. A take and its repaired render can occupy one slot between them. The producer can select any finalist as keeper. Expose tied scores for audition with a deterministic display order, initially original take order. Record the audio revision that won.

## Worked examples of song boundaries

Suppose a synthetic Bible edition contains these four verses. The verse numbers mark where each verse begins.

> **1:1** At dawn the singers gathered  
> **1:2** beside the river;  
> **1:3** then the bells rang. The choir waited; everyone listened.  
> **1:4** Dr. Vale called, “Ready?”

The producer can allow songs to end at a sentence ending, at a sentence ending or semicolon, or after any whole word. **Require a verse ending** is an independent choice. When enabled, a position must satisfy both the selected ending rule and the verse-end requirement. The same rules apply to producer-selected cuts, artist-proposed cuts, and the final word of the source passage.

### Where could a song end?

| Position | Which rules allow the song to end here? | Is it also a verse ending? |
| --- | --- | --- |
| After “gathered” in 1:1 | Only **any whole word**. The sentence continues into 1:2. | Yes |
| After “river;” in 1:2 | **Sentence ending or semicolon**, or **any whole word**. | Yes |
| After “rang.” in 1:3 | All three rules. A sentence ends partway through the verse. | No |
| After “waited;” in 1:3 | **Sentence ending or semicolon**, or **any whole word**. | No |
| After “listened.” in 1:3 | All three rules. The sentence and verse end together. | Yes |
| After “Dr.” in 1:4 | Only **any whole word**. The period belongs to an abbreviation. | No |
| After the quoted question “Ready?” in 1:4 | All three rules. The closing quotation mark belongs with the question. | Yes |

### What happens to a passage plan?

- **A pinned cut at a semicolon.** The producer selects 1:1–1:4 and pins a cut after “river;”. With semicolons allowed and verse endings required, the plan produces two songs. The first ends after “river;” and the second after “Ready?” Switching to sentence endings only makes the pin invalid. The preview identifies the conflict and leaves the pin in place for the producer to revise.
- **A sentence ending inside a verse.** For the same source, the producer chooses sentence endings and places a cut after “rang.” The first song ends there, and the second begins with “The choir waited” and continues through “Ready?” Turning on the verse-end requirement makes that cut invalid because 1:3 continues past “rang.”
- **A source that ends mid-sentence.** The producer selects only 1:1 and requires sentence endings. Even with no internal cuts, the plan is invalid. Its only song would end after “gathered,” partway through a sentence. The preview identifies the source endpoint as the conflict so the producer can revise the selection or the rule.
- **A source that fits one song.** The producer selects 1:1–1:3, requires both a sentence ending and a verse ending, and chooses no internal cuts. The plan is valid as one song because “listened.” satisfies both requirements. Earlier eligible positions are available cuts, not mandatory ones.