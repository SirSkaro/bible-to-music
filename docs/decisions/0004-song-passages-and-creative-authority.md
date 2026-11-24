# ADR 0004 · Song passages and creative authority

**Status** · Product decisions from the producer discussion, with an initial policy for conflicting cuts described below.

## Song boundaries

Resolve the source against the selected translation and edition. The Scripture adapter supplies the exact text and verse anchors, with headings, verse numbers and footnotes distinguished from sung text. Report an invalid reference such as Titus 4 before planning. A source passage and a song passage can use the same range representation. An endpoint inside a verse also needs a stable position in that edition's text. Display the verse reference and neighboring words so the producer can identify the break.

| Producer control | Choices and meaning |
| --- | --- |
| Who chooses the breaks? | The producer marks the end of each song, the artist proposes breaks, or the producer pins some breaks and delegates the rest. A proposal can be previewed and edited. |
| Where may a song end? | At a sentence ending, at a sentence ending or semicolon, or after any whole word. The last option leaves punctuation unrestricted. |
| Must it also end at a verse boundary? | When enabled, the chosen position must be the end of a verse **and** satisfy the punctuation choice. When disabled, a qualifying position inside a verse is available. |

Recognize sentence endings in context across verse lines. A verse number, line break, abbreviation or footnote marker does not establish a sentence ending. Associate closing quotes and parentheses with the preceding punctuation. Use edition annotations when available, otherwise use a deterministic text segmenter checked against examples for that edition. Resolve doubtful punctuation during preview. Keep normalization offsets traceable to the original text.

Compute the eligible positions before asking the artist to plan. The artist can then choose breaks that preserve a thought, fit a singable length and respect pinned positions. Validate the complete proposal in code. The ordered, nonempty ranges must cover the source exactly once with no gaps or overlaps. Moving one internal break updates its two neighboring passages. A chapter break can fall inside a song.

**Initial conflict policy.** Apply the ending rules to the last song too. If the selected source ends mid-sentence, name the reference and conflicting rule. Show the nearest eligible ending when one exists and let the producer revise the selection or the rule. Preserve their source and pins until they change them. When the whole source fits one song and its endpoint qualifies, a single song is a valid plan even if there are no legal internal breaks. Give edits to an already-used plan a new revision and keep earlier recordings associated with the passage they actually cover. [Boundary acceptance cases](../examples/boundary-cases.json)

## Arrangements and prompts

Resolve authority independently for structure, genre and Mureka prompt. **Use mine exactly** preserves the supplied decision and defaults on when a producer supplies a finished value. A fixed prompt is passed verbatim. **Use mine as direction** lets the artist adapt the supplied brief. **Let the artist decide** delegates the choice. Allow creative latitude within open decisions, including free text such as “EDM should lead, experiment with the brass.” A model temperature is an optional adapter setting. Custom lyrical material requires explicit permission regardless of creative latitude.

| Arrangement preset | Expected sung text |
| --- | --- |
| Psalm 119 repeated Scripture chorus | An authorized span recurs at designated places in the arrangement. |
| 2 Peter single terminal chorus | The passage moves forward once and its final portion becomes the sole chorus. |
| 1 Peter custom connecting chorus | An explicitly authorized refrain can connect multiple tracks. Record its text and origin once, with each placement declared. |

Compile the expected lyrics from source spans and authorized material. Preserve the source words while representing tags, echoes, simultaneous parts, pronunciation hints and repeated sections separately. Check coverage against the song passage before generation. Then compare each recording against its own arrangement. A sung chorus can legitimately occur twice while its underlying source span belongs to one song passage.

## Finalists

Keep up to the requested number of the strongest eligible recordings **per song passage**, pooled across all arrangements, genres and takes. The producer's example is three finalists. Three takes of the same arrangement can occupy all three places. Keep the evidence, rubric revision and any unresolved concerns visible. Use a stable tie-break, such as original take order, for reproducible replay. A take with multiple repair revisions contributes its selected eligible revision once. When fewer qualify, expose the shortfall and retain other takes for inspection.

A weak genre experiment can receive fewer subsequent attempts when genre is delegated. A strong take from that experiment still competes. A generation retry can reuse an arrangement. Trying a different arrangement requires authority over the choices being changed and creates its own expected lyric sequence. Both actions retain the song passage.
