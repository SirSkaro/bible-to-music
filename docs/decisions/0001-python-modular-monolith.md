# ADR 0001 · A local modular monolith with inward dependencies

**Decision.** One Python process can serve the producer, run a repeatable offline test and integrate workstation audio tools. Use Clean Architecture with ports and adapters. The domain owns invariants. The application owns use cases and defines the external capabilities each use case consumes. Adapters translate those contracts. The composition root selects the concrete implementations.

**Ports.** Define narrow application-owned interfaces with `typing.Protocol`. A driving adapter calls the use case through its callable inbound protocol. A use case calls external capabilities through outbound protocols it receives at construction. The composition root binds the implementations. A class or function satisfies a protocol through its signature.

**Application requests.** A wired public use case takes one immutable, application-owned command or query. Both contain scalars, immutable collections, request value objects, and explicitly approved domain value objects. Apply the rule recursively. Use an audio revision reference to ask for an exact performance and let the use case load the take and its associated arrangement through a driven port. An approved domain value becomes part of the caller contract. [ADR 0007](0007-command-query-separation.md)

**Value objects.** Use simple typed fields for simple values. Promote a value when business meaning, equality, or an invariant belongs with its data. A time span owns its ordered bounds. A song boundary policy owns the producer's ending choice. A proposed cut remains a word position the domain can diagnose, including when the producer enters an invalid position.

**Application results.** Public use cases project results into immutable application-owned views, including nested fields and collection elements. Preserve the evidence and identifiers consumers need, such as the exact audio revision and audition timing precision. Reject `None` in required view fields and collection elements. Use optional annotations for expected absence. Domain objects own business invariant validation. [ADR 0008](0008-application-view-mapping.md)

**Reason.** A paid generator, a listener and a desktop framework have independent reasons to change. Replaying an observation exercises the same omission policy as a production listen. The audition client consumes the application result contract as the domain's review and revision models evolve. Keep Qt time objects, provider response shapes and SQLite rows at the edge.

**Verification.** Import Linter enforces inward dependencies and keeps views independent of the domain. Architecture tests match public use-case signatures to their inbound protocols and inspect the command or query fields and view results recursively. Use-case tests verify the wired results, and projection tests exercise the translation of domain values.

**Cost and alternatives.** Translating at each real integration adds code. Physically splitting deployables or releasing each Python module separately would add distribution work for a single workstation. Introduce a protocol when a use case needs that capability. A listener/replay pair supplies the first such seam.

**Change trigger.** Revisit for an independently deployed consumer, or when a mandatory device or model has an incompatible runtime. Add an import contract when a new external SDK enters an adapter. [Martin, The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
