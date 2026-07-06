<!--
iso_week: 2026-W28
through_date: 2026-07-06
profile_id: builder-tpm
registry_version: 7
matrix_run_id: MTRX-W28-loop-harness-evidence
-->

# The loop is the unit of work now

**Week of 2026-07-06 - Vol. 10**

## Field thesis

The week had plenty of framework news. The useful pattern sat one layer below the announcements: a working agent product now needs a loop that can see its own traces, shrink its context, govern its memory, prove its tool path, and turn a failed run into the next checked artifact. The model still matters. The operating surface around it is where the product gets better or quietly rots.

## Top signals

### 1. Loop engineering made the recurring system the design object

**Source:** [Addy Osmani, "Loop Engineering"](https://addyosmani.com/blog/loop-engineering/), [OpenAI, "Harness engineering"](https://openai.com/index/harness-engineering/)

**Payload:** Osmani frames the shift from prompting an agent to designing a loop that finds work, hands it out, checks it, writes state, and decides the next step. OpenAI describes the same shape inside Codex: worktree-local app boot, browser control, logs, metrics, traces, and repository knowledge as the system of record.

**Mechanism:** The loop becomes a small operating system: trigger, context map, workcell, worker, verifier, evidence, repair queue.

**Why it matters:** This is the missing line between "we used agents" and "the system can improve next week." A loop without a state file forgets. A loop without a verifier grades itself. A loop without evidence creates motion the operator cannot audit.

**Reusable pattern:** Every recurring agent task gets a `loop_contract.yaml`: trigger, source item, allowed paths, tool loadout, budget, verifier, stop reason, evidence sink, and repair target.

**Action surface:** `workflow`, `run-evidence`, `software-control-plane`

**Try this week:** Take one scheduled or repeated task and write the loop contract before running it again.

**Systems map:** source item -> loop contract -> isolated workcell -> worker run -> verifier -> evidence packet -> repair queue.

**Transferable principle:** Repetition needs an artifact spine. This applies to brief generation, factory cohorts, CI triage, and source scouting.

**Falsification test:** If the next run cannot tell what the prior run tried, passed, failed, and changed, the loop is a recurring prompt, not an operating system.

**Adoption ladder:**
  - Minimum viable: one loop contract for one recurring task.
  - Mid: evidence packet plus separate verifier.
  - Full: failure routes to eval, patch, context edit, or hold decision.
  - Monitoring: count repeated failures, missing evidence packets, and self-approved runs.

**Confidence:** High.

**Evidence:** W28-LOOP-001, W28-OPENAI-001.

### 2. Harness changes beat model changes when traces drive the patch

**Source:** [LangChain, "Improving Deep Agents with harness engineering"](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering), [Google Developers, "Driving the Agent Quality Flywheel"](https://developers.googleblog.com/en/driving-the-agent-quality-flywheel-from-your-coding-agent/)

**Payload:** LangChain reports a fixed-model coding-agent score move from 52.8 to 66.5 on Terminal Bench 2.0 by changing the harness: prompt, tools, middleware, trace analysis, and self-verification. Google packages the quality loop as data preparation, inference, grading, failure analysis, and targeted iteration, with the optimizer kept separate from the evaluator.

**Mechanism:** Trace analysis is becoming the unit of repair. A failed path becomes a metric or test, then a targeted change, then a before/after comparison.

**Why it matters:** Prompt edits without a trace corpus are guesswork. A trace-backed change can say what failure it fixed and whether the fix moved the measured behavior.

**Reusable pattern:** Add a `trace_to_change` record beside run evidence: failure class, source trace, candidate eval, patch type, baseline score, rerun score, and rollback.

**Action surface:** `eval`, `workflow`, `run-evidence`

**Try this week:** Convert one failed factory run into one new test or one new gate before editing the worker prompt.

**Systems map:** trace -> failure label -> eval case -> patch -> rerun -> comparison.

**Transferable principle:** The repair target should be produced by the trace, not by the operator's memory of the trace.

**Falsification test:** If a prompt change cannot name the trace it came from, it belongs in a trial branch, not in the main loop.

**Adoption ladder:**
  - Minimum viable: store failing traces and labels.
  - Mid: one eval per recurring failure class.
  - Full: patch proposals require before/after metrics.
  - Monitoring: track fixes that help one case and regress another.

**Confidence:** High.

**Evidence:** W28-LANGCHAIN-001, W28-GOOGLE-001.

### 3. Context failures need diagnoses, not bigger windows

**Source:** [Drew Breunig, "How Long Contexts Fail"](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html), [Redis, "Quality Context"](https://redis.io/blog/quality-context-ai-agents/)

**Payload:** Breunig's taxonomy - poisoning, distraction, confusion, clash - gives names to four ways long contexts fail. Redis extends the same frame into "context rot": the pile-up of wrong, excess, irrelevant, and conflicting material over an agent's life.

**Mechanism:** The context window behaves like working memory with failure modes. Each failure asks for a different repair: validate, prune, isolate, or reconcile.

**Why it matters:** Many agent failures get misfiled as model weakness. The source was often a poisoned handoff, too many tools, stale memory, or two authority surfaces fighting inside the same prompt.

**Reusable pattern:** Add a context-failure label to every failed run: `poisoning`, `distraction`, `confusion`, `clash`, or `none-observed`.

**Action surface:** `personal-knowledge-base`, `workflow`, `eval`

**Try this week:** Take three failed agent runs and label the context failure before proposing a fix.

**Systems map:** context assembly -> failure mode -> targeted repair -> rerun with shorter evidence.

**Transferable principle:** A smaller correct context beats a large contradictory one. This applies to RAG, repo context, and source-scanning briefs.

**Falsification test:** If shrinking or reconciling context does not change the failure, look at tools, model choice, or task ambiguity next.

**Adoption ladder:**
  - Minimum viable: label context failures after bad runs.
  - Mid: add pruning and authority-order rules.
  - Full: context assembly emits a manifest with included and excluded blocks.
  - Monitoring: count repeated failure modes by repo and task type.

**Confidence:** High.

**Evidence:** W28-CONTEXT-001.

### 4. Retrieval is becoming a filesystem, not a single search box

**Source:** [LlamaIndex, "Announcing Retrieval Harness"](https://www.llamaindex.ai/blog/announcing-retrieval-harness), [arXiv:2606.04315 on agentic memory systems](https://arxiv.org/abs/2606.04315)

**Payload:** LlamaIndex's Retrieval Harness exposes document corpora through hybrid retrieve, list files, file grep, and file read, plus layout evidence. The memory-systems paper finds a strong baseline in flat text paired with agentic grep/read tools across scenarios.

**Mechanism:** The agent asks the corpus a sequence of concrete questions instead of accepting one semantic top-k bundle as context.

**Why it matters:** Semantic retrieval is useful for narrowing the search space. It is weak as a proof path when an answer depends on file structure, exact strings, surrounding context, or layout.

**Reusable pattern:** Give source-ingestion agents four primitives: `list`, `grep`, `read`, and `cite_span`. Treat vector search as one primitive, not the whole system.

**Action surface:** `source-registry`, `architecture`, `eval`

**Try this week:** Add one retrieval eval that fails unless the agent uses an exact span from `read`, not only a retrieved chunk.

**Systems map:** corpus map -> exact search -> source read -> cited answer -> citation gate.

**Transferable principle:** Search finds candidates; reads prove claims. This applies to briefs, docket RAG, EDGAR ingestion, and policy replay.

**Falsification test:** If a vector-only answer and a read-backed answer agree across hard cases, the extra retrieval tools may be unnecessary for that corpus.

**Adoption ladder:**
  - Minimum viable: add exact grep and read tools.
  - Mid: require citations from read spans.
  - Full: preserve layout evidence for tables and forms.
  - Monitoring: track unsupported claims by retrieval primitive.

**Confidence:** Medium-high.

**Evidence:** W28-RETRIEVAL-001, W28-MEMORY-001.

### 5. Memory became a governance problem

**Source:** [arXiv:2604.08224, "Externalization in LLM Agents"](https://arxiv.org/abs/2604.08224), [arXiv:2603.11768, "Governing Evolving Memory in LLM Agents"](https://arxiv.org/abs/2603.11768)

**Payload:** The externalization review treats memory, skills, protocols, and harnesses as ways to move cognitive burdens out of the model and into system artifacts. The memory-governance paper names the hard part: semantic drift, privacy leakage, and memory corruption when agents write to their own long-term state.

**Mechanism:** Memory stops being a cache and becomes a controlled write surface. Each durable memory needs provenance, review status, expiry, and a deletion path.

**Why it matters:** A bad memory item is worse than a bad context chunk. It becomes the starting premise for future runs.

**Reusable pattern:** Store durable memory as typed records: claim, scope, source run, provenance, review status, expiry, and tombstone reason.

**Action surface:** `personal-knowledge-base`, `run-evidence`, `security`

**Try this week:** Convert one handoff note into typed memory and reject at least one stale or unsupported claim instead of summarizing everything.

**Systems map:** run output -> memory candidate -> verification -> durable memory -> future context.

**Transferable principle:** Memory writes should be reviewed like code. This applies to repo brains, prompt-library updates, brief source notes, and agent skills.

**Falsification test:** If unreviewed memory produces no measurable failures over a cohort, a lighter memory gate may be enough for that task class.

**Adoption ladder:**
  - Minimum viable: provenance on each memory line.
  - Mid: review status and expiry.
  - Full: memory write gate plus tombstone log.
  - Monitoring: count stale-memory hits and rejected memory candidates.

**Confidence:** Medium-high.

**Evidence:** W28-MEMORY-002, W28-EXT-001.

### 6. Sandboxes need grant logs, not just permission prompts

**Source:** [Anthropic, "How we contain Claude across products"](https://www.anthropic.com/engineering/how-we-contain-claude), [Model Context Protocol specification](https://modelcontextprotocol.io/specification/)

**Payload:** Anthropic's containment write-up is blunt about missed risks: project-local config before trust, user-supplied injection, egress through approved domains, and VM observability blind spots. MCP's spec also reminds implementers that tools are arbitrary code paths and that user consent, data privacy, tool safety, and sampling controls sit outside the protocol's automatic enforcement.

**Mechanism:** Runtime safety shifts from approval clicks to environmental boundaries. The grant - visible paths, writable paths, denied paths, network, egress, and artifact sink - is the security artifact.

**Why it matters:** A sandbox can work and still leak through an allowed API. A prompt can be typed by a real user and still be malicious. The boundary has to be explicit and testable.

**Reusable pattern:** Add `sandbox_grant` to every code-execution run record. Include a denied-path fixture and an egress statement.

**Action surface:** `security`, `tool-policy`, `run-evidence`

**Try this week:** Add one denied-path test to the factory workcell and record the grant in the run packet.

**Systems map:** task -> grant -> command -> boundary check -> evidence -> drift gate.

**Transferable principle:** Access is a capability, even when it looks like a destination or a convenience flag.

**Falsification test:** If the agent can read or send outside the grant and no gate fires, the sandbox is undocumented trust.

**Adoption ladder:**
  - Minimum viable: grant fields in run records.
  - Mid: denied-path and no-network fixtures.
  - Full: egress provenance and artifact-sink audit.
  - Monitoring: alert on grant expansion by task type.

**Confidence:** High.

**Evidence:** W28-SANDBOX-001, W28-MCP-001.

### 7. Product proof is moving from prose to replayable demos

**Source:** [Simon Willison on DSPy and Datasette Agent prompts](https://simonwillison.net/2026/Jul/2/dspy-datasette-agent-prompts/), [Simon Willison on `shot-scraper video`](https://simonwillison.net/2026/Jun/30/shot-scraper-video/)

**Payload:** Willison's DSPy note shows prompt optimization against the actual Datasette Agent tool path, not a detached toy prompt. His `shot-scraper video` note gives agents a way to record a browser routine as a review artifact.

**Mechanism:** The proof surface moves closer to the product. The agent runs the real tool implementation and produces a replayable artifact a reviewer can inspect.

**Why it matters:** A good run report still leaves the product experience invisible. A scripted video or browser trace shows whether the user path works, not just whether the code compiled.

**Reusable pattern:** For every UI-facing factory task, require either a screenshot, browser trace, or short scripted video in the evidence packet.

**Action surface:** `eval`, `workflow`, `software-control-plane`

**Try this week:** Add one storyboard to a deployed Streamlit or Vercel demo and store the output path in the run evidence.

**Systems map:** app boot -> scripted user path -> video/trace -> reviewer check -> release note.

**Transferable principle:** Show the artifact doing the work. This applies to app demos, brief publishing, source ingestion, and eval dashboards.

**Falsification test:** If the demo artifact does not catch defects beyond the test suite after several runs, keep it for launch surfaces only.

**Adoption ladder:**
  - Minimum viable: screenshot after the first action.
  - Mid: scripted browser path.
  - Full: video plus console/network log.
  - Monitoring: compare demo failures against unit-test failures.

**Confidence:** Medium-high.

**Evidence:** W28-PROOF-001.

## Reusable patterns

- **Loop contract.** Where it applies: recurring agent work, factory tasks, CI triage, weekly briefs. Caveats: it adds ceremony; use it where repetition or autonomy is real.
- **Trace-to-change.** Where it applies: prompt edits, worker prompts, eval harnesses, agent product tuning. Caveats: a trace can overfit the repair unless held-out cases exist.
- **Context failure labels.** Where it applies: long-running agents and source sweeps. Caveats: labels are diagnostic aids, not proof by themselves.
- **Filesystem retrieval.** Where it applies: documents, repos, dockets, SEC filings, policy text. Caveats: exact tools need rate and cost budgets.
- **Sandbox grant log.** Where it applies: code execution, browser automation, local MCP, file-write agents. Caveats: the grant must be enforced, not just written.

## Action queue

| Candidate | Surface | Effort | Risk | Test |
|---|---|---|---|---|
| Add `loop_contract.yaml` to one factory queue task | workflow | S | low | run the task and verify evidence names trigger, workcell, verifier, and repair target |
| Add context-failure labels to factory stop records | run-evidence | S | low | force one poisoning and one distraction fixture; metrics counts both |
| Add `sandbox_grant` to code-execution run records | security | M | medium | denied-path fixture fails before worker runs |
| Add filesystem retrieval eval to ai-field-brief | eval | M | medium | source claim must cite a read span, not only a search hit |
| Add browser proof artifact to one public app fix | workflow | M | low | run stores screenshot or video path in the run packet |

## Action packets

| Source | Target | Surface | Try | Proof metric | Rollback | Kill criterion |
|---|---|---|---|---|---|---|
| loop-engineering | factory | workflow | Add `loop_contract.yaml` for one ratified task | task evidence validates and stop reason is present | remove contract gate from task template | more than 20 minutes added with no new caught defect |
| google-flywheel | trace-to-eval-harness | eval | Add `trace_to_change` schema and one failed-run sample | validator rejects a record with no next artifact | keep schema as example-only | no failed run can be converted into a test or patch |
| context-failure | factory | run-evidence | Add context-failure label to stop events | metrics report failures by label | keep labels optional | labels are mostly `unknown` after one cohort |
| retrieval-harness | ai-field-brief | source-registry | Add a read-span citation gate for one source lane | unsupported-claim fixture fails | gate scoped to one lane | too many false positives on primary-source docs |
| sandbox-grant | procurement-negotiation-lab | security | Add grant fields plus denied-path fixture | denied read fails and run record records the grant | mark grant advisory | grant expands silently across two tasks |

## Scout radar

| Item | Why it might matter early | What to watch | Revisit trigger |
|---|---|---|---|
| Google quality-flywheel skills | They turn agent evaluation into a coding-agent-driven loop. | Whether the skills expose portable trace formats outside Google Cloud. | A non-ADK repo publishes a clean adapter. |
| LlamaIndex Retrieval Harness | It gives retrieval agents file-like tools instead of a single search box. | API shape, export format, layout evidence. | A public benchmark shows fewer unsupported claims. |
| Role-confusion defenses | The paper gives a more precise prompt-injection frame than "ignore tool instructions." | Destyling, role-classifier, and tool-output sanitation fixtures. | A practical repo ships reusable eval cases. |
| Agentic memory flat-file baseline | It challenges complex memory stacks with grep/read tools. | Reproducible tasks and failure cases. | The baseline holds on a repo or docket corpus. |
| Shot-scraper video | It turns product proof into a run artifact. | Browser automation reliability in CI. | One portfolio app stores a video artifact in run evidence. |
| AgentCore Policy | Cedar-backed policy at the tool call layer could become a useful hosted comparator. | Exportability of policy decisions and trace spans. | A local factory task maps cleanly to an AgentCore policy fixture. |

## Watchlist

- **Will managed agent platforms export enough evidence?** Revisit trigger: AgentCore, ADK, or a similar platform publishes a portable run-evidence export.
- **Will memory governance move from papers into tooling?** Revisit trigger: a memory library adds provenance, expiry, and tombstones as first-class fields.
- **Will context-failure labels predict repair cost?** Revisit trigger: one factory cohort records labels and rework rounds.
- **Will role-confusion defenses become standard eval fixtures?** Revisit trigger: a mainstream agent framework adds role-confusion tests to CI examples.

## Archive notes

- **Daily Systems Brief, July 1-6.** Useful mechanism feed for power, policy, capital, and frontier-access themes. Several claims need primary verification before they can become public brief claims.
- **Vendor framework launch posts.** Many framework pages were useful as source-registry coverage but did not earn Top-signal status without a failure mode or proof path.
- **SEO multi-agent orchestration posts.** Patterns were familiar; production-success statistics were not sourced well enough to carry.

## Sources reviewed

| Source | Status | Note |
|---|---|---|
| Weekly GenAI Digest folder | ok | selected as synthesis input; public sources verified separately |
| Daily Systems Brief folder | ok | used as mechanism scout; unverified claims not promoted |
| Addy Osmani | ok | loop-engineering source promoted |
| OpenAI harness engineering | ok | repository knowledge and app-legibility source promoted |
| LangChain harness engineering | ok | trace-analysis and self-verification source promoted |
| Google Agent Quality Flywheel | ok | evaluator/optimizer separation and trace grading promoted |
| LlamaIndex Retrieval Harness | ok | filesystem retrieval primitive promoted |
| Anthropic containment postmortem | ok | sandbox grant and egress risk promoted |
| MCP specification | ok | protocol security principles promoted |
| Role-confusion project | ok | watchlist and registry addition |
| arXiv agentic memory baseline | ok | retrieval/memory signal promoted |
| arXiv externalization review | ok | memory/skills/protocols/harness frame promoted |
| arXiv governed memory | ok | memory-governance signal promoted |
| Simon Willison DSPy note | ok | product-prompt optimization source promoted |
| Simon Willison shot-scraper video | ok | demo-as-proof source promoted |
| Redis context article | ok | registry addition and context-failure support |
| Drew Breunig context failure post | ok | context-failure taxonomy promoted |

## Closing thought

The loop does not need to be grand. It needs to leave enough evidence that the next run can be less wrong.
