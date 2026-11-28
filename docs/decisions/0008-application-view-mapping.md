# ADR 0008 · Map domain results to application views

**Decision.** Use small, typed functions in `app.mapping` to project domain results into immutable application views. A use case loads its inputs, runs the domain operation, and hands the completed result to its mapper. Mappers translate values and preserve ordering, exact identities, and expected absence. Views validate required values for presence. Business policy and invariant validation live in the domain. [ADR 0001](0001-python-modular-monolith.md)

**Reason.** Domain decisions and their presentation change for different reasons. Take assessment binds evidence to the exact audio and arrangement revisions. A projection can change which evidence fields the caller sees while the assessment continues to own those rules. A later save-review command can project the same assessment using the same mapping. [ADR 0007](0007-command-query-separation.md)

**Verification.** Test the mapping functions directly with completed domain results. Take review cases cover revision identity, timing precision, evidence source, and an absent audition window. Passage preview cases cover boundary conflicts, missing neighboring words, and legal alternatives. Keep public use-case tests to verify the path from request through domain policy to the returned view.
