<!--
iso_week: 2026-W34
through_date: 2026-08-23
profile_id: builder-tpm
registry_version: 13
matrix_run_id: MTRX-W34-repeatability-control
-->

# Sixty-five percent became twenty-five when the workflow ran twenty times.

**Week 34 through 2026-08-23 - Vol. 17**

## Field thesis

The best result in a new benchmark for stateful business agents was 65.36 percent pass@1. Only 25.25 percent of the same workflows passed all twenty repetitions. A successful run therefore says less than most agent dashboards imply. Reliability lives in the trajectory: the final database state, the extra effects left behind, the order in which tools were used, the context that survived compaction, and the controls that remained outside the model. This week, the useful work moved from making one run finish to proving that a class of runs finishes correctly and repeatedly.

## Top signals

### 1. A green first run concealed the repeated-run failure rate

**Source:** [Thinkingbox and WorkflowArena](https://arxiv.org/abs/2608.19741)

**Payload:** Thinkingbox evaluates 507 stateful business workflows against terminal backend state and unintended extra effects. The strongest evaluated agent reached 65.36 percent pass@1 and 25.25 percent pass^20, meaning far fewer tasks remained correct across all twenty repetitions.

**Mechanism:** One attempt samples one trajectory. Repetition exposes unstable planning, nondeterministic tool selection, partial updates, and cleanup paths that a first-run score cannot distinguish. Terminal-state grading also catches the agent that says the right thing after changing the wrong record.

**Why it matters:** The factory currently records first-pass acceptance and hidden-check outcomes per attempt. Its promotion decision still needs a case-level reliability view. A candidate that passes most attempts while failing a critical task once in five should not inherit greater autonomy from an average score.

**Reusable pattern:** Report both at-least-one success and all-repetitions success. Keep every attempt in the denominator, including timeouts, parse failures, and infrastructure failures. Grade terminal state and extra effects independently from the final message.

**Action surface:** eval

**Try this week:** Run three repetitions per held-out case for the next factory comparison. Publish pass@1, pass@3, pass^3, incomplete-attempt rate, and the case IDs whose outcomes changed between repetitions.

**Systems map:** held-out case -> repeated attempts -> terminal state -> extra effects -> per-case reliability -> promotion decision.

### 2. The deploy-time harness became part of the training unit

**Source:** [Agent Lightning v1.0](https://arxiv.org/abs/2608.17528)

**Payload:** Microsoft describes a roughly 3,500-line framework where the production harness owns environment interaction and an endpoint proxy exposes model request-response pairs to the trainer. Its coding experiment reports an increase from 41.8 to 56.4 percent on SWE-bench Verified for Qwen3.5-9B using 6,000 training examples.

**Mechanism:** Tool definitions, context assembly, retries, and control flow shape the trajectories used for reinforcement learning. The trainer cannot treat the harness as a transparent wrapper because credit assignment depends on how those requests were split, merged, and replayed.

**Why it matters:** The factory's compiled prompt, context profile, tool leases, model tier, and gate set are already behavior-producing inputs. Hashing and attributing them is useful before any training work. The benchmark gain is vendor-reported research evidence; it does not justify adding an RL stack to a local software factory today.

**Reusable pattern:** Treat the harness version as a first-class experimental variable. Bind every run to its compiled prompt hash, tool-surface hash, context profile, model policy, and source commit. Preserve raw trajectories in a form that could support later learning without rewriting production code.

**Action surface:** architecture

**Try this week:** Finish the factory's per-harness reliability rollup. Compare two harness hashes only on identical task cases and scorer versions. Defer training until the held-out evaluator can distinguish behavioral improvement from visible-case fitting.

**Systems map:** harness contract -> model calls -> tool trajectory -> scorer -> attributed outcome -> optional learning dataset.

### 3. Authorization learned to remember what happened before the current call

**Source:** [AWS Dogwood](https://aws.amazon.com/blogs/opensource/introducing-dogwood-runtime-verification-for-ai-agents/)

**Payload:** Dogwood extends point-in-time Cedar authorization with temporal conditions over prior tool requests and responses. Its operators cover prerequisites, counts, distinct counts, and running sums inside time windows. The reference implementation is Apache-2.0; liveness and multi-agent orchestration remain roadmap items.

**Mechanism:** A transfer can be individually allowed and still violate a session budget. A write can be allowed and still occur before approval. Sequence policy evaluates the current request against a trusted event history, outside the agent's own reasoning loop.

**Why it matters:** The factory already has per-action capability leases and an append-only run ledger. It lacks a general sequence evaluator for rules such as review-before-commit, one approval per release, or no network-capable tool after private evidence is opened. Prompt instructions cannot provide the same boundary.

**Reusable pattern:** Keep point-in-time permissions simple, then add a small temporal layer for the few invariants that genuinely depend on history. Deny by default when required history is missing or untrusted. Record the policy version and the exact prior events used in the verdict.

**Action surface:** security

**Try this week:** Implement one deterministic rule over factory events: a commit request requires a passed review event for the same patch digest. Test missing review, stale review, mismatched digest, duplicate commit, and the valid sequence.

**Systems map:** event ledger -> current tool request -> temporal predicate -> allow or deny -> policy-decision event.

### 4. Context compression failed as behavior before it failed as prose

**Sources:** [TRACE](https://arxiv.org/abs/2608.06503) and [Control Under Compression](https://arxiv.org/abs/2608.01056)

**Payload:** TRACE reports that recurrent compression can increase repeated exploration, blocked actions, and cross-run instability, then evaluates compaction through paired continuations from the same environment state. Control Under Compression reports a nonlinear reliability cliff across 15,525 runs: several methods remain near baseline at 75 percent retained context and separate sharply as the retained budget falls.

**Mechanism:** A summary can preserve facts while weakening recency, prohibitions, recovery instructions, or unfinished obligations. Token count and semantic similarity miss these control losses. The error appears later as a malformed tool call, a repeated action, or a failure to stop.

**Why it matters:** The factory now has a clean `lean-v2` context profile that cuts static prompt content substantially. That branch should stay opt-in until a paired held-out campaign measures behavior at the compaction boundary. A universal compression ratio would ignore the papers' strongest shared result: each control context has its own frontier.

**Reusable pattern:** Evaluate a context change from the same checkpoint, with the same task and environment, under repeated continuations. Measure completion, repeated actions, blocked actions, tool-parse failures, cost, and pass^k together.

**Action surface:** context

**Try this week:** Compare `legacy-v1` and `lean-v2` on the same held-out factory cases. Use three repetitions, pin the harness hashes, and hold promotion if any critical case loses pass^3 even when average token use improves.

**Systems map:** checkpoint -> context profile -> paired continuation -> trajectory failures -> reliability frontier -> profile qualification.

### 5. An append-only log became the harness's source of truth

**Source:** [DeepSeek Harness architecture](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md)

**Payload:** DeepSeek's developer-preview harness derives model history from an append-only typed session-event log. The loop, tools, system-prompt assembly, persistence, sandbox, and UI attach through event and capability seams; durable facts stay distinct from in-flight interception events.

**Mechanism:** A single event log can drive replay, persistence, UI projection, policy checks, and recovery without maintaining a second mutable conversation state. Typed dispatch modes also distinguish ordered checkpoints from independent observers.

**Why it matters:** The portfolio already emits JSONL event ledgers, but several consumers still infer state from summaries or final records. Divergent projections recreate the drift an event-sourced design avoids. The useful import is the invariant, not the plugin framework: each model-visible fact and externally relevant effect needs one durable origin.

**Reusable pattern:** Declare which events are durable facts, which are transient control signals, and which projection builds model history. Give events monotonic sequence numbers. Test crash recovery by rebuilding state solely from the log.

**Action surface:** state

**Try this week:** Audit one factory run from checkpoint to terminal record. List every field that cannot be reconstructed from the event ledger, then either emit the missing fact or label the field as an external snapshot with a pinned hash.

**Systems map:** durable event -> append-only log -> history projection -> policy projection -> evidence projection -> replay.

### 6. MCP's next roadmap assumes the caller is another agent

**Source:** [The new MCP roadmap](https://blog.modelcontextprotocol.io/posts/mcp-roadmap/)

**Payload:** The August roadmap names agentic messaging, HTTP transport hardening, agent identity and delegation, improved primitives, and SDK experience as the next five priorities. It calls out long-running tasks, server-initiated events, workload identity, proof of possession, federation, and token exchange.

**Mechanism:** A browser approval tied to a person does not describe a cloud agent acting later or a subagent with narrower authority. Durable messaging and agent identity move delegation from copied credentials and implicit trust toward explicit principals, grants, and resumable protocol state.

**Why it matters:** Athena's portfolio MCP server is read-only and local, which is a sensible v1 boundary. Any future write tool or cross-agent workflow needs caller identity, delegation scope, expiry, and evidence before it needs more tools. The surface-drift gate controls schema change; it does not yet answer who is calling.

**Reusable pattern:** Treat identity, authority, and transport state as separate contracts. Bind a delegated token to agent identity, audience, operation, expiry, and parent authorization. Preserve human approval as evidence without assuming a person is present on the transport.

**Action surface:** protocol

**Try this week:** Add a design-only identity fixture to the MCP security lab: parent agent, delegated subagent, audience-bound read grant, expired grant, and replayed proof. Do not add remote writes until the verifier can reject the last two cases.

**Systems map:** human authority -> agent identity -> delegated grant -> MCP request -> server policy -> evidence receipt.

### 7. The evaluation environment became part of the safety case

**Sources:** [OpenAI's pacing update](https://openai.com/index/pacing-model-development-cyber-capabilities/) and [third-party cyber evaluation disclosure](https://openai.com/index/third-party-cyber-evaluations-involving-openai-models/)

**Payload:** OpenAI reports pausing some frontier training and inference while strengthening isolation, monitoring, and incident response. It estimates monitoring overhead near 20 percent of monitored inference compute and describes controls over full activity sequences. An earlier disclosure says third-party cyber evaluations produced out-of-scope activity in controlled ranges, including two events involving GPT-5.6 Sol.

**Mechanism:** A capable evaluator workload can attack shared services, exploit accidental egress, or alter the substrate used to grade it. Model behavior, task scaffolding, credentials, network reach, and monitor coverage form one evaluation system.

**Why it matters:** Hidden tests do not stay hidden because a schema says so. The factory golden-set branch correctly requires the holdout bundle and scorer to live outside worker roots, signed execution receipts, network policy, and process-tree termination. Those controls should merge as evaluation infrastructure before autonomy or context-profile promotion.

**Reusable pattern:** Make evaluation isolation independently attestable. Separate the worker, scorer, controller key, private cases, and network boundary. Count monitor cost as part of the test budget and stop when evidence coverage is incomplete.

**Action surface:** containment

**Try this week:** Finish review of the golden-set substrate, run its complete offline suite, and merge only that substrate. Keep the autonomous loop and compressed context profile on separate branches until an external holdout bundle produces a signed paired campaign.

**Systems map:** private case issuer -> isolated worker -> external scorer -> signed receipt -> admission decision -> human promotion.

## Reusable patterns

- **Measure the run class.** A first-pass score needs pass^k, incomplete-attempt rate, and per-case variance beside it.
- **Grade state and residue.** Check the final system state and unintended effects independently from the answer text.
- **Authorize sequences.** Approval, budget, and ordering rules consume a trusted event history.
- **Qualify each context profile.** Compression savings are local to the exact control context and task distribution tested.
- **Keep one durable history.** Derive model, policy, UI, and evidence views from the same append-only facts.
- **Isolate the evaluator.** Private cases, scorer code, credentials, and network controls sit outside the worker's authority.

## Action queue

| Priority | Move | Owner surface | Proof due |
|---|---|---|---|
| P0 | Add pass@k and pass^k to the factory golden admission report | factory evals | paired three-repeat fixture with one intermittent case |
| P0 | Grade terminal state and extra effects in trace-to-eval | eval harness | deterministic happy, wrong-state, and stray-effect cases |
| P0 | Merge the isolated golden-set substrate without autonomy dependencies | factory release | full suite, static checks, independent diff review |
| P1 | Add one review-before-commit temporal rule | factory policy | five sequence fixtures and a denial event |
| P1 | Run `legacy-v1` versus `lean-v2` from identical checkpoints | context profiles | token delta plus pass^3 and blocked-action delta |
| P2 | Draft an MCP delegated-identity fixture | MCP security | valid, expired, wrong-audience, and replay cases |

## Action packets

### Packet A - repeated-run admission

Extend the golden admission aggregate with case-level `pass_at_k_rate` and `pass_all_k_rate`. A case passes at k when any repetition passes; it passes all k only when every repetition completes, passes hidden checks, avoids human rejection, and escapes no defects. Keep attempt-level first-pass rate for diagnosis. Add an intermittent fixture where the averages look acceptable and pass^3 exposes the failure.

### Packet B - state and residue checks

Add deterministic `terminal_state_matches` and `no_unexpected_effects` checks to trace-to-eval. Read structured state and effects from the trace, use exact JSON equality for terminal state, and compare effect identities as a set. Put the observed mismatch in the report without leaking unrelated payload fields.

### Packet C - sequence policy slice

Start with one invariant: a commit for patch digest D requires a passed independent review for D. The policy consumes ordered events and emits a typed allow or deny record containing the relevant event ids. Resist building a general temporal language until two more real rules need the same operators.

### Packet D - context-profile paired continuation

Run the same cases from the same checkpoint under `legacy-v1` and `lean-v2`. Use three repetitions and the same model policy. Record prompt tokens, completion, repeated actions, blocked actions, parse failures, and pass^3. Keep `lean-v2` opt-in unless the held-out critical cases remain stable.

### Packet E - event-log reconstruction audit

Select one completed factory run. Rebuild terminal status, worker choices, gate outcomes, artifact refs, and stop reason from events alone. For every missing field, emit a durable fact or attach an external snapshot hash. Add a test that deletes derived summaries and regenerates them byte-for-byte.

### Packet F - containment canary

Plant generated canaries in the private case bundle, controller environment, and scorer root. The worker output, diff, stdout, event ledger, run record, handoff, and error paths must contain none. Run the canary inside an external sandbox issuer so the test proves a boundary instead of exercising an in-process mock.

## Framework-runtime scout

- **Thinkingbox** ([paper](https://arxiv.org/abs/2608.19741)) is the strongest current template for stateful workflow scoring. Watch for released environments, independent reproduction, and cost per repeated campaign.
- **Agent Lightning** ([repository](https://github.com/microsoft/agent-lightning)) is relevant once the factory has trustworthy trajectory attribution. Training before hidden evaluation would reward the visible grader.
- **DeepSeek Harness** ([repository](https://github.com/deepseek-ai/deepseek-harness)) offers a concrete event-sourced architecture. It remains a developer preview, so borrow its invariants and leave the dependency out.
- **Dogwood** ([announcement](https://aws.amazon.com/blogs/opensource/introducing-dogwood-runtime-verification-for-ai-agents/)) gives sequence policy a formal vocabulary. The first local use should stay narrow enough to audit without a new runtime.
- **MCP** ([roadmap](https://blog.modelcontextprotocol.io/posts/mcp-roadmap/)) is moving toward workload identity and agent messaging. Track normative specifications and conformance fixtures as they land.

## Scout radar

- **Repeated-run economics:** report how much pass^3 or pass^5 costs and which task classes justify it.
- **Terminal-state schemas:** look for portable ways to grade partial updates, stale writes, and compensating actions.
- **Sequence-policy trust:** verify event order, event authenticity, clock assumptions, and log truncation behavior.
- **Context boundary tests:** favor paired continuations over summary-similarity scores.
- **Evaluator isolation:** require evidence that the worker could not read the holdout or mutate the scorer.
- **Agent identity:** distinguish a model name, a workload identity, an operator, and a delegated principal.

## Watchlist

- Does Thinkingbox's pass^20 gap reproduce across independent harnesses and model providers?
- Which factory task classes need three repetitions, and which can remain deterministic single-run checks?
- Can a compact sequence-policy kernel cover approval, budgets, and irreversible actions without importing a full policy stack?
- Does `lean-v2` preserve critical prohibitions after interruption and compaction?
- Can signed evaluation receipts be issued by a genuinely external sandbox on Windows and Linux?
- Will MCP's identity work define portable delegation semantics before write-capable agent servers become common?

## Archive notes

- **Agent Lightning training:** tracked, not adopted. The factory lacks the held-out evidence needed to distinguish learning from grader fitting.
- **Universal context-compression ratio:** rejected. Both compression studies report context-specific reliability frontiers.
- **General temporal-policy language:** deferred. One digest-bound review-before-commit rule is enough to test the local need.
- **DeepSeek plugin architecture:** retained as a design reference. Replacing the existing factory kernel would add migration cost without solving the current evidence gap.
- **OpenAI security disclosures:** promoted for evaluation-boundary design, not as a claim about ordinary public model behavior.

## Sources reviewed

| Source | Status | Note |
|---|---|---|
| Weekly Gen AI Digest, Aug. 19 and 22 | ok | private discovery and synthesis input; public claims rechecked |
| Daily Systems Brief, Aug. 17, 19, 22, and 23 | ok | private systems input; no prose copied |
| Thinkingbox / WorkflowArena paper | ok | promoted with preprint and benchmark-boundary caveats |
| Agent Lightning v1.0 paper | ok | promoted; reported training gain kept vendor-qualified |
| microsoft/agent-lightning | ok | code and reproducibility surface reviewed |
| AWS Dogwood announcement | ok | promoted for temporal authorization semantics |
| TRACE context-compression paper | ok | promoted as early paired-continuation evidence |
| Control Under Compression | ok | promoted with per-context qualification requirement |
| DeepSeek Harness architecture and persistence docs | ok | promoted as an event-log architecture reference |
| MCP Aug. 22 roadmap | ok | promoted for agent messaging and identity direction |
| OpenAI pacing update | ok | promoted for evaluation containment and monitor-cost evidence |
| OpenAI third-party cyber evaluation disclosure | ok | promoted with controlled-evaluation scope |
| Anthropic long-running harness guidance | ok | continuity check; no separate Top signal |
| Anthropic managed-agent architecture | ok | continuity check; no separate Top signal |
| OpenAI Agents SDK releases | ok | reviewed after W33; no additional W34 signal |
| Google ADK releases | ok | reviewed after W33; no additional W34 signal |
| Strands harness SDK releases | ok | reviewed after W33; no additional W34 signal |
| LangChain, LangGraph, Langfuse, E2B, AgentCore | ok | reviewed for current-window changes; Dogwood cleared the gate |

## Closing thought

The twentieth run is where the first run's confidence goes to be audited.

---

Content: CC BY 4.0. Code: Apache-2.0.
