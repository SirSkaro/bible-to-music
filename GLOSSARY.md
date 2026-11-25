# Bible Music · Ubiquitous language

Use these terms when talking with the producer, naming use cases, and writing acceptance examples. The [editable domain model](docs/domain/Bible-Music-Domain-Model.drawio) shows their relationships. Read an arrow in its direction. A count describes how many targets one source can have. An asterisk means any number, and N is the requested finalist count.

## Song passages

| Term | Meaning |
| --- | --- |
| Bible edition | The chosen translation and text edition. Its words, punctuation and verse anchors determine the available material and possible song endings. |
| Scripture range | A contiguous span in one Bible edition. An endpoint inside a verse includes a position in that edition's text. A range can serve either passage role below. |
| Source passage | The complete Scripture selection for a production run. Selecting Titus makes the whole book the source passage. |
| Song passage | The contiguous part of the source assigned to one song. In a one-song plan it can equal the source passage. |
| Song boundary | The position after the last word of a song passage. At an internal boundary, the next word begins the next song passage. |
| Song boundary policy | The permitted endings and the independent verse-end requirement. Sentence endings, semicolons and verse endings are properties of positions in the selected edition. |
| Passage plan | One revision of the ordered song passages and their boundaries for a source. A completed plan covers the whole source once, in order. A producer can set all breaks, pin some, or delegate them. |

**In use.** “Let the artist propose song boundaries for Titus. Allow sentence endings or semicolons, and require each song to end at a verse boundary.” The producer and artist use the same eligibility rule, including at the end of Titus. A plan used for recordings remains identifiable if the producer later moves a break. [Passage and authority rules](docs/decisions/0004-song-passages-and-creative-authority.md)

## Arrangements and takes

| Term | Meaning |
| --- | --- |
| Producer | The person who directs the project, sets the limits, supplies the listening criteria and chooses the keeper. |
| Artist | The role that makes delegated choices about boundaries, song structure, genre or the generation prompt and requests performances within the brief. |
| Producer brief | The producer's choices and direction for a song. For structure, genre and prompt, **creative authority** determines who decides and what is fixed. **Creative latitude** determines how widely the artist can explore an open choice. |
| Arrangement | The expected performance of one song passage. It assigns words to musical sections and parts, including authorized repeats, overlaps, pronunciation cues and any authorized custom refrain. |
| Musical section | A verse, pre-chorus, chorus, bridge or other musical division of an arrangement. It identifies the words and vocal parts assigned to that section. Its placement can specify a deliberate repeat. |
| Custom refrain | Explicitly authorized additional lyrical material, with a known origin and declared placements. It can connect several songs. A Scripture span repeated as a chorus is a planned repetition in the arrangement. |
| Take | One distinct performance of an arrangement, whether generated or imported. Requesting another full performance can produce another take of that same arrangement. |
| Audio revision | One specific recording of a take as originally received or subsequently rendered. A repair produces a new revision of the same take and identifies its parent audio. |

**In use.** “Keep the 2 Peter arrangement's single terminal chorus and generate another take.” A musical verse is an arrangement section. A Scripture verse is a division of the source text. The two can have different boundaries.

## Review and selection

| Term | Meaning |
| --- | --- |
| Listener observation | A record of what a listener heard on one audio revision. A blind observation uses the audio and a neutral ID. Timings carry the precision the listener can support. |
| Finding | A concern or discrepancy that the producer can check. It identifies the audio revision, the supporting evidence, and an audition window when known. A comparison can infer an omission from the words on either side. |
| Audition window | The portion of the audio to play when checking a finding. Its start and end can be approximate. |
| Producer rubric | The versioned listening criteria the producer supplies. It describes audible cues, what makes a recording eligible, and the preferences that affect ranking. |
| Take review | An assessment of a particular audio revision against its arrangement. A scored review identifies the applicable rubric revision. A repaired render receives its own review. |
| Finalist list | The ranked list for one song passage under a common rubric revision. It holds up to N eligible recordings across every arrangement and genre tried for that passage. |
| Finalist | The role of an audio revision that earns a place on a finalist list. Each distinct take can contribute one revision to that list. |
| Keeper | The role of the exact audio revision the producer selects for export after auditioning. The ranking informs that choice. |

**In use.** “Take 2's transcript says *fulfillment*. The finding identifies the phrase where I heard *foo-fillment*. Audition the repaired revision before ranking it.” Both revisions belong to take 2. They compete for one slot between them. Three distinct takes of the same arrangement can earn all three slots. [Producer QA worksheet](experiments/producer-qa.md)

## Production limits

| Term | Meaning |
| --- | --- |
| Production run | One production of a selected source passage under a run budget and per-song-passage attempt limits. |
| Run budget | The run-wide dollar cap and its current accounting. Available budget equals the cap less settled spend and outstanding reservations. |
| Paid operation | An individual potentially billable action such as artist planning, generation, listening or repair. Its identity survives a restart so the application can reconcile it. |
| Cost reservation | The upper bound held against the run budget for a paid operation. Settlement records the actual cost and releases any unused amount. |
| Generation attempt | One requested full-song performance for one song passage. A single generation request can use several attempts. A failed attempt can yield zero takes. |

**In use.** “Try two more takes for this song passage.” That uses two available full-song attempts. “Repair the ending of take 2” creates a new audio revision, uses the repair allowance and consumes budget if the edit is billable. [Counting and recovery rules](docs/decisions/0002-replaceable-workflow-steps.md)
