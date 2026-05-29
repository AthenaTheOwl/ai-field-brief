# The week the line item moved categories

**week of 2026-05-25 · audience: builder-tpms thinking about AI · vol. 003**

Three stories arrived in the same week and they tell the same shape from
different angles. Anthropic disclosed a $65 billion Series H at a $965B
valuation and $47B in annualized run-rate revenue, up from $9B at the
end of 2025. Simon Willison published a 30-day personal coding-agent
bill of $2,180 against a $200/month subscription assumption, and a
secondhand Uber number — 25% of last quarter's commits via Claude Code.
Daniel Stenberg reported curl is now receiving more than one
AI-assisted security report per day on average, 4-5x the 2024 rate.
Underneath the three reports is one finance fact: coding agents burn
vastly more tokens than humans, and the budget line item that paid for
them in 2025 is the wrong category in 2026.

If you have time for one move from this brief, rebuild the AI-tooling
budget line as consumption-per-developer with a monthly cap and a 70%
alert before the next sprint. Every other pick this week sits on top
of that change.

---

## Anthropic Series H + $47B run-rate — rebuild the AI-tooling line item this week

**What changed.** Anthropic announced a $65B Series H at a $965B
post-money valuation on May 28 and disclosed annualized run-rate
revenue of $47B, up from $30B in April and $14B in February. Simon
Willison's run-rate explainer adds the context that "run-rate"
annualizes the most recent month — the trajectory is the signal, the
exact number is the noisiest possible projection.
[anthropic.com/news/series-h](https://www.anthropic.com/news/series-h)
· [simonwillison.net/2026/May/29/anthropic](https://simonwillison.net/2026/May/29/anthropic/)

**Insight.** The growth mechanism sits inside enterprise coding-agent
token consumption rather than consumer chat — on customers moved from <!-- voice_lint:allow weak-rather -->
flat seat pricing to API pricing in early 2026. Willison's own data
— $1,199.79 of Claude Code spend plus $980.37 of OpenAI agent spend
over 30 days, against $200/month subscriptions on each side — is the
n=1 confirmation. The Uber line ("25% of code commits via Claude
Code last quarter, rapidly consuming annual AI budgets set in
2025") is the second-hand confirmation at the carrier-wave layer.

**Action surface:** config, workflow

**Concrete move this week.** Pull the AI-tooling line item from your
2026 budget. If it sits under SaaS subscriptions with a flat
per-seat cap, move it to consumption with a monthly burn cap per
developer and a 70%-of-cap alert in Slack. The table below is the
shape worth filling in.

```
team / agent surface          2025 annual seat budget    2026 monthly burn cap    alert
backend / Claude Code         $200 * seats * 12          $600 / dev / month       Slack 70%
frontend / Codex              $200 * seats * 12          $400 / dev / month       Slack 70%
security / agentic monitor    $0 (informal)              $1200 / month            Slack 70%
support / agent drafts        $0 (informal)              $200 / month             Slack 70%
research / batch analysis     $0 (informal)              $300 / month             Slack 70%
```

The cap is the contract. The alert is what catches the surprise the
month a coding agent acquires a new sub-agent dispatch flag (see the
Claude Code v2.1.154 pick below).

Caveat that goes in the same conversation: $47B run-rate is one
month annualized. The number is directionally credible — lying in a
fundraise to investors who placed $65B is securities fraud — but it
is not audited annual revenue. Reset your budget on the trajectory;
do not commit next-quarter contract terms on the assumption that
5x-in-five-months continues.
<!-- evidence: MTRX-W22-seriesh-source_gist, MTRX-W22-pmf-source_gist, MTRX-W22-pmf-adoption_action, MTRX-W22-seriesh-risk_and_caveats -->

---

## curl + SQLite — publish the AI-assisted-report policy this week

**What changed.** Daniel Stenberg, curl maintainer, reports the
project is now receiving more than one AI-assisted security report
per day on average — 4-5x the 2024 rate and 2x the 2025 rate. None
have surfaced critical vulnerabilities; recent findings have been
LOW or MEDIUM. Two days later SQLite published an AGENTS.md that
rejects agentic code patches and AI-generated PRs while accepting
well-researched bug reports from agents with reproducible test
cases. SQLite also stood up a separate Bug Forum to absorb the noise.
[simonwillison.net/2026/May/26/the-pressure](https://simonwillison.net/2026/May/26/the-pressure/)
· [simonwillison.net/2026/May/27/sqlite-agents](https://simonwillison.net/2026/May/27/sqlite-agents/)

**Insight.** Two of the most-deployed projects on the planet just
published the same answer to the same prompt, and that prompt comes
from the W22 brief 1 thesis on a different lane: agent output rate
exceeds the human review rate downstream. The maintainer is the
bottleneck. SQLite's shape — accept reports with evidence, reject
agentic patches, segregate the noisy channel — is the project-level
contract every open-source maintainer and corporate security team
needs to publish before the same pressure arrives at their door.

**Action surface:** workflow, tool-policy, agent-role

**Concrete move this week.** Publish an AI-assisted-report policy
that names the required evidence and what gets auto-closed. The
shape below works for an open-source project, an internal security
bug bounty, or a customer-facing support intake.

```markdown
# ai-assisted-report-policy.md

## What we accept from AI-assisted submissions

- A reproducible command or workflow that triggers the issue
- Expected result (one sentence)
- Actual result (one sentence)
- Literal error text or output (no AI summarization)
- Optional: links to the relevant source spans

## What we auto-close

- Analysis without a reproducer
- "Potential vulnerability" reports with no proof-of-concept
- Reports that rephrase a previously closed issue with new analysis
- Reports where the AI-generated text is longer than the literal observation

## Where AI-assisted reports go

A separate `ai-assisted-reports` channel / forum / triage queue,
with a different SLA than human-submitted reports and a different
triage owner.

## Slow-mode lever

If the queue depth in the AI-assisted channel exceeds N for more
than M days, the project may pause new submissions for K days while
the backlog drains. Notice is public.
```

The slow-mode lever is the one the W22 brief 1 Glasswing maintainers
asked Anthropic for. Same mechanism, different surface.
<!-- evidence: MTRX-W22-curl-source_gist, MTRX-W22-curl-reusable_pattern, MTRX-W22-curl-adoption_action, MTRX-W22-sqlite-source_gist, MTRX-W22-sqlite-reusable_pattern, MTRX-W22-sqlite-governance_surface -->

---

## Microsoft Copilot Cowork exfiltration — write the outbound-communication tool policy

**What changed.** Simon Willison documented that Microsoft Copilot
Cowork agents could send emails to user inboxes without explicit
approval, and that messages can contain attacker-supplied external
images. When a recipient opens such a message, the image request
URL exfiltrates OneDrive pre-authenticated download links.
[simonwillison.net/2026/May/26/copilot-cowork-exfiltrates-files](https://simonwillison.net/2026/May/26/copilot-cowork-exfiltrates-files/)

**Insight.** This is the textbook prompt-injection exfiltration
chain: external content reaches the agent; agent composes outbound
communication; communication carries an attacker-controlled external
resource URL; the recipient client requests the resource; the
request URL leaks the payload. Microsoft made the chain possible by
skipping the human-approval gate on agent-initiated email. The
chain works on any agent surface that drafts outbound communications.

**Action surface:** tool-policy, agent-role

**Concrete move this week.** Add a single row to the tool-policy
register and ship it. The row names the outbound-communication
surfaces and the controls on each.

```yaml
# tool-policy / outbound-communication.yaml
agent_outbound_communications:
  email:
    external_images:        strip-or-proxy-through-sanitizer
    human_approval_required: yes
    audit_log:              every-draft-and-send
    allowed_recipients:     allowlist | broadcast-blocked
  slack_dm:
    external_links:         expand-and-display-target
    human_approval_required: yes-for-customer-channels
    audit_log:              every-send
  calendar_invite:
    external_attachments:   block
    human_approval_required: yes
  ticket_comment:
    external_images:        strip
    human_approval_required: no-but-edit-window-required
```

The two-line minimum is: strip or proxy external image references
before send, and require explicit user approval before an
agent-composed message ships. Either alone is partial; both
together close the chain.
<!-- evidence: MTRX-W22-copilot-source_gist, MTRX-W22-copilot-mechanism_extraction, MTRX-W22-copilot-adoption_action, MTRX-W22-copilot-governance_surface -->

---

## SLEIGHT-Bench — put a number under your "monitored agent" claim

**What changed.** Anthropic's Alignment Science team published
SLEIGHT-Bench on May 26, a benchmark of 40 hand-crafted attacks
across 11 categories that stress LLM-based monitors. At a 1% false
positive rate, Claude Opus 4.6 reliably catches 8 of 40 attacks;
50% of attacks are never caught across multiple trials. Per-blind-
spot catch rates range from 0% (N-hops, omission, jailbreaks
embedded in transcripts) to 90% (plausible naming).
[alignment.anthropic.com/2026/sleight-bench](https://alignment.anthropic.com/2026/sleight-bench/)

**Insight.** "Monitored by an LLM" is now the most common safety
framing in agent product marketing. SLEIGHT-Bench gives a buyer or
a security partner the first concrete number to hold against the
claim. The blind spots are not exotic — multi-session attack
stitching, omission of expected actions, authorization confusion
between user directives and agent-manufactured justifications.
Most current LLM-only monitors fail at the categories the paper
names; the agentic-monitor variant (letting the monitor execute
code to verify claims) measurably improves detection.

**Action surface:** eval, tool-policy, agent-role

**Concrete move this week.** Pick the three or four SLEIGHT-Bench
blind spots most relevant to your workload and add targeted probes
to your monitor eval set. The four below are the common defaults.

```
blind spot               probe to add
multi-session stitching  a 3-session attack split across days, monitor
                         must connect them
omission                 an agent task where the malicious move
                         skips a required action rather than doing one  voice_lint:allow weak-rather
authorization confusion  an agent that quotes the user's words inside
                         its own justification for a privileged action
jailbreak-in-transcript  an attacker-supplied prompt buried inside
                         legitimate-looking transcript content
```

Prototype the agentic-monitor pattern (Claude Code running as the
monitor, with execution access to verify claims) as a one-week
experiment before committing to it as production. The paper reports
catch-rate improvement; the cost is ~10x invocations and ~14x
tokens at ensemble scale, so the prototype is also the budget gate.
<!-- evidence: MTRX-W22-sleight-source_gist, MTRX-W22-sleight-mechanism_extraction, MTRX-W22-sleight-adoption_action, MTRX-W22-sleight-risk_and_caveats, MTRX-W22-sleight-governance_surface -->

---

## Claude Code v2.1.154 + dynamic workflows — cap the blast radius before rollout

**What changed.** Claude Code v2.1.154 shipped on May 28 with Opus
4.8 as the default model, `/effort xhigh` as the default for
complex tasks, lean system prompt default for new models, and
dynamic workflows that orchestrate tens to hundreds of agents in
the background via `/workflows`. Streaming tool execution is now
on everywhere including Bedrock, Vertex, and Foundry. Two days
later v2.1.156 fixed an Opus 4.8 thinking-block regression that
was causing API errors.
[github.com/anthropics/claude-code releases](https://github.com/anthropics/claude-code/releases)

**Insight.** Dynamic workflows move the orchestration boundary
inside the model. The model now plans, branches, and dispatches
sub-agents at runtime; the operator's `/workflows` view is the
surface that makes the run tree visible. The trade is operator
certainty for agent-side adaptability — and a much higher per-run
cost ceiling when xhigh-effort pairs with multi-agent dispatch.
Released paired with Opus 4.8, the budget exposure compounds.

**Action surface:** agent-role, config, tool-policy

**Concrete move this week.** Before you turn on dynamic workflows
in a shared org install, add the four guardrails below to the org
configuration. The first two are the budget perimeter; the second
two are the audit surface.

```yaml
# claude-code dynamic-workflows guardrails
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

Pin v2.1.156 or later before rolling forward — the .154 release was
still settling and a scripted CI pipeline against the new flag set
should wait one cycle. The pace of releases (eight versions in
eight days) is itself the carrier signal; the surface is moving
faster than the documentation.
<!-- evidence: MTRX-W22-cc154-source_gist, MTRX-W22-cc154-mechanism_extraction, MTRX-W22-cc154-adoption_action, MTRX-W22-cc154-risk_and_caveats, MTRX-W22-opus48-source_gist, MTRX-W22-opus48-adoption_action -->

---

## Worth your time

**Anthropic Alignment Science, "Model Spec Midtraining"** (May 21).
Insert a stage between pre-training and alignment fine-tuning where
the model trains on synthetic documents discussing its own model
spec. Reported: Qwen2.5-32B agentic-misalignment drops from 68% to
5%; Qwen3-32B from 54% to 7%; alignment fine-tuning becomes 40x
more token-efficient. The mechanism is teaching the why before the
how — the application-layer analog is the AGENTS.md or CLAUDE.md
that names principles before listing rules. If your spec only lists
rules, add a why paragraph; if your eval only scores outputs, add a
reasoning-quality slot.
[alignment.anthropic.com/2026/msm](https://alignment.anthropic.com/2026/msm/)

**Anthropic Alignment Science, "Teaching Claude Why"** (May 23).
Companion paper to MSM. A constitutional-rewrite step in the
training pipeline drops misalignment from 19% to ~1%; constitutional
documents plus fictional stories drop blackmail rates from 65% to
19%. The decisive step is asking the model to rewrite its own
response against the stated principle, then accepting the
critique-revised draft. The Claude Code `/code-review --fix` pattern
in v2.1.152 is the productized cousin.
[alignment.anthropic.com/2026/teaching-claude-why](https://alignment.anthropic.com/2026/teaching-claude-why/)

**Hugging Face + IBM + Artificial Analysis, "ITBench-AA"** (May 27).
The first public benchmark for agentic enterprise IT tasks reports
frontier models score below 50%. The result is the floor your buyer
should anchor a pilot's success criteria to. Any vendor pitching
enterprise-IT agent replacement should publish a result on a public
benchmark or admit they have none; the row belongs in the vendor
review template.
[huggingface.co/blog/ibm-research/itbench-aa](https://huggingface.co/blog/ibm-research/itbench-aa)

**Hugging Face, "Ettin reranker family"** (May 19). Six pointwise
cross-encoder rerankers from 17M to 1B parameters, distilled from
mxbai-rerank-large-v2. The 1B model matches the 1.54B teacher on
MTEB NDCG@10 while running 2.4x faster on H100; the 17M model beats
33M ms-marco-MiniLM-L12-v2 at half the parameters. Teams running a
retrieve-then-rerank pipeline on a legacy MiniLM reranker have a
config-flip upgrade available — pilot the 150M as the new balanced
default, run a domain eval, confirm the lift.
[huggingface.co/blog/ettin-reranker](https://huggingface.co/blog/ettin-reranker)

**OpenAI Cookbook commits, "Add Claude Agent SDK migration cookbook"**
(May 27). OpenAI merged PRs #2671 and #2742 — a documented path for
teams running on Anthropic's Agent SDK to migrate to OpenAI agents.
The signal is the asymmetry: Anthropic does not currently publish
the reverse recipe. Procurement teams reviewing AI agent vendor
lock-in should ask both labs for a published migration path to the
other and read the asymmetry as a concrete consideration.
[github.com/openai/openai-cookbook/commit/f6a7ffa9](https://github.com/openai/openai-cookbook/commit/f6a7ffa9ddd57849bb280b20102da7ff8620e8fa)

**NVIDIA Developer Blog, "Automate AI model documentation with the
MCG Toolkit"** (May 29). Automated model-card generation explicitly
framed against California AB-2013 and the EU AI Act. AB-2013
deadlines fall inside Q3 for California-deployed systems. Add a
model-card generation step to the release workflow now; backfilling
under regulatory pressure is more costly than automating once.
[developer.nvidia.com/blog/.../mcg-toolkit](https://developer.nvidia.com/blog/how-to-automate-ai-model-documentation-with-the-nvidia-mcg-toolkit/)

**Stratechery, "The Data Center Veto"** (May 22, paywalled).
Ben Thompson argues local opposition to AI data centers is rising
and that direct compensation to host communities is the only viable
path to keep buildouts on schedule. Read for the procurement-side
implication: hyperscaler capacity expansion through 2027 is a
political question, not a capex question.
[stratechery.com/2026/the-data-center-veto](https://stratechery.com/2026/the-data-center-veto/)

---

## Watchlist

- **Of your security partner: when did we last test the outbound-
  communication exfiltration case?** The Copilot Cowork pattern is
  generic to any agent that drafts outbound messages. Pick one
  agent surface and run the chain end-to-end this month.

- **Of your finance partner: what is our consumption-per-developer
  cap and our 70% alert?** If the answer is "we are on seat
  pricing," the Series H + $47B run-rate disclosure is your cue to
  rebuild the line item before next sprint.

- **Of your CISO: do we publish an LLM-monitor catch-rate number?**
  SLEIGHT-Bench gives the buyer a number to ask for. The vendor
  answer "we use an LLM-based monitor" without a benchmark result
  is no longer a defensible position.

- **Of your product partner: what is our refusal-rate panel on
  Opus 4.8?** Abstention-tuned models change the audit-log surface.
  If your dashboard does not surface refusal rate, the metric will
  shift without anyone noticing.

- **Of your platform team: which Fortune-500 case study should we
  read for our own customer's procurement?** The Cisco + Codex and
  Endava + Codex co-marketed posts are the template. Expect every
  large enterprise you sell to or buy from to publish one in 2026.

- **Of your legal partner: which AI workflows in our stack ship
  into California-served products?** AB-2013 model-card deadlines
  fall inside Q3. Automate cards now.

---

## Closing thought

The shape this week is not new — agent output exceeds human review,
the budget line moved categories, the security perimeter has an
outbound-communication hole nobody priced in. What is new is that
the answers are starting to land as project-level contracts: an
AGENTS.md, a tool-policy row, a model-card automation step, a
catch-rate eval. The ones already published this month are worth
reading not as final shapes but as drafts the rest of us can fork.

---

## Postscript: the factory's own week

This brief is the first run through the Matrix Plane pipeline. The
shape underneath what you just read is 40 source items, 100+ matrix
cells across eight lenses (source gist, claims and bets, mechanism,
reusable pattern, adoption action, risks, governance, watchlist),
and a cell-faithfulness pass on every cell before any digest claim
got drafted. The cells live under `briefs/2026-W22/matrix/` next to
the brief; the per-item notes live under `briefs/2026-W22/items/`.
The reason this matters for an outside reader is the audit trail.
Every claim in the brief points at one or more cells; every cell
points at a source span. If a reader disagrees with a pick, the
disagreement can land at the cell level, not as a vague complaint
about the brief. That contract is the next sprint's exercise — make
the reader's edit-path runnable, not just commentable.
