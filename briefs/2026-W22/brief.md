<!--
meta:
  iso_week: 2026-W22
  through_date: 2026-05-29
  profile_id: broad_builder
  matrix_run_id: MTRX-W22-massive-rerun
  sources_swept_count: 144
  cells_verified_count: 1994
  volume: 4
-->

# The week the operating boundary became the product

**week of 2026-05-25 · audience: builder-tpms thinking about AI · vol. 004**

## Field thesis

After 144 sources and 1,994 verified cells, the week sorts into one
shape: the binding work has migrated out of the model and into the
operating boundary around the model. The Series H tells one half of
the story — a $965B private valuation against a $47B run-rate funded
almost entirely by enterprise coding-agent token burn. The other half
arrived as project-level contracts: curl's pressure post on >1 AI-
assisted report per day, SQLite's AGENTS.md rejecting agentic code
patches, Anthropic's Glasswing reporting >10,000 high/critical
findings against vetted partners with the patch pipeline now the
bottleneck, Cursor's three-tier Auto-review policy ladder, Vercel's
team-wide provider allowlist with BYOK enforcement, and Microsoft's
Copilot Cowork exfiltration via agent-composed external images. Each
of these is the same artifact: a policy file, a budget cap, a
tiered ladder, an intake rubric, an outbound-communication guard. The
model is no longer the load-bearing variable. The contract around the
model — who can call which tool, who reviews which patch, who pays
for which token, what gets logged — is the variable everyone shipped
this week.

If you have time for one move from this brief, write the policy
ladder for one agent surface and ship it: name the allowlisted tier,
the sandboxed tier, the classifier-routed tier, and the human-prompt
tier. Then put the cost cap on top. Cursor productized this exact
shape in 2.1.154's `/effort xhigh` knob and Auto-review; Vercel
shipped the gateway-side counterpart for BYOK traffic; Anthropic's
dynamic workflows make the budget cap an existential parameter, not
a footnote. The picks below each sit on top of the policy-ladder
move.

---

## Top signals

### 1. Glasswing + curl + SQLite + Armin Ronacher — the disclosure pipeline is the new bottleneck

