---
name: langchain-build-agent
description: "Apply when implementing Bible Music’s durable LangGraph adapter. Use checked-in decisions and the locked implementation."
---

# Build and modify LangChain applications

This project selects LangGraph only for the durable adapter described in ADR 0002. Use the application's existing ports and inspect locked package source, signatures, local examples and contract tests. The following ecosystem notes help interpret an existing integration.

## Understand the application

Identify the requested behavior, language, package versions, existing agent or
graph, tool interfaces, state, and deployment constraints. For an existing
application, preserve its architecture and explicit provider/model choices unless
the requested change needs a different approach. For a new application, build
the user's actual use case rather than substituting a tutorial demo.

Distinguish ecosystem requests from concrete implementation constraints. A request
to “build an agent with LangChain” leaves the implementation architecture open.
Building with Deep Agents satisfies that ecosystem request.

Requirements such as “use `langchain.agents.create_agent` directly” or “do not add
the `deepagents` package” constrain the implementation. Honor explicit constraints;
do not infer an API choice from the ecosystem name alone.

## How the components relate

Deep Agents uses LangChain's `create_agent` internally, extending it with
preconfigured middleware, tools, and system prompting for capabilities such as
planning, filesystem access, and delegation. It supports further customization
through tools and middleware.

Calling `langchain.agents.create_agent` directly constructs a base LangChain
agent; it does not include the Deep Agents harness. Use Deep Agents' public
builder to get that harness, and verify the corresponding entrypoint in the
installed package for your language.

Both LangChain agents and Deep Agents run on LangGraph, which provides their
underlying execution runtime. LangGraph also supports explicit workflow
orchestration. Composition works in both directions: a LangGraph workflow can
contain a Deep Agent as a node, and a Deep Agent can invoke a LangGraph workflow
exposed as a tool.

## Project architecture

Use the application’s transition and operation contracts. A graph may persist a pause or resume a step. The production run owns the budget. Start with ordinary Python for replay. Keep hosted runtime selection a separate project decision.

## Retrieve the implementation contract

Inspect the manifest, lockfile, and relevant installed packages. Check Deep Agents
availability and version alongside LangChain and LangGraph when building an agent;
these are separate packages. Verify the APIs you intend to use against the
installed versions.

Current documentation may describe a newer release. Match the implementation to
the installed version; do not silently upgrade an existing project to fit an
example. Treat a dependency update as a separate reviewed change. Do not
assume Python and TypeScript expose identical capabilities or defaults.

## Implement at the right layer

Choose the component that owns the behavior. Agent-loop adaptation belongs in
supported middleware; deterministic business routing belongs in workflow control;
tool implementation owns the operation and its authorization. Inspect which
middleware and tools the harness already supplies before adding replacements.

Use runtime context for request identity and dependencies. Decide explicitly
which data is transient, belongs to one conversation, or should survive across
conversations and process restarts. Conversation checkpoints and cross-conversation
memory have different scopes; verify storage lifetime and user isolation.
Verify configuration and inheritance at integration boundaries rather than
assuming that nested agents share all parent settings.

Give tools narrow contracts and descriptions that explain when to call them.
Enforce consequential operations in application code; prompt instructions and
model-visible tool filtering do not provide authorization.

For human review, use the harness's supported review capability for tool calls
and workflow interrupts for other pauses. Implement the caller-facing proposal
and resume flow, accounting for replay of side effects.

## Verify the requested behavior

Exercise the actual agent or graph path, not only construction or imports. Use
realistic inputs to check tool effects, state changes, and the caller's output
contract. When human review is involved, verify that approved or edited actions
execute as reviewed, rejected actions do not execute, and resuming does not
repeat side effects. Separate infrastructure or provider failures from
application logic failures.

## Local reference and updates

Use the exact packages in the project's lockfile. Consult checked-in examples, installed source and tests to resolve a signature. Record unresolved version questions with the adapter. This copy is updated by a reviewed repository diff.
