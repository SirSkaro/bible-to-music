# Skills for this harness

## Coding agent

| Selection | When to use it | Project-specific boundary |
| --- | --- | --- |
| Matt Pocock's `tdd` | From the first offline slice. Exercise one producer-visible behavior at a time through a public interface. | The review and passage-preview use cases in the ADRs already name the seams. The project's acceptance examples and mutation checks supply the expected outcomes. [Upstream skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md) |
| LangChain's `langchain-build-agent` | When implementing the durable LangGraph integration for a paid operation or a pause/resume workflow. | Use the Python and LangGraph guidance for the chosen adapter. The application owns transitions, budget and retries. [Upstream collection](https://github.com/langchain-ai/langchain-skills) · [Skill listing](https://www.skills.sh/langchain-ai/langchain-skills/langchain-build-agent) |
| Project procedure **Evaluate a listener** | When comparing QA models, prompts, or producer rubric revisions. | Run identically identified recordings, protect the blind pass and holdout labels, and compare misses and audition time. The [experiment protocol](../../experiments/README.md) is the procedure a future local skill can reference. |

For a project-local Codex setup, the corresponding selective install commands are `npx skills add mattpocock/skills --agent codex --skill tdd` and, when the graph work begins, `npx skills add langchain-ai/langchain-skills --agent codex --skill langchain-build-agent`. Record the reviewed upstream revision in the project when adopting a skill. The list above identifies selections for the producer's development checkout.

## Producer-owned runtime skill

**Review a Bible Music take** supplies the listening criteria the producer has learned by making Scripture songs. Its contents are producer-editable and versioned. The runtime explicitly supplies the chosen rubric to the evidence-aware reviewing step. Installing a skill in Codex affects the coding environment. The application needs its own loading path for the rubric to reach a production listener.

Start with the [producer QA worksheet](../../experiments/producer-qa.md). Keep reusable criteria and approved teaching examples together. Keep held-out recordings and answers in the evaluation set. Record the rubric revision with every scored take, and compare takes under the same rubric revision for a given finalist decision. Allow a producer to audition or label an unscored take manually. Until a criterion is supplied, surface observations about it for audition and leave its severity or weight unspecified.

Cut eligibility, Scripture coverage, monetary caps and authorized decisions are program rules. SoundCraft editing and Mureka generation are tools accessed through adapters. Skills carry the judgment and procedures those mechanisms cannot derive from a reference, a receipt or a provider response.
