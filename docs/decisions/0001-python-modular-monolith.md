# ADR 0001 · A local modular monolith with inward dependencies

**Decision.** One Python process can serve the producer, run a repeatable offline test and integrate workstation audio tools. Use Clean Architecture with ports and adapters. The domain owns invariants. The application owns use cases and defines the external capabilities each use case consumes. Adapters translate those contracts. The composition root selects the concrete implementations.

**Application results.** Public use cases project their results into immutable application-owned views. This applies recursively to nested fields and collection elements. Preserve the evidence and identifiers that consumers need, such as an exact audio revision and the precision of its audition window. Current domain-valued inputs and driven ports can continue to pass domain values into the application.

**Reason.** A paid generator, a listener and a desktop framework have independent reasons to change. Replaying an observation exercises the same omission policy as a production listen. The audition client consumes the application result contract as the domain's review and revision models evolve. Keep Qt time objects, provider response shapes and SQLite rows at the edge.

**Verification.** Import Linter enforces inward dependencies and keeps the views independent of the domain. Architecture tests check the declared result types of public use cases and recursively inspect their view fields. Public use-case tests verify the returned views and their values.

**Cost and alternatives.** Translating at each real integration adds code. Physically splitting deployables or releasing each Python module separately would add distribution work for a single workstation. Introduce a protocol when a use case needs that capability. A listener/replay pair supplies the first such seam.

**Change trigger.** Revisit for an independently deployed consumer, or when a mandatory device or model has an incompatible runtime. Add an import contract when a new external SDK enters an adapter. [Martin, The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
