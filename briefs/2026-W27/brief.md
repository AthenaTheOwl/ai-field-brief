<!--
iso_week: 2026-W27
through_date: 2026-06-30
profile_id: builder-tpm
registry_version: 6
matrix_run_id: MTRX-W27-framework-runtime
-->

# Frameworks are becoming the control plane for agent work

**Week of 2026-06-29 - Vol. 9**

## Field thesis

The useful agent framework is no longer a prettier way to call a model. It is becoming the place where work is split, memory is shaped, sandboxes are granted, traces become evals, tool access is governed, and a failed run turns into the next artifact.

The W27 signal is dense because several framework surfaces moved at once. LangChain's blog filled three gaps the old registry would have missed: interpreter isolation, dynamic subagents, and wiki-shaped memory. Google is pushing the same quality loop from another angle through ADK and the Agent Quality Flywheel. AWS is packaging runtime primitives under AgentCore while Strands gives builders a model-driven loop that can sit on top of it. OpenAI's Agents SDK remains the reference shape for typed handoffs, guardrails, sessions, and traces. MCP is the protocol layer that keeps turning those tools into a shared surface.

The practical read: the next brief-worthy agent product has to name its runtime contract. Who owns state, who owns tool policy, who owns memory, who owns evals, and where does the run leave evidence?

## Source refresh

The source registry moved from v5 to v6 and now tracks 188 active sources. The important fix: LangChain Blog was missing even though LangGraph releases were already present. That left a blind spot exactly where framework practice is moving fastest.

Added this week:

| Source | Why it was added | Lane |
|---|---|---|
| LangChain Blog | Agent eval loops, memory, sandbox boundaries, subagents, and LangSmith/LangGraph practice notes | builder-practice |
| LangGraph docs | Durable graph state, interrupts, persistence, and human-in-the-loop control | builder-practice |
| LangSmith docs | Tracing, datasets, feedback, evals, and observability artifact paths | builder-practice |
| OpenAI Agents SDK docs | Handoffs, sessions, guardrails, tracing, and replay-shaped runtime concepts | primary-source |
| Google ADK docs | Google-side baseline for agents, tools, sessions, artifacts, evals, and deployment | primary-source |
| Google Developers AI Blog | Coding-agent quality loops, ADK updates, Gemini CLI, and applied agent guidance | builder-practice |
| AWS Bedrock AgentCore docs | Runtime, memory, identity, gateway, observability, code interpreter, and browser tools | primary-source |
| Strands Agents docs | AWS-backed model-driven agent framework with MCP and AgentCore paths | builder-practice |
| LlamaIndex Blog | Retrieval, workflows, memory, and agent eval patterns | builder-practice |
| CrewAI docs | Crews, flows, tools, knowledge, and operator-console patterns | builder-practice |
| MCP official spec | Protocol drift, tool schema semantics, auth shape, and security effects | primary-source |
| Cloudflare Agents docs | Durable agent state on Workers as a serverless comparator | builder-practice |
| E2B Blog | Sandbox runtime practice beyond release notes | frontier-scout |
| Mem0 Blog | Agent memory extraction, consolidation, portability, and eval claims | frontier-scout |
| Blaxel Blog | Runtime and sandbox startup signal; scout source only until claims are verified | frontier-scout |

## Top signals

### 1. Google named the agent-quality flywheel

