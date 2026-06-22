<!--
iso_week: 2026-W26
through_date: 2026-06-22
profile_id: builder-tpm
registry_version: 5
matrix_run_id: MTRX-W26-loop-runtime
-->

# Loop engineering reached the runtime layer: discovery, durability, and audit gates now carry the work

**Week of 2026-06-22 - Vol. 8**

## Field thesis

The center moved again. Agent teams now need to know whether the surrounding loop can find work, pick tools, run in a bounded workspace, preserve state, turn failures into evals, and expose enough evidence for another system to audit the run.

This week the public signals lined up around that layer. Claude Code made MCP tool search context-aware by default. OpenAI's agent-improvement recipe ties traces, feedback, evals, labels, and Codex handoff into one repeatable flywheel. Vercel is packaging sandbox execution and durable workflow state for code agents. Hugging Face is turning resource discovery into a searchable agent layer. MCP security work is converging on default-deny tool policy. Agent benchmark researchers are auditing the tasks behind the scores.

The practical read: the next useful agent product is a loop with a contract, not a chat surface with a longer prompt.

## Top signals

### 1. Claude Code moved MCP discovery into the runtime budget

**Source:** [Claude Code changelog](https://code.claude.com/docs/en/changelog), [Claude Code releases](https://github.com/anthropics/claude-code/releases)

**Payload:** Claude Code enabled MCP tool search in auto mode when tool descriptions take more than 10% of the context budget. Nearby changes harden the local operating surface: closest `.claude/` settings win, subagent spawns are classifier-reviewed, and destructive git actions are blocked under improved auto-mode safety.

**Mechanism:** The tool surface is becoming lazy-loaded and policy-checked. A runtime can no longer assume every tool description belongs in the prompt.

**Why this matters:** MCP scale creates a new failure mode: the agent loses context to tools it never calls. Context-aware discovery makes tool choice part of runtime design.

**Reusable pattern:** Add a tool-surface budget gate. If declared tools exceed a context threshold, move to search-first discovery and log which tools were selected.

**Action surface:** `tool-policy`, `agent-role`, `runtime-adapter`

**Try this week:** Build a small MCP registry report with three fields per tool: description tokens, allowed roles, and last-used run id.

**Systems map:** tool registry -> context budget gate -> tool search -> policy check -> selected tool trace

**Transferable principle:** A large tool list is a data set. Treat it like one.

**Falsification test:** If the selected tools are identical before and after search-first routing, the registry was already small enough or too weakly typed.

**Adoption ladder:** inventory tools -> add budget report -> enable search-first route -> add per-role allowlist -> record tool choice in run evidence.

**Confidence:** High.

### 2. OpenAI's improvement loop turns traces into the next work packet

**Source:** [OpenAI Cookbook: agent improvement loop](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop)

**Payload:** The recipe ties together run traces, user feedback, evals, labeling, prompt changes, and Codex handoff. The harness defines instructions, tools, routing, output requirements, and validation checks as a single improvable surface.

**Mechanism:** The trace is the intake artifact. A failed or weak run can become a labeled example, an eval, and an implementation packet without losing the chain of evidence.

**Why this matters:** Agent teams often split the loop across logs, tickets, prompt files, and test suites. The recipe collapses those into a flywheel.

**Reusable pattern:** Every failed agent run should have one of three exits: new eval, prompt patch, or product bug.

**Action surface:** `eval`, `workflow`, `run-evidence`

**Try this week:** Pick one recent failed run and write the missing artifact: eval case, label note, or code change request.

**Systems map:** trace -> feedback -> labeled case -> eval -> implementation handoff -> next run

**Transferable principle:** A trace without an action mapping is observability theater.

**Falsification test:** If a trace cannot name the next artifact, the loop is recording symptoms with no learning path.

**Adoption ladder:** store traces -> classify failures -> convert two failures to evals -> wire eval into CI -> require a run id in follow-up tickets.

**Confidence:** High.

### 3. Loop engineering is the product spec for long-running agents

**Source:** [Addy Osmani: Loop Engineering](https://addyosmani.com/blog/loop-engineering/), [O'Reilly Radar](https://www.oreilly.com/radar/loop-engineering/)

**Payload:** The framing names the shift from prompt craft to loop design: trigger, context, worker, verifier, memory, escalation, budget, and stop rule.

**Mechanism:** The human moves up one layer. Instead of nudging the agent turn by turn, the product defines the loop that finds work and decides when to stop.

**Why this matters:** Many agent demos fail because the product is a transcript. A loop contract gives the system an operating shape.

**Reusable pattern:** Write a one-page loop contract before writing the worker prompt.

**Action surface:** `workflow`, `spec`, `operator-console`

**Try this week:** For one recurring workflow, write the trigger, state file, worker, verifier, stop rule, and human escalation condition.

**Systems map:** trigger -> context load -> worker -> verifier -> state update -> next action or stop

**Transferable principle:** Autonomy without a stop rule is unattended work generation.

**Falsification test:** If the loop cannot explain when to ask a human, the verifier is too weak or the scope is too broad.

**Adoption ladder:** name one loop -> add state file -> add verifier -> add budget -> add run record.

**Confidence:** High.

### 4. Durable code-agent infrastructure is getting packaged

**Source:** [Vercel durable AI code agent guide](https://vercel.com/guides/how-to-build-a-durable-ai-code-agent), [Vercel Workflows](https://vercel.com/docs/workflow), [Vercel Sandbox](https://vercel.com/docs/vercel-sandbox)

**Payload:** Vercel's public guidance now treats code agents as long-running workflow systems: isolated microVM execution, retries, workflow state, and artifact handling.

**Mechanism:** The agent is split from the work environment. The runtime can run code in a bounded workspace, pause, resume, and recover after transient failures.

**Why this matters:** File-writing agents need isolation and durable state more than another chat widget.

**Reusable pattern:** Put sandbox identity, retry count, and artifact path into the run record.

**Action surface:** `runtime-adapter`, `deployment`, `run-evidence`

**Try this week:** Run one code-agent task inside a disposable sandbox and store the sandbox id beside the output artifact.

**Systems map:** task -> workflow state -> sandbox -> tool calls -> artifact -> retry or close

**Transferable principle:** The workspace is part of the model input. Pin it.

**Falsification test:** If a run cannot be recreated from the task, tool surface, workspace ref, and artifact refs, the system is missing replay evidence.

**Adoption ladder:** isolate execution -> record workspace ref -> add retry metadata -> store artifacts -> add replay check.

**Confidence:** Medium-high.

### 5. Agentic resource discovery is becoming its own layer

**Source:** [Hugging Face: Agentic Resource Discovery](https://huggingface.co/blog/AgenticResourceDiscovery)

**Payload:** Hugging Face launched resource discovery around Skills, ML apps, and MCP servers, with a Discover Tool that lets agents search external capabilities.

**Mechanism:** The agent does not need every possible capability preloaded. It can search a resource layer and pick a candidate.

**Why this matters:** Discovery changes integration work. The build task becomes curating sources, ranking candidates, and pinning the resource chosen for a run.

**Reusable pattern:** Treat external skills and MCP servers as source-registry entries with owner, trust tier, last checked date, and allowed scopes.

**Action surface:** `source-registry`, `tool-policy`, `scout`

**Try this week:** Add a scout lane that reviews five external Skills or MCP servers and promotes only one into the allowed registry.

**Systems map:** discovery query -> candidate resource -> trust check -> registry entry -> run evidence

**Transferable principle:** Discovery without curation is dependency sprawl.

**Falsification test:** If the same result wins under every task, the query is too generic or the ranking criteria are missing.

**Adoption ladder:** scout list -> trust rubric -> allowed registry -> pin versions -> record selected resource in each run.

**Confidence:** Medium.

### 6. Benchmark audits are becoming part of eval engineering

**Source:** [Automated Benchmark Auditing for AI Agents and LLMs](https://arxiv.org/abs/2605.26079), [AgentProcessBench](https://arxiv.org/abs/2605.24659), [Efficient Benchmarking of AI Agents](https://arxiv.org/abs/2605.22453)

**Payload:** Recent papers are moving attention from aggregate scores to task quality, process quality, and cost-aware benchmark subsets. One audit reports critical issues across a large benchmark set and score movement after filtering.

**Mechanism:** Eval quality depends on the tasks, trajectories, and scoring rules, not only the model under test.

**Why this matters:** Agent products are starting to gate decisions on evals. A weak benchmark can ship the wrong change with high confidence.

**Reusable pattern:** Add `benchmark_audit.md` beside every eval suite with task source, known defects, exclusion rules, and last audit date.

**Action surface:** `eval`, `qa`, `decision-record`

**Try this week:** Audit ten eval tasks and mark each as keep, fix, quarantine, or retire.

**Systems map:** eval suite -> task audit -> exclusion rule -> score report -> decision gate

**Transferable principle:** The eval suite is a product dependency.

**Falsification test:** If removing bad tasks does not move any conclusion, the suite may be stable; if it does, the gate needs audit status.

**Adoption ladder:** inventory tasks -> audit sample -> tag defects -> quarantine failures -> require audit status in score reports.

**Confidence:** Medium.

### 7. MCP security is moving toward default-deny tool governance

**Source:** [IETF draft: MCP security considerations](https://datatracker.ietf.org/doc/draft-mohiuddin-mcp-security-considerations/), [Kong: MCP tool governance](https://konghq.com/blog/engineering/mcp-tool-governance)

**Payload:** The IETF draft catalogs MCP security concerns and mitigations. Kong's guidance pushes gateway-level filtering by actor, credential isolation, and default-deny access to tools.

**Mechanism:** MCP standardizes access, but policy has to sit at the gateway or runtime boundary.

**Why this matters:** A tool protocol can make unsafe access feel official. The safe shape is role-scoped access plus surface drift detection.

**Reusable pattern:** Store a tool-surface snapshot, hash every input schema, and fail CI when the live surface changes without a decision record.

**Action surface:** `security`, `tool-policy`, `ci`

**Try this week:** Pick one MCP server and write its allowed-role matrix before adding another tool.

**Systems map:** MCP server -> tool snapshot -> role matrix -> gateway policy -> drift gate

**Transferable principle:** Tool access is authorization, not convenience.

**Falsification test:** If a low-trust role can still see high-impact tools after policy routing, discovery and access control are coupled incorrectly.

**Adoption ladder:** snapshot surface -> default deny -> role allowlist -> credential isolation -> drift gate.

**Confidence:** High.

## Reusable patterns

| Pattern | Where it showed up | How to use it |
|---|---|---|
| Loop contract | Addy Osmani, OpenAI, Vercel | Require trigger, state, worker, verifier, budget, and stop rule before expanding agent scope. |
| Search-first tool surface | Claude Code, Hugging Face ARD | Defer tool descriptions until task context selects a shortlist. |
| Trace-to-action mapping | OpenAI, LangChain | Every failed trace exits as eval, prompt patch, or product bug. |
| Benchmark audit | ABA, AgentProcessBench | Eval tasks get their own audit status before their scores gate product work. |
| Default-deny MCP | IETF, Kong, Claude Code safety changes | Treat tool exposure as a role-scoped policy surface. |

## Action queue

| Rank | Action | Repo fit | Output |
|---|---|---|---|
| 1 | Add loop contracts to active factory task templates | procurement-negotiation-lab | `ops/factory-templates/*` field set: trigger, state, verifier, stop rule |
| 2 | Add benchmark audit sidecars for eval suites | trace-to-eval-harness, supplier-risk-rag-agent | `benchmark_audit.md` with keep/fix/quarantine/retire status |
| 3 | Add tool-surface budget reports | athena-site MCP server, mcp-security-lab | context-token count per tool and deferred-discovery threshold |
| 4 | Add scout registry for external Skills/MCP servers | ai-field-brief | promoted candidate entries with trust tier and last_checked |
| 5 | Add sandbox refs to all new MVP run records | factory-generated repos | run evidence field or status note |
| 6 | Add W26 bridge packet after publish | trace-to-eval-harness | `examples/run_evidence/<run-id>.packet.json` |

## Action packets

### Packet A: loop contract gate

**Target:** procurement-negotiation-lab factory templates

**Change:** Add required fields to task YAML: `trigger`, `state_artifact`, `worker_scope`, `verifier_scope`, `stop_rule`, `human_escalation`.

**Acceptance:** A generated task fails validation when any loop field is missing. Existing active-MVP templates pass after update.

**Why now:** The factory is creating many repos. The loop contract keeps each repo from becoming a pile of scripts.

### Packet B: eval audit sidecar

**Target:** trace-to-eval-harness

**Change:** Add `benchmark_audit.schema.json` and a sample audit for one existing packet fixture. Fields: task_id, source, defect_status, exclusion_reason, reviewer, last_checked.

**Acceptance:** `validate benchmark-audit` exits 0 on sample and 1 when a gated score references a quarantined task.

**Why now:** Recent benchmark-audit work says score movement can come from task defects. The portfolio already gates decisions on evals.

### Packet C: MCP tool budget gate

**Target:** mcp-security-lab and athena-site MCP server

**Change:** Extend the tool-surface snapshot with estimated description tokens and allowed roles.

**Acceptance:** Drift gate reports added tools, changed input schema hashes, and context-budget impact.

**Why now:** Claude Code's default tells us context budget is now part of tool governance.

### Packet D: external resource scout lane

**Target:** ai-field-brief

**Change:** Add `ops/scout-resources/` entries for Skills, MCP servers, and agent resource catalogs. Include trust tier, owner, install path, last_checked, and promotion target.

**Acceptance:** At least one promoted resource becomes a real action packet each brief.

**Why now:** Hugging Face ARD makes discovery a live surface. The brief should separate candidate discovery from adopted dependencies.

### Packet E: run-failure conversion drill

**Target:** any active agent repo

**Change:** Pick one failed run, then create one eval, one fix ticket, and one run-evidence note from the same trace.

**Acceptance:** The three artifacts all cite the same run id.

**Why now:** OpenAI's loop recipe is only useful if failed traces create product work.

## Scout radar

| Item | Why to watch | Promote when |
|---|---|---|
| AgentDiet | Cuts trajectory token cost while preserving task outcome. | A local run-evidence packet exceeds cost budget. |
| Formal workflow verification with Lean | Turns agent workflow structure into a proof target. | A factory task becomes repetitive enough to formalize. |
| Agent Skill Evaluation and Evolution | Treats skills as measurable artifacts. | The portfolio adopts external Skills beyond scout status. |
| GUI agent paper lists | The GUI-agent stack is moving quickly and will affect browser QA. | A repo needs cross-browser interaction beyond Playwright smoke. |
| Gemini CLI and Actions | Adds another terminal-agent baseline to compare against Codex and Claude Code. | It supports the same run-evidence fields or clean export path. |
| LangChain trace loops | Useful comparative pattern for trace-to-action mapping. | A trace-to-eval dashboard needs another ingestion adapter. |
| MCP spec release candidates | Protocol surface may shift around tasks, apps, and auth. | A field becomes stable in final spec and affects tool-surface hashes. |
| Vercel Workflows | Good candidate for durable public demos. | One portfolio app needs retry/state without standing up custom queue infra. |

## Watchlist

1. Tool discovery may hide policy errors. Deferred loading should not bypass allowlists.
2. Agent benchmark scores may get less comparable as scaffolds and harnesses vary.
3. Sandboxes reduce blast radius, but workspace identity still has to be pinned in run evidence.
4. Resource discovery creates supply-chain pressure: every external skill becomes dependency metadata.
5. Loop automation can bury human review under a green status if stop rules are vague.

## Sources reviewed

| Source | Type | Disposition |
|---|---|---|
| OpenAI Cookbook agent improvement loop | Primary docs | Top signal |
| OpenAI Codex changelog | Primary docs | Context |
| OpenAI Codex GitHub releases | Changelog | Top signal |
| Claude Code changelog | Primary docs | Top signal |
| Claude Code GitHub releases | Changelog | Top signal |
| Addy Osmani Loop Engineering | Practitioner post | Top signal |
| O'Reilly Radar Loop Engineering | Practitioner post | Context |
| Vercel durable AI code agent guide | Primary docs | Top signal |
| Vercel Workflows | Primary docs | Context |
| Vercel Sandbox | Primary docs | Context |
| Hugging Face Agentic Resource Discovery | Primary blog | Top signal |
| IETF MCP security considerations draft | Standards draft | Top signal |
| Kong MCP tool governance | Engineering post | Action packet |
| Automated Benchmark Auditing | Academic preprint | Top signal |
| Efficient Benchmarking of AI Agents | Academic preprint | Scout |
| AgentProcessBench | Academic preprint | Context |
| Agent Skill Evaluation and Evolution | Academic preprint | Scout |
| Formal Modeling and Verification for Agent Workflow and Trajectory | Academic preprint | Scout |
| AgentDiet | Academic preprint | Scout |
| LangChain traces start the agent improvement loop | Practitioner post | Context |

## Archive notes

- The New Stack article was blocked during direct fetch. It remains directionally aligned with the loop-engineering sources used here, but it is not cited as a primary source in this issue.
- Secondary vulnerability writeups were useful for triage but the MCP security signal relies on the IETF draft and Kong's governance guidance.
- Google Gemini CLI and GitHub Actions are watchlist items this week, not top signals. They are useful comparative baselines once the run-evidence export path is clear.

## Closing thought

The agent frontier is becoming less about a stronger worker and more about the loop around the worker. The teams that win will know what the agent saw, which tools it could reach, where it ran, why it stopped, and which artifact its failure created.
