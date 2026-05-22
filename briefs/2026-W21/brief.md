# Contract speed, not model speed

**week of 2026-05-18 · audience: builder-tpms thinking about AI · vol. 001**

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

**Concrete move this week.** Forward the link to the two teammates
whose AI assumptions you suspect are six months stale. Schedule 15
minutes on Friday to discuss one slide together. The conversation
prompt you want is:

> "Which of these eight items changed your mental model? Of the ones
> that didn't, what would have to be true for them to?"

The second half does the heavy lifting. It surfaces the unstated
priors that drive their decisions.

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

**Simon Willison, *Datasette Agent*** (May 21). Three years of work on
the `llm` library, finally merged with Datasette. The artifact is
small next to the time horizon — Simon's personal infra has compounded
for 23 years, which Karpathy publicly flagged this week. Most readers
can't copy the path. The discipline behind it is the part that
travels: pick one personal tool you intend to own for the next five
years, and treat the upkeep as a non-negotiable monthly hour.
[simonwillison.net/2026/May/21/datasette-agent](https://simonwillison.net/2026/May/21/datasette-agent/)

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