**Source:** [Google Developers: Driving the Agent Quality Flywheel from your coding agent](https://developers.googleblog.com/en/driving-the-agent-quality-flywheel-from-your-coding-agent/), [Google ADK docs](https://google.github.io/adk-docs/)

**Payload:** Google's developer post frames agent improvement as a repeatable loop: capture traces, turn behavior into evals, review failures, and feed corrections back into the coding agent. ADK gives that loop concrete primitives: agents, tools, sessions, artifacts, evals, deployment, and multi-agent coordination.

**Mechanism:** The trace becomes the product intake object. The framework defines how weak behavior is converted into a testable change.

**Why this matters:** "Better prompt" is too small a unit of improvement. The useful unit is trace -> diagnosis -> eval -> patch -> rerun.

**Reusable pattern:** Add a `trace_to_change.md` sidecar to every agent repo. Each failed run gets one row: run id, failure class, proposed eval, proposed code or prompt change, owner, close condition.

**Action surface:** `eval`, `run-evidence`, `workflow`

**Try this week:** Pick one failed run record and create a failing eval before changing the prompt. Google uses model-based graders and user-approved optimization; keep a human-checked holdout so the optimizer does not merely learn its grader.

**Systems map:** run trace -> failure label -> eval case -> implementation patch -> next run packet

**Transferable principle:** The loop learns only when a trace becomes a checked artifact.

**Falsification test:** Compare the patched agent with the baseline on an untouched, human-checked set at the same budget. If only the optimizer's own grader improves, hold the patch. A trace can also end in an explicit hold.

**Adoption ladder:** store traces -> label failures -> write evals -> gate patches -> cite run ids in release notes.

**Confidence:** high

**Evidence:** MTRX-W27-EARLY-01


### 2. LangChain is moving orchestration into generated code

**Source:** [LangChain: Introducing dynamic subagents in Deep Agents](https://www.langchain.com/blog/introducing-dynamic-subagents-in-deep-agents), [LangGraph docs](https://docs.langchain.com/oss/python/langgraph/overview)

**Payload:** Dynamic subagents let an agent split work by writing a small orchestration program that creates subagents at run time. The pattern pairs naturally with LangGraph's stateful execution and human-in-the-loop controls.

**Mechanism:** Orchestration becomes a first-class artifact. The worker does not only call tools; it can decide how to fan out a task, assign local context, and collect results.

**Why this matters:** Static subagent lists go stale. Dynamic fan-out fits research sweeps, repo audits, and source scouting where the shape of the work is discovered after the first read.

**Reusable pattern:** Store the generated orchestration plan next to the run record. Treat it as reviewable code, not invisible reasoning.

**Action surface:** `factory`, `review`, `run-evidence`

**Try this week:** For one source sweep, record the subagent split as JSON: task, inputs, allowed files, verifier, output contract.

**Systems map:** task read -> orchestration program -> subagent packet -> worker output -> verifier -> merged artifact

**Transferable principle:** A fan-out plan should be inspectable before its outputs are trusted.

**Falsification test:** Compare dynamic fan-out with the static split on the same tasks, total budget, and verifier. If it adds latency or loses coverage without improving accepted output, keep the static split. Saving the plan alone does not prove throughput.

**Adoption ladder:** static packets -> generated packet preview -> bounded fan-out -> verifier merge -> orchestration replay.

**Confidence:** medium

**Evidence:** MTRX-W27-EARLY-02


### 3. Wiki memory gives long-lived agents a reviewable context file

**Source:** [LangChain: Wiki memory for agents](https://www.langchain.com/blog/wiki-memory), [Mem0 Blog](https://mem0.ai/blog)

**Payload:** LangChain's memory post argues for an agent-readable wiki layer: a maintained summary of durable domain facts, decisions, and context. The post places Mem0 among adjacent memory approaches; it does not benchmark them against a wiki.

**Mechanism:** Memory shifts from "retrieve chunks from the past" to "maintain a compact knowledge object the agent can inspect." The object can be reviewed, versioned, and pruned.

**Why this matters:** A wiki can save repeated synthesis of durable domain knowledge. Chase explicitly excludes some conversation state and fast event logs from that fit. The smaller file still needs links back to the facts it compressed.

**Reusable pattern:** Add `ops/agent-memory.md` to repos with recurring agents. Sections: current objective, durable decisions, failed approaches, open questions, and forbidden shortcuts.

**Action surface:** `memory`, `operator-console`, `run-evidence`

**Try this week:** Convert one messy handoff thread into a five-section agent memory file, then use it as the first context block for the next run.

**Systems map:** prior runs -> memory extraction -> reviewed wiki -> next run context -> update proposal

**Transferable principle:** Memory should be edited like code.

**Falsification test:** On the same held-out questions, compare the wiki with raw retrieval for source fidelity, stale answers, and cost. If compression drops the fact that changes the answer, keep retrieval or use both.

**Adoption ladder:** handoff notes -> wiki memory -> review gate -> stale-section detector -> memory diff in release notes.

**Confidence:** medium

**Evidence:** MTRX-W27-EARLY-03


### 4. AgentCore and Strands package the runtime layer AWS wants builders to standardize on

**Source:** [Amazon Bedrock AgentCore docs](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html), [Strands Agents docs](https://strandsagents.com/latest/), [AWS: web search on AgentCore](https://aws.amazon.com/blogs/aws/announcing-web-search-on-amazon-bedrock-agentcore-ground-your-ai-agents-in-current-accurate-web-knowledge/)

**Payload:** AgentCore names the managed building blocks: runtime, memory, identity, gateway, observability, browser tool, and code interpreter. Strands gives builders a model-driven agent framework that can use those primitives and expose tools through MCP-style paths.

**Mechanism:** The cloud provider is carving the agent system into hosted control points. Runtime, identity, memory, and gateway are no longer side scripts; they are platform objects.

**Why this matters:** This is one managed path for agent systems that need audit, identity, and managed tool access without hand-rolled infra.

**Reusable pattern:** Maintain a runtime-primitives matrix for every agent repo: execution, memory, identity, tool gateway, observability, artifact store, eval gate, and human stop rule.

**Action surface:** `runtime-adapter`, `security`, `deployment`

**Try this week:** Pick one repo and fill the matrix with "owned", "outsourced", or "missing" for each primitive.

**Systems map:** application agent -> runtime -> identity -> gateway -> tool -> observation -> evidence record

**Transferable principle:** Agent architecture is becoming a set of named platform contracts.

**Falsification test:** Map one local and one hosted runtime, then run the same permission and recovery probes. If the matrix cannot predict which probe fails, add the missing behavior before using it to pick a platform.

**Adoption ladder:** name primitives -> map ownership -> add evidence fields -> gate drift -> compare hosted and local runtimes.

**Confidence:** high

**Evidence:** MTRX-W27-EARLY-04


### 5. Sandbox access is becoming a grant, not a convenience

**Source:** [LangChain: Running untrusted agent code without a sandbox](https://www.langchain.com/blog/running-untrusted-agent-code-without-a-sandbox), [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/), [E2B Blog](https://e2b.dev/blog)

**Payload:** LangChain is writing about untrusted code execution and interpreter boundaries. OpenAI's Agents SDK docs keep the runtime concepts close to tools, guardrails, sessions, and traceability. E2B is the scout feed for what breaks in real sandbox practice.

**Mechanism:** Code execution is being pulled behind explicit grants: which files are visible, which tools can run, how outputs are captured, and how the environment is identified.

**Why this matters:** Sandboxes do not make untrusted code safe by themselves. The valuable artifact is the access contract and the evidence that the run obeyed it.

**Reusable pattern:** Add a `sandbox_grant` object to run records that execute code: visible paths, writable paths, denied paths, network mode, max runtime, artifact sink.

**Action surface:** `security`, `runtime-adapter`, `run-evidence`

**Try this week:** Write the grant, enforce it in the runner, then attempt a harmless read of one denied fixture path. A temp working directory alone does not restrict filesystem access.

**Systems map:** task -> sandbox grant -> tool call -> artifact sink -> grant audit -> run record

**Transferable principle:** A sandbox without a grant log is only a different place to make the same mistake.

**Falsification test:** Under the real runner identity, attempt the explicitly denied fixture read and a disallowed network request. Either success fails the grant test. The grant log records the policy; the runner has to enforce it.

**Adoption ladder:** temp workspace -> explicit grant -> denied-path test -> artifact sink -> replay from grant.

**Confidence:** medium

**Evidence:** MTRX-W27-EARLY-05


### 6. MCP needs to be tracked as a protocol source, not only as a tool directory

**Source:** [Model Context Protocol specification](https://modelcontextprotocol.io/specification/), [Smithery MCP Registry](https://smithery.ai/), [Glama MCP Server Directory](https://glama.ai/mcp/servers)

**Payload:** The old registry watched MCP through directories and security commentary, but not the official spec. That is now fixed.

**Mechanism:** Tool directories tell you what people are publishing. The spec tells you which surface can break your assumptions about auth, tools, resources, prompts, sampling, and client behavior.

**Why this matters:** If the portfolio treats MCP as a contract surface, it has to watch the contract itself.

**Reusable pattern:** Pin the MCP spec version in every tool-surface snapshot and record which fields affect the hash.

**Action surface:** `tool-policy`, `schema`, `ci`

**Try this week:** Extend one MCP surface snapshot with `spec_url`, `spec_checked_at`, and `hash_fields`.

**Systems map:** official spec -> tool schema -> snapshot hash -> drift gate -> decision record

**Transferable principle:** A registry is not a standard.

**Falsification test:** Change one protocol field the snapshot declares relevant. The drift gate must catch it; an unrelated spec edit need not change the hash.

**Adoption ladder:** add spec source -> pin spec version -> hash dependent fields -> gate surface drift -> write DEC on changes.

**Confidence:** high

**Evidence:** MTRX-W27-EARLY-06


### 7. The framework comparison should become a repo test, not a paragraph

**Source:** [LlamaIndex Blog](https://www.llamaindex.ai/blog), [CrewAI docs](https://docs.crewai.com/), [Cloudflare Agents docs](https://developers.cloudflare.com/agents/), [Braintrust Product Updates](https://www.braintrust.dev/docs/changelog), [Langfuse Changelog](https://langfuse.com/changelog)

**Payload:** The framework field is too crowded for prose-only comparison. LlamaIndex, CrewAI, Cloudflare, Braintrust, Langfuse, AgentOps, and the vendor SDKs all claim parts of the same lifecycle.

**Mechanism:** A comparison becomes useful only when the same task is run through the same contract: input, tool surface, memory, eval, trace, artifact, and cost.

**Why this matters:** Teams will otherwise pick the framework that has the clearest blog post, not the runtime that fits their failure mode.

**Reusable pattern:** Build a tiny `framework-shootout` fixture: one task, one tool, one memory object, one eval, one trace export. Run it through two frameworks at a time.

**Action surface:** `eval`, `source-registry`, `framework-adapter`

**Try this week:** Compare ADK and LangGraph on one toy task: fetch one source, summarize it into a schema, record trace id, and fail if the citation is missing.

**Systems map:** common task -> framework adapter -> run evidence -> eval result -> comparison memo

**Transferable principle:** Framework taste should be measured against a task, not a launch post.

**Falsification test:** Run both adapters repeatedly under the same cost and timeout limits. Compare accepted outputs, missing citations, recovery, and trace export. A tie is valid; do not invent a loser to justify a migration.

**Adoption ladder:** common fixture -> two adapters -> trace export -> eval gate -> comparison memo -> promoted pattern.

**Confidence:** medium

**Evidence:** MTRX-W27-EARLY-07


## Reusable patterns

| Pattern | Where it showed up | How to use it |
|---|---|---|
| Trace-to-change loop | Google, OpenAI, LangSmith | Failed runs create evals, patches, or explicit hold decisions. |
| Generated orchestration | LangChain dynamic subagents, LangGraph | Store fan-out plans as artifacts; review them like code. |
| Wiki memory | LangChain, Mem0 | Maintain a compact reviewed state file instead of replaying logs. |
| Runtime-primitives matrix | AgentCore, Strands, Cloudflare Agents | Map execution, memory, identity, gateway, observability, artifacts, evals, and stops. |
| Sandbox grant | LangChain, OpenAI Agents SDK, E2B | Declare and test what the code runner can read, write, and emit. |
| Spec-pinned tool surface | MCP spec, Smithery, Glama | Hash tools against a named protocol version and gate drift. |

## Action queue

| Rank | Action | Repo fit | Output |
|---|---|---|---|
| 1 | Add framework runtime sources to the registry | ai-field-brief | registry v6, 188 active sources |
| 2 | Add a trace-to-change sidecar | trace-to-eval-harness | `trace_to_change.md` schema and one sample |
| 3 | Add a runtime-primitives matrix to factory tasks | procurement-negotiation-lab | task YAML section: execution, memory, identity, gateway, observability, artifact sink, eval gate, stop rule |
| 4 | Add MCP spec pinning to tool-surface snapshots | mcp-security-lab, athena-site | spec URL and hash-fields in snapshot report |
| 5 | Add a sandbox grant fixture | procurement-negotiation-lab | denied-path test and run-record grant object |
| 6 | Create a framework-shootout fixture | ai-field-brief or trace-to-eval-harness | one task across ADK and LangGraph with shared eval |

## Action packets

Proposed prototypes; the brief has not run these repo tests.

### Packet A: framework source scout

**Target:** ai-field-brief

**Disposition:** prototype

**Change:** Keep the v6 source additions active and add a weekly `framework-runtime` scout section to the brief template. The section lists new framework posts, new docs pages, runtime primitives touched, and whether the item is top-signal, context, or scout.

**Acceptance:** Reviewed framework items have primary support and a disposition. No source-count or promotion quota; an empty scout section passes.

**Why now:** The old registry missed LangChain Blog while it was publishing exactly the patterns this brief needed.

**Surface:** source-registry, scout. **Expected benefit:** primary-backed dispositions without a promotion quota.

**Risk:** extra feeds crowd out better evidence. **Rollback:** remove the proposed scout section. **Kill:** archive if no reviewed source changes a named build decision.

### Packet B: trace-to-change sidecar

**Target:** trace-to-eval-harness

**Disposition:** prototype

**Change:** Add a small schema for converting a failed run into one of three next artifacts: eval case, implementation patch, or hold decision.

**Acceptance:** A sample failed run validates, and the validator fails if the record lacks a next artifact.

**Why now:** Google and OpenAI are both pointing at the same flywheel. The portfolio already has run evidence; it needs the next-action mapping.

**Surface:** eval, run-evidence. **Expected benefit:** a failure has a tested repair or a reasoned hold.

**Risk:** a generated eval rewards the same mistaken assumption. **Rollback:** restore the baseline and retain the failed case. **Kill:** hold if an independent label does not confirm the failure.

### Packet C: runtime-primitives matrix

**Target:** procurement-negotiation-lab

**Disposition:** prototype

**Change:** Extend factory task packets with a `runtime_primitives` section: execution, memory, identity, gateway, observability, artifact store, eval gate, stop rule.

**Acceptance:** New factory tasks fail validation when a primitive is missing or marked `unknown` without a reason.

**Why now:** AgentCore/Strands makes the platform breakdown explicit. Local factory tasks should carry the same vocabulary.

**Surface:** runtime-adapter, deployment. **Expected benefit:** permission and recovery probes match the ownership map.

**Risk:** a tidy matrix hides provider limits. **Rollback:** restore the previous task schema. **Kill:** stop if the fields cannot predict a concrete probe result.

### Packet D: MCP spec pin

**Target:** mcp-security-lab

**Disposition:** prototype

**Change:** Extend MCP surface diff reports with `spec_url`, `spec_checked_at`, and `hash_fields`.

**Acceptance:** Drift reports name whether a change comes from local implementation, input schema, or protocol-dependent fields.

**Why now:** The registry now watches the official MCP spec. The gate should know which spec it is enforcing against.

**Surface:** tool-policy, schema. **Expected benefit:** a relevant protocol-field mutation triggers drift.

**Risk:** unrelated edits cause false blocks. **Rollback:** restore the old snapshot gate. **Kill:** drop fields that cannot be tied to a runtime assumption.

### Packet E: sandbox grant fixture

**Target:** procurement-negotiation-lab

**Disposition:** prototype

**Change:** Add a fixture that grants one writable temp path, denies one sibling path, runs a harmless command, and records the grant in run evidence.

**Acceptance:** The denied-path read fails; the run record carries visible paths, writable paths, denied paths, network mode, max runtime, and artifact sink.

**Why now:** Code execution is moving behind sandboxes. The portfolio needs a grant contract before it needs another sandbox provider.

**Surface:** security, runtime-adapter. **Expected benefit:** denied fixture reads and network calls fail.

**Risk:** a recorded grant is mistaken for enforcement. **Rollback:** return to the existing restricted runner. **Kill:** stop on any successful denied operation.

## Scout radar

| Item | Why to watch | Promote when |
|---|---|---|
| Mem0 memory eval claims | Memory is becoming a product category, but benchmark claims need checking. | A memory post includes reproducible fixtures or open eval data. |
| Cloudflare Agents | Durable state on Workers may fit small public demos better than heavier orchestration. | A portfolio app needs scheduled stateful agent work. |
| CrewAI flows | Business-process demos may use this shape well. | A repo needs explicit human process lanes when graph-state control is too low-level. |
| LlamaIndex workflows | Retrieval-heavy agents may map better to LlamaIndex than LangGraph. | A source-ingestion repo needs agentic retrieval with citation gates. |
| Blaxel runtime posts | Useful startup signal for sandbox and fleet practice. | A post includes code, failure mode, or pricing detail that changes build decisions. |
| E2B sandbox changes | Sandboxes are now part of replay evidence. | An E2B release changes file, network, or artifact semantics. |
| AgentOps spans | Agent observability schemas may converge around session/replay exports. | Exports can feed trace-to-eval without hand-written adapters. |
| MCP auth changes | Protocol auth will affect every tool-surface gate. | The official spec changes auth or tool visibility semantics. |
| ADK eval patterns | Google's eval primitives may become a strong fixture source. | ADK examples include runnable eval assets. |
| Dynamic subagent planning | Generated orchestration is powerful and easy to abuse. | A framework exposes a clean preview/review hook before execution. |

## Watchlist

1. Dynamic subagents can hide bad decomposition. Revisit when a saved plan misses inputs or exceeds the static baseline budget.
2. Wiki memory can turn stale decisions into fake certainty. Revisit when its source changes or the review date expires.
3. Managed runtimes may limit trace export. Revisit when a run cannot export the fields the local verifier needs.
4. Sandbox grant logs still need local tests. Revisit when a denied read, write, or network probe succeeds.
5. Framework comparisons need shared fixtures. Revisit a selection when the task mix, budget, or required recovery behavior changes.

## Sources reviewed

| Source | Type | Disposition |
|---|---|---|
| LangChain Blog | Primary framework blog | Registry addition |
| LangChain untrusted-code post | Engineering post | Top signal |
| LangChain dynamic-subagents post | Engineering post | Top signal |
| LangChain wiki-memory post | Engineering post | Top signal |
| LangChain trace-loop post | Engineering post | Context |
| LangGraph docs | Primary docs | Registry addition |
| LangSmith docs | Primary docs | Context |
| Google Developers AI Blog | Primary developer blog | Registry addition |
| Google Agent Quality Flywheel | Engineering post | Top signal |
| Google ADK docs | Primary docs | Top signal |
| Google ADK Go 2.0 | Engineering post | Context |
| AWS Bedrock AgentCore docs | Primary docs | Top signal |
| AWS AgentCore web search | Product post | Context |
| Strands Agents docs | Primary docs | Top signal |
| OpenAI Agents SDK docs | Primary docs | Context |
| OpenAI agent-improvement loop | Cookbook | Context |
| MCP official spec | Standards docs | Top signal |
| Cloudflare Agents docs | Primary docs | Scout |
| LlamaIndex Blog | Framework blog | Scout |
| CrewAI docs | Primary docs | Scout |
| E2B Blog | Frontier scout | Scout |
| Mem0 Blog | Frontier scout | Scout |
| Blaxel Blog | Frontier scout | Scout |
| Braintrust Product Updates | Product changelog | Context |
| Langfuse Changelog | Product changelog | Context |
| AgentOps GitHub | GitHub releases | Scout |
| Vercel Workflows | Primary docs | Context |
| Vercel Sandbox | Primary docs | Context |

## Archive notes

- This is a two-day issue for W27. The issue catches up the site and closes the framework-source blind spot.
- LangChain Blog was the user's catch, and the registry now treats it as a weekly source.
- AWS AgentCore and Strands are now tracked separately because they answer different questions: managed runtime primitives versus open framework ergonomics.
- Blaxel and Mem0 are scout sources. They can surface useful early patterns, but claims from those feeds need primary fixtures or code before promotion.

## Closing thought

The agent stack is turning into a set of contracts: state, memory, tool access, runtime, evidence, and repair. A framework is useful when it makes those contracts easier to inspect.