**Source:** [Anthropic Glasswing initial update](https://www.anthropic.com/research/glasswing-initial-update) · [Simon Willison on curl pressure](https://simonwillison.net/2026/May/26/the-pressure/) · [SQLite AGENTS.md](https://simonwillison.net/2026/May/27/sqlite-agents/) · [Simon Willison on Armin Ronacher](https://simonwillison.net/2026/May/24/armin-ronacher/)

**Payload:** Anthropic's Project Glasswing report disclosed >10,000
high/critical vulnerabilities across ~50 partners running Claude
Mythos Preview against critical infrastructure — including 2,000
bugs at Cloudflare and 271 Firefox vulnerabilities at Mozilla
(roughly 10x prior testing). In the same week Daniel Stenberg
reported curl is now receiving more than one AI-assisted security
report per day on average (4-5x the 2024 rate, 2x 2025). SQLite
published an AGENTS.md that rejects agentic code patches and accepts
agentic bug reports only with reproducible test cases. Armin
Ronacher, quoted by Willison, named the failure mode at the input
side: AI-reworded GitHub issues lose the reporter's own observational
detail and become "inaccurate but full of confidence."

**Mechanism:** Agent-assisted vulnerability discovery and report
drafting have lowered the unit cost of producing a security report
by roughly an order of magnitude on each axis (Glasswing on the
finding side, the curl deluge on the submission side). Patch
pipelines, CVE coordination, and maintainer attention have not
scaled. Glasswing's own language — that the bottleneck "has moved
to verify/disclose/patch" — names the shape; SQLite's policy and
Ronacher's complaint about reworded issues describe the contract
shifts maintainers are writing in response.

**Why it matters:** Four signals converged on the same project-level
artifact in seven days. Maintainers and security teams are no longer
debating whether to accept AI-assisted work; they are publishing
policy files at the conventional path that name what they accept and
what they auto-close. The contract bar is verifiability — a
reproducible test case, a literal observation, a proof-of-concept.
Anything that fails that bar belongs in the separate triage queue
with its own SLA.

**Reusable pattern:** Two patterns transfer. First, AGENTS.md as a
first-class repository artifact at the same altitude as
CONTRIBUTING.md and CODE_OF_CONDUCT.md — name what the project
accepts from agent-assisted contributions and key acceptance to
verifiable artifacts. Second, the intake-rubric pattern itself —
require raw observations over narrative summaries, require a
reproducer over an analysis, require a PoC over a "potential
vulnerability" framing. The same shape works for an open-source
project, an internal security bug-bounty intake, a customer support
queue, or an enterprise IT ticket triage.

**Action surface:** workflow, tool-policy, agent-role

**Try:** Publish an AGENTS.md or an `ai-assisted-report-policy.md`
in the repo or runbook that names (a) what evidence the project
accepts from agent-assisted submissions, (b) what gets auto-closed,
and (c) which queue agent-submitted work lands in with which SLA.
Two weeks: write it, link it from the contributor docs, point new
agent-authored submissions at it.

**Confidence:** high

<!-- Evidence: MTRX-W22-anthropic-glasswing-source_gist, MTRX-W22-anthropic-glasswing-mechanism_extraction, MTRX-W22-anthropic-glasswing-adoption_action, MTRX-W22-anthropic-glasswing-governance_surface, MTRX-W22-curl-pressure-source_gist, MTRX-W22-curl-pressure-mechanism_extraction, MTRX-W22-curl-pressure-reusable_pattern, MTRX-W22-curl-pressure-adoption_action, MTRX-W22-sqlite-agents-md-source_gist, MTRX-W22-sqlite-agents-md-reusable_pattern, MTRX-W22-sqlite-agents-md-governance_surface, MTRX-W22-armin-ai-issues-source_gist, MTRX-W22-armin-ai-issues-adoption_action, MTRX-W22-armin-ai-issues-governance_surface -->

---

### 2. Anthropic Series H + $47B run-rate + the PMF post — the AI-tooling line item is a consumption line

**Source:** [Anthropic Series H announcement](https://www.anthropic.com/news/series-h) · [Simon Willison on the $47B run-rate](https://simonwillison.net/2026/May/29/anthropic/) · [Simon Willison on coding-agent PMF](https://simonwillison.net/2026/May/27/product-market-fit/)

**Payload:** Anthropic announced a $65B Series H at a $965B
post-money valuation on May 28, and run-rate revenue grew from ~$9B
at end of 2025 to ~$47B by May 2026 — roughly 5x in five months.
Simon Willison's PMF post argues both Anthropic and OpenAI have
found product-market fit through enterprise coding agents that
"burn vastly more tokens but are becoming daily drivers for
well-compensated professionals," with the pricing moves and observed
spend patterns as the evidence.

**Mechanism:** Run-rate annualizes a single month, so the 5x is the
trajectory not the audited revenue. The mechanism underneath is
coding-agent token consumption replacing flat per-seat pricing.
Willison's own 30-day coding-agent spend ($2,180 against a $200
subscription assumption) is the n=1 confirmation; the per-developer
burn rate is now the load-bearing variable for any AI-tooling
budget set in 2025. Run-rate as a metric is, in Willison's framing,
a "habit" of Anthropic's announcements — marketing-shaped and
amplifying recent months.

**Why it matters:** Any 2026 AI-tooling budget built on per-seat
subscription assumptions is the wrong category. The Series H and
$47B trajectory land as a finance fact for every team running
coding agents inside a 2025 seat budget, regardless of how anyone
reads the vendor-side narrative. Combined with Cisco scaling Codex
across engineering,
Endava compressing requirements analysis from weeks to hours,
Ramp's cycle-time reduction from hours to minutes, and Virgin
Atlantic shipping a fixed-deadline mobile app with near-total unit
test coverage, the procurement pattern is consistent: coding agents
are daily drivers for well-paid developers, and the token spend per
developer reflects that.

**Reusable pattern:** PMF detection via pricing moves and observed
spend, not NPS or self-reported satisfaction — when a customer's
per-seat token spend stabilizes high, that's the durable-demand
signal. Useful for any team selling tokens or buying them.

**Action surface:** config, workflow

**Try:** Pull the AI-tooling line item from your 2026 budget. If it
sits under SaaS subscriptions, move it to consumption with a monthly
burn cap per developer and a 70%-of-cap Slack alert. Sample shape
worth filling in:

```
team / agent surface          2025 annual seat budget    2026 monthly burn cap    alert
backend / Claude Code         $200 * seats * 12          $600 / dev / month       Slack 70%
frontend / Codex              $200 * seats * 12          $400 / dev / month       Slack 70%
security / agentic monitor    $0 (informal)              $1200 / month            Slack 70%
support / agent drafts        $0 (informal)              $200 / month             Slack 70%
research / batch analysis     $0 (informal)              $300 / month             Slack 70%
```

The cap is the contract. The 70% alert catches the surprise the
month a coding agent acquires a new sub-agent dispatch flag (see
pick 4 on dynamic workflows).

**Confidence:** high

<!-- Evidence: MTRX-W22-anthropic-series-h-source_gist, MTRX-W22-anthropic-series-h-mechanism_extraction, MTRX-W22-anthropic-series-h-risk_and_caveats, MTRX-W22-anthropic-47b-runrate-source_gist, MTRX-W22-anthropic-47b-runrate-mechanism_extraction, MTRX-W22-anthropic-47b-runrate-reusable_pattern, MTRX-W22-anthropic-openai-pmf-source_gist, MTRX-W22-anthropic-openai-pmf-claims_and_bets, MTRX-W22-anthropic-openai-pmf-reusable_pattern, MTRX-W22-anthropic-openai-pmf-adoption_action, MTRX-W22-openai-cisco-source_gist, MTRX-W22-openai-endava-source_gist, MTRX-W22-openai-ramp-source_gist, MTRX-W22-openai-virgin-atlantic-source_gist -->

---

### 3. Microsoft Copilot Cowork exfiltration + SLEIGHT-Bench — outbound-policy + monitor catch-rate as a paired procurement question

**Source:** [Simon Willison on Copilot Cowork exfiltration](https://simonwillison.net/2026/May/26/copilot-cowork-exfiltrates-files/) · [Anthropic Alignment, SLEIGHT-Bench](https://alignment.anthropic.com/2026/sleight-bench/)

**Payload:** Microsoft Copilot Cowork agents could send messages
containing attacker-supplied external images; opening the message
triggered a network request whose URL carried exfiltrated data.
Anthropic's Alignment Science team published SLEIGHT-Bench, a
benchmark of evasive transcripts designed to surface blind spots
in frontier monitor systems before deployment. The two land on the
same page because they are the offense and defense of the same chain:
agent composes outbound content → outbound content carries
attacker-influenced payload → no monitor catches the chain.

**Mechanism:** Image-load exfiltration is a textbook side channel:
external content reaches the agent; agent drafts outbound
communication; communication carries an attacker-controlled URL;
recipient client renders the URL on open; the request leaks the
payload. SLEIGHT-Bench is the dual — an adversarial dataset that
scores whether monitor systems detect the evasive transcripts that
exploit this kind of chain. Neither artifact is novel as a class;
what is new is the production shipment of the offense (in a major
vendor product) and the publication of a regulator-credible defense
benchmark in the same week.

**Why it matters:** "We use an LLM-based monitor" without a
benchmark number is now an insufficient answer for any agent
deployment that drafts outbound communications. SLEIGHT-Bench gives
the buyer a concrete artifact to ask for; the Copilot Cowork
finding gives the buyer the concrete failure mode to test against.
Both translate directly into a procurement question and an
internal red-team checklist.

**Reusable pattern:** Treat any agent surface that drafts outbound
content as an exfiltration channel by default. Strip or proxy
external image references before send; require explicit human
approval before an agent-composed message ships; allowlist
recipient domains where possible. The monitor side: when a vendor
claims supervisory coverage, ask for a SLEIGHT-Bench or
SLEIGHT-Bench-equivalent number on the specific evasion classes
relevant to the workload (multi-session stitching, omission,
authorization confusion, jailbreak-in-transcript).

**Action surface:** tool-policy, eval, agent-role

**Try:** Ship a one-row `outbound-communication.yaml` tool-policy
this week that names every outbound surface (email, Slack DM,
calendar invite, ticket comment) and the controls on each. The
minimum is two lines per surface: strip-or-proxy external images
on send, and require human approval before send.

```yaml
agent_outbound_communications:
  email:
    external_images:        strip-or-proxy-through-sanitizer
    human_approval_required: yes
    audit_log:              every-draft-and-send
    allowed_recipients:     allowlist | broadcast-blocked
  slack_dm:
    external_links:         expand-and-display-target
    human_approval_required: yes-for-customer-channels
  calendar_invite:
    external_attachments:   block
    human_approval_required: yes
  ticket_comment:
    external_images:        strip
    human_approval_required: no-but-edit-window-required
```

Then add a SLEIGHT-Bench probe to your monitor eval set this
quarter. Pick the three evasion classes most relevant to your
workload; report the catch rate at a 1% false-positive rate.

**Confidence:** high

<!-- Evidence: MTRX-W22-copilot-cowork-exfil-source_gist, MTRX-W22-copilot-cowork-exfil-mechanism_extraction, MTRX-W22-copilot-cowork-exfil-reusable_pattern, MTRX-W22-copilot-cowork-exfil-adoption_action, MTRX-W22-copilot-cowork-exfil-governance_surface, MTRX-W22-anthropic-sleight-bench-source_gist, MTRX-W22-anthropic-sleight-bench-reusable_pattern, MTRX-W22-anthropic-sleight-bench-adoption_action, MTRX-W22-anthropic-sleight-bench-governance_surface -->

---

### 4. Claude Code v2.1.154 dynamic workflows + Cursor Auto-review + Vercel provider allowlist — the policy-ladder is the new agent platform

**Source:** [Claude Code v2.1.154 release](https://github.com/anthropics/claude-code/releases/tag/v2.1.154) · [Claude Code v2.1.156 hotfix](https://github.com/anthropics/claude-code/releases/tag/v2.1.156) · [Cursor Auto-review](https://cursor.com/changelog/auto-review) · [Vercel team-wide provider allowlist](https://vercel.com/changelog/team-wide-provider-allowlist-on-ai-gateway)

**Payload:** Three platforms shipped the same shape in the same
week. Claude Code v2.1.154 set Opus 4.8 as default, exposed an
`/effort xhigh` knob for the hardest tasks, made the lean system
prompt default for new models, and introduced "dynamic workflows"
that orchestrate tens to hundreds of background agents via
`/workflows`. Two days later v2.1.156 hotfixed an Opus 4.8
thinking-block regression. Cursor's Auto-review introduced a
three-tier action policy: allowlist immediate, sandboxable
isolated, classifier-routed for the ambiguous middle (permit /
alternative / human prompt). Vercel added a team-wide AI Gateway
provider allowlist enforced on BYOK traffic with owner-only
mutation.

**Mechanism:** All three are policy ladders. Cursor names the
tiers explicitly (allowlist / sandbox / classifier / prompt human);
Claude Code expresses the same shape across `/effort`, `/workflows`,
and lean-prompt defaults; Vercel expresses the gateway-side
counterpart (which vendors are even reachable, including for BYOK).
The classifier subagent in Cursor is the load-bearing piece — it
sits between the allowlist and the human prompt, and turns the
binary allow/prompt question into a graded one. The same week, the
Cloudflare AI code-review post-mortem and Hugging Face's agent
glossary added the vocabulary (harness, scaffold) to talk about
these tiers without each team inventing its own.

**Why it matters:** "Add another model and a chat box" is no longer
the agent platform. The platform is the policy ladder plus the cost
cap plus the audit log plus the credential scope. Dynamic workflows
multiply both the value and the blast radius — a single user prompt
can now spawn tens of background agents, each consuming tokens and
calling tools. Without per-workflow caps, the budget overrun is the
default outcome. Without per-tier audit logging, the post-incident
investigation has no surface to land on.

**Reusable pattern:** Express agent action authority as a policy
ladder, not a binary allow/prompt switch. Four tiers: allowlist
immediate; sandboxed isolated with rollback; classifier-routed with
a soft middle (permit / alternative / human prompt); explicit human
prompt for everything else. Audit-log which tier handled each
action. Cap by-workflow cost. Pin vendor allowlists at the gateway,
not in each application.

**Action surface:** agent-role, tool-policy, config, software-control-plane

**Try:** Before turning on dynamic workflows or any equivalent
fan-out feature in a shared install, ship four guardrails. The
first two are the budget perimeter; the second two are the audit
surface.

```yaml
# dynamic-workflows guardrails — agent harness of your choice
per_workflow_budget_cap_usd: 50
per_workflow_max_subagents: 10
allowed_subagent_skills:
  - code-review
  - test-runner
  - doc-extractor
  # deny by default; add per business need
audit_log_retention_days: 90
require_human_review_when:
  - workflow_writes_to_branch: main
  - workflow_calls_tool: prod_database_write
  - workflow_cost_exceeds_usd: 25
```

Pin Claude Code at v2.1.156 or later before standardizing — the
v2.1.154 thinking-block regression was real, the cadence (eight
versions in eight days) is itself the carrier signal that the
surface is moving faster than the documentation.

**Confidence:** high

<!-- Evidence: MTRX-W22-claude-code-2-1-154-source_gist, MTRX-W22-claude-code-2-1-154-mechanism_extraction, MTRX-W22-claude-code-2-1-154-adoption_action, MTRX-W22-claude-code-2-1-154-risk_and_caveats, MTRX-W22-claude-code-2-1-154-governance_surface, MTRX-W22-claude-code-2-1-156-source_gist, MTRX-W22-claude-code-2-1-156-adoption_action, MTRX-W22-cursor-auto-review-source_gist, MTRX-W22-cursor-auto-review-mechanism_extraction, MTRX-W22-cursor-auto-review-reusable_pattern, MTRX-W22-cursor-auto-review-governance_surface, MTRX-W22-vercel-provider-allowlist-source_gist, MTRX-W22-vercel-provider-allowlist-mechanism_extraction, MTRX-W22-vercel-provider-allowlist-adoption_action, MTRX-W22-vercel-provider-allowlist-governance_surface -->

---

### 5. Conductor on Vercel Sandbox + Mistral Vibe remote agents + Cursor shared canvases — coding agents moved off the laptop this month

**Source:** [Vercel on Conductor](https://vercel.com/blog/how-conductor-moved-parallel-coding-agents-from-the-laptop-to-the-cloud-with-vercel-sandbox) · [Mistral Medium 3.5 + Vibe remote agents](https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5) · [Cursor shared canvases](https://cursor.com/changelog/shared-canvases) · [Vercel Sandbox persistence GA](https://vercel.com/changelog/sandbox-persistence-is-now-ga)

**Payload:** Conductor described moving its parallel-coding-agent
execution layer off developer laptops onto Vercel Sandboxes,
model-agnostic across Claude Code, Codex, and others, with a UX
the operator says "feels just like the local version." Mistral
shipped Medium 3.5 paired with cloud-side coding agents in Vibe and
a new Work mode in Le Chat — the same architectural shape from a
different vendor. Vercel made Sandbox filesystem persistence GA and
on-by-default. Cursor added shared canvases and a `/loop` skill
that runs prompts on a local schedule until an outcome or user
stop.

**Mechanism:** The cold-start latency on hosted execution
environments has dropped enough to make remote parallel agents feel
local, which removes the laptop as the bottleneck for fan-out
work. Conductor is model-agnostic across multiple agent SDKs;
Mistral's pairing of Medium 3.5 with cloud-side agents is the
EU-domiciled counterpart; Vercel's persistence flip turns the
sandbox into a long-lived data store by default and ends its life
as an ephemeral runtime. Cursor's `/loop` is the same idea on the local
side — a recurring agent prompt as a first-class primitive
replacing cron + ad-hoc scripts.

**Why it matters:** The default place to run a coding agent in
H2 2026 is not your laptop. The platform decision is now: which
sandbox provider, with which persistence semantics, behind which
gateway allowlist, with which audit log. Model-agnosticism is the
hedge — Conductor's choice to interface across multiple agent
SDKs is the architecture worth copying for any team that wants to
remain hedged across vendors as the model frontier moves week-to-
week. Persistence on by default is the trap — PII and secrets now
linger across sessions unless you write a retention policy.

**Reusable pattern:** "Fast remote sandbox preserves local UX" as
a near-universal architectural shape for parallel coding agents.
Pair it with a model-agnostic orchestrator adapter so the agent
SDK is a config choice, not a structural lock-in. Make the
persistence layer's retention policy an explicit design decision,
not a vendor default. Treat the recurring-prompt primitive
(`/loop`, equivalents) as a budget surface, not just a workflow
surface.

**Action surface:** architecture, runtime-adapter, tool-policy

**Try:** If your team runs parallel coding agents on laptops,
spend a week prototyping one workflow on a hosted sandbox (Vercel
Sandbox, E2B, Daytona, Modal — bench cold-start times). Write the
data-retention policy first: which directories persist, for how
long, encrypted by what key, surfaced to which audit log. Decide
which projects opt out of persistence. Pin recurring-prompt
budgets at a per-user / per-team cap with the same 70% alert as
the consumption budget.

**Confidence:** medium-high

<!-- Evidence: MTRX-W22-vercel-conductor-source_gist, MTRX-W22-vercel-conductor-mechanism_extraction, MTRX-W22-vercel-conductor-reusable_pattern, MTRX-W22-vercel-conductor-governance_surface, MTRX-W22-conductor-cloud-agents-source_gist, MTRX-W22-conductor-cloud-agents-reusable_pattern, MTRX-W22-mistral-medium-3-5-source_gist, MTRX-W22-mistral-medium-3-5-mechanism_extraction, MTRX-W22-mistral-vibe-source_gist, MTRX-W22-cursor-shared-canvas-source_gist, MTRX-W22-cursor-shared-canvas-mechanism_extraction, MTRX-W22-cursor-shared-canvas-governance_surface, MTRX-W22-vercel-sandbox-persistence-source_gist, MTRX-W22-vercel-sandbox-persistence-adoption_action, MTRX-W22-vercel-sandbox-persistence-governance_surface -->

---

### 6. MagenticLite + Fara1.5 + "The model isn't the agent anymore" — orchestration beats model scale past the reasoning threshold

**Source:** [Microsoft Research, MagenticLite + Fara1.5](https://www.microsoft.com/en-us/research/blog/magenticlite-magenticbrain-fara1-5-an-agentic-experience-optimized-for-small-models/) · [AlphaSignal, "The model isn't the agent anymore"](https://alphasignalai.substack.com/p/the-model-isnt-the-agent-anymore) · [Hugging Face agent glossary](https://huggingface.co/blog/agent-glossary) · [DeepMind Co-Scientist](https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/)

**Payload:** Microsoft Research shipped MagenticLite — a stack
pairing a 14B-param MagenticBrain (planner / coder / delegator)
with Fara1.5 (web/browser SOTA among small computer-use models,
nearly doubling its predecessor on web-navigation tasks) — and
framed the release as evidence that agentic capability comes from
orchestration and not from scale. UC Berkeley's Shangding Gu, via
AlphaSignal, published a six-factor decomposition of long-horizon
agent performance arguing that once reasoning capability clears a
threshold, marginal gains shift to the other five factors (memory,
retrieval, planning, tooling, feedback). DeepMind's Co-Scientist
launched as a role-specialized multi-agent system with a human
strategy lead. Hugging Face published an agent glossary
disambiguating "harness," "scaffold," and adjacent terms.

**Mechanism:** Agent performance over a horizon H decomposes into
the model and five surrounding system factors. Past a reasoning
threshold, model scaling alone delivers diminishing returns;
system-scaling — better harness, memory architecture, retrieval,
planner, tool-policy, feedback loop — delivers the marginal lift.
MagenticLite is the product expression of the same thesis: split
the agent into MagenticLite (interface) + MagenticBrain (14B
planner / coder) + Fara1.5 (browser executor), each tuned for the
factor it owns. Co-Scientist is a research-domain expression: role-
specialized agents with a shared context store and a human
strategy lead.

**Why it matters:** This reframes the "which model" question into
"which six factors are bottlenecking your horizon-H workflow." For
buyers, it means a benchmark on the model alone is no longer
sufficient evidence of production fitness; the benchmark needs to
score the system. For builders, it means a 14B planner + a 1B
browser executor may beat a frontier-model-only stack on cost per
completed task. For the W22 brief specifically, this pick is the
theoretical underpinning of the picks above — the policy ladder
(pick 4), the consumption budget (pick 2), and the remote sandbox
(pick 5) are all system-level scaling moves, not model-level
moves.

**Reusable pattern:** When an agent underperforms on horizon-H
work, diagnose against the six factors before reaching for a
bigger model. Pair every model eval with a system eval that
measures the harness, memory, retrieval, planner, and feedback
loop independently. Mirror Co-Scientist's separation of strategy
(human) from execution (agents) in any multi-agent setup — define
explicit agent roles plus a shared context-store contract, not a
free-form agent pool.

**Action surface:** architecture, agent-role, eval

**Try:** Pick one multi-step agent workflow you run today. Run a
six-factor diagnostic: reasoning quality, memory hits and misses,
retrieval precision and recall, planner step-count and revision
rate, tool-policy false-permits and false-denies, feedback-loop
latency. The bottleneck factor is the one to invest in next.
Resist the default of swapping to a larger model.

**Confidence:** medium

<!-- Evidence: MTRX-W22-magenticlite-fara-source_gist, MTRX-W22-magenticlite-fara-mechanism_extraction, MTRX-W22-magenticlite-fara-adoption_action, MTRX-W22-msr-magentic-fara-source_gist, MTRX-W22-msr-magentic-fara-mechanism_extraction, MTRX-W22-model-not-agent-source_gist, MTRX-W22-model-not-agent-claims_and_bets, MTRX-W22-model-not-agent-reusable_pattern, MTRX-W22-model-not-agent-governance_surface, MTRX-W22-co-scientist-source_gist, MTRX-W22-co-scientist-reusable_pattern, MTRX-W22-co-scientist-adoption_action, MTRX-W22-hf-agent-glossary-source_gist, MTRX-W22-hf-agent-glossary-adoption_action -->

---

### 7. HBM memory shortage + Stratechery NVIDIA reporting + DC veto — the physical world is the binding constraint

**Source:** [Simon Willison on the memory shortage](https://simonwillison.net/2026/May/22/memory-shortage/) · [Stratechery on NVIDIA reporting](https://stratechery.com/2026/nvidia-earnings-the-ai-stack-nvidias-new-reporting/) · [Stratechery on the data-center veto](https://stratechery.com/2026/the-data-center-veto/) · [NVIDIA on AI factories](https://blogs.nvidia.com/blog/ai-factories-the-new-infrastructure-of-intelligence/)

**Payload:** HBM allocation is moving from roughly 2% of wafer
capacity at the start of 2026 to an expected 20% by year-end, with
each gigabyte of HBM consuming roughly 3x the wafer area of standard
DRAM. Consumer DRAM prices are rising as a downstream effect.
Stratechery covered NVIDIA's revised earnings reporting separating
hyperscaler GPU sales (under commoditization pressure) from
enterprise / other (where NVIDIA controls the stack). The week's
data-center-veto roundup landed the political-economy point:
municipal zoning, water, and power-permit processes are now a
binding constraint on AI infra siting, more active in 2026 than
the federal Executive Order discussion. NVIDIA's own "AI factories"
post reframed infra economics as tokens-per-watt.

**Mechanism:** Three physical-world variables are now load-bearing
on the AI roadmap. HBM wafer allocation is a fab-capacity
constraint that AI demand cannot relieve faster than 24 months.
Hyperscaler GPU revenue commoditization is the margin compression
that NVIDIA's reporting changes acknowledge. Municipal permitting
is the binding gate on data-center siting, and the federal AI
Executive Order's indefinite postponement (per Zvi's W22 read)
means state and local regimes are the dominant US AI-policy
surface for the foreseeable horizon.

**Why it matters:** Capex planning that assumes federal preemption
of state AI rules, or assumes HBM availability scales to demand,
or assumes hyperscaler GPU procurement remains the dominant
margin pool, is now planning against the wrong physical facts.
The infra economic frame this quarter shifts from "how many GPUs"
to "tokens-per-watt at which siting decision under which state
auditing regime." Hardware buyers should plan on 12-24 months of
elevated DRAM pricing.

**Reusable pattern:** When digital scaling hits a physical
constraint, the binding decisions move to the institution
controlling the physical resource — fab capacity, the municipality,
the substation. Add $/token and tokens/W to AI infra dashboards
alongside utilization; use those metrics for capex justification
in place of headline GPU counts. Track Illinois SB 315 and peer
state AI-audit bills as the active regulatory surface; the
postponed federal EO is no longer the right anchor for compliance
planning.

**Action surface:** architecture, watchlist, source-registry

**Try:** Add three rows to the AI infra dashboard: HBM allocation
share by quarter (track Samsung / SK Hynix / Micron capex notes),
$/token at current utilization, tokens/W on the dominant
deployment tier. If your buildout schedule has a 2026-H2 site
selection, run the local-permitting risk as a top-3 schedule risk
and consider pre-permitted brownfield sites as a fallback.

**Confidence:** medium

<!-- Evidence: MTRX-W22-memory-shortage-source_gist, MTRX-W22-memory-shortage-mechanism_extraction, MTRX-W22-memory-shortage-adoption_action, MTRX-W22-memory-shortage-governance_surface, MTRX-W22-stratechery-nvidia-source_gist, MTRX-W22-stratechery-nvidia-claims_and_bets, MTRX-W22-stratechery-nvidia-mechanism_extraction, MTRX-W22-stratechery-dc-veto-source_gist, MTRX-W22-stratechery-dc-veto-mechanism_extraction, MTRX-W22-stratechery-dc-veto-adoption_action, MTRX-W22-stratechery-dc-veto-governance_surface, MTRX-W22-ai-factories-source_gist, MTRX-W22-ai-factories-adoption_action, MTRX-W22-zvi-ai-170-source_gist, MTRX-W22-zvi-ai-170-mechanism_extraction, MTRX-W22-zvi-ai-170-governance_surface -->

---

## Reusable patterns

- **AGENTS.md as a first-class repository artifact.** Where it
  applies: any open-source project, any internal monorepo with
  external contributors, any vendor whose customers ship code with
  agent assistance. Caveats: enforcement is honor-system — projects
  cannot reliably detect agent-authored code; the policy works as a
  norm-setting artifact and a triage-routing rule, not as an
  airtight gate.
- **Policy ladder over binary allow/prompt.** Where it applies: any
  agent that calls tools (shell, fetch, MCP, DB write). Express
  authority as allowlist / sandbox / classifier-routed / human
  prompt, audit-log which tier handled each action, cap by-workflow
  cost. Caveats: the classifier subagent is its own training and
  monitoring obligation; false-permits at the classifier layer
  bypass the user.
- **System eval, not model eval.** Where it applies: any production
  agent deployment past a single-turn use case. Score the harness,
  memory, retrieval, planner, and tool-policy independently
  alongside the model. Caveats: there is no public system-eval
  benchmark yet; ITBench-AA is the closest analog at the workload
  level, and frontier models still score below 50% there.
- **Verifiability as the contract bar for agent-assisted intake.**
  Where it applies: bug reports, security findings, customer-
  support tickets, vendor-onboarding intake. Require a reproducible
  PoC, raw observations, or a literal error string over an AI-
  rephrased summary. Caveats: legitimate human-augmented-by-agent
  contributions can be excluded by an overly strict rule; route
  ambiguous items to a separate triage queue, not the close button.
- **Consumption-per-developer with a 70% alert.** Where it applies:
  any team running coding agents inside a 2025 seat budget.
  Replaces flat seat pricing with monthly token caps; the 70%
  alert catches harness-side changes (dynamic workflows, new
  sub-agent dispatch flags) before they consume the cap.
  Caveats: caps that bite mid-sprint create incentive to bypass
  governance; pair with an explicit cap-raise process.

## Action queue

| Candidate | Surface | Effort | Risk | Test |
|---|---|---|---|---|
| Publish `AGENTS.md` at repo root with intake rubric | workflow, agent-role | S | low | merge it; redirect next agent-authored issue to it; measure auto-close rate over 2 weeks |
| Move AI-tooling budget line from seats to consumption + 70% alert | config | S | low | run for 30 days; compare actuals to old per-seat projection; report variance |
| Ship `outbound-communication.yaml` tool-policy row for one agent | tool-policy | S | medium | red-team with a Copilot-Cowork-style image exfil payload; confirm strip + approval gate fire |
| Pin Claude Code at v2.1.156+ and add dynamic-workflows guardrails | config, software-control-plane | S | low | confirm `per_workflow_budget_cap_usd` and audit-log retention apply; run one workflow to threshold |
| Prototype hosted sandbox for one parallel-agent workflow | architecture | M | medium | bench cold-start vs laptop; write retention policy before turning persistence on |
| Run six-factor agent diagnostic on one horizon-H workflow | architecture, eval | M | low | identify bottleneck factor before next model swap; commit a no-model-swap rule for one sprint |
| Add SLEIGHT-Bench probes to monitor eval suite | eval | M | medium | publish catch rate at 1% FPR across three evasion classes; gate next monitor change on it |
| Add HBM / $-per-token / tokens-per-watt rows to infra dashboard | architecture, watchlist | S | low | dashboard surfaces three new rows next sprint review |

## Watchlist

- **When will the first vendor publish a SLEIGHT-Bench number in
  product marketing?** Revisit trigger: any agentic product launch
  that cites a monitor catch-rate against the benchmark, or any
  EU AI Act / AISI guidance that references it. Pick 3 sits on
  this watchlist's resolution.
- **When does the first state-AI-audit deadline (Illinois SB 315
  or peer) bite?** Revisit trigger: Illinois SB 315 effective date,
  any first audit finding, or the next state AI-auditing bill
  passing committee. Pick 7's governance surface lands here.
- **When does an HBM-allocation actual diverge from the 20%-by-end-
  2026 forecast?** Revisit trigger: any Samsung / SK Hynix / Micron
  quarterly call that confirms or revises the share; consumer DRAM
  spot price moves >10% in a month. Pick 7's mechanism either
  holds or breaks here.
- **When does Anthropic disclose audited revenue alongside a
  run-rate?** Revisit trigger: a follow-on round filing, an IPO
  S-1, or any Anthropic post that pairs the run-rate with a TTM
  number. Pick 2's central caveat ("run-rate is the trajectory,
  not the audit") closes here.
- **When does a major project beyond SQLite publish an AGENTS.md
  with comparable scope?** Revisit trigger: openssl, kernel,
  Postgres, Curl, or a top-100 GitHub repo by stars adopts the
  pattern. Pick 1's reusable-pattern claim either generalizes or
  remains an early-adopter signal.
- **When does the Glasswing patch pipeline catch up — or fall
  further behind?** Revisit trigger: Cloudflare, Mozilla, or any
  Glasswing partner publishes a methodology + pipeline-throughput
  number, or a CVE backlog data point lands in 4-12 weeks. The
  bottleneck claim either resolves or compounds.
- **When does the first SEC or FINRA opinion on agent-executed
  retail trades issue?** Revisit trigger: any SEC guidance, FINRA
  notice, or high-profile loss / suit involving an agent-executed
  trade on Robinhood or a peer brokerage. The agent-identity and
  authorization-flow questions either get a regulatory anchor or
  remain a vendor-side T&C question.

## Archive notes

High-quality items the sweep surfaced but that did not earn a pick
this week. Recorded so the corpus stays honest.

- **OpenAI, "Frontier Governance Framework"**
  ([openai.com](https://openai.com/index/openai-frontier-governance-framework)).
  Vendor-self-mapped framework crosswalking internal practices to
  EU AI Act and California rules. Useful as a procurement
  attachment; not picked because the excerpt lacks the
  obligation-level crosswalk needed to verify claimed alignment.
  Archive until EU AI Office or California issues a counterpart
  response.
- **Anthropic Alignment, "Model Spec Midtraining"** and
  **"Teaching Claude Why"**
  ([msm](https://alignment.anthropic.com/2026/msm/),
  [teaching-why](https://alignment.anthropic.com/2026/teaching-claude-why/)).
  Both posts re-verified at higher fidelity than the prior W22
  sweep — but the excerpts still do not publish the
  generalization-gap numbers that would promote them to a Top
  signal this week. Watch for the paper preprint.
- **Stratechery, "The SpaceX IPO and data centers in space"**
  ([stratechery.com](https://stratechery.com/2026/the-spacex-ipo-and-data-centers-in-space/)).
  Ben Thompson concludes racks-in-space are viable but earth still
  wins on cost. Read for strategic optionality framing; not on
  the 12-24-month roadmap.
- **Hugging Face + IBM + Artificial Analysis, "ITBench-AA"**
  ([huggingface.co](https://huggingface.co/blog/ibm-research/itbench-aa)).
  First public benchmark for agentic enterprise IT tasks, with
  frontier models scoring below 50%. The floor a buyer should
  anchor pilot success criteria to. Folded into the policy-ladder
  pick because the <50% number is what justifies "no autonomous
  prod write access" as policy; archived as a standalone because
  the standalone story is "wait for the next leaderboard refresh."
- **AI Snake Oil, "Did Google's AI agents truly build an OS for
  $916?"**
  ([normaltech.ai](https://www.normaltech.ai/p/did-googles-ai-agents-really-build)).  <!-- voice_lint:allow weak-really -->

  Names the methodological issue with Google's $916 demo (prompt
  was "many thousands of lines"). Worth reading on the disclosure-
  norms point; not a Top signal because the response surface
  (require full-prompt disclosure for AI-build demos) is too
  upstream for any single team this week.
- **NVIDIA, "MCG Toolkit for AI model documentation"**
  ([developer.nvidia.com](https://developer.nvidia.com/blog/how-to-automate-ai-model-documentation-with-the-nvidia-mcg-toolkit/)).
  Auto-generates AB-2013 / EU AI Act-shaped model docs. Useful for
  teams training models that fall under those rules. Archived
  because the excerpt does not surface the schema details needed
  to evaluate against a legal-team checklist.
- **Microsoft + EY, ">$1B AI pilots alliance"**
  ([blogs.microsoft.com](https://blogs.microsoft.com/blog/2026/05/21/from-ai-pilots-to-enterprise-impact-why-execution-is-the-new-differentiator/)).
  EY's reported 15% productivity / 94% adoption / 81% time-savings
  numbers anchor an FDE-style alliance. Useful as a procurement
  comparable; not a Top signal because the numbers are vendor-
  reported and the FDE-coverage pattern is already on the radar
  via The Batch 355.
- **Robinhood agent trading**
  ([techcrunch via HN](https://techcrunch.com/2026/05/27/robinhood-now-lets-your-ai-agents-trade-stocks/)).
  Retail brokerage opens an agent-trading rail. The agent identity,
  authorization, and accountability surface is real; archived
  because the picks already carry the policy-ladder framing, so
  this lands as a watchlist item and not a procurement move.
- **OpenAI + Brazilian publishers (Folha + UOL)**
  ([openai.com](https://openai.com/index/grupo-folha-grupo-uol-partnership)).
  Publisher licensing with attribution at presentation time. Useful
  as a precedent for any non-US publisher negotiation; archived
  because the action surface (terms-watching) is narrow.
- **Stanford CRFM, HELM Arabic Enterprise**
  ([crfm.stanford.edu](https://crfm.stanford.edu/2026/05/26/helm-arabic-enterprise.html)).
  Six-competency Arabic enterprise leaderboard; closed-book legal
  QA at 0.495 mean. The procurement primitive for MENA buyers.
  Archived because the audience is narrower than the W22 builder-
  TPM profile.
- **Pope Leo XIV, "Magnifica Humanitas" encyclical on AI** (via
  [Simon Willison](https://simonwillison.net/2026/May/25/encyclical-on-ai/),
  with [Chris Olah's response](https://www.anthropic.com/news/chris-olah-pope-leo-encyclical)).
  Catholic social-teaching document on AI, labor, and human
  dignity. Will enter procurement and ethics-review conversations
  at Catholic-affiliated institutions; archived as a vocabulary
  signal and not a technical move.
- **Alignment Forum, "Eval cooperativeness" and "Robust model
  organisms"**
  ([eval-coop](https://www.alignmentforum.org/posts/j8fkk38B8L7hEcGtg/eval-cooperativeness-may-be-a-scalable-mitigation-for-eval),
  [robust-organisms](https://www.alignmentforum.org/posts/CmkAxJi83jRv9eXgJ/advice-for-making-robust-to-training-model-organisms-1)).
  Methodological posts that strengthen the "system eval, not model
  eval" pattern; archived for safety-research audience.
- **OpenAI, model disproves discrete-geometry conjecture**
  ([openai.com](https://openai.com/index/model-disproves-discrete-geometry-conjecture)).
  Frontier-model attack on an 80-year-old math problem. Worth
  watching for the preprint and a Lean-verified proof; archived
  because the vendor announcement has not been peer-verified.
- **OpenAI + Cisco + Endava + Ramp + Virgin Atlantic + Warp +
  Braintrust + MUFG + AdventHealth + Boston Children's** (the
  enterprise-Codex roster on
  [openai.com/index](https://openai.com/index/)). Folded into pick
  2 as PMF evidence and not archived per-customer; each one
  individually is a procurement comparable, not a Top signal.

## Sources reviewed

The full sweep manifest lives in `briefs/2026-W22/meta.yaml`. The
massive-rerun added 82 sources to the registry (v2 → v3, 52 → 134
total active feeds), attempted 144 sources, succeeded on 108, and
captured 322 source items. The matrix ran 8 lenses per item across
~250 items, producing 2,112 cells with 1,994 verified-passed after
faithfulness review (70 failed, 48 patched-on-revision). The cell
artifact is at `briefs/2026-W22/matrix/cells.yaml` for any reader
who wants to land disagreement at the cell level instead of the
brief level.

Source-level highlights (the full table is in `meta.yaml`):

| Lane | Captured this week | Picks anchored here |
|---|---|---|
| primary-source (Anthropic, OpenAI, Google, Mistral, NVIDIA, Meta, MSR, AWS, HF, etc.) | ~140 items | picks 1, 2, 3, 4, 6 |
| fast-signal (Simon Willison, Import AI, Last Week in AI, ThursdAI, TLDR, Latent Space, The Batch) | ~95 items | picks 1, 2, 3, 5, 7 |
| builder-practice (Cursor, Vercel, Conductor, alphasignal, Datasette, HF blogs) | ~65 items | picks 4, 5, 6 |
| strategy (Stratechery, Interconnects, ACX, Zvi, Stratechery, AI Snake Oil) | ~25 items | pick 7 |

## Closing thought

If the W22 brief had a one-line carrier signal it would be this:
the production-readiness gate has moved out of the model and into
the contract around the model. Glasswing names the contract for
vulnerability disclosure; SQLite names the contract for code
contributions; Cursor names the contract for tool authority;
Vercel names the contract for vendor allowlists; the Series H plus
the PMF post name the contract for finance. None of these
contracts existed in their current shape three months ago. All
of them are draft files this month. The job for the rest of us is
to fork the drafts, not wait for the standard.

---

<!-- voice notes for the author / agent:
  - no banned phrases (see scripts/voice_lint.py BANNED_FAIL)
  - no antithetical reversals
  - no empty adverbial openers
  - every claim links to a primary source where possible
  - the brief is published; it reads in 10-15 minutes

  evidence-spine rules (see AGENTS.md):
  - every Top signal carries an Evidence: line listing one or more
    verified matrix cell ids
  - every Top signal carries a Confidence: label
  - every watchlist item carries a Revisit trigger
  - every action queue row carries a Test column
-->
