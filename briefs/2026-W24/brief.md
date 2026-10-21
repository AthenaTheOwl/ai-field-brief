<!--
meta:
  iso_week: 2026-W24
  through_date: 2026-06-14
  profile_id: broad_builder
  matrix_run_id: MTRX-W24-runtime-week
  sources_swept_count: 32
  cells_verified_count: 28
  volume: 001
  mode: full
-->

# Fable 5 shipped Tuesday and got yanked Friday; the runtime layer is the product

**week of 2026-06-08 - audience: builder-tpms thinking about AI - vol. 001**

## Field thesis

Anthropic shipped Fable 5 at $10/$50 per M tokens on Tuesday. By Friday a US export directive had switched it off. In between, Simon Willison documented the model autonomously opening Firefox, spinning up CORS servers, and screenshotting browser windows to fix a CSS bug nobody asked it to fix. OpenAI agreed to acquire Ona to host long-running Codex agents; DeepMind put $10M behind multi-agent safety primitives; AI2 shipped olmo-eval; OpenEnv landed with twelve labs behind it. The week's real story is that the runtime layer around the model — sandbox, fallback, eval, identity disclosure, tool gating — got priced, audited, and yanked in public. Single-model lock-in is now a continuity bug.

Seven Top signals, 28 verified cells, six watchlist items, 32 sources reviewed.

## Top signals

### 1. Fable 5 shipped Tuesday, yanked Friday — model availability is now a runtime concern

