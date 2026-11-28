# ADR 0007 · Name commands and queries by their effects

**Decision.** Use command–query separation at the application boundary. A query reads or computes a result while leaving observable production state intact. A command can modify production state or initiate external work, such as rendering audio or submitting a billable request. The distinction applies to the effects the caller authorizes, including work that may ultimately fail.

Name the immutable request dataclasses in `app.queries` with a `Query` suffix and those in `app.commands` with a `Command` suffix. Both follow the application request value rules. Both may return an immutable application view. A command result can give the caller the exact identity or status of what the operation accomplished. Use the request type and the inbound port contract to communicate effects. The convention applies to the existing modular monolith and shared domain model. [ADR 0001](0001-python-modular-monolith.md)

**Reason.** Martin Fowler credits Bertrand Meyer with command–query separation. In its classical form, a query returns information without changing observable state and a command changes state with no return value. Knowing which operations change state lets callers repeat or reorder read-only calls with more confidence. We keep that behavioral distinction and allow commands to return a view, so a caller can use the result of a write without a separate lookup. [Martin Fowler, Command Query Separation](https://martinfowler.com/bliki/CommandQuerySeparation.html)

**Examples.** `PreviewPassageQuery` computes song boundaries and conflicts. `AssessTakeQuery` turns recorded evidence into an assessment view. Saving that assessment, choosing a keeper, and submitting generation are commands. Saving an assessment can reuse the domain assessment and its view mapper. A save result can report the stored review ID and the exact audio revision.

**Verification.** Architecture tests check the request name, fields, and inbound signature for both kinds. Use-case tests exercise the observable behavior. Keep query dependencies read-only and verify writes or external work through the relevant command contract.
