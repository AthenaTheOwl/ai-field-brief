<!--
meta:
  iso_week: 2026-W23
  through_date: 2026-06-03
  profile_id: broad_builder
  matrix_run_id: MTRX-W23-catchup-codex
  sources_swept_count: 24
  cells_verified_count: 24
  volume: 001
  mode: catch-up
-->

# The week replay became the operating contract

**week of 2026-06-01 - audience: builder-tpms thinking about AI - vol. 001**

## Field thesis

Three releases this week describe the same thing from three angles. OpenAI's Agents SDK adds a model-native loop, a sandbox, a Manifest, snapshots, and state rehydration. OpenAI's June 2 Codex update extends agent work into reports, spreadsheets, contracts, dashboards, and small apps. Langfuse ships deterministic code evaluators that sit next to traces and experiments. Same shape every time: the artifact needs a replay record, a deterministic gate where one exists, a reviewer, and a rollback path. Shipping the output without those four is shipping a demo.

Catch-up issue. Six Top signals, 24 verified cells, three Action packets.

## Top signals

### 1. OpenAI Agents SDK sandbox + RunState - replay moves into the runtime

**Source:** [OpenAI, "The next evolution of the Agents SDK"](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)

**Payload:** OpenAI's April 15 SDK update adds a model-native agent
loop and native sandbox execution for agents that inspect files, run
commands, edit code, and work across long tasks in controlled
environments. The same post describes Manifest-backed workspaces,
provider sandboxes, snapshotting, and rehydration.

**Mechanism:** The run state becomes separate from the sandbox that
executes the work. A container can fail, expire, or be replaced while a
serialized run continues from the last checkpoint.

**Why it matters:** This turns "can the agent finish" into "can we
prove the same run conditions can resume." That is the bridge between
agent demos and CI. It also gives the portfolio a concrete next step:
map OpenAI RunState snapshots to CDCP Run records and trace-to-eval
packets.

**Reusable pattern:** Treat every long agent task as a replay envelope:
prompt hash, tool-schema hash, sandbox ref, checkpoint ref, gate
summary, and artifact refs.

**Action surface:** runtime-adapter, eval

**Try:** Run a two-hour spike that serializes an Agents SDK RunState
for one tiny file-edit task, then compare its fields with the existing
CDCP Run schema.

**Systems map:** The system boundary moves from prompt call to
work-envelope. The unit under review is prompt plus tools plus files
plus state plus sandbox plus output.

**Transferable principle:** If a task can change files, the resume
object is part of the product. This applies to coding agents, brief
generation, research agents, and spreadsheet agents.

**Falsification test:** If the SDK cannot expose enough state to verify
prompt, tools, sandbox, checkpoint, and artifact refs without private
vendor telemetry, CDCP keeps its own run-evidence emitter as the source
of truth.

**Adoption ladder:**

  - Minimum viable: serialize one RunState from a local sandbox task and
    record which CDCP Run fields can be populated.
  - Mid: add a trace-to-eval fixture that consumes both the CDCP ledger
    and the SDK state snapshot.
  - Full: require a replay packet for every agent task before a commit
    can land.
  - Monitoring: mismatch count between SDK state, CDCP Run record, and
    trace packet.

**Confidence:** high

**Evidence:** MTRX-W23-openai-agents-sdk-source_gist, MTRX-W23-openai-agents-sdk-mechanism_extraction, MTRX-W23-openai-agents-sdk-adoption_action, MTRX-W23-openai-agents-sdk-systems_thinking

---

### 2. Codex role plugins + knowledge-work report - artifact work moves outside engineering

