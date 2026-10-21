# Contract speed, not model speed

**week of 2026-05-18 · audience: builder-tpms thinking about AI · vol. 002**

*Vol. 1 → 2 changelog: added the four systems-thinking fields (Systems
map, Transferable principle, Falsification test, Adoption ladder) to
each Top Signal per DEC-MTRX-007. Source picks and evidence cells are
stable; the upgrade is in the explanatory altitude.*

Five things happened this week, and the institutional/contract moves matter more than the model releases. KPMG signed a multi-year deployment. PwC deepened its partnership. The Gates Foundation committed $200M over several years. Anthropic acquired the company whose tooling powers its own SDKs. Google made the new Gemini Flash the default free-tier model.

Last quarter's LLM cost line: rerun it under the new Flash pricing now. Worked numbers below. Your CFO will get there on Monday.

---

## Anthropic acquires Stainless — pin your SDK versions this week

**What changed.** Stainless makes the OpenAPI-to-SDK generation tooling
behind the Anthropic Python and TypeScript clients. OpenAI is also a
Stainless customer. Public confirmation either way on the continuing
OpenAI contract has not arrived; that confirmation, when it comes, is
its own signal.
[anthropic.com/news/anthropic-acquires-stainless](https://www.anthropic.com/news/anthropic-acquires-stainless)

**Insight.** Stainless ships SDK defaults: retry policy, error shape, timeouts. Now Stainless reports to Anthropic. Error handling is one place to watch for drift; the acquisition alone does not show any.

**Action surface:** config, eval

**Concrete moves this week.**

1. Pin the tested version of `@anthropic-ai/sdk` in `package.json`
   (or `anthropic` in `pyproject.toml`) and commit the lockfile.
   Upgrade deliberately; the TypeScript and Python packages have different names.
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

it("preserves our required 400 error shape from a local fixture", async () => {
  const client = new Anthropic({
    apiKey: "local-fixture", maxRetries: 0,
    fetch: async () => new Response(JSON.stringify({
      type: "error",
      error: { type: "invalid_request_error", message: "fixture" },
    }), { status: 400, headers: { "content-type": "application/json" } }),
  });
  const result = await client.messages.create({
    model: "claude-opus-4-7",
    max_tokens: 1,
    messages: [{ role: "user", content: "fixture" }],
  }).catch(e => e);

  expect(result.status).toBe(400);
  expect(result).toBeInstanceOf(Anthropic.APIError);
  expect(result.error?.error?.type).toBe("invalid_request_error");
});
```

The fetch stub makes this an offline SDK regression test. It cannot
prove the live API still returns that error. A live canary needs its
own budget and a documented expected response.

**Systems map:** SDK ownership changed. Retry, error, and timeout
behavior are the dependency surfaces to compare on the next upgrade.

**Transferable principle:** When a vendor acquires the tooling that
generates client SDKs against its own API, pin minor versions and add
a contract test for the surfaces you depend on. Same shape applies to
cloud-provider SDKs (AWS, GCP), payment-processor clients, and
auth-provider SDKs whenever the upstream vendor brings generation
in-house.

**Falsification test:** Compare the next four minor releases with the
previous four on retry, timeout, and error changes, and run the same
fixtures. No increase weakens the ownership-drift story. Either way,
keep the dependency test.

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

**Evidence:** MTRX-W21-EARLY-01

---

**Confidence:** medium
## KPMG, PwC, Gates in five days — build the AI incident playbook before someone asks for it

**What changed.** Three deployment headlines between May 14 and May 19.
The Gates partnership combines $200M in grants, usage credits, and
technical support over four years. PwC announced a rollout across
core functions. KPMG says its 276,000+ employees will gain access;
that is an access commitment, not a count of active users.
[anthropic-kpmg](https://www.anthropic.com/news/anthropic-kpmg) · [gates-foundation-partnership](https://www.anthropic.com/news/gates-foundation-partnership) · [pwc-expanded-partnership](https://www.anthropic.com/news/pwc-expanded-partnership)

**Insight.** A 100k-seat access announcement is a good time to open the incident playbook. Check its date before blaming the Slack rollout.

**Action surface:** workflow

**Concrete moves this week.**

1. If you advise large firms: add an "AI incident" page to your
   runbook. Three sections: model-output incident, data-exposure
   incident, vendor-outage incident. Each one with detect / contain /
   communicate sub-steps.
2. If you sell to large firms: expect more AI-specific security questions. Pre-write the answers to the dozen most common
   questions (data residency, sub-processors, model-isolation, audit
   logging, deletion SLAs) before sales pings you at 5pm Friday.
3. If you build internal tooling that uses Claude/OpenAI: today is a
   good day to audit which workflows lack a kill switch. A workflow
   without a 1-minute kill switch is a workflow that can hold your
   weekend hostage.

```markdown

**Confidence:** medium


## Model-output incident — generated PII in customer-facing channel

### Detect
- Audit query on `messages.create` in last 24h matching:
  - email regex `[\w.-]+@[\w.-]+\.\w+`
  - SSN regex `\d{3}-\d{2}-\d{4}`
- Trigger: review-queue rule + Sentry breadcrumb on output token tag.

### Contain
1. Disable the offending route in the feature flag dashboard.
2. Restrict affected outputs and preserve only authorized incident evidence.
3. Revoke/rotate credentials if compromise or continued access is in scope.

### Communicate
- Legal + comms: <owner and internal escalation deadline>.
- Impacted users/regulators: <counsel-confirmed contractual/legal deadline>.
- Internal post-mortem: <owner, due date, restricted incident link>.
```

One page. Write the playbook now, before there's an incident.

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

**Falsification test:** Run a tabletop against the existing playbook
first. If it already detects, contains, and assigns communication for
the three incident classes within your risk limits, patch only the
gaps. No publicly reported incident tells us little about coverage.

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

**Evidence:** MTRX-W21-EARLY-02

---

**Confidence:** medium
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
   revoking an API key after a customer reports it compromised?" Set a revocation target from your threat model, then test it.
   The minute and 15-minute thresholds below are proposed intake
   targets, not Glasswing findings or universal SLAs.

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
api_key_compromise_sla_seconds: <int>  # proposed target: < 60; approve per risk
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

**Evidence:** MTRX-W21-EARLY-03

---

**Confidence:** medium
## Gemini 3.5 Flash GA — rerun your unit economics this week

**What changed.** Google launched Gemini 3.5 Flash to general availability
and made it the default in the Gemini app and AI Mode in Search.
That app default does not migrate a pinned API route or its contract.
[simonwillison.net coverage](https://simonwillison.net/2026/May/19/gemini-35-flash/)

**Insight.** When the cheap-tier model's price goes up, the customer
math behind your last six months of LLM cost projections is wrong.
Most teams haven't reopened the sheet.

**Action surface:** config

**Concrete moves this week.** Pull last quarter's LLM cost line. Build
the table below for your actual call volume; use dated API or contract rates and separate input from output tokens.
Bill = input millions × input rate + output millions × output rate.

```
route              input $/1M   output $/1M   input M   output M   period bill
current API route  <dated rate> <dated rate>  <logs>    <logs>     I*Ri + O*Ro
Flash 3.5          <dated rate> <dated rate>  <same>    <same>     <compute>
OSS/managed mix    <mix>        <mix>         <same>    <same>     <plus hosting>

+30% volume scenario: bill * 1.30 only if token mix and rates stay fixed.
Include cache, reasoning tokens, retries, tools, and serving costs separately.
```

Three decisions fall out of this table:

1. If Flash 3.5 at +30% growth breaks your gross margin: your default
   model selection has to change before someone notices in a board
   review.
2. If you route on price alone, rerun the comparison at a fixed
   task-quality floor. A higher rate can still buy a cheaper completed task.
3. If your enterprise contract was signed assuming Flash 2.5 unit
   economics, the renewal conversation just got harder. Pre-write the
   talking points.

**Systems map:** A proposed model upgrade changes the rate and may
change the token count. Price both before changing the API route;
the app default is a separate product decision.

**Transferable principle:** A model name is not a unit-cost contract.
Keep the dated rates, token mix, and completed-task denominator
next to the routing decision.

**Falsification test:** Replay a fixed workload on both routes, with
the same acceptance test. If cost per accepted task and latency stay
inside the existing budget, there is no cost case for a reroute.
This is a proposed comparison, not a measured Q2 bill.

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

**Evidence:** MTRX-W21-EARLY-04

---

**Confidence:** medium
## Simon Willison's *Last Six Months in LLMs* — forward to one specific person

**What changed.** Simon published annotated slides from a PyCon US
lightning talk covering November 2025 through May 2026.
[5-minute-llms](https://simonwillison.net/2026/May/19/5-minute-llms/)

**Insight.** Some teammate's AI assumptions froze in Nov 2025, and their decisions cascade onto yours. The vendor shortlist on your desk was built by that mental model.

**Action surface:** workflow

**Concrete move this week.** Forward the link to the two teammates
whose AI assumptions you suspect are six months stale. Schedule 15
minutes on Friday to discuss one slide together. The conversation
prompt you want is:

> "Which of these eight items changed your mental model? Of the ones
> that didn't, what would have to be true for them to?"

The second half does the heavy lifting. It surfaces the unstated
priors that drive their decisions.

**Systems map:** Stale priors in a few teammates cascade through hiring, vendor picks, and tooling.

**Transferable principle:** When a domain's underlying tech base
churns faster than ordinary team-knowledge maintenance, a short
shared review is worth testing against ad-hoc reading.
Same pattern shows up in security teams tracking exploit-class
shifts, finance teams tracking macro-regime shifts, and platform
teams tracking cloud-feature deprecations.

**Falsification test:** Name one pending vendor decision before the
read. Afterward, check which factual assumptions changed and whether
they survive a source check. If the discussion only changes confidence,
keep it as a conversation. A decision-quality claim needs more.

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

**Evidence:** MTRX-W21-EARLY-05

---

**Confidence:** medium
## Three more, in shorter form

**Eugene Yan, *How to Work and Compound with AI*** (May 3). Four
frames — context infrastructure, taste configuration, verification,
delegation. For most builders the one that does the work is **context
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

Pick a decision you've been sitting on because you don't know if AI changes the answer. Write it down, date it, and set a calendar reminder for 30 days from now. The reminder is the only honest part of this exercise.

---

## Postscript: 2026-W21 dream candidates

The week's offline-cognition pass landed alongside this brief. Six
promotion candidates surfaced from the last seven days of commits, the
brief itself, and the CI run history. Three propose memory updates to
`.agents/AGENTS.md`, one proposes a new skill, two propose regression
tests. The candidates are proposals, not patches; each one carries
`human_review_required: true` and waits for a reviewer to pick it up.
Full report at [`dreams/2026-W21/report.md`](../../dreams/2026-W21/report.md).
