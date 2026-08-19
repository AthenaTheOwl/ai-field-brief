<!--
iso_week: 2026-W33
through_date: 2026-08-16
profile_id: builder-tpm
registry_version: 12
matrix_run_id: MTRX-W33-routing-contracts
-->

# Seven percent of the calls ate sixty-eight percent of the bill.

**Week 33 through 2026-08-16 - Vol. 16**

## Field thesis

Model routing acquired a price tag this week. In one 145-task experiment, frontier models handled 7 percent of agent calls and consumed 68.4 percent of model spend. The cheap route saved 74 percent and lost six accuracy points. That trade can be managed only when the runtime knows what each call is doing, preserves the state around interruptions, and records the credential and capability boundaries under which it ran. A router without those records is a discount dial. A router with them can become an engineering control.

## Top signals

### 1. Seven percent of calls set the economics of the whole run

**Source:** [LangChain's model-routing experiment](https://blog.langchain.com/how-many-of-your-agents-calls-%61ctually-need-a-frontier-model/)

**Payload:** LangChain ran 145 controlled tasks through three configurations. Frontier models handled 7 percent of calls in the routed arm but accounted for 68.4 percent of its model spend. Routing cut model cost by 74 percent relative to the frontier-only arm while finishing six accuracy points lower. The judge consumed another 21.2 percent of routed spend.

**Mechanism:** Agent cost is concentrated in a few decisions: planning, recovery, judging, and hard tool selection. A router can move routine calls down the model ladder, yet the judge and escalation policy remain part of the bill. The same policy can look efficient or wasteful depending on task mix and failure cost.

**Why it matters:** The factory already assigns S, A, and B model tiers by role. This result supplies a measurement design for the next step: attribute cost and acceptance by role, task class, tier, and escalation reason. The authors also warn that their workload was saturated and the routed arm did not decisively beat a cheap model on value. One workload cannot ratify a portfolio policy.

**Reusable pattern:** Treat routing as a controlled policy with a baseline, an escalation rule, and a quality budget. Report frontier-call share, frontier-spend share, judge-spend share, task acceptance, and rework together.

**Action surface:** cost

**Try this week:** Run a paired factory cohort on the same ratified tasks. Compare all-A against role-based S/A/B routing. Hold prompts, tool leases, gates, and task fixtures constant. Promote only when the routed arm stays inside a predeclared acceptance margin.

**Systems map:** task class -> role -> initial tier -> confidence or failure signal -> escalation -> verdict -> accepted cost per task.

### 2. The test suite learned to run without a provider

**Source:** [OpenAI Agents SDK 0.21](https://github.com/openai/openai-agents-python/releases/tag/v0.21.0)

**Payload:** Version 0.21 introduced deterministic helpers under `agents.testing`, expanded realtime and voice tests, and hardened RunState snapshots, MCP lifecycle isolation, retry backoff, sandbox path grants, and sensitive error handling.

**Mechanism:** Provider-free tests remove network and sampler variance from orchestration checks. They can assert tool order, state transitions, handoffs, guardrail outcomes, and terminal status with fixed inputs. Live-model evaluations still carry model-behavior questions; unit tests can now own the deterministic runtime contract.

**Why it matters:** Agent teams often spend provider tokens to test code paths that contain no model uncertainty. That is slow and noisy. It also hides missing assertions behind a successful API call. The release draws a useful boundary: deterministic lifecycle behavior belongs in ordinary tests, while model quality belongs in an eval set.

**Reusable pattern:** Split verification into a providerless contract suite and a model-backed behavior suite. A runtime release must pass the first; a prompt, model, or policy promotion must pass both.

**Action surface:** eval

**Try this week:** Inventory the factory tests that still shell out to Claude or Codex to prove deterministic state behavior. Replace three with captured protocol fixtures or fakes, then keep one live smoke per CLI family to catch production flag drift.

**Systems map:** typed task -> deterministic runner fixture -> state and event assertions -> provider-backed golden set -> promotion verdict.

### 3. Pending user input became durable before continuation

**Source:** [OpenAI Agents SDK 0.20](https://github.com/openai/openai-agents-python/releases/tag/v0.20.0)

**Payload:** Version 0.20 added `RunState.add_input()` and persisted pending user input before the resumed model call. The same release expanded MCP protocol support and added explicit acknowledgement around sandbox credential exposure.

**Mechanism:** A pause produces state that must survive process death, retry, and operator delay. Persisting the new input before continuation establishes an ordered write boundary. A crash after persistence can be retried; a crash after the model call but before persistence can otherwise duplicate or lose the human decision.

**Why it matters:** Human approval is often treated as a chat event. In a durable workflow it is a state transition with idempotency requirements. The queue executor, checkpoint store, and approval UI must agree on which input was accepted and which continuation consumed it.

**Reusable pattern:** Use persist-before-act for every external decision. Give the input an id, write it to the checkpoint, bind the continuation to that id, and reject duplicate consumption.

**Action surface:** state

**Try this week:** Add a crash-at-boundary test to one factory approval flow: before input persistence, after persistence, and after worker dispatch. Replaying each checkpoint should produce one accepted input and at most one worker invocation.

**Systems map:** interrupt -> human input id -> durable write -> continuation lease -> worker call -> consumed marker -> replay check.

### 4. Model capabilities moved out of the framework's guesswork

**Source:** [Google ADK 2.7](https://github.com/google/adk-python/releases/tag/v2.7.0)

**Payload:** Google ADK 2.7 lets providers declare model capabilities instead of relying on framework inference from model identifiers. It also preserves tool media, thought signatures, server-tool parts, and parallel function results through history.

**Mechanism:** A model name is a weak proxy for supported inputs, tool semantics, reasoning artifacts, and replay behavior. Provider-declared capabilities create an explicit negotiation surface. Preserving provider-specific parts prevents a generic history layer from silently discarding state needed by the next turn.

**Why it matters:** Model routers usually answer which model is cheapest or strongest. They must first answer which model can legally and faithfully continue this run. Capability mismatch is a correctness failure before it becomes a quality regression.

**Reusable pattern:** Route through a capability predicate before a cost or quality policy. Store the selected model, capability snapshot, and any provider-specific history parts in run evidence.

**Action surface:** architecture

**Try this week:** Add a capability manifest to the factory's model registry. Encode tool calling, image input, structured output, reasoning controls, context limit, and resumable-history support. Refuse a route that cannot satisfy the task contract.

**Systems map:** task requirements -> provider capability declaration -> eligible models -> tier policy -> selected model -> evidence snapshot.

### 5. Routing, storage, and interrupts met in one runtime release

**Source:** [Strands harness SDK 1.52](https://github.com/strands-agents/harness-sdk/releases/tag/python/v1.52.0)

**Payload:** Strands 1.52 added a first-class `ModelRouter`, top-level storage configuration, and middleware-initiated interrupts. These followed the previous release's snapshot sessions and batch tool hooks.

**Mechanism:** Middleware can observe a risky or expensive transition, interrupt the run, and rely on a configured store to preserve the boundary. The router then participates in the state machine alongside storage and policy.

**Why it matters:** Cost routing, safety intervention, and resume behavior are often designed by different teams. Their failure modes meet at the same point: the call that should be paused, escalated, or moved to another model. A shared lifecycle contract prevents each layer from inventing its own partial state.

**Reusable pattern:** Put route decisions and interrupts in the event ledger. Store the trigger, prior tier, next tier, checkpoint reference, and policy version. A replay should reproduce the decision from those inputs or explain why it cannot.

**Action surface:** workflow

**Try this week:** Extend one factory task fixture with an uncertainty-triggered escalation. Assert that the B-tier worker stops, the checkpoint persists, the A-tier continuation receives the same task state, and the ledger contains one route transition.

**Systems map:** worker event -> middleware policy -> interrupt -> checkpoint -> route decision -> resumed worker -> terminal evidence.

### 6. The sandbox used a credential it never possessed

**Source:** [E2B SDK 2.39](https://github.com/e2b-dev/E2B/releases/tag/%40e2b%2Fsdk%402.39.0)

**Payload:** E2B 2.39 added workload identity tokens registered by name and injected into approved egress by a proxy callback. Sandbox code can request an authorized outbound call without receiving the credential value.

**Mechanism:** Credential possession and credential use become separate permissions. The workload identifies itself; the egress layer checks the destination and policy; the proxy adds the token after the request leaves the untrusted process.

**Why it matters:** Environment-variable injection gives every tool in the sandbox a chance to read and exfiltrate the same secret. Proxy-side injection narrows the exposure path and creates an audit point. Destination policy, token scope, and log redaction still decide whether the boundary is useful.

**Reusable pattern:** Keep provider secrets outside worker memory. Grant named egress capabilities, bind them to destinations and methods, inject credentials at the proxy, and record use without recording the value.

**Action surface:** security

**Try this week:** Replace one low-risk test credential in a sandbox fixture with a fake egress broker. Prove that the worker process cannot read the value, an approved host receives it, an unapproved host does not, and logs contain only the credential name.

**Systems map:** workload identity -> egress request -> destination policy -> proxy injection -> upstream service -> redacted audit event.

### 7. A runtime contract turned safety claims into inspectable events

**Source:** [Agent Safety Should Be a Runtime Contract](https://arxiv.org/abs/2608.11274)

**Payload:** The position paper organizes 52 reported incidents, proposes twelve trajectory schemas, and includes a false-completion audit. Its central claim is that safety properties should be expressed as runtime-enforced contracts over actions, state, and evidence.

**Mechanism:** A prose instruction can be ignored or lost during delegation. A runtime contract can deny an action, require evidence, or stop a run when a typed invariant fails. The trajectory becomes the object that a reviewer can inspect.

**Why it matters:** The proposal matches the direction of modern agent SDKs, yet the paper does not prove that its contract set reduces incidents in production. It is strongest as a design vocabulary and test inventory. Adoption should proceed through fixtures and measured failure classes.

**Reusable pattern:** Translate a safety claim into four artifacts: a typed invariant, an enforcement point, an emitted event, and a break-then-fix fixture. Claims without all four remain policy prose.

**Action surface:** governance

**Try this week:** Choose one factory rule currently expressed only in a prompt. Implement the invariant at the capability layer, add a denied-action event, and write a fixture that fails before the enforcement change and passes after it.

**Systems map:** safety claim -> typed invariant -> capability check -> allow or deny -> evidence event -> held-out regression fixture.

## Reusable patterns

- **Measure routing as a policy.** Attribute spend, quality, escalation, and rework to the same task cohort.
- **Test deterministic lifecycle code without a provider.** Save live calls for behavior uncertainty and CLI compatibility.
- **Persist external input before acting on it.** Resume from a consumed input id, not conversational memory.
- **Filter by capability before price.** A cheap model that cannot preserve the run contract is ineligible.
- **Broker credentials at egress.** The worker asks for a capability; the proxy holds the secret.
- **Compile prose rules into runtime evidence.** An invariant needs enforcement, an event, and a failure fixture.

## Action queue

| Priority | Move | Owner surface | Proof due |
|---|---|---|---|
| P0 | Run a paired all-A versus S/A/B factory cohort | factory routing | accepted cost, quality delta, escalation rate |
| P0 | Add provider-free lifecycle fixtures for pause, resume, and terminal state | factory tests | deterministic suite with no CLI process |
| P0 | Add persist-before-act crash tests to one approval flow | state/checkpoints | one input, one continuation across three crash points |
| P1 | Add capability declarations to the model registry | model routing | ineligible route rejected before dispatch |
| P1 | Prototype proxy-side credential injection with fake tokens | sandbox security | approved destination succeeds; secret remains unreadable |
| P1 | Convert one prompt-only safety rule into a typed runtime contract | policy/gates | break-then-fix fixture and denial event |

## Action packets

### Packet A - routing economics cohort

Run the same 20 ratified tasks under all-A and role-based S/A/B policies. Freeze task text, context profile, tools, gates, and retry budget. Report accepted cost, first-pass acceptance, rework, judge spend, and frontier-call share. Hold promotion if any critical task class regresses or the confidence interval crosses the declared quality margin.

### Packet B - providerless lifecycle suite

Create deterministic fixtures for tool ordering, handoff, guardrail failure, interrupt, resume, cancellation, and terminal evidence. Keep one real CLI smoke for Claude and one for Codex. A unit test should never need a provider to prove that a state transition is ordered correctly.

### Packet C - durable human input

Give each approval an immutable input id. Persist it before continuation, bind the next worker lease to it, and mark it consumed atomically. Test process death before persistence, after persistence, and after dispatch.

### Packet D - capability-first router

Define provider capability records and task requirements. Compute an eligible set before tier selection. Emit the requirement snapshot, eligible set, selection, and reason into run evidence so a replay can audit the route.

### Packet E - egress credential broker

Use generated test credentials only. Keep values outside the sandbox, authorize a named capability for one host and method, inject at the proxy, and inspect every output sink for leakage. Record the capability name and decision, never the value.

### Packet F - runtime-contract conversion

Select a recurring defect class from the factory ledger. State its invariant, enforcement point, denial event, and held-out fixture. Remove the equivalent prompt warning only after the executable contract has passed a cohort.

## Framework-runtime scout

- **Claude Code 2.1.227-2.1.233** ([releases](https://github.com/anthropics/claude-code/releases)) expanded forked subagents and cross-session messaging while tightening memory cgroups, identity forwarding, and Windows path validation. Watch the delegation boundary and OS-specific regressions.
- **Langfuse 4.7-4.11** ([releases](https://github.com/langfuse/langfuse/releases)) made load-shed observations visible as incomplete and stopped quietly presenting partial traces as whole. That status belongs in any eval fed by production telemetry.
- **LangGraph 1.2.11** ([release](https://github.com/langchain-ai/langgraph/releases/tag/1.2.11)) was reviewed for state-machine changes; no separate signal cleared the promotion gate beyond the checkpoint contract covered last week.

## Scout radar

- **Model routing benchmarks:** seek repeated results on mixed task distributions, not one saturated workload.
- **Provider capability manifests:** watch for a portable schema across OpenAI, Anthropic, Google, and open-model gateways.
- **Interrupt idempotency:** collect crash tests that cover human input, payment, and tool approval boundaries.
- **Credential brokers:** compare proxy injection, workload identity, short-lived tokens, and destination-bound grants.
- **Runtime-contract evidence:** look for controlled studies that measure defect or incident reduction.
- **Incomplete traces:** require telemetry systems to distinguish partial, sampled, dropped, and complete observations.

## Watchlist

- Does role-based model routing preserve acceptance once the workload contains novel architecture and security tasks?
- Can capability declarations be hashed and pinned without freezing provider evolution?
- Do agent SDKs expose durable input consumption as an idempotent primitive across storage backends?
- Will sandbox vendors publish independent tests for proxy-side credential isolation?
- Which runtime-contract invariants survive adversarial tasks without blocking legitimate work?

## Archive notes

- **LangChain routing result:** promoted with a medium-confidence label and the authors' workload caveat.
- **Runtime-contract paper:** promoted as a design and test vocabulary; causal safety claims were not adopted.
- **Claude Code patch cluster:** retained as scout evidence because the individual fixes span multiple surfaces and lack a common controlled evaluation.
- **Framework release volume:** version count alone did not qualify as a signal.

## Sources reviewed

| Source | Status | Note |
|---|---|---|
| Daily Systems Brief folder | ok | Aug 11 and 14 used as private discovery; public claims rechecked |
| Weekly Gen AI Digest folder | ok | no issue after Jul 3; continuity only |
| LangChain model-routing study | ok | promoted with single-workload and accuracy caveats |
| OpenAI Agents SDK releases | ok | 0.20 and 0.21 promoted as separate state and test contracts |
| Google ADK releases | ok | 2.7 capability declaration promoted |
| Strands releases | ok | 1.52 routing, storage, and interrupt cluster promoted |
| E2B releases | ok | 2.39 workload identity promoted |
| Runtime-contract paper | ok | position paper promoted with evidence-class caveat |
| Claude Code releases | ok | 2.1.227-2.1.233 retained in scout radar |
| Langfuse releases | ok | incomplete-observation status retained in scout radar |
| LangGraph releases | ok | reviewed; no additional Top signal |
| Cloudflare Agents, AgentCore, Braintrust, CrewAI, LlamaIndex, AgentOps | ok | reviewed; no additional current-window item cleared the promotion gate |

## Closing thought

The expensive call deserves more than a larger model. It deserves a receipt for why it was necessary.

---

Content: CC BY 4.0. Code: Apache-2.0.
