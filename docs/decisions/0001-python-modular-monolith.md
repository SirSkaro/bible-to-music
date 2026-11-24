# ADR 0001 · A Python modular monolith with ports and adapters

**Status** · Ports and adapters is a project requirement. A single local Python application and PySide6 are the working implementation choices.

## Context

One producer runs the workflow on a workstation. The listening model, music generator, audio editor and presentation can change independently. A producer should be able to audition a finding in the GUI and a test should be able to reproduce the same decision from recorded observations.

## Decision

Keep the domain and application independent of Qt, LangGraph, MCP, provider SDKs and storage. Group related policy by capability as the application grows. The composition root constructs the concrete adapters and injects them. The following boundaries describe responsibilities. Create each package and interface when its first use case needs it.

| Owner | Responsibility and dependency direction |
| --- | --- |
| Domain | Resolve whether a cut, arrangement, expense or finalist selection is admissible using edition data and recorded facts. Plain Python has enough expressive power for these rules. |
| Application | Expose use cases such as previewing song passages, reviewing a take and auditioning finalists. Define the small outbound contracts each use case needs. Own workflow decisions and progress events. |
| Driving adapters | PySide6 translates producer gestures to use-case inputs and progress/results to view state. Acceptance tests can drive the same use cases with a fixture. |
| Driven adapters | Resolve edition text, plan delegated artistic choices, generate a take with Mureka, obtain a listener observation, render a SoundCraft repair or store run state. Translate external formats here. |
| Composition root | Select real or replay adapters. Supply the same policy to both. Keep credentials, filesystem paths and provider clients at the edge. |

## Design consequences for Codex

Apply SOLID at the places where change costs us something. Edition parsing and validating a resolved text span have different reasons to change. The use case owns the listener contract, and a replacement can report coarser or missing timing within that contract. Give playback only the capabilities it consumes. Add another listener by supplying an adapter and running its contract cases.

Apply Martin's common closure and common reuse principles to packaging. Group rules that change together when the producer changes the meaning of an acceptable song. Keep Qt and audio SDK dependencies out of packages used for plain text coverage. Keep imports acyclic and make the more stable policy own its interfaces. [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

Apply Beck's features and futures tradeoff to actual changes. A listener port pays for itself when the first replay runs beside a real listener. A generic plug-in registry can wait for a concrete use case. Prefer an inexpensive, reversible design that keeps the next useful experiment affordable. [Earn *and* Learn](https://newsletter.kentbeck.com/p/earn-and-learn)

PySide6 is the desktop driving adapter. Run long jobs outside the GUI thread, deliver progress through Qt signals, and let the presenter turn application events into labels and controls. A small GUI test can verify that selecting a timed finding requests playback at the correct position. [Qt for Python](https://doc.qt.io/qtforpython-6/) · [QMediaPlayer](https://doc.qt.io/qtforpython-6/PySide6/QtMultimedia/QMediaPlayer.html)
