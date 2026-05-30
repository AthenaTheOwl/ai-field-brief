# The audience sorts into shapes

**week of 2026-05-11 · audience: builder-tpms thinking about AI · vol. 003**

*Vol. 2 to 3: added systems-thinking treatment per DEC-MTRX-007 —
each Top Signal now carries Systems map, Transferable principle,
Falsification test, and Adoption ladder. No new evidence; the four
fields sharpen what vol. 2 already supported.*

This week the AI customer base started sorting into shapes you can
name. Anthropic shipped Claude for Small Business on Tuesday, signed
PwC and the Gates Foundation on Thursday, and last week's SpaceX
compute deal kept echoing through rate-limit conversations. The
under-20-person shop, the global firm, the multilateral foundation,
and the single developer with five-hour windows are now four
products inside one company. That shape rarely holds for long. The
load-bearing question for builders this week is which shape your
own product is currently selling to.

If you only have time for one move from this brief: write down the
single buyer persona your AI feature ships for today, and the
specific behavior change that persona will make next quarter. The
brittle products this year are the ones that try to span three
shapes at once.

---

## Claude for Small Business — pick the buyer persona your AI feature sells to today

**What changed.** Anthropic launched Claude for Small Business on
May 13. The package wraps Claude with connectors into QuickBooks,
PayPal, HubSpot, Canva, Docusign, Google Workspace, and Microsoft
365, and ships 15 pre-built agentic workflows across finance, sales,
marketing, HR, and customer service. The framing language calls out
payroll forecasting, monthly reconciliation, cash-flow analysis,
campaign management, and contract review by name.
[anthropic.com/news/claude-for-small-business](https://www.anthropic.com/news/claude-for-small-business)

**Insight.** Two days later the company announced PwC and Gates.
The same model now ships in three distinct buyer shapes — the
ten-seat shop with QuickBooks, the 100k-seat firm with a CIO
office, and the foundation underwriting global health work. Most
B2B AI features try to span at least two of these shapes inside one
product page. The page reads as muddled because the buyer behaviors
underneath are different — the small-shop owner toggles a workflow,
the CIO runs a procurement review, the foundation runs a grant
process. One UI cannot land all three.

**Action surface:** prompt, architecture

**Concrete move this week.** Open the page where your AI feature is
sold. Write down the literal sentence the buyer would say to a
peer to recommend it. If the sentence works for both a small-shop
owner and a CIO, the positioning is muddled. Cut the second buyer
from the page. Pick one shape; rewrite the page for that shape;
park the second shape behind a different URL or a sales-led path.

```markdown
# buyer-persona-check.md — fill this in before any AI feature ships

product: <feature name>
target_buyer_shape: [ small-business | enterprise-line-of-business | individual-developer | foundation-grantee ]

the sentence the buyer would say to a peer:
"<one quoted sentence; max 25 words>"

specific behavior change in 90 days:
"<one quoted sentence; concrete and observable>"

what this product is NOT:
- not for: <other shape A>
- not for: <other shape B>
- if asked, redirect to: <other page / sales path>

unit economics fit for this shape:
- ACV: <number>
- support load per seat: <hours/month>
- expansion path: <named>

review_date: 2026-MM-DD
owner: <name>
```

The hard part is the "not for" lines. Most teams cannot bring
themselves to write them. The exercise is worth doing the day after
your competitor ships a feature that looks like yours — that's
when the positioning stretch is most expensive.

**Systems map:** One model surface, three distinct buyer behaviors —
the small-shop owner toggling a workflow, the CIO running a
procurement review, the foundation running a grant process. A single
product page tries to compress three buyer state machines into one
UI, and the compression shows up as muddled positioning.

**Transferable principle:** When one vendor's surface spans
incompatible buyer behaviors, the seller below them must pick one
shape per page or the page reads as muddled. Example beyond AI:
horizontal SaaS dashboards (analytics, CRM) that try to land both
self-serve SMB sign-ups and enterprise procurement on the same
landing page consistently underperform single-shape pages on either
conversion or ACV.

**Falsification test:** The buyer-shape thesis breaks if a product
page that explicitly spans two of the three shapes (small business +
enterprise, with both buyer sentences on the page) shows comparable
or better 90-day pipeline conversion vs a single-shape page in a
controlled A/B over a quarter. That observation would mean the
"single shape per page" rule is rhetoric, not mechanism.

**Adoption ladder:**

  - Minimum viable: fill in `buyer-persona-check.md` for the one
    AI feature you ship today; write the literal buyer sentence and
    the "not for" lines. One page, one owner, one review date.
  - Mid: rewrite the public product page for the chosen shape; park
    the second shape behind a different URL or a sales-led path.
    Add the 90-day behavior-change sentence to internal launch docs.
  - Full: every AI feature in the portfolio carries a buyer-persona
    sheet under version control; sales, marketing, and product
    review the sheets quarterly; new features cannot ship without
    one.
  - Monitoring: page conversion by shape, expansion path utilization
    per shape, inbound support load per seat by shape, share of
    sales calls that get redirected vs progressed.

---

## PwC + Gates in one day — three numbers your security partner will get asked about by July

**What changed.** Two Anthropic announcements landed within hours
of each other on May 14. PwC is deploying Claude across consulting
practices and product teams (the language is "build technology,
execute deals, and reinvent enterprise functions"). Gates is a $200
million, four-year partnership covering global health, education,
and economic mobility, with the largest portion targeted at health
work in low- and middle-income countries.
[pwc-expanded-partnership](https://www.anthropic.com/news/anthropic-pwc-partnership) · [gates-foundation-partnership](https://www.anthropic.com/news/gates-foundation-partnership)

**Insight.** Each headline pulls a different procurement
conversation into your inbox. PwC pulls the supply-chain question
("does our vendor stack include a sub-processor that PwC also
uses?"). Gates pulls the data-residency question ("our partner ships
to LMIC clinics — what data leaves the country?"). Both pull the
same audit-log question ("can we pull every API call our workspace
made last quarter?"). The questions land in three different
inboxes inside your company and converge on one answer your
security partner has to be ready to give.

**Action surface:** tool-policy

**Concrete move this week.** Pre-write the answers to the three
questions below in a one-page security FAQ. The doc lives in your
shared drive, links from your security@ inbox auto-responder, and
saves you a 5pm Friday scramble when sales asks.

```markdown
# ai-vendor-faq.md — pre-written answers to the three questions you will get this quarter

## Q1: Sub-processor list
The current sub-processors for our AI features are:
- <vendor> — <function> — <data-residency region>
- <vendor> — <function> — <data-residency region>
Last reviewed: 2026-MM-DD. Next review: <date + 90 days>.

## Q2: Data-residency
Customer prompts and outputs route to <region>.
EU / India / LMIC routing options: <available | on roadmap | not supported>.
We do NOT train any third-party model on customer data; the contract
clause is at <link to MSA section>.

## Q3: Audit log
Every API call we make on behalf of a customer is logged with:
prompt-hash, model, timestamp, sub-processor, tokens-in, tokens-out.
Retention: <N days>. Customer-pull on demand: yes, via <endpoint>.
Format: NDJSON with one record per call.
```

Three blanks filled in is the difference between a one-day reply
and a one-week scramble. The doc also doubles as the first page of
your next SOC2 narrative section.

**Systems map:** Multiple procurement conversations converging on
one security partner — the supply-chain question from one inbox,
the data-residency question from another, the audit-log question
from a third, all routing to a single response that has to land in
hours, not weeks. Pre-writing the answers turns a three-inbox fan-in
into a one-document fan-out.

**Transferable principle:** When N upstream signals converge on one
responder with shared sub-questions, pre-compute the shared answers
and host them at a stable URL. Example beyond AI vendors: incident
response, where pager rotations from N services hit one on-call
engineer — the answer is a runbook per service plus a shared
"during-incident" FAQ for stakeholder questions (status, ETA,
scope) hosted at a stable status URL.

**Falsification test:** The pre-written-FAQ thesis breaks if teams
with the doc in place still take a full week to answer the three
questions when a real PwC- or Gates-shaped buyer asks, over the next
two quarters. That would mean the bottleneck is review/sign-off,
not lookup, and the artifact to ship is an approval workflow, not
a doc.

**Adoption ladder:**

  - Minimum viable: write three short paragraphs answering the
    sub-processor, data-residency, and audit-log questions; commit
    them to a shared doc; link from the security@ auto-responder.
  - Mid: extend the doc with vendor-by-vendor rows, region-by-region
    routing options, and a worked example of an audit-log pull. Add
    a "last reviewed" date and a 90-day review cadence.
  - Full: the FAQ doubles as the first page of the SOC2 narrative;
    the audit-log endpoint is exposed to customers self-serve;
    sub-processor changes trigger an auto-update with email
    notification to enterprise accounts.
  - Monitoring: median time-to-answer on inbound security
    questionnaires, fraction of questionnaires answered without
    engineering interrupt, count of audit-log pulls per quarter,
    sub-processor changes per quarter.

---

## Simon Willison, *Not so locked in* — write down the one technology decision you are still afraid to revisit

**What changed.** Simon picked up Mitchell Hashimoto's observation
that programming languages used to be lock-in technologies and
increasingly aren't. The post is anchored on a real example: a
company rewrote its iPhone and Android apps to React Native via
coding agents, confident they could revert if the migration soured.
[simonwillison.net/2026/May/14/not-so-locked-in](https://simonwillison.net/2026/May/14/not-so-locked-in/)

**Insight.** Coding-agent productivity changes the math on
reversible architecture choices. The decisions most teams have
been afraid to revisit — language migrations, database swaps,
front-end framework changes — are now closer to two-week experiments
than two-quarter rewrites. The architectural conservatism that made
sense in 2023 is a tax in 2026. The teams that move first to
revisit one of those choices have a one-cycle window before
everyone else does the same calculation.

**Action surface:** architecture

**Concrete move this week.** Write down the one technology
decision your team has been afraid to revisit. Score it on the
table below. If two of the three scores are green, run the spike
this quarter — two weeks, one engineer plus a coding agent, one
specific deliverable. If the answer is no, the table tells you
exactly why, and that's the artifact your CTO needs anyway.

```
decision-to-revisit: <e.g. "move from Django REST to FastAPI">
                                            score    threshold-to-spike
coding-agent fit for the migration          [g/y/r]  green or yellow
production blast-radius if it goes wrong    [g/y/r]  green
team capacity in the next two weeks         [g/y/r]  green or yellow

decision: [run spike | do not run]
spike scope: <one specific deliverable, e.g. "one endpoint migrated
              and load-tested at 2x production volume">
spike owner: <name>
spike review date: <2 weeks out>
rollback path: <one sentence>
```

Two of three green is the threshold because all-green almost never
shows up. The reversibility argument from the post is what makes the
yellow squares acceptable, where they weren't before.

**Systems map:** Coding-agent productivity collapses migration cost,
which moves architecture decisions from the "irreversible bet"
category to the "two-week experiment" category. The architectural
conservatism that priced in 2023's migration cost is a tax once the
cost line shifts; the teams that re-price first get a one-cycle lead
before the market re-prices.

**Transferable principle:** When a tool reduces the cost of reversing
a decision by an order of magnitude, the decision moves up the
reversibility ladder and the conservatism that priced the old cost
becomes a tax. Example beyond language migrations: feature flags
moved A/B testing from a quarter-long release decision to a same-day
experiment, and teams that kept treating launches as one-way doors
underperformed teams that started running 10x more experiments per
quarter.

**Falsification test:** The reversibility thesis breaks if teams
running coding-agent migration spikes report median time-to-revert
(once they decide to revert) exceeding the time they would have spent
on the original migration without an agent. That would mean the
forward-pass speed-up is offset by hidden rework cost on the reverse
pass, and the spike framing fails to de-risk the decision once you
sum forward and reverse cost.

**Adoption ladder:**

  - Minimum viable: write down the one decision your team has been
    afraid to revisit and score it on the three-axis table. If two
    of three are green, you have an artifact; if not, you have the
    explanation your CTO wanted anyway.
  - Mid: run the two-week spike with one engineer plus a coding
    agent against one specific deliverable. Document the rollback
    path before the spike starts. Review at the two-week date.
  - Full: every architecture decision over a defined size carries a
    "revisit cadence" line; the spike framing becomes the default
    way to retire 2023-era conservatism across the stack.
  - Monitoring: number of spikes initiated per quarter, fraction
    that ship vs revert, median spike duration vs estimate, dollar
    impact of each shipped spike at the 90-day mark.

---

## SpaceX compute deal — re-rank your inference vendors before the quarter closes

**What changed.** Last week (May 6) Anthropic announced an
agreement to take all the compute at xAI's Colossus 1 facility:
"more than 300 megawatts of new capacity (over 220,000 NVIDIA GPUs)
within the month." The same announcement doubled Claude Code rate
limits for Pro/Max/Team/Enterprise and removed peak-hour
restrictions. The capacity deal stacks on top of the Amazon (5GW),
Google + Broadcom (5GW), and Microsoft/NVIDIA Azure ($30B)
commitments already in place.
[higher-limits-spacex](https://www.anthropic.com/news/higher-limits-spacex)

**Insight.** Capacity expansions arrive at the user as rate-limit
expansions. Last six months of vendor selection assumed scarcity:
queues at peak hours, hard daily caps on Opus calls, "Claude Code is
slow on Wednesday afternoons" tickets. That scarcity is dissolving
for Anthropic at the same time multiple OSS-on-cloud paths are
maturing. The team that benchmarked vendors in November and
shipped a routing decision in January is now ranking by stale data.

**Action surface:** runtime-adapter

**Concrete move this week.** Re-rank your inference vendors on
the four-axis table below. The exercise takes 90 minutes if you
have your last quarter's traffic logs handy.

```
                   latency-p95    cost/1M out    rate-limit-headroom    quality-on-task
                   (ms)           ($)            (current vs Q2 need)   (eval score)
Claude Opus 4.7    <fill>         <fill>         <fill>                 <fill>
Claude Sonnet 4.7  <fill>         <fill>         <fill>                 <fill>
GPT-5.x            <fill>         <fill>         <fill>                 <fill>
Gemini Flash 3.5   <fill>         <fill>         <fill>                 <fill>
Llama-3.3-70B OSS  <fill>         <fill>         <fill>                 <fill>

primary route:     <model>
fallback route:    <model + condition>
escape hatch:      <model + circuit-breaker rule>
re-rank cadence:   monthly  | <date>
```

Two outputs from this exercise change your week. First, the
routing decision your team has been carrying for six months may now
be the wrong one. Second, the table itself becomes the artifact
your finance partner asks for when the AWS or GCP bill spikes
next month — which it will.

**Systems map:** Vendor selection is a function of the capacity
landscape at the time the decision was made. When upstream capacity
expands (Colossus 1, Amazon 5GW, Google + Broadcom 5GW,
Microsoft/NVIDIA $30B), the rate-limit, latency, and cost
assumptions baked into a six-month-old routing decision become stale
data — and the older the routing decision, the larger the gap.

**Transferable principle:** When upstream supply curves shift fast,
downstream selection criteria must be re-evaluated on a cadence
shorter than the shift interval, or the cached decision drifts
arbitrarily far from optimal. Example beyond LLM inference: cloud
region selection during a major provider's regional buildout — teams
that locked in us-east-1 in 2018 paid latency and capacity tax for
years vs teams that ran a quarterly region-selection review.

**Falsification test:** The re-rank thesis breaks if a team that
re-runs the four-axis table monthly produces the same primary route
for four consecutive quarters with no measurable cost or latency
improvement vs a team that re-ran it once at the start. That would
mean the capacity landscape is more stable than the SpaceX headline
suggests and the re-rank cadence is overhead, not signal.

**Adoption ladder:**

  - Minimum viable: 90 minutes with last quarter's traffic logs and
    the four-axis table. Fill in latency-p95, cost/1M out,
    rate-limit headroom, and quality-on-task for your current
    vendor set. Pick a primary route, a fallback, and an escape
    hatch.
  - Mid: instrument production with a routing-decision log so the
    re-rank is data-driven, not anecdotal. Run the exercise monthly.
    Add an OSS-on-cloud row to widen the option set.
  - Full: a routing service in production with circuit-breakers per
    vendor, a finance dashboard tied to the same vendor labels, and
    a documented procurement playbook that names the re-rank cadence
    and the threshold for switching primary routes.
  - Monitoring: monthly per-vendor cost per 1M output tokens,
    rate-limit hit rate, P95 latency by route, eval-score by route,
    monthly inference bill variance vs the cap.

---

## Hamel Husain, *Revenge of the Data Scientist* — pick one LLM judge and validate it as a classifier this week

**What changed.** Hamel's late-March post argues that the eval
discipline most teams ship is unscientific in the literal sense:
LLM judges deployed without train/dev/test splits, vague
helpfulness scores in place of task-specific metrics, no precision
or recall reporting. The fix is to treat every LLM judge as a
classifier that needs validation against human labels.
[hamel.dev/blog/posts/revenge](https://hamel.dev/blog/posts/revenge/)

**Insight.** The post predates this week, but the week's events
make it newly load-bearing. Three new buyer shapes (small business,
PwC-scale enterprise, foundation) means three new audit pressures
on the eval pipeline. None of those buyers will accept "we use
GPT-4 to judge helpfulness on a 1-5 scale" as an answer to "how do
you know the model output is correct?" The judge has to be a
classifier the buyer can interrogate.

**Action surface:** eval

**Concrete move this week.** Pick one LLM judge already running
in your stack. Label 50 historical responses by hand. Compute
precision and recall against the judge's verdict. The judge prompt
below is a starting point; the labeling pass is the part that
matters.

```python
# eval/validate_judge.py — run this against 50 labeled samples
# from your last 30 days of production traffic.

import json
from collections import Counter

# 1. Hand-labeled gold set (you sit down for 90 minutes and label).
gold = [
    {"id": "r-001", "label": "fail", "reason": "hallucinated date"},
    {"id": "r-002", "label": "pass", "reason": "answered the question"},
    # ... 48 more
]

# 2. Run your existing judge against the same 50 responses.
judge_verdicts = [run_judge(r["id"]) for r in gold]

# 3. Confusion matrix.
tp = sum(1 for g, j in zip(gold, judge_verdicts)
         if g["label"] == "pass" and j["verdict"] == "pass")
fp = sum(1 for g, j in zip(gold, judge_verdicts)
         if g["label"] == "fail" and j["verdict"] == "pass")
fn = sum(1 for g, j in zip(gold, judge_verdicts)
         if g["label"] == "pass" and j["verdict"] == "fail")

precision = tp / (tp + fp) if (tp + fp) else 0
recall    = tp / (tp + fn) if (tp + fn) else 0

print(json.dumps({"precision": precision, "recall": recall}, indent=2))

# 4. If precision < 0.85 or recall < 0.85, the judge prompt needs
#    work before it can gate releases. Common failure modes:
#    - judge over-favors verbose answers (precision drop)
#    - judge under-flags hallucination (recall drop on "fail" class)
```

The 50-sample pass is one afternoon. The output is the
spreadsheet you hand your security partner when the question
arrives — which, on the timeline implied by the W20 news, lands
some time in July.

**Systems map:** An LLM judge is a classifier whether or not the
team treats it as one. Skipping train/dev/test splits and
precision/recall reporting does not make the judge less of a
classifier; it makes its error rate undocumented. Three new buyer
shapes (small business, enterprise, foundation) are three new
auditors who will ask for the documented number.

**Transferable principle:** Any decision-maker priced in human
authority that gets delegated to an automated component must be
validated against ground truth on a labeled set, or its error rate
becomes load-bearing-and-unknown. Example beyond LLM judges: rule
engines for fraud detection — a hand-coded rule that flags 2% of
transactions still needs a labeled holdout to report precision and
recall, or downstream chargeback rates surprise the team months
later.

**Falsification test:** The judge-as-classifier thesis breaks if a
team that runs the 50-sample labeling pass and reports precision
and recall to a procurement buyer gets the same procurement outcome
as a team that ships a "we use GPT-4 to score helpfulness 1-5"
answer, across a sample of 10+ enterprise sales cycles over the
next two quarters. That would mean buyers are not asking the
classifier question on the timeline implied here, and the eval
discipline is internal-quality work, not procurement work.

**Adoption ladder:**

  - Minimum viable: pick one LLM judge in production; sit down for
    90 minutes; hand-label 50 historical responses; compute
    precision and recall against the judge's verdict; write the
    two numbers in a doc.
  - Mid: extend the labeled set to 200+; split into train/dev/test;
    track precision and recall per class (pass/fail) over time; gate
    releases on a precision-and-recall floor, not a vibe score.
  - Full: every judge in the stack carries a maintained labeled
    set, a per-release precision/recall report, and a documented
    update cadence. The eval pipeline becomes a buyer-facing
    artifact in security and procurement reviews.
  - Monitoring: precision and recall per judge per release,
    labeled-set drift (re-label rate per quarter), buyer questions
    answered with the eval report vs deferred to engineering,
    release-gate hit rate.

---

## Worth your time

**Simon Willison, *LLM in a shebang line*** (May 11). A short TIL
on running prompts as executable scripts via
`#!/usr/bin/env -S llm -f`. The artifact is small; the move
underneath — treating prompts as version-controlled, runnable
files instead of console paste — is the move. Pick one prompt
your team currently runs by hand each week and turn it into a
shebang script in your dotfiles repo. The next person who needs
to run it gets a `git pull` and a path, not a Slack thread.
[til.simonwillison.net/llms/llm-shebang](https://til.simonwillison.net/llms/llm-shebang)

**Tobi Lütke on Shopify's River agent** (May 11, via Simon). River
runs publicly on Slack inside Shopify so the rest of the company
learns by watching it work — Tobi calls it "osmosis learning."
The concrete artifact you can copy is the channel itself. Pick one
internal AI workflow your team runs, dedicate a Slack channel to
its outputs, and let anyone watch. Reading other people's prompts
in flight is the cheapest training your team will get this year.

**Simon Willison, *Welcome to the Datasette blog*** (May 13). A
new official Datasette blog, built with OpenAI Codex as the
constructor. Worth a five-minute read for the meta point: when a
maintainer of a 23-year-old personal stack ships a new public
surface with a coding agent as co-author, the bar for "I should
write this up" just dropped. If you've been sitting on a writeup
for two months, this is the week to ship the rough draft.
[simonwillison.net/2026/May/13/welcome-to-the-datasette-blog](https://simonwillison.net/2026/May/13/welcome-to-the-datasette-blog/)

---

## Questions to ask in the next 30 days

- **Of your product partner:** "Which of the three buyer shapes
  (small business, line-of-business enterprise, individual
  developer) does our AI feature primarily sell to?" If the answer
  is "all of them," the page is muddled — see the first pick.
- **Of your security partner:** "How fast can we answer the three
  questions in the pre-written FAQ for a customer asking on a
  Friday afternoon?" Anything over four hours is the gap to close
  this quarter.
- **Of your finance partner:** "When did we last rebuild the
  per-vendor cost table for inference?" If the answer is older
  than 60 days, the SpaceX-capacity move from earlier is the
  trigger to rebuild.

---

## Closing thought

The most useful sentence to write down this week is the one that
names the buyer your AI feature sells to. Most product pages
flinch at writing it. The flinch is the work — the sentence is the
artifact.