**Source:** [OpenAI, "Codex for every role, tool, and workflow"](https://openai.com/index/codex-for-every-role-tool-workflow/) and [OpenAI, "Codex is becoming a productivity tool for everyone"](https://openai.com/index/codex-for-knowledge-work/)

**Payload:** OpenAI says Codex now has more than five million weekly
users. Knowledge workers are about one-fifth of the user base and are
growing faster than developers. The June 2 product release adds
role-specific plugins, annotations, and shareable sites.

**Mechanism:** The agent surface has moved from code diffs into reports,
spreadsheets, presentations, contracts, dashboards, research, and light
apps. That means review cannot live only at pull requests.

**Why it matters:** The next weak point is artifact governance. A
finance memo, investor packet, contract draft, or ops dashboard needs
source boundaries and approval gates with the same seriousness as a code
change.

**Reusable pattern:** Create a role-surface table for every agent
artifact class: who can invoke it, what data it may read, which tools it
may call, who reviews output, where the run evidence lands, and what
undo path exists.

**Action surface:** agent-role, workflow

**Try:** Pick one artifact class outside code and write its
role-surface table before letting an agent produce the next version.

**Systems map:** Codex expansion converts knowledge work into
agent-created artifacts. The governance shape must follow the artifact,
not the old job title.

**Transferable principle:** The review surface belongs where the
artifact changes risk. A dashboard needs data-lineage review; a contract
needs legal review; a report needs source review.

**Falsification test:** If non-engineering Codex use grows without new
artifact defects, approval misses, or data-scope incidents over one
quarter, the artifact-gate urgency is lower than this brief claims.

**Adoption ladder:**

  - Minimum viable: one table row for one artifact class.
  - Mid: require source list, reviewer, and rollback for every
    agent-created external artifact.
  - Full: route artifact classes through role-specific plugins and
    evidence packets.
  - Monitoring: number of artifacts with source refs, reviewer signoff,
    and rollback path.

**Confidence:** high

**Evidence:** MTRX-W23-codex-role-source_gist, MTRX-W23-codex-role-mechanism_extraction, MTRX-W23-codex-role-adoption_action, MTRX-W23-codex-role-systems_thinking

---

### 3. Langfuse code evaluators - deterministic checks join trace review

**Source:** [Langfuse code evaluators changelog](https://langfuse.com/changelog/2026-05-28-code-evaluators) and [Langfuse code evaluator docs](https://langfuse.com/docs/evaluation/evaluation-methods/code-evaluators)

**Payload:** Langfuse now runs Python or TypeScript evaluators against
observations and experiments, returning native scores for trace views,
experiment comparisons, filters, dashboards, and score analytics.

**Mechanism:** Objective checks move into code. JSON parseability,
schema validation, exact match, required tool arguments, and business
rules can run with deterministic logic while model judges handle
semantic scoring.

**Why it matters:** This is the eval split most agent teams need:
deterministic gates for invariants, model judges for judgment calls.
The brief system already has rules that fit this rail: every Top Signal
must include source, action surface, confidence, systems map,
transferable principle, falsification test, and adoption ladder.

**Reusable pattern:** Move invariant checks out of prompts and into code
evaluators. Leave model review for quality, caveats, and synthesis.

**Action surface:** eval, config

**Try:** Write one evaluator that fails a brief item if it lacks source
link, action surface, confidence, and the four systems fields.

**Systems map:** Agent quality control splits into invariants and
judgment. Invariants belong in code because they are cheap, repeatable,
and explainable.

**Transferable principle:** Any rule you can state as a schema should
be tested as code before a judge model sees the output. This applies to
briefs, support responses, tool calls, contract drafts, and dashboards.

**Falsification test:** If deterministic checks create too many false
failures after two weekly briefs, keep them as advisory scores and gate
only source-link presence plus schema validity.

**Adoption ladder:**

  - Minimum viable: one local Python evaluator in `scripts/`.
  - Mid: attach the evaluator to every brief run and emit a score.
  - Full: ingest scores into Langfuse or an equivalent trace system.
  - Monitoring: false-failure rate, true defect catch rate, and time
    spent fixing evaluator findings.

**Confidence:** high

**Evidence:** MTRX-W23-langfuse-code-eval-source_gist, MTRX-W23-langfuse-code-eval-mechanism_extraction, MTRX-W23-langfuse-code-eval-adoption_action, MTRX-W23-langfuse-code-eval-systems_thinking

---

### 4. AgentTrust + SLEIGHT-Bench - monitors need a pre-execute policy layer

**Source:** [AgentTrust paper](https://arxiv.org/abs/2605.04785) and [Anthropic Alignment Science, "SLEIGHT-Bench"](https://alignment.anthropic.com/2026/sleight-bench/)

**Payload:** AgentTrust proposes runtime safety evaluation and
interception for agent tool use. SLEIGHT-Bench studies monitor blind
spots with 40 harmful coding-agent transcript attacks across 11
categories.

**Mechanism:** SLEIGHT-Bench tests what monitors miss after a transcript
exists. AgentTrust shifts the control point earlier by turning tool
requests into typed Action records and scoring the proposed side effect
before execution.

**Why it matters:** A monitor can tell you a run looked suspicious. A
pre-execute policy layer can stop the bad tool call. Engineering-grade
agents need both.

**Reusable pattern:** Put every risky tool call through a typed action
record: actor, tool, target path or URL, data class, requested side
effect, verdict, and reviewer.

**Action surface:** tool-policy, software-control-plane

**Try:** Add one `ActionRecord` fixture to the security-lab MCP diff
gate and test allow, warn, block, and review outcomes.

**Systems map:** Agent safety becomes a sequence of checkpoints:
permission before execution, monitor during execution, evidence after
completion. Missing any one of the three leaves a blind spot.

**Transferable principle:** The safest time to classify a side effect is
before it happens. The same pattern applies to shell commands, emails,
database writes, deploys, and outbound HTTP.

**Falsification test:** If SLEIGHT-style transcripts no longer bypass
frontier monitors on the same attack categories, then the pre-execute
layer should run only on high-risk paths.

**Adoption ladder:**

  - Minimum viable: typed action record for one shell command gate.
  - Mid: policy verdicts for file write, HTTP, email, and deploy tools.
  - Full: every high-risk tool call produces an ActionRecord before it
    runs and a Run event after it completes.
  - Monitoring: blocked calls, reviewed calls, false blocks, and missed
    incidents.

**Confidence:** medium-high

**Evidence:** MTRX-W23-agenttrust-source_gist, MTRX-W23-sleight-source_gist, MTRX-W23-agenttrust-sleight-mechanism_extraction, MTRX-W23-agenttrust-sleight-adoption_action

---

### 5. ITBench-AA - enterprise agent tasks need stateful ops evals

**Source:** [Hugging Face / IBM Research, "ITBench-AA"](https://huggingface.co/blog/ibm-research/itbench-aa)

**Payload:** IBM Research and Artificial Analysis published ITBench-AA,
a benchmark for agentic enterprise IT tasks, and report frontier models
below 50 percent on the first release.

**Mechanism:** Enterprise IT tasks force an agent to handle partial logs,
symptoms, changing state, remediation choices, and rollback. A static
prompt score does not measure that shape.

**Why it matters:** The fastest way to fool yourself is to test the
agent on clean examples while deploying it into messy ops. Every serious
agent repo needs at least one ugly Tuesday eval.

**Reusable pattern:** Add "stateful ops realism" rows to eval suites:
stale context, one tempting wrong fix, partial evidence, and a required
rollback decision.

**Action surface:** eval, workflow

**Try:** Add one ITBench-inspired case to each product repo that runs an
agent or eval. Keep it tiny but make it stateful.

**Systems map:** The enterprise agent must act inside a changing system.
The evaluation must include time, partial observability, and recovery,
or it measures only prose skill.

**Transferable principle:** If the production surface has state, the
eval must carry state. This applies to supplier-risk refreshes,
watchlist exports, brief generation, and negotiation engines.

**Falsification test:** If an agent passes stateful ops cases while still
failing user-visible deployments, the eval is missing the wrong state
dimension. Add the real failure trace to the suite.

**Adoption ladder:**

  - Minimum viable: one failing ops case copied from a real bug.
  - Mid: gate one repo on the case.
  - Full: every agent repo keeps a messy-state eval lane.
  - Monitoring: failures caught before demo, rollback correctness, and
    time to isolate root cause.

**Confidence:** high

**Evidence:** MTRX-W23-itbench-source_gist, MTRX-W23-itbench-mechanism_extraction, MTRX-W23-itbench-adoption_action, MTRX-W23-itbench-systems_thinking

---

### 6. Rosalind Biodefense - domain agents ship with access review attached

**Source:** [OpenAI, "Strengthening societal resilience with Rosalind Biodefense"](https://openai.com/index/strengthening-societal-resilience-with-rosalind-biodefense/) and [OpenAI, "Introducing GPT-Rosalind"](https://openai.com/index/introducing-gpt-rosalind/)

**Payload:** OpenAI launched Rosalind Biodefense on May 29 for vetted
defensive partners. The earlier GPT-Rosalind launch includes a Codex
life-sciences plugin with more than 50 tools and data sources, plus a
trusted-access model for qualified users.

**Mechanism:** High-stakes domain agents are packaging model, tool
plugin, access review, and governance into one deployment structure.
The model is not shipped as an unconstrained general assistant for the
domain.

**Why it matters:** This is the pattern for any agent touching regulated
or dual-use data: capability and access policy ship together. The
portfolio can reuse it for supplier-risk, security, health, and
financial artifacts.

**Reusable pattern:** Write the access rubric before the demo: allowed
users, allowed data, blocked outputs, audit log, escalation path, and
revocation trigger.

**Action surface:** tool-policy, agent-role

**Try:** Pick one repo with sensitive outputs and add an access rubric
beside the demo README.

**Systems map:** Domain agents move risk into the distribution layer.
The access contract decides who can turn capability into action.

**Transferable principle:** A domain plugin without an access rubric is
an unfinished product. The same rule applies to legal, finance, medical,
security, and procurement agents.

**Falsification test:** If open domain plugins show lower incident rates
than trusted-access domain plugins over the same period and task class,
the access-review burden should shrink.

**Adoption ladder:**

  - Minimum viable: one access rubric beside one demo.
  - Mid: tie every high-risk demo to allowed data, allowed users, and
    blocked outputs.
  - Full: emit access-decision events into the Run ledger.
  - Monitoring: access denials, escalations, and any artifact that
    leaves the intended audience.

**Confidence:** medium

**Evidence:** MTRX-W23-rosalind-biodefense-source_gist, MTRX-W23-rosalind-plugin-source_gist, MTRX-W23-rosalind-mechanism_extraction, MTRX-W23-rosalind-adoption_action

## Reusable patterns

- **Replay envelope.** Where it applies: long-running agents, brief
  generation, evals, and data refreshes. Caveat: vendor state snapshots
  may omit fields CDCP needs, so keep local Run records until parity is
  proven.
- **Artifact role surface.** Where it applies: non-code Codex outputs
  such as memos, dashboards, contracts, reports, and spreadsheets.
  Caveat: the reviewer changes by artifact class.
- **Deterministic first gate.** Where it applies: schema, source, tool
  argument, and required-field checks. Caveat: quality judgment still
  needs a human or model review pass.
- **Pre-execute policy.** Where it applies: file writes, shell commands,
  outbound HTTP, database writes, emails, and deploys. Caveat: bad policy
  blocks useful work, so track false blocks.

## Action queue

| Candidate | Surface | Effort | Risk | Test |
|---|---|---|---|---|
| Agents SDK RunState to CDCP Run mapping spike | runtime-adapter | M | low | Serialize one sandbox run and report field parity against `run.schema.json` |
| Brief deterministic evaluator | eval | S | low | Fail a fixture brief missing source, action surface, confidence, or systems fields |
| Typed ActionRecord for one risky tool | tool-policy | M | medium | Run allow/warn/block/review fixtures through a local gate |
| Role-surface table for one non-code artifact | agent-role | S | low | Produce one row with source, reviewer, allowed tools, gate, and rollback |

## Action packets

| Source | Target | Surface | Try | Proof metric | Rollback | Kill criterion |
|---|---|---|---|---|---|---|
| OpenAI Agents SDK | trace-to-eval-harness | runtime-adapter | Serialize one RunState and compare to a CDCP Run record | Field parity report with gaps named | Keep current CDCP emitter as source of truth | SDK state cannot expose prompt/tool/checkpoint refs |
| Langfuse code evaluators | ai-field-brief | eval | Add a local evaluator for brief required fields | Fixture with missing field fails | Keep as advisory check | False-failure rate above 20 percent after two briefs |
| AgentTrust + SLEIGHT-Bench | mcp-security-lab | tool-policy | Add typed ActionRecord fixtures to one gate | Four verdict fixtures pass | Remove ActionRecord branch | Gate cannot name target, data class, and side effect |

## Scout radar

| Item | Why it might matter early | What to watch | Revisit trigger |
|---|---|---|---|
| [MCPWorks](https://www.mcpworks.io/) | Open-source agent runtime around MCP, sandboxing, scheduling, encrypted state, and webhooks | Cloud launch, repo activity, issue quality | First working CDCP-compatible run ledger or public customer |
| [Agentic Index](https://agenticindex.io/) | Directory and comparison layer for agent products | Methodology updates and data freshness | Weekly change log adds source timestamps and diffable vendor fields |
| [E2B docs](https://www.e2b.dev/docs) | Sandbox docs expose snapshots, persistence, auto-resume, OTel export, MCP gateway, and provider adapters | Whether SandboxHandle-style APIs become stable | API adds replay-friendly metadata or run IDs |
| [Smithery](https://smithery.ai/servers/smithery) | MCP registry and server distribution surface | Credential handling, versioning, and security notes | Credential broker exposes auditable rotation or scope reports |
| [MagenticLite](https://www.microsoft.com/en-us/research/blog/magenticlite-magenticbrain-fara1-5-an-agentic-experience-optimized-for-small-models/) | Small-model agent stack with browser and file-system flow | Local-run reproducibility and cost profile | A repo task succeeds with local small-model orchestration |

## Watchlist

- **Does Agents SDK TypeScript get sandbox parity?** Revisit trigger:
  OpenAI ships TypeScript sandbox support or a public RunState example
  for file-edit tasks.
- **Do code evaluators displace judge models for agent CI?** Revisit
  trigger: Langfuse or another eval vendor publishes production usage
  data for deterministic evaluator catch rate.
- **Does ITBench-AA change enterprise agent marketing?** Revisit
  trigger: first vendor publishes ITBench-AA score next to SWE-Bench or
  TAU-bench.
- **Does trusted-access become the default for domain agents?** Revisit
  trigger: a second vendor ships a domain model with plugin plus access
  review as the product bundle.

## Archive notes

- **OpenAI, "OpenAI's Frontier Governance Framework"** ([source](https://openai.com/index/openai-frontier-governance-framework/)). Kept as a governance reference; less actionable than the SDK and role-surface releases for this issue.
- **Microsoft Research, "MagenticLite, MagenticBrain, Fara1.5"** ([source](https://www.microsoft.com/en-us/research/blog/magenticlite-magenticbrain-fara1-5-an-agentic-experience-optimized-for-small-models/)). Already covered in W22; moved to Scout radar for local-agent testing.
- **OpenAI Help Center, ChatGPT Enterprise and Edu release notes** ([source](https://help.openai.com/en/articles/10128477-chatgpt-enterprise-ve-edu-s%C3%BCr%C3%BCm-notlar%C4%B1)). Useful admin-surface detail; the Codex product posts made the cleaner Top Signal.
- **Vercel, "Sandbox vs E2B"** ([source](https://vercel.com/kb/guide/vercel-sandbox-vs-e2b)). Useful provider comparison; held for the next runtime-adapter pass.
- **OpenAI, "Introducing GPT-Rosalind"** ([source](https://openai.com/index/introducing-gpt-rosalind/)). Used as supporting source for the Rosalind Biodefense pick.

## Sources reviewed

| Source | Status | Note |
|---|---|---|
| OpenAI Agents SDK | ok | Top Signal 1 |
| OpenAI Codex role release | ok | Top Signal 2 |
| OpenAI Codex knowledge-work report | ok | Top Signal 2 |
| Langfuse code evaluators | ok | Top Signal 3 |
| Langfuse experiments CI | ok | supporting eval context |
| AgentTrust paper | ok | Top Signal 4 |
| Anthropic SLEIGHT-Bench | ok | Top Signal 4 |
| Hugging Face / IBM ITBench-AA | ok | Top Signal 5 |
| OpenAI Rosalind Biodefense | ok | Top Signal 6 |
| OpenAI GPT-Rosalind | ok | supporting source for Top Signal 6 |
| OpenAI Frontier Governance Framework | ok | archive |
| Microsoft MagenticLite | ok | Scout radar |
| Microsoft Fara1.5 article | ok | supporting scout context |
| E2B docs | ok | Scout radar |
| Vercel Sandbox vs E2B | ok | archive |
| Smithery | ok | Scout radar |
| MCPWorks | ok | Scout radar |
| Agentic Index | ok | Scout radar |
| OpenAI Enterprise/Edu notes | ok | archive |
| MCPlato agent-stack landscape | skipped | secondary source; use only if primary sources thin |
| Reddit agent-platform comparison | skipped | discussion source; no Top Signal without primary support |
| GPT-5.6 rumor threads | skipped | no official source |
| Wikipedia model pages | skipped | avoid for current product facts |
| vendor roundup posts | skipped | use primary sources first |

## Closing thought

The next useful brief action is a smaller gate: take one source-backed
rule from this issue and make it fail in CI when the next agent-created
artifact breaks it.