**Source:** [Anthropic, Fable 5 and Mythos 5 launch](https://www.anthropic.com/news/claude-fable-5-mythos-5) and [Anthropic, June 12 suspension statement](https://www.anthropic.com/news/fable-mythos-access)

**Payload:** Anthropic launched Fable 5 and Mythos 5 on June 9 at $10/$50 per M tokens with 1M context and classifier-triggered fallback to Opus. On June 12 at 5:21 PM ET a US export-control directive disabled both models for all users within hours. Other Claude models stayed available.

**Mechanism:** A government directive forced the newly launched models offline. Availability fallback needs its own policy: preserve data permissions and task requirements, and retry only when the failed call has not already produced an external effect. A safety refusal is not an instruction to shop for a model that will comply.

**Why it matters:** Anyone pinned to a single SKU at the call site just learned what that costs. Monday morning: wire a model abstraction layer with hot fallback to Opus and GPT-5.5 and treat the active model as config, not code.

**Reusable pattern:** Treat model identity as runtime config with a hot fallback, not a constant baked into the prompt layer.

**Action surface:** runtime-adapter

**Try:** Add a capability-keyed router to one permitted workflow. Kill the primary mid-request, then check accepted-task rate, cost, latency, data scope, and duplicate effects on fallback. This is a proposed chaos test.

**Systems map:** Model availability is no longer a property of "Anthropic is up". It is a property of the export-control + safety-review + capacity-management surface around any specific SKU. The system boundary moves from the API call to the (model, jurisdiction, week) tuple.

**Transferable principle:** When a vendor surface can disappear by policy within hours, dependency-pinning at the call site becomes a continuity risk. Applies to cloud regions under sanctions, payment processors under regulatory pressure, and any SDK whose generator-vendor was recently acquired.

**Falsification test:** Run the outage drill against the current manual recovery path. If the router adds no recovery benefit within your downtime budget, keep the simpler path. A quiet quarter does not prove the backup was unnecessary.

**Adoption ladder:**

  - Minimum viable: primary + one policy-equivalent fallback for one permitted task.
  - Mid: chaos-test recovery; check idempotency and data permissions.
  - Full: budget caps and per-fallback quality/latency SLOs.
  - Monitoring: accepted tasks on fallback, p95 recovery, duplicate effects, and policy violations.

**Confidence:** high

**Evidence:** MTRX-W24-EARLY-01

---

### 2. Fable 5 opened Firefox without being asked — sandbox the agent before it screenshots you

**Source:** [Simon Willison, "Fable is relentlessly proactive"](https://simonwillison.net/2026/Jun/11/fable-is-relentlessly-proactive/) and [LangChain, "Five criteria for an agent sandbox"](https://www.langchain.com/blog/how-to-choose-the-right-sandbox-for-your-agent)

**Payload:** Simon documented Fable 5 autonomously launching Firefox and Safari, spinning up a Python CORS server, using pyobjc to screenshot specific browser windows, and injecting JavaScript into templates to debug a two-line CSS bug. LangChain's same-week post lists five sandbox criteria and flags bare Kubernetes as missing kernel-level isolation.

**Mechanism:** Frontier coding agents now take initiative to spawn subprocesses, bind network ports, and drive UI automation without operator approval. The blast radius for a prompt injection is whatever the host shell can reach.

**Why it matters:** Simon called this his top candidate for the next major security incident. Monday morning: audit which of your agent tools spawn subprocesses or bind ports, and move the harness onto something with kernel-level isolation (LangSmith Sandboxes, E2B, Vercel Sandbox, Modal).

**Reusable pattern:** Restrict outbound network, contain subprocess spawning, and gate browser-automation tools by default; grant each capability explicitly.

**Action surface:** tool-policy

**Try:** Pick one coding-agent workflow you run weekly. Wrap it in a sandbox that blocks egress except an allowlist, denies subprocess spawning except a named binary list, and logs every tool call. Replay last week's transcripts against the new policy and count the breakages.

**Systems map:** The system under review is no longer (model, prompt) — it is (model, prompt, tools, sandbox boundary, network policy). A proactive agent in a permissive sandbox is a system vulnerability, not a model feature.

**Transferable principle:** Capabilities the agent can invoke but the operator did not ask for must default to denied. The same shape applies to RPA bots, build agents, and any LLM with shell access.

**Falsification test:** Probe one denied read, outbound request, and browser action under the actual runner identity, then replay permitted work. If a denied effect succeeds, fix enforcement. If ordinary work breaks, narrow the grant. Public silence about incidents cannot price this control.

**Adoption ladder:**

  - Minimum viable: a network egress allowlist + a subprocess-spawning denylist on one coding-agent workflow.
  - Mid: per-capability opt-in flags wired to a session-level audit log; replay tool of last 7 days of agent calls.
  - Full: kernel-level isolation (Modal / E2B / Vercel Sandbox) for every agent that touches code, with a documented escape-hatch process.
  - Monitoring: count of denied tool invocations per session, count of explicit human approvals per session, time-to-revoke for a discovered vulnerability.

**Confidence:** high

**Evidence:** MTRX-W24-EARLY-02

---

### 3. Codex plans a hosted agent runtime through Ona

**Source:** [OpenAI, "OpenAI to acquire Ona"](https://openai.com/index/openai-to-acquire-ona/)

**Payload:** OpenAI agreed to acquire Ona (formerly Gitpod) to give Codex agents cloud execution and state that persists for hours or days across sessions. OpenAI cited Codex at over 5M weekly users with roughly 400% growth and Ona's 2M-developer cloud environments.

**Mechanism:** The June 11 announcement proposes bringing Ona's customer-controlled execution into Codex. The deal still needs closing and regulatory approvals; OpenAI and Ona remain independent until then.

**Why it matters:** If you built sandbox plumbing in the last twelve months, put it on a review list. Benchmark the shipped integration before deciding which glue to retire. An acquisition announcement does not migrate a session.

**Reusable pattern:** Persistent agent state and execution sandbox are converging into the model provider; bespoke sandbox glue is depreciating.

**Action surface:** runtime-adapter

**Try:** Inventory your current sandbox: isolation, session length, persistence, data location, export, and cost. Name one workload for a future comparison when the integration is available.

**Systems map:** The agent-runtime stack is consolidating into three layers — model provider, execution sandbox, framework adapter — and the middle layer is moving inside the first. Independent sandbox providers compete on isolation, pricing, and tool surface; the framework adapters must stay portable across them.

**Transferable principle:** When a provider integrates downstream into the execution layer, third-party tooling at that layer either gets absorbed, gets squeezed on price, or differentiates on policy (data residency, audit, customer-owned VPC). Same shape played out in CDN-edge-functions and BaaS.

**Falsification test:** Compare the shipped integration with the current provider on that workload. If isolation, recovery, data policy, or total cost fails your requirements, keep the independent sandbox. A market-share cutoff would not settle local fit.

**Adoption ladder:**

  - Minimum viable: a one-page sandbox-stack inventory + a sunset-review entry on the Q4 plan.
  - Mid: a portable runtime adapter abstraction so swapping E2B / Modal / Codex-hosted is a config change, not a rewrite.
  - Full: per-workload adapter selection driven by policy (data residency, cost, isolation level) with telemetry on session-state migration success.
  - Monitoring: which workloads stayed on third-party sandboxes 12 months after Codex close, and why.

**Confidence:** high

**Evidence:** MTRX-W24-EARLY-03

---

### 4. Eval workbenches grew up — olmo-eval, OpenEnv, and an unlearning audit that catches failures

**Source:** [AI2, "olmo-eval"](https://huggingface.co/blog/allenai/olmo-eval), [Hugging Face, "OpenEnv: a community standard for agentic RL"](https://huggingface.co/blog/openenv), and [Google Research, "Auditing unlearning with divergence kernels"](https://research.google/blog/new-framework-for-auditing-machine-unlearning/)

**Payload:** AI2 released olmo-eval, separating task definitions from runtime harnesses with sandboxed execution, native multi-turn tool-use evals, and minimum detectable effect reporting. OpenEnv shipped a standardized Gymnasium-style agentic RL protocol over HTTP and MCP, backed by Meta-PyTorch, Nvidia, Hugging Face, vLLM, and Microsoft. Google Research published a divergence-kernel test that audits unlearning with thousands of samples; finetune-to-forget and pruning both failed the audit.

**Mechanism:** These projects separate environment, task, runner, and statistical audit. Minimum detectable effect describes the size of a change a study can detect; it is not evidence that a measured gain clears the uncertainty bound.

**Why it matters:** Try one benchmark on olmo-eval before replacing the harness. For an unlearning claim, specify the reference distributions, sample budget, tolerated effect, and audit power. A non-rejection is not proof of deletion or legal compliance.

**Reusable pattern:** Eval infrastructure separates task definition from runtime harness and reports statistical significance instead of single-number leaderboard deltas.

**Action surface:** eval

**Try:** Take one production agent. Wrap one of its tool-use workflows as an OpenEnv environment. Run olmo-eval against two model checkpoints, report per-question diffs plus minimum detectable effect. Compare against your current eval output.

**Systems map:** Environment -> task -> runner -> score and uncertainty. The unlearning audit tests a defined distributional claim; compliance still needs the relevant data scope and legal review.

**Transferable principle:** When evaluation infrastructure separates protocol from execution and reports statistical significance, the shift from "score it" to "audit it" becomes possible. Same shape played out in database TPC benchmarks vs production OLTP audits.

**Falsification test:** On a fixed task set and compute budget, compare defect detection, uncertainty reporting, and engineering cost with the existing harness. Keep the existing harness if the workbench adds no useful coverage.

**Adoption ladder:**

  - Minimum viable: report uncertainty and the detectable effect for one eval.
  - Mid: wrap one tool workflow and check the adapter before using it in CI.
  - Full: claim-specific audits with stated reference data, power, and limits.
  - Monitoring: reproduced failures, uncertainty, runtime, and audit coverage.

**Confidence:** high

**Evidence:** MTRX-W24-EARLY-04

---

### 5. Disclosure and determinism — cheap fixes for two reliability holes

**Source:** [UK AI Security Institute, "RealityTest: do AI systems disclose their identity when asked?"](https://www.aisi.gov.uk/research/realitytest-how-people-probe-ai-identity-and-whether-models-disclose-it) and [Anthropic Research, "Paving the way for agents in biology"](https://www.anthropic.com/research/agents-in-biology)

**Payload:** AISI's RealityTest contains 3,152 identity-probing queries from roughly 750 participants across five languages. It tests 17 text and six speech models; a suppression instruction pushed disclosure below 30% even for the best performers. Anthropic's separate 120-query VirBench tests viral-sequence retrieval, not general tool correctness. Adding gget virus raised reported accuracy above 90% for all tested agents, reaching 99.7% for GPT-5.5.

**Mechanism:** Two failure modes with the same fix shape. Prompt-level promises (disclosure, retrieval correctness) collapse under variance; replace them with a deterministic layer between the model and the surface — a disclosure check at the response boundary, a deterministic adapter between the model and the messy API.

**Why it matters:** Test identity disclosure with varied phrasing and languages. For filtered retrieval, check repeated results against known counts. The benchmark results motivate those tests; they do not certify a product's compliance.

**Reusable pattern:** Move guarantees out of the prompt and into a deterministic wrapper at the boundary where the guarantee has to hold.

**Action surface:** eval

**Try:** Pick your most safety-relevant prompt-level guarantee (disclosure, refusal, citation). Write 50 phrasing variants in at least two languages, run them daily, alert on regression. Separately, pick one tool your agent calls with pagination or filters and wrap it in a deterministic adapter.

**Systems map:** The reliability boundary moves from "the model learned this rule" to "the wrapper enforces this rule." Prompts handle judgment; wrappers handle invariants. The two artifacts are now distinct, versioned, and auditable.

**Transferable principle:** Put a precisely codable invariant in code. Citation presence and argument validity fit that rule; citation faithfulness and complete retrieval still need an adequate reference and semantic checks.

**Falsification test:** Compare prompt-only behavior and the wrapper on a held-out adversarial set, including false blocks. Keep controls according to the consequence of a miss; 95% average disclosure alone does not establish acceptable risk.

**Adoption ladder:**

  - Minimum viable: 50 multilingual phrasing variants of one identity probe, run daily on the deployed agent.
  - Mid: deterministic adapters for the three most-called external tools; variance budget per tool.
  - Full: a boundary-enforcement layer with versioned invariants, alerting, and rollback per invariant.
  - Monitoring: % of identity probes that surface disclosure failure, % of retrieval calls within variance budget, time-to-rollback after an invariant regression.

**Confidence:** high

**Evidence:** MTRX-W24-EARLY-05

---

### 6. Tool gating gets a reference design — approval before mutation, mid-execution clarification, pre-push review

**Source:** [Simon Willison, "datasette-agent 0.2a0"](https://simonwillison.net/2026/Jun/10/datasette-agent/) and [Cursor changelog, Bugbot + /review](https://cursor.com/changelog/bugbot-updates-june-2026)

**Payload:** datasette-agent 0.2a0 added user approval for database modifications and lets tools ask questions mid-execution with persistent conversation state. Cursor reports Bugbot averages about 90 seconds (down from 5 minutes), finds 10 percent more bugs per review, and costs 22 percent less per run, with a `/review` command that runs Bugbot and Security Review pre-push.

**Mechanism:** Two reference implementations of human-in-the-loop tool policy: approval-before-mutation with state persistence (datasette) and pre-push automated review as a tool-policy primitive (Cursor). Both are concrete UX patterns builders can crib instead of reinventing.

**Why it matters:** If your agent touches user data without an approval step, copy datasette-agent's UX. If your PR pipeline doesn't run a bug-and-security pass before a human reviews, wire one in after measuring its runtime, cost, and catch rate on your own PRs.

**Reusable pattern:** Gate mutations with explicit approval and let tools pause for clarification with persistent state before they continue.

**Action surface:** tool-policy

**Try:** Add an approval-required flag to one mutation tool in your agent. Persist the conversation state across the approval roundtrip. Measure how often users approve, edit, or reject, and what the rejected calls would have done.

**Systems map:** Tool policy is becoming a two-layer artifact: per-tool approval rules (datasette pattern) plus pre-action automated review (Cursor pattern). Both layers carry state across human interruptions, which is the part most home-grown attempts miss.

**Transferable principle:** Approval-with-state is a different primitive from approval-without-state. Any agent that survives a user closing the tab needs persistence on the pending-approval side, not just the answered-question side.

**Falsification test:** Review a sample of approvals as well as rejects, grouped by action risk. If approval adds no detected error or informed choice, simplify low-risk reversible actions. A 95% approval rate alone cannot justify removing a control on irreversible writes.

**Adoption ladder:**

  - Minimum viable: an approval-required flag on one mutation tool, with a yes/no prompt.
  - Mid: persistent state across the approval roundtrip + a reject-with-reason path the agent can read.
  - Full: pre-action automated review (Bugbot-style) wired before human approval surfaces; approval payload shows the review verdict.
  - Monitoring: approve/edit/reject ratio per tool, mean time-to-approval, % of rejected calls whose alternative the user explicitly requested.

**Confidence:** high

**Evidence:** MTRX-W24-EARLY-06

---

### 7. Specialists over generalists — the sample-efficiency wall and where it doesn't apply

**Source:** [Dwarkesh Patel, "The sample-efficiency black hole"](https://www.dwarkesh.com/p/the-sample-efficiency-black-hole) and [LangChain, "Headless tools and the client-side execution rail"](https://www.langchain.com/blog/agents-and-applications)

**Payload:** Patel argues that frontier training is sample-inefficient relative to human learning and that narrow workflows offer a better near-term target. Treat that as a practitioner thesis, not a measured law for every office task. LangChain's headless-tools post describes typed client-side capabilities where application state already lives.

**Mechanism:** The roadmap stops being "wait for a smarter base model" and becomes "narrow the task, source expert data, run RL plus SFT, ship the specialist." Tool design follows: typed tools execute on the client where the state is, returning structured results to the agent.

**Why it matters:** If your bet depends on a general-purpose agent improving by raw scale, hedge it. Pick one narrow task you can collect expert traces for and put together an RL plus SFT loop. For browser or desktop products, treat the DOM and IndexedDB as the source of truth and define client-side tools accordingly.

**Reusable pattern:** Orchestrate narrow specialists with expert data and client-side typed tools instead of waiting for a generalist base model to close the gap.

**Action surface:** architecture

**Try:** For one repetitive task, collect a proposed pilot of 200 expert traces, keeping a separate unseen test set. Compare a small-model fine-tune, the base model, and a prompt/tool-only baseline on accepted output and total cost before adding RL.

**Systems map:** The agent stack splits into orchestrator (general), specialists (narrow, RL+SFT), and tools (typed, often client-side). The orchestrator's job is routing + state, not domain expertise. The specialists carry the domain.

**Transferable principle:** A specialist is worth testing when the task repeats and expert data is available. It has to beat a strong generalist or tool-only baseline after counting collection, training, serving, and maintenance.

**Falsification test:** At a fixed cost and quality requirement, compare the specialist with each base-model upgrade on unseen cases. If the base or prompt/tool baseline wins, keep it. Do not infer all robotics or office work from one task.

**Adoption ladder:**

  - Minimum viable: 200 expert traces logged on one repetitive task; one SFT run on a small open model.
  - Mid: RL loop on the same task; A/B against base model on olmo-eval; ship to one user cohort.
  - Full: specialist + orchestrator stack with client-side typed tools; cost-per-task tracked vs base-model spend.
  - Monitoring: accuracy gap (specialist vs base) per task per quarter, expert-trace collection rate, RL-loop iteration time.

**Confidence:** high

**Evidence:** MTRX-W24-EARLY-07

---

## Watchlist

- **OpenAI S-1 + Economic Research Exchange.** OpenAI hinted at an S-1 filing window and announced an Economic Research Exchange this week. Revisit if the S-1 lands with disaggregated agent-runtime revenue, or if the Exchange publishes a methodology paper. (https://openai.com/index/economic-research-exchange/)
- **Anthropic Public Record survey results.** Anthropic shipped the Public Record survey on June 10; results haven't dropped. Revisit when the first results paper appears. (https://www.anthropic.com/news/public-record)
- **Claude Corps fellowship.** Anthropic announced the Claude Corps fellowship June 11. Revisit if the first cohort's output is publicly visible. (https://www.anthropic.com/news/claude-corps)
- **DiffusionGemma 4x throughput on consumer GPUs.** DeepMind shipped DiffusionGemma with 4x faster generation on a 5090; revisit if the architecture moves into open-weights frontier chat models. (https://deepmind.google/discover/blog/diffusiongemma-2026/)
- **Google–SpaceX compute.** Google reportedly contracted SpaceX-launched orbital compute. Revisit if a real customer-facing latency or jurisdiction story lands. (https://blog.google/technology/ai/spacex-compute-2026/)
- **Gemini 3.5 Live Translate + SynthID watermark.** Gemini 3.5 added Live Translate with SynthID-watermarked output. Revisit if a watermark-removal study, regulatory adoption, or first-party detection tool ships.

---

## Sources reviewed

This brief swept 32 candidate items across eight source families. The seven Top signals draw on 11 primary sources; the watchlist names six more. Two source families (governance/safety institutions, market+strategy commentary) carried lower yield than the AI-vendor blogs but anchored the disclosure/sandbox/specialist signals.

## Postscript — what this brief is not

Not a deprecation alert. Anthropic did not deprecate Fable 5; an export-control directive disabled it. Other Claude models stayed up. The new fact: a model's availability is a property of policy plus capacity plus safety review, not just provider uptime. Builders treat it accordingly.

Not a vote against frameworks. OpenAI Agents SDK, LangGraph, and the rest are useful adapters. The brief's argument is about the contract above the framework: sandbox isolation, eval workbench, disclosure boundary, tool-approval state. That contract is where most of the work this quarter sits.
