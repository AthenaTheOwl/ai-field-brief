<!--
iso_week: 2026-W32
through_date: 2026-08-09
profile_id: builder-tpm
registry_version: 12
matrix_run_id: MTRX-W32-runtime-seams
-->

# The tests were green. They never touched the patch.

**Week 32 through 2026-08-09 - Vol. 15**

## Field thesis

In 64.8 percent of the Python pull requests in a study of 4,882 agent-authored changes, the existing suite never executed a changed line. The week's patch notes supply the operational version of the same warning. A worktree could edit safely while its shell reached the main checkout. A guardrail could fire while its result vanished from the trace. A checkpoint could expire while a backend still returned it. The hosted runtimes arrived with longer sessions, persistent files, and more places for those seams to hide. Green status is useful only when the check crosses the boundary where the failure can occur.

## Top signals

### 1. Changed-line coverage found the green suite's blind spot

**Source:** [Test Coverage Analysis of Agentic Pull Requests](https://arxiv.org/abs/2607.18057)

**Payload:** The authors reconstructed 4,882 agent-generated pull requests across Java and Python. Existing tests executed 61.5 percent of changed executable Java lines and 27.0 percent of changed Python lines. In 64.8 percent of Python pull requests, existing tests executed none of the changed lines. Agent-written tests improved coverage in 22.5 percent of Python code-plus-test pull requests, and error handling had the highest miss rates.

**Mechanism:** A suite can stay green because its test graph never reaches the new branch. Counting test files or successful cases measures activity around the patch; differential coverage measures contact with it.

**Why it matters:** The factory's gates currently answer whether a command passed. For higher autonomy, they also need to answer whether the command exercised the changed behavior, especially error paths and terminal states.

**Reusable pattern:** Bind acceptance evidence to the changed surface. Require changed-line coverage, mutation evidence, or a purpose-built behavior probe for code that existing tests do not touch.

**Action surface:** eval

**Try this week:** Add a report-only changed-line coverage gate to five factory tasks. Record touched executable lines, lines reached by the full suite, new tests added, and missed error branches. Do not block until the baseline is known.

**Systems map:** patch -> executable-line map -> test execution -> changed-line coverage -> uncovered branch classification -> targeted test or accepted exception.

**Transferable principle:** Verification must touch the object under review. Data-pipeline reconciliation and financial control sampling use the same rule.

**Falsification test:** If suite pass/fail predicts hidden acceptance as well as changed-line coverage across the same cohort, the extra metric adds little.

**Adoption ladder:**
  - Minimum viable: Report changed-line coverage for one Python task class.
  - Mid: Require a named test or approved exception for every changed error branch.
  - Full: Add mutation or break-then-fix evidence to promotion cohorts.
  - Monitoring: Track changed-line coverage, hidden failures, exception age, and test additions by task class.

**Confidence:** High for the reported dataset; medium for transfer to this portfolio until the report-only cohort runs.

**Evidence:** MTRX-W32-CHANGED-LINES.

### 2. The worktree boundary stopped at the shell

**Source:** [Claude Code 2.1.222](https://github.com/anthropics/claude-code/releases/tag/v2.1.222), [Claude Code 2.1.223](https://github.com/anthropics/claude-code/releases/tag/v2.1.223)

**Payload:** Two Claude Code patch releases closed several permission gaps. Worktree-isolated sessions and subagents could run destructive Git commands against the main checkout. Background tasks could receive an auto-allow result that bypassed tool restrictions. Crafted Bash, tabs, invisible Unicode, and dynamic imports could obscure commands or escape workflow checks.

**Mechanism:** Isolation covered one execution path while adjacent paths retained broader authority. The user saw a worktree; the shell and background runner still carried capabilities from the host.

**Why it matters:** The factory uses worktrees as a workcell boundary. A path assertion is incomplete until shell commands, hooks, nested agents, Git metadata, and cleanup routines all resolve against the same root.

**Reusable pattern:** Test boundaries through every interpreter and lifecycle path that can cross them. Plant harmless canaries outside the lease and require denials from foreground, background, resumed, and nested execution.

**Action surface:** tool-policy, runtime-adapter

**Try this week:** Extend the factory's privacy canary into a worktree escape fixture. Attempt a read, write, Git operation, hook-driven command, and background subtask against the main checkout; require five denials and five evidence events.

**Systems map:** declared worktree -> capability lease -> shell and tool adapters -> nested execution -> canary probe -> hard denial -> run evidence.

**Transferable principle:** A boundary belongs to the whole call chain. Container mounts, database roles, and CI credentials fail when one adapter retains host authority.

**Falsification test:** Any path can touch the main checkout without a terminal stop and preserved evidence.

**Adoption ladder:**
  - Minimum viable: Run five non-mutating canary probes in one fixture.
  - Mid: Repeat across planner, implementer, reviewer, and resumed runs.
  - Full: Enforce the lease in the host controller and sandbox independently.
  - Monitoring: Count denied paths, unexpected roots, inherited credentials, and missing stop events.

**Confidence:** High. The release notes name the affected paths and fixes; the local fixture still needs to prove coverage on Windows.

**Evidence:** MTRX-W32-BOUNDARY-REGRESSION.

### 3. Patch releases repaired the order of truth

**Source:** [OpenAI Agents SDK 0.19.3](https://github.com/openai/openai-agents-python/releases/tag/v0.19.3), [0.19.4](https://github.com/openai/openai-agents-python/releases/tag/v0.19.4)

**Payload:** The SDK fixed guardrail results lost across streamed aborts, approved tool output lost on resume, max-turn output omitted from sessions, sibling work continuing after concurrent failure, session state saved before output guardrails, failure spans left unmarked, and sandbox output budgets left unenforced.

**Mechanism:** Each defect sat between two individually reasonable components. The failure emerged from ordering: persist before guardrail, resume before approval state, emit before cancellation, or finish before tracing records the terminal verdict.

**Why it matters:** The factory's pipeline has the same seams: worker output, gate result, patch round, reviewer verdict, commit, handoff, and evidence. Unit tests for each module can miss the order in which authority and state move across them.

**Reusable pattern:** Turn lifecycle ordering into executable invariants. Every terminal path should preserve the final guardrail result, cancel siblings, commit state once, close streams, and record one terminal status.

**Action surface:** workflow, eval

**Try this week:** Write a cancellation-and-resume fixture with two sibling workers. Fail one after the other emits partial output, resume after approval, and assert one terminal state, no orphan process, preserved approval, and no pre-guardrail persistence.

**Systems map:** concurrent work -> partial output -> guardrail -> cancellation barrier -> durable state -> terminal trace -> resume or closure.

**Transferable principle:** Correct components can form an incorrect transaction. Payment workflows and distributed jobs use the same ordering tests.

**Falsification test:** Property tests over reordered events cannot produce duplicate completion, lost guardrail evidence, or post-failure work.

**Adoption ladder:**
  - Minimum viable: One deterministic failure-and-resume fixture.
  - Mid: Generate event-order permutations around every terminal transition.
  - Full: Gate releases on lifecycle conformance across worker families.
  - Monitoring: Track orphan processes, duplicate terminal events, late writes, and missing guardrail results.

**Confidence:** High for the defects; medium for the local analogy until the event-order fixture runs.

**Evidence:** MTRX-W32-LIFECYCLE-ORDER.

### 4. Cloudflare gave the agent a filesystem before giving it a container

**Source:** [Cloudflare Agents changelog, August 3](https://developers.cloudflare.com/changelog/product/agents/)

**Payload:** The `@cloudflare/computer` preview gives each agent a SQLite-backed virtual filesystem, shell and Git access, and a runtime that chooses between isolates and Linux containers. Files can be populated from source control, object storage, or another provider.

**Mechanism:** The durable working set is separated from the compute process. Lightweight operations stay in an isolate; heavier commands move to a container while the filesystem remains the handoff surface.

**Why it matters:** The factory currently treats a Git worktree as workspace, evidence source, and recovery anchor. Cloudflare's design supplies a comparator: preserve the artifact surface while selecting compute per operation.

**Reusable pattern:** Make files and state portable across compute classes. Route work by capability and cost while keeping one explicit, inspectable artifact boundary.

**Action surface:** architecture, runtime-adapter

**Try this week:** Model one factory task as three operations: read-only inventory, isolated edit, and heavy test. Record which compute class each needs and which files must survive every handoff; keep this as a design fixture.

**Systems map:** durable virtual filesystem -> operation classifier -> isolate or container -> bounded command -> artifact sync -> evidence packet.

**Transferable principle:** State placement and compute placement are separate choices. Build systems and notebook platforms gain efficiency from the same split.

**Falsification test:** If moving between compute classes loses provenance, permissions, or deterministic file state, the portability claim fails.

**Adoption ladder:**
  - Minimum viable: Produce the operation and artifact contract for one task.
  - Mid: Run the same fixture in a worktree and an ephemeral sandbox.
  - Full: Route operations while preserving one content-addressed artifact ledger.
  - Monitoring: Track handoff failures, sync bytes, cold starts, permission drift, and replay mismatch.

**Confidence:** High for the preview's documented shape; low for production reliability until public evidence accumulates.

**Evidence:** MTRX-W32-COMPUTE-LADDER.

### 5. Fourteen-day sessions moved uptime into the agent contract

**Source:** [AWS, AgentCore runtime instances](https://aws.amazon.com/blogs/aws/runtime-instances-persistent-compute-for-production-ai-agents-on-amazon-bedrock-agentcore/)

**Payload:** AgentCore added managed EC2-backed runtime instances for sessions lasting up to fourteen days, compared with up to eight hours for its microVM runtime. The instances support GPUs, multiple collaborating agents, stop and restart, container packaging, and optional EBS or AgentCore Memory for state that outlives a session.

**Mechanism:** Long-running work keeps a host and shared session alive instead of reconstructing state around short invocations. Hibernation lowers idle cost; durable storage carries knowledge beyond the host's lifecycle.

**Why it matters:** Longer uptime makes hidden state, resource leaks, stale credentials, and partial failure more consequential. A fourteen-day process needs heartbeat, checkpoint, cancellation, and resource accounting as first-class evidence.

**Reusable pattern:** Match execution lifetime to task lifetime, then require a recovery contract that survives process and host replacement.

**Action surface:** software-control-plane, architecture

**Try this week:** Stretch one deterministic factory fixture through three synthetic days: checkpoint, stop, rotate the worker process, resume, and compare the final artifact hash with an uninterrupted baseline.

**Systems map:** owned session -> heartbeat -> checkpoint -> hibernate -> fresh process -> state restore -> artifact equivalence -> terminal evidence.

**Transferable principle:** Long duration turns recovery into normal operation. Data migrations and supply-chain simulations need the same restart contract.

**Falsification test:** A resumed run differs from the uninterrupted baseline without an attributed external input change.

**Adoption ladder:**
  - Minimum viable: Synthetic stop and resume over one checkpoint.
  - Mid: Add credential rotation, process death, and stale-heartbeat recovery.
  - Full: Admit multi-day tasks only after replay-equivalence cohorts pass.
  - Monitoring: Track checkpoint age, restore success, orphan sessions, resource drift, and final hash mismatch.

**Confidence:** High for the service limits; medium for the pattern until a local failure-injection run completes.

**Evidence:** MTRX-W32-PERSISTENT-RUNTIME.

### 6. Strands put policy around the tool batch

**Source:** [Strands harness SDK Python 1.51](https://github.com/strands-agents/harness-sdk/releases/tag/python/v1.51.0)

**Payload:** The release added snapshot sessions, before-tools and after-tools batch hooks, an LLM-driven risk classifier for human intervention, selective context offload, utilization estimates, and interrupt round trips over A2A.

**Mechanism:** The framework exposes named seams around a set of tool calls. A policy can inspect the batch before execution, interrupt it, preserve the session, and continue after a human or remote agent responds.

**Why it matters:** Per-call controls can miss a harmful sequence made of harmless steps. Batch hooks provide a place to evaluate cumulative blast radius, shared credentials, and the combined write set before execution.

**Reusable pattern:** Judge the action set and the action. Preserve deterministic rules as verdict authority; use a model classifier to add context and escalation, never to waive a hard boundary.

**Action surface:** tool-policy, agent-role

**Try this week:** Add a fixture with three individually allowed commands whose combined write set crosses the task lease. Require the batch policy to hold before the first command and record the full proposed set.

**Systems map:** proposed tool batch -> deterministic lease check -> contextual risk label -> allow, hold, or block -> snapshot -> human response -> resumed batch.

**Transferable principle:** Sequence risk differs from action risk. Procurement approvals and privileged-access systems inspect cumulative authority for the same reason.

**Falsification test:** The batch hook cannot catch a cumulative violation that per-call checks miss.

**Adoption ladder:**
  - Minimum viable: One cumulative-write fixture with deterministic verdicts.
  - Mid: Add snapshot and human response with idempotent resume.
  - Full: Evaluate batch policies against hidden attack sequences.
  - Monitoring: Track holds, overridden recommendations, cumulative violations, and resume duplication.

**Confidence:** High for the release surface; medium for the model-risk classifier until independent calibration exists.

**Evidence:** MTRX-W32-INTERRUPTIBLE-STATE.

### 7. Expired state became a backend conformance problem

**Source:** [LangGraph checkpoint 4.2](https://github.com/langchain-ai/langgraph/releases/tag/checkpoint%3D%3D4.2.0), [Postgres checkpoint 3.1.2](https://github.com/langchain-ai/langgraph/releases/tag/checkpointpostgres%3D%3D3.1.2)

**Payload:** LangGraph added opt-in omission of expired checkpoint rows, fixed collection and traversal from plain-value delta-history seeds, and ran the same conformance suite against SQLite and Postgres.

**Mechanism:** Expiry is part of read semantics, while delta traversal reconstructs state across writes. A backend that interprets either rule differently can resume an agent from a stale or incomplete history.

**Why it matters:** The factory's run state, checkpoint references, and evidence packets cross files, SQLite, Git, and external sandboxes. Backend parity belongs in the contract before another store is added.

**Reusable pattern:** Define one state-store conformance suite covering put, read, expiry, history, concurrency, interruption, and recovery; make every adapter pass it.

**Action surface:** eval, architecture

**Try this week:** Write a store-neutral checkpoint fixture with one expired row and one delta chain. Run it against the current state store and a file-backed reference implementation.

**Systems map:** state writes -> history chain -> expiry clock -> backend adapter -> reconstructed checkpoint -> resumed run -> equivalence check.

**Transferable principle:** Storage adapters implement behavior, not plumbing. Cache, queue, and artifact-store swaps need semantic parity tests.

**Falsification test:** Both adapters return the same visible rows while reconstructing different resumed state.

**Adoption ladder:**
  - Minimum viable: Put, read, expire, and reconstruct one chain.
  - Mid: Add concurrent writes, cancellation, and clock skew.
  - Full: Gate every state backend on the shared suite.
  - Monitoring: Track stale reads, restore mismatches, adapter-specific exceptions, and expired-state resumes.

**Confidence:** High. The release notes tie the feature, defect, and cross-backend conformance work together.

**Evidence:** MTRX-W32-STATE-EXPIRY.

## Reusable patterns

- **Measure contact, not ceremony.** Where it applies: tests, security reviews, and audit sampling. Caveat: coverage proves execution, not assertion quality.
- **Test the seam as a system.** Where it applies: guardrails, cancellation, persistence, and resume. Caveat: event permutations grow quickly; start with terminal paths.
- **Separate durable state from chosen compute.** Where it applies: agent workspaces, notebooks, and build workers. Caveat: handoff provenance must survive the move.
- **Make long duration recoverable by design.** Where it applies: research, migrations, and multi-agent work. Caveat: checkpointing without equivalence tests can preserve the wrong state longer.

## Action queue

| Candidate | Surface | Effort | Risk | Test |
|---|---|---:|---:|---|
| Changed-line coverage baseline | eval | M | low | Five factory tasks report changed-line and error-branch coverage without blocking |
| Worktree escape canary | tool-policy | M | medium | Five foreground, background, and nested probes are denied with evidence |
| Lifecycle ordering fixture | workflow | M | medium | Concurrent failure, approval resume, and persistence yield one terminal state |
| Compute-class contract | architecture | S | low | One task names isolate, sandbox, and durable-artifact requirements per operation |
| Multi-day replay fixture | software-control-plane | M | medium | Interrupted and uninterrupted artifacts hash identically |
| Checkpoint store conformance | eval | M | low | File and current store agree on expiry and delta reconstruction |

## Action packets

| Source | Target | Surface | Try | Proof metric | Rollback | Kill criterion |
|---|---|---|---|---|---|---|
| Agent PR coverage study | factory | eval | Add report-only changed-line coverage to five tasks | Per-task line contact and missed error branches emitted | Remove report from run summary | Instrumentation changes test behavior or adds unstable overhead |
| Claude Code 2.1.222-223 | factory | tool-policy | Extend privacy canary across Git and background paths | 5/5 denials and evidence events | Revert fixture registration | Any probe risks mutating the main checkout |
| OpenAI Agents 0.19.3-0.19.4 | factory | workflow | Add cancellation, guardrail, persistence, and resume ordering fixture | One terminal state and zero orphan work | Keep existing deterministic unit fixtures | Fixture depends on a live provider |
| Cloudflare computer | factory design | architecture | Classify one task's operations and persistent artifacts | Every operation has one required compute class and handoff contract | Retain current worktree executor | Classification adds no measurable cost or isolation signal |
| AgentCore runtime instances | factory | software-control-plane | Run synthetic multi-day stop, rotate, and resume | Final hash equals uninterrupted baseline | Disable long-duration profile | Restore cannot preserve bounded authority |
| LangGraph checkpoint | trace-to-eval-harness | eval | Add one expired-row and delta-history evidence fixture | Two adapters reconstruct one state and reject expired input | Keep one reference adapter | Clock or backend behavior cannot be made deterministic |

## Framework-runtime scout

| Source | Primitive changed | Why it matters | 30-90 minute test |
|---|---|---|---|
| Cloudflare computer preview | compute, filesystem, observability | durable files can cross isolate and container execution | Map one task's artifact handoff and compare trace fields with the worktree path |
| AgentCore runtime instances | execution, checkpoint, multi-agent | managed sessions now span days and shared hosts | Inject stop and restart into one fixture and compare artifact hashes |
| Managed Deep Agents public beta | execution, memory, sandbox, eval | a managed bundle now exposes files, skills, tools, and runtime as one deployable unit | Port one read-only agent definition and list every hidden platform dependency |
| Strands 1.51 | interrupt, storage, tool policy | batch hooks and snapshots create explicit policy seams | Hold a cumulative-write batch before its first command |
| LangGraph checkpoint 4.2 | state, expiry | expired rows and delta history now share a conformance surface | Run one expired checkpoint across file and SQLite adapters |
| Cloudflare agent traces | observability, identity | turns, model calls, tools, approvals, usage, and runtime operations share one trace | Compare the schema with one factory run-evidence packet |

## Scout radar

| Item | Why it might matter early | What to watch | Revisit trigger |
|---|---|---|---|
| [Managed Deep Agents](https://www.langchain.com/blog/introducing-managed-deep-agents) | public beta packages a harness with durable runtime, files, memory, and evals | exportability, pricing, hidden state, incident evidence | one independent team publishes a recovery or migration report |
| [Cloudflare computer](https://developers.cloudflare.com/changelog/product/agents/) | isolate-to-container routing could reduce sandbox cost | filesystem semantics, network policy, cold starts, replay | a public conformance suite covers both compute classes |
| [Braintrust SDK 3.27](https://github.com/braintrustdata/braintrust-sdk-javascript/releases/tag/braintrust%403.27.0) | session and eval-input instrumentation broadens trace coverage | schema stability and cross-provider parity | one trace crosses provider, session, tool, and evaluator without losing identity |
| [E2B custom-cluster volume routing](https://github.com/e2b-dev/E2B/releases/tag/e2b%402.38.0) | persistent state follows tenant-selected compute placement | cross-cluster consistency and access policy | a migration test preserves bytes, ownership, and audit identity |
| [Agent Native Engineering](https://agentnativeengineering.com/) | the daily format surfaces empirical agent-operations work quickly | primary links, corrections, and independence | three consecutive editions lead to reproducible local tests |

## Watchlist

- **Does changed-line coverage predict hidden acceptance better than suite status?** Revisit trigger: the first five-task factory cohort.
- **Can a persistent agent session survive credential rotation and process replacement without authority drift?** Revisit trigger: a published AgentCore recovery example or a local injected-failure run.
- **Will managed-agent bundles preserve portable evidence when an application leaves the platform?** Revisit trigger: an export-and-replay walkthrough with content hashes.
- **Do model-based risk classifiers catch sequence risk without producing approval fatigue?** Revisit trigger: a released calibration set with false-positive costs.

## Archive notes

- **Google ADK 2.6.2 and 2.6.3** ([releases](https://github.com/google/adk-python/releases)). The window contained targeted deployment fixes; the larger capability contract arrived in W33.
- **E2B 2.38** ([release](https://github.com/e2b-dev/E2B/releases/tag/e2b%402.38.0)). Custom-cluster volume routing matters for state placement and needs migration evidence before promotion.
- **Langfuse 4.3-4.6** ([releases](https://github.com/langfuse/langfuse/releases)). Evaluator metadata propagation and background execution were useful incremental changes; neither carried enough independent mechanism for a Top signal.
- **CrewAI 1.15.11-1.15.14** ([releases](https://github.com/crewAIInc/crewAI/releases)). Reviewed as version activity; no single current-window contract change survived the promotion gate.

## Sources reviewed

| Source | Status | Note |
|---|---|---|
| Daily Systems Brief folder | ok | Aug 2, 3, 4, 5, and 9 used as private discovery; public claims rechecked |
| Weekly Gen AI Digest folder | ok | no issue after Jul 3; continuity only |
| Agent PR coverage paper | ok | late-discovered empirical signal promoted with date caveat |
| Claude Code releases | ok | 2.1.221-2.1.226 reviewed; two boundary releases promoted |
| OpenAI Agents SDK releases | ok | 0.19.3 and 0.19.4 promoted as one lifecycle cluster |
| Cloudflare Agents changelog | ok | computer runtime and traces reviewed |
| AWS AgentCore | ok | runtime instances promoted |
| Strands releases | ok | Python 1.51 and TypeScript 1.12 reviewed; lifecycle seam promoted |
| LangGraph releases | ok | checkpoint 4.2 and Postgres 3.1.2 promoted |
| LangChain Blog | ok | Managed Deep Agents public beta retained in scout radar |
| Google ADK releases | ok | deployment and v1 safety fixes reviewed; no Top signal |
| E2B releases | ok | custom-cluster volume routing retained in scout radar |
| Braintrust releases | ok | instrumentation retained in scout radar |
| Langfuse releases | ok | evaluator metadata and background execution archived |
| CrewAI releases | ok | release activity reviewed; no material contract change promoted |
| AgentOps, LlamaIndex, MCP, AgentCore, and framework docs | ok | no additional current-window item cleared the evidence and action gates |

## Closing thought

A passing check that never reaches the changed line is a green lamp wired to the wrong room.

---

Content: CC BY 4.0. Code: Apache-2.0.
