# Contract speed, not model speed

**week of 2026-05-18 · audience: builder-tpms thinking about AI · vol. 002**

*Vol. 1 → 2 changelog: added the four systems-thinking fields (Systems
map, Transferable principle, Falsification test, Adoption ladder) to
each Top Signal per DEC-MTRX-007. Source picks and evidence cells are
stable; the upgrade is in the explanatory altitude.*

This week's quiet pattern is that AI is finishing its handshake with
institutions that move slowly. KPMG signed a multi-year deployment. PwC
deepened its partnership. The Gates Foundation committed $200M over
several years. Anthropic acquired the company whose tooling powers its
own SDKs. Google made the new Gemini Flash the default model people
get for free. The model-of-the-week ritual rolled on, but the
load-bearing news arrived in the unglamorous shape of contracts,
procurement reviews, and embedded-in-Workspace defaults.

If you only have time for one move from this brief: rerun your last
quarter's LLM cost line under the new Flash pricing before someone
else does it for you. Worked numbers below.

---

## Anthropic acquires Stainless — pin your SDK versions this week

**What changed.** Stainless makes the OpenAPI-to-SDK generation tooling
behind the Anthropic Python and TypeScript clients. OpenAI is also a
Stainless customer. Public confirmation either way on the continuing
OpenAI contract has not arrived; that confirmation, when it comes, is
its own signal.
[anthropic.com/news/anthropic-acquires-stainless](https://www.anthropic.com/news/anthropic-acquires-stainless)

**Insight.** The contract surface you depend on — retry policy, error
shape, type generation, timeout defaults — moves under one roof. When
that happens, the SDK starts reflecting vendor preferences first and
broad community conventions second. The first place you'll feel it is
in error handling, because that's where the "improvements" tend to
land.

**Action surface:** config, eval

**Concrete moves this week.**

1. Stop using `anthropic@latest` in `package.json` or `pyproject.toml`.
   Pin a minor: `"anthropic": "^0.42.0"` (or whatever you're on).
2. Add a one-file SDK contract test to CI that exercises the two or
   three call shapes you rely on day to day. When a future SDK update
   silently re-shapes an error, the contract test fails before your
   users do.
3. Read the next two Anthropic SDK changelogs end-to-end. Watch for
   "improved error handling" and "default timeout adjusted" — these
   are the cheap-to-write phrases that quietly break in-flight code.

```ts
// apps/web/test/sdk-contract.test.ts
import Anthropic from "@anthropic-ai/sdk";

it("Messages.create returns a 400 with invalid_request_error on empty content", async () => {
  const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY! });
  const result = await client.messages.create({
    model: "claude-opus-4-7",
    max_tokens: 1,
    messages: [{ role: "user", content: "" }],
  }).catch(e => e);

  expect(result.status).toBe(400);
  expect(result.error?.type).toBe("invalid_request_error");
});
```

The test costs you nothing — it never reaches the model — and it's the
canary for an upstream contract change.

**Systems map:** SDK vendor consolidation moves the dependency contract
under one organization, so retry/error/timeout defaults start
reflecting vendor preferences ahead of community conventions. The
load-bearing surface for downstream code is the contract shape, not
the model behavior.

**Transferable principle:** When a vendor acquires the tooling that
generates client SDKs against its own API, pin minor versions and add
a contract test for the surfaces you depend on. Same shape applies to
cloud-provider SDKs (AWS, GCP), payment-processor clients, and
auth-provider SDKs whenever the upstream vendor brings generation
in-house.

**Falsification test:** This claim breaks if the next four Anthropic
SDK minor releases ship without a single change to retry policy,
default timeouts, or error-shape semantics. Two clean changelogs over
60 days would falsify the consolidation-pressure read.

**Adoption ladder:**

  - Minimum viable: pin the Anthropic SDK minor version in
    `package.json` or `pyproject.toml` this week; remove `@latest` or
    unbounded ranges.
  - Mid: add one SDK contract test in CI exercising your two or three
    most-used call shapes plus one error path.
  - Full: extend the contract-test pattern to every vendor SDK whose
    generation tooling moved in-house (OpenAI, the cloud providers,
    the auth provider); review the next two changelogs per vendor on
    every release.
  - Monitoring: changelog entries naming "improved error handling" or
    "default timeout adjusted"; CI contract-test failures on SDK
    bumps; vendor blog posts naming an SDK ownership change.

---

## KPMG, PwC, Gates in five days — build the AI incident playbook before someone asks for it

**What changed.** Three deployment headlines between May 14 and May 19.
Gates is $200M over multiple years, focused on global health. PwC
calls its rollout a "core function" deployment. KPMG names 276,000
seats.
[anthropic-kpmg](https://www.anthropic.com/news/anthropic-kpmg) · [gates-foundation-partnership](https://www.anthropic.com/news/gates-foundation-partnership) · [pwc-expanded-partnership](https://www.anthropic.com/news/pwc-expanded-partnership)

**Insight.** When AI tools cross the 100k-seat line inside a firm,
three workflows tend to break first: incident response, audit, and
new-hire training. Customer-success teams at vendors get pulled into
roles they weren't staffed for. Most internal playbooks haven't been
updated since the team rolled out Slack.

**Action surface:** workflow

**Concrete moves this week.**

1. If you advise large firms: add an "AI incident" page to your
   runbook. Three sections: model-output incident, data-exposure
   incident, vendor-outage incident. Each one with detect / contain /
   communicate sub-steps.
2. If you sell to large firms: your security questionnaire just grew
   by about 30%. Pre-write the answers to the dozen most common
   questions (data residency, sub-processors, model-isolation, audit
   logging, deletion SLAs) before sales pings you at 5pm Friday.
3. If you build internal tooling that uses Claude/OpenAI: today is a
   good day to audit which workflows lack a kill switch. A workflow
   without a 1-minute kill switch is a workflow that can hold your
   weekend hostage.

```markdown
## Model-output incident — generated PII in customer-facing channel

### Detect
- Audit query on `messages.create` in last 24h matching:
  - email regex `[\w.-]+@[\w.-]+\.\w+`
  - SSN regex `\d{3}-\d{2}-\d{4}`
- Trigger: review-queue rule + Sentry breadcrumb on output token tag.

### Contain
1. Rotate the workspace API key (`anthropic console > keys > revoke`).
2. Disable the offending route in the feature flag dashboard.
3. Snapshot the conversation transcript before any deletion.

### Communicate
- Legal + comms: within 2 hours.
- Impacted users: within 24 hours per DPA terms.
- Internal post-mortem: within 7 days, link in #incidents.
```

The playbook is one page. It's worth writing this week, when no one is
asking, because that's the only time you have to write it well.

**Systems map:** AI tooling crossing the 100k-seat line inside a firm
turns three institutional workflows into incident surfaces that were
sized for SaaS-era loads: incident response, audit, and new-hire
training. The deployment moves faster than the playbooks the
organization writes to govern it, and customer-success teams at the
vendor get pulled into roles the contract did not staff.

**Transferable principle:** When a vendor tool crosses an
organizational scale threshold, the runbook around it has to be
rewritten before the first incident — not after. Same pattern held for
Slack rollouts past 10k seats in 2015, for Workday rollouts at large
firms in 2019, and for cloud-IAM rollouts at financial firms in 2020.

**Falsification test:** The "runbook gap" claim breaks if KPMG, PwC,
or a peer publishes a model-incident retrospective in the next 90
days showing detect/contain/communicate steps already in place at
rollout. Either an incident with a clean response, or the lack of any
reported incident over a quarter at 276k seats, would weaken the
claim.

**Adoption ladder:**

  - Minimum viable: draft a one-page AI-incident page in your runbook
    naming the three incident classes (model-output, data-exposure,
    vendor-outage) with detect / contain / communicate sub-steps.
  - Mid: pre-write the dozen most-common security-questionnaire
    answers for the AI vendor, link them from the runbook, and add a
    1-minute kill switch to every AI-touching workflow.
  - Full: tabletop the runbook quarterly with legal, comms, and
    security; treat the kill switch as a tested control with an
    expected-rotation cadence.
  - Monitoring: time-to-revoke on a test API key; security
    questionnaires returned per month; runbook last-updated date;
    incidents detected by audit-log query vs reported by user.

---

## Project Glasswing — add five items to your AI vendor review

**What changed.** Anthropic published an update on a collaborative
effort to secure critical software infrastructure across major
technology and financial firms.
[research/glasswing-initial-update](https://www.anthropic.com/research/glasswing-initial-update)

**Insight.** AI vendors are starting to inhabit the role cloud vendors
filled around 2014: the security and compliance posture becomes the
product in the customer's eyes before any single feature does. The
review questions stop being about model quality and start being about
the vendor's audit log.

**Action surface:** tool-policy

**Concrete moves this week.** Add these five items to your next AI
vendor review, and refuse "industry-standard" as an answer to any of
them.

1. **SOC2 Type II — report date and audit firm.** The date matters as
   much as the report. A 2024 report on a 2026 stack is theater.
2. **DPA terms.** Specifically — sub-processor list, data-residency
   options, deletion-on-request SLA, audit-log retention period.
3. **Model-isolation guarantee.** Is your tenant data ever used for
   training? Eval suites? Red-teaming?
4. **Audit-log retention + export.** Can you pull every API call your
   workspace made last quarter, with prompts, on demand?
5. **API-key compromise SLA.** Ask: "What's your published SLA for
   revoking an API key after a customer reports it compromised?" The
   answer you want is < 1 minute. Any answer over 15 min is a
   procurement red flag worth escalating.

```
# vendor-review-ai.yaml — drop this into procurement intake

vendor: <name>
review_date: 2026-MM-DD
soc2_type_ii:
  report_date: <YYYY-MM-DD>
  audit_firm: <name>
dpa:
  sub_processors: <list>
  data_residency: [us|eu|other]
  deletion_sla_days: <int>
  audit_log_retention_days: <int>
model_isolation:
  used_for_training: false  # required: false
  used_for_evals: false
  used_for_red_teaming: false
audit_log:
  pull_quarter_on_demand: yes|no
api_key_compromise_sla_seconds: <int>  # required: < 60
```

**Systems map:** AI vendors now occupy the role cloud vendors filled
around 2014 — the security and compliance posture becomes the product
in the customer's eyes before any single feature does. The review
question moves from "is the model good" to "can I audit and revoke."

**Transferable principle:** When a vendor category matures from
capability competition to compliance competition, procurement intake
has to grow new contract fields ahead of the renewal cycle. Same
transition ran through SaaS in 2014 (SOC2 became table stakes), through
cloud in 2016 (data residency became table stakes), and through
payments in 2018 (PCI scope became the procurement gate).

**Falsification test:** This claim breaks if a major AI procurement
in the next two quarters closes without the five items on the
checklist surfacing as gating questions. A renewal that hinges
entirely on model quality benchmarks would falsify the maturity
read.

**Adoption ladder:**

  - Minimum viable: add the five items (SOC2 Type II report date +
    audit firm, DPA terms, model-isolation, audit-log retention, API
    key compromise SLA) to your next AI vendor review intake form.
  - Mid: codify the five items into a YAML procurement template and
    require completion before legal review.
  - Full: extend the template across every AI-touching vendor in the
    portfolio; run a quarterly audit on completed templates and
    escalate any answer over the published thresholds.
  - Monitoring: percent of completed templates with all five items
    filled; vendors with SLA > 15 min on API-key compromise; vendors
    with SOC2 reports more than 18 months old.

---

## Gemini 3.5 Flash GA across Workspace — rerun your unit economics this week

**What changed.** Google launched Gemini 3.5 Flash directly to general
availability and embedded it across Gmail, Calendar, and other
Workspace surfaces. The new Flash costs more than the prior Flash, and
Google made the new one the default for users without a paid plan.
[simonwillison.net coverage](https://simonwillison.net/2026/May/19/gemini-35-flash/)

**Insight.** When the cheap-tier model's price goes up, the customer
math behind your last six months of LLM cost projections is wrong.
Most teams haven't reopened the sheet.

**Action surface:** config

**Concrete moves this week.** Pull last quarter's LLM cost line. Build
the table below for your actual call volume; the directional shape of
this example is wrong for you, but the spreadsheet shape is the move.

```
                     input cost     output cost   Q2 cost @ current vol   Q2 cost @ +30% vol
Flash 2.5 (old)      $0.075/1M      $0.30/1M      $42k                    $55k
Flash 3.5 (new)      $0.13/1M       $0.50/1M      $71k                    $92k
Claude Haiku 4.5     $0.25/1M       $1.25/1M      $115k                   $150k
60% on Llama-OSS     mix            mix           $61k                    $80k
                                                  + infra carry: ~$24k
```

Three decisions fall out of this table:

1. If Flash 3.5 at +30% growth breaks your gross margin: your default
   model selection has to change before someone notices in a board
   review.
2. If you've been routing 100% of traffic to Flash on price alone, the
   premise of that routing is gone.
3. If your enterprise contract was signed assuming Flash 2.5 unit
   economics, the renewal conversation just got harder. Pre-write the
   talking points.

**Systems map:** Default-model price moves reshape downstream unit
economics even when no application code changes. The pricing of the
cheap tier is the load-bearing input for any routing decision built on
price alone, so a price increase at the default tier rewrites every
spreadsheet built on the prior assumption.

**Transferable principle:** When a vendor moves the default tier's
price, every cost projection downstream of "we'll just use the
default" silently breaks. Same shape applies to default-tier S3
pricing changes, default-tier database storage rate changes, and
default-tier CDN egress changes — anywhere a routing decision was made
on the default tier and never revisited.

**Falsification test:** The unit-economics claim breaks if a sample
of teams currently routing primarily to Flash 2.5 do the new sheet and
find Q2 cost growth under 10% under Flash 3.5 pricing at current
volumes. A small enough delta would mean the routing decision did not
in fact depend on the price line that moved.

**Adoption ladder:**

  - Minimum viable: pull last quarter's LLM cost line into a sheet and
    rerun the column under Flash 3.5 pricing at current call volume.
  - Mid: add two adjacent columns — Flash 3.5 at +30% volume and a
    mixed OSS/managed scenario — so the next routing decision is
    informed by three rows, not one.
  - Full: rebuild model selection as a per-route choice priced
    against each model's input + output rates, gross margin per route
    becomes a tracked metric in finance review.
  - Monitoring: monthly LLM spend per route; gross margin per route;
    default-tier price-change announcements from Google, Anthropic,
    OpenAI; enterprise renewal cycle dates against vendor pricing
    moves.

---

## Simon Willison's *Last Six Months in LLMs* — forward to one specific person

**What changed.** Simon published annotated slides from a PyCon US
lightning talk covering November 2025 through May 2026.
[5-minute-llms](https://simonwillison.net/2026/May/19/5-minute-llms/)

**Insight.** Most teams have one or two members whose AI mental model
is still operating on November 2025 assumptions. They're shaping
decisions — vendor selection, hiring screens, tooling buys — that you
inherit. Six months out of date in this space is closer to two years
out of date in a normal one.

**Action surface:** workflow

**Concrete move this week.** Forward the link to the two teammates
whose AI assumptions you suspect are six months stale. Schedule 15
minutes on Friday to discuss one slide together. The conversation
prompt you want is:

> "Which of these eight items changed your mental model? Of the ones
> that didn't, what would have to be true for them to?"

The second half does the heavy lifting. It surfaces the unstated
priors that drive their decisions.

**Systems map:** In a fast-moving capability landscape, the
load-bearing risk on team decisions is a stale mental model held by a
small number of teammates whose decisions cascade. Six months out of
date in this space is closer to two years out of date in a more
stable one, and the lag compounds through hiring, vendor selection,
and tooling buys.

**Transferable principle:** When a domain's underlying tech base
churns faster than ordinary team-knowledge maintenance, deliberate
priors-update rituals (a forwarded annotated talk, a 15-minute
weekly read, a one-slide-per-week deck) outperform ad-hoc reading.
Same pattern shows up in security teams tracking exploit-class
shifts, finance teams tracking macro-regime shifts, and platform
teams tracking cloud-feature deprecations.

**Falsification test:** Non-falsifiable; this is a normative claim
about how teams should maintain shared priors in a fast-moving
domain. There is no clean observation that would prove "forwarding
the talk is not useful" — only weak proxies like whether the
recipient changes a decision after the discussion.

**Adoption ladder:**

  - Minimum viable: forward the link to the two teammates whose AI
    assumptions you suspect are six months stale; schedule 15
    minutes on Friday.
  - Mid: hold the 15-minute discussion against the suggested prompt;
    name one decision in flight that each teammate would revisit
    after the talk.
  - Full: standardize a quarterly "priors review" — one annotated
    talk or post per quarter, 15 minutes per teammate, named
    decisions revisited as the output.
  - Monitoring: decisions explicitly revisited after the discussion;
    self-reported confidence shift on a 1-5 scale before and after;
    follow-on Slack threads referencing the talk.

---

## Three more, in shorter form

**Eugene Yan, *How to Work and Compound with AI*** (May 3). Four
frames — context infrastructure, taste configuration, verification,
delegation. For most builders the load-bearing one is **context
infrastructure**: the persistent decisions, preferences, and
constraints you re-feed the agent so it doesn't relearn your taste
each session. Start with a short `AGENTS.md` or `CLAUDE.md` at the
root of your most-used repo:

```markdown
# Coding style
- Prefer Edit over Write for existing files. Read first.
- Default to functional React components; no class components.
- All env vars validated at boot via zod (see lib/env.ts).
- TS strict; noUncheckedIndexedAccess on.

# Domain decisions
- Multi-tenant rule: every query takes workspace_id.
- Apache-2.0 for code, CC BY 4.0 for content.
- Vendor pinning rule: pin SDK minors, run a contract test in CI.

# Workflow conventions
- Push small commits. Don't batch unrelated changes.
- voice_lint and spec_check are PR gates; fix locally first.
```

Keep it under 200 lines. Update when a decision changes; delete when
it doesn't apply.
[eugeneyan.com/writing/working-with-ai](https://eugeneyan.com/writing/working-with-ai/)

**Action surface:** agent-role

**Hamel Husain, *Evals Skills for Coding Agents*** (Mar 2). The eval
gap on coding agents is mostly a labeling problem; "did the PR fix
the bug as intended" is the hard part, not the runner. Pick one
production failure mode in your AI feature this week, write the
LLM-as-judge prompt for it, run it against 20 historical responses,
and look at the disagreements. The judge prompt to start from:

```
You are evaluating whether a coding-agent's PR correctly fixes the bug
described in the issue. Be strict. Return JSON:
  { "fixed": boolean,
    "reason": string,
    "regression_risk": "low" | "medium" | "high",
    "untested_paths": string[] }

Issue: <pasted issue>
PR diff: <pasted diff>
Test plan executed: <pasted test plan>

A "fixed" verdict requires: the change addresses the named root cause,
not a symptom; existing tests still pass; at least one new test covers
the case named in the issue.
```

Run this against 20 PRs from your archive. If the judge disagrees with
your team on more than 20% of them, the judge prompt is wrong — or
your team's review bar is. Either answer is useful.
[hamel.dev/blog/posts/evals-skills](https://hamel.dev/blog/posts/evals-skills/index.html)

**Action surface:** eval

**Simon Willison, *Datasette Agent*** (May 21). Three years of work on
the `llm` library, finally merged with Datasette. The artifact is
small next to the time horizon — Simon's personal infra has compounded
for 23 years, which Karpathy publicly flagged this week. Most readers
can't copy the path. The discipline behind it is the part that
travels: pick one personal tool you intend to own for the next five
years, and treat the upkeep as a non-negotiable monthly hour.
[simonwillison.net/2026/May/21/datasette-agent](https://simonwillison.net/2026/May/21/datasette-agent/)

**Action surface:** architecture, experiment

**Systems map (for the three shorter picks):** Each of Eugene Yan,
Hamel Husain, and Simon Willison points at the same upstream
mechanism — durable AI work compounds when a small persistent
artifact carries the context an agent or a team would otherwise have
to relearn. Context-infrastructure files, LLM-as-judge eval prompts,
and decade-spanning personal tooling are three instances of the same
"persistent typed artifact" pattern.

**Transferable principle:** When agent or team work is high-variance
session to session, the lever is a small, versioned artifact that
carries the decisions and priors across sessions. Examples beyond
these three: a `style.md` for code review preferences, a saved
search-query template for a recurring analytics question, or a
templated agenda that anchors a recurring meeting.

**Falsification test:** The pattern weakens if teams that adopt
`AGENTS.md` files, LLM-as-judge prompts, and durable personal
tooling do not report fewer re-explanation cycles or fewer rework
PRs over a 60-90 day window. Absent any measurable reduction in
context-relearning, the persistent-artifact claim is closer to a
preference than a system.

**Adoption ladder:**

  - Minimum viable: pick one of the three artifacts (an `AGENTS.md`
    or `CLAUDE.md`, an LLM-as-judge eval prompt for one failure
    mode, or one personal tool's monthly upkeep slot) and ship it
    before Friday.
  - Mid: run all three in parallel — keep the `AGENTS.md` under 200
    lines, run the judge prompt against 20 historical responses, and
    book the monthly upkeep hour on the calendar as a recurring
    event.
  - Full: treat each artifact as a versioned control surface — the
    `AGENTS.md` lives next to the code under PR review, the eval
    prompt sits in CI on a sampled subset of PRs, and the personal
    tool gets a quarterly retrospective on what the monthly hour
    bought.
  - Monitoring: PR-review iteration count on agent-authored work;
    judge-vs-human disagreement rate trend; hours spent on each
    personal tool's upkeep vs hours saved using it.

---

## Questions to ask in the next 30 days

- **Of a colleague at KPMG, PwC, or any 100k+ firm:** "What's your
  firm-wide policy on Claude prompt review?" The answer tells you
  whether the rollout is governed or improvised.
- **Of your finance partner:** "What's our LLM spend exposure under
  Flash 3.5 pricing at +30% volume?" If they can't answer in a week,
  the spreadsheet from earlier is a starting place.
- **Of your security partner:** "When did we last update our AI
  vendor review template?" If the answer predates Project Glasswing,
  add the five items from earlier.
- **Of a teammate whose AI mental model is six months stale:** "Of
  these eight slides, which two would change a decision you're making
  this quarter?"

---

## Closing thought

Write down one decision you're delaying because you're not sure
whether AI changes it. Date the entry. Revisit in 30 days. The
entry is the artifact — the decision is downstream.

---

## Postscript: 2026-W21 dream candidates

The week's offline-cognition pass landed alongside this brief. Six
promotion candidates surfaced from the last seven days of commits, the
brief itself, and the CI run history. Three propose memory updates to
`.agents/AGENTS.md`, one proposes a new skill, two propose regression
tests. The candidates are proposals, not patches; each one carries
`human_review_required: true` and waits for a reviewer to pick it up.
Full report at [`dreams/2026-W21/report.md`](../../dreams/2026-W21/report.md).
