# ADR 0006 · Annotate Python contracts

**Decision.** Give authored Python functions and methods parameter and return annotations across source, tests, and scripts. The types of `self` and `cls` follow the containing class. Annotate fields that form contracts, including command, domain, view, and port types. Use inference for locals with clear types.

**Reason.** Annotations give callers and IDEs usable signatures and make application boundary rules inspectable. A producer-facing command should make the allowed input values visible at the call site. An explicit optional view field tells a caller when evidence may be absent.

**Verification.** The lint gate runs Ruff's annotation rules. Use precise types and narrow unknown external data at the boundary before use. Keep runtime validation where the application or domain owns it. Revisit adding a pinned static type checker when the project needs compatibility checks across call sites.
