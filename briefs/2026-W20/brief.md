# Anthropic sold the same model to four kinds of buyer

**week of 2026-05-11 · audience: builder-tpms thinking about AI · vol. 003**

*Vol. 2 to 3: added systems-thinking treatment per DEC-MTRX-007 —
each Top Signal now carries Systems map, Transferable principle,
Falsification test, and Adoption ladder. No new evidence; the four
fields sharpen what vol. 2 already supported.*

Wednesday: Claude for Small Business. Thursday: PwC and the Gates Foundation. Still echoing from last week: the SpaceX compute deal. Four kinds of buyer across the announcements. Pick which one your feature is for.

Write down the buyer persona your AI feature ships for today. Write down the behavior change you expect from that persona next quarter.

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

**Insight.** PwC and Gates landed the day after the small-business launch. Same model, three buyers: a ten-seat QuickBooks shop, a large-firm CIO office, Gates. One product page cannot honestly sell to a ten-seat shop, a CIO, and a foundation at the same time.

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
a SaaS dashboard selling both self-serve sign-ups and enterprise
procurement can test separate pages. Keep traffic mix and acquisition
cost comparable; a different ACV alone does not settle the page question.

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

**Evidence:** MTRX-W20-EARLY-01

---

**Confidence:** medium
## PwC + Gates in one day — three questions to prepare for your security partner

**What changed.** Two Anthropic announcements landed within hours
of each other on May 14. PwC is deploying Claude across consulting
practices and product teams (the language is "build technology,
execute deals, and reinvent enterprise functions"). The Gates partnership combines $200
million in grants, Claude usage credits, and technical support over four years covering global health, education,
and economic mobility, with the largest portion targeted at health
work in low- and middle-income countries.
[pwc-expanded-partnership](https://www.anthropic.com/news/pwc-expanded-partnership) · [gates-foundation-partnership](https://www.anthropic.com/news/gates-foundation-partnership)

**Insight.** Three questions to put to your security partner. PwC: does our vendor stack include a sub-processor PwC also uses? Gates: our partner ships to LMIC clinics — what data leaves the country? Both: can we pull every API call our workspace made last quarter? Pre-write the answers before they ask.

**Action surface:** tool-policy

**Concrete move this week.** Pre-write the answers to the three
questions below in a one-page security FAQ. The doc lives in your
shared drive, links from your security@ inbox auto-responder, and
saves you a 5pm Friday scramble when sales asks.

```markdown
# ai-vendor-faq.md — pre-written answers to the three questions to check this quarter

## Q1: Sub-processor list
The current sub-processors for our AI features are:
- <vendor> — <function> — <data-residency region>
- <vendor> — <function> — <data-residency region>
Last reviewed: 2026-MM-DD. Next review: <date + 90 days>.

## Q2: Data-residency
Customer prompts and outputs route to <region>.
EU / India / LMIC routing options: <available | on roadmap | not supported>.
Use for model training: <yes/no; scope and contract clause>.
Use for evals or red-teaming: <yes/no; scope and contract clause>.

## Q3: Audit log
Available log fields: <verified fields and any gaps>.
Retention: <N days>. Customer-pull on demand: <yes/no; endpoint>.
Export format: <format>. Do not put raw customer prompts in a public FAQ.
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

**Evidence:** MTRX-W20-EARLY-02

---

**Confidence:** medium
## Simon Willison, *Not so locked in* — write down the one technology decision you are still afraid to revisit

**What changed.** Simon picked up Mitchell Hashimoto's observation
that programming languages used to be lock-in technologies and
increasingly aren't. The post is anchored on a real example: a
company rewrote its iPhone and Android apps to React Native via
coding agents, confident they could revert if the migration soured.
[simonwillison.net/2026/May/14/not-so-locked-in](https://simonwillison.net/2026/May/14/not-so-locked-in/)

**Insight.** The anecdote makes one old decision worth reopening.
It does not measure a migration or a revert. Try a two-week spike
on one endpoint before pricing the whole database swap as a two-week job.

**Action surface:** architecture

**Concrete move this week.** Write down the one technology
decision your team has been afraid to revisit. Score it on the
table below. If blast radius is green, neither other score is red, and at least two are green, run the spike
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

These are proposed spike gates, not results from the post. A green
coding-agent score cannot cancel a red production blast radius.

**Systems map:** Faster code changes may lower migration cost. Data
conversion, operational behavior, and rollback still need their own
checks. The spike buys a cost estimate before the migration buys an outage.

**Transferable principle:** Reprice a decision when the cost of
reversing it changes. Measure the return trip too. A feature flag can
reverse exposure; it cannot reverse a destructive data migration.

**Falsification test:** The reversibility thesis breaks if teams
running coding-agent migration spikes report median time-to-revert
(once they decide to revert) exceeding the time they would have spent
on the original migration without an agent. That would mean the
forward-pass speed-up is offset by hidden rework cost on the reverse
pass, and the spike framing fails to de-risk the decision once you
sum forward and reverse cost.

**Adoption ladder:**

  - Minimum viable: write down the one decision your team has been
    afraid to revisit and score it on the three-axis table. If the blast-radius gate passes, you have a candidate spike; if not, you have the
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

**Evidence:** MTRX-W20-EARLY-03

---

**Confidence:** medium
## SpaceX compute deal — re-rank your inference vendors before the quarter closes

**What changed.** Last week (May 6) Anthropic announced an
agreement to take all the compute at xAI's Colossus 1 facility:
"more than 300 megawatts of new capacity (over 220,000 NVIDIA GPUs)
within the month." The same announcement doubled Claude Code rate
five-hour limits for Pro/Max/Team/seat-based Enterprise and removed
peak-hour reductions for Pro and Max. The deal joins future commitments:
Amazon up to 5GW, Google + Broadcom 5GW starting in 2027, and
Microsoft/NVIDIA Azure capacity worth $30B. Those are different
delivery schedules, not capacity already switched on.
[higher-limits-spacex](https://www.anthropic.com/news/higher-limits-spacex)

**Insight.** Capacity expansions arrive at the user as rate-limit
expansions. Last six months of vendor selection assumed scarcity:
queues at peak hours, hard daily caps on Opus calls, "Claude Code is
slow on Wednesday afternoons" tickets. The announced headroom is a reason to retest scarcity
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
Current Claude route    <fill>         <fill>         <fill>                 <fill>
Alternate Claude route  <fill>         <fill>         <fill>                 <fill>
Current GPT route            <fill>         <fill>         <fill>                 <fill>
Current Gemini route   <fill>         <fill>         <fill>                 <fill>
Llama-3.3-70B OSS  <fill>         <fill>         <fill>                 <fill>

primary route:     <model>
fallback route:    <model + condition>
escape hatch:      <model + circuit-breaker rule>
re-rank cadence:   monthly  | <date>
```

The routing decision may now be wrong, and finance will want the table when the cloud bill spikes.

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

**Falsification test:** On the same task mix and quality floor, compare
the proposed route with the current route, including switching and
review cost. If the savings and headroom do not cover that cost, keep
the route and lengthen the review interval. The same winner can still
get cheaper; an unchanged vendor name alone proves nothing.

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

**Evidence:** MTRX-W20-EARLY-04

---

**Confidence:** medium
## Hamel Husain, *Revenge of the Data Scientist* — pick one LLM judge and validate it as a classifier this week

**What changed.** Hamel's late-March post argues that the eval
discipline most teams ship is unscientific in the literal sense:
LLM judges deployed without train/dev/test splits, vague
helpfulness scores in place of task-specific metrics, no precision
or recall reporting. The fix is to treat every LLM judge as a
classifier that needs validation against human labels.
[hamel.dev/blog/posts/revenge](https://hamel.dev/blog/posts/revenge/)

**Insight.** A buyer may ask how you know the output is correct.
A score of 4/5 from another model does not answer that by itself.
Validate the judge before handing its score to procurement.

**Action surface:** eval

**Concrete move this week.** Pick one LLM judge already running
in your stack. Start with 50 historical responses by hand. Compute
precision and recall against the judge's verdict. The judge prompt
below is a diagnostic, not a release certificate. Keep a separate
held-out set once you start tuning the judge.

```python
# eval/validate_judge.py — run this against 50 labeled samples
# from your last 30 days of production traffic.

import json

# 1. Hand-labeled gold set (you sit down for 90 minutes and label).
gold = [
    {"id": "r-001", "label": "fail", "reason": "hallucinated date"},
    {"id": "r-002", "label": "pass", "reason": "answered the question"},
    # ... 48 more
]

# 2. Run your existing judge against the same 50 responses.
judge_verdicts = [run_judge(r["id"]) for r in gold]

# 3. Confusion matrix: "pass" is the positive class.
tp = sum(1 for g, j in zip(gold, judge_verdicts)
         if g["label"] == "pass" and j["verdict"] == "pass")
fp = sum(1 for g, j in zip(gold, judge_verdicts)
         if g["label"] == "fail" and j["verdict"] == "pass")
fn = sum(1 for g, j in zip(gold, judge_verdicts)
         if g["label"] == "pass" and j["verdict"] == "fail")

precision = tp / (tp + fp) if (tp + fp) else None
recall    = tp / (tp + fn) if (tp + fn) else None

print(json.dumps({"positive_class": "pass", "tp": tp, "fp": fp, "fn": fn,
                  "precision": precision, "recall": recall}, indent=2))

# 4. Set release thresholds from the cost of false passes/blocks.
#    Missing hallucinations raises fp and lowers pass precision.
#    Also report fail-class recall: the fraction of real failures caught.
#    A zero denominator is undefined (None), not a measured score of zero.
```

The first pass fits an afternoon. Rare failures need more examples
and uncertainty bounds before a release gate. Keep the spreadsheet;
the security partner can ask for the denominator too.

**Systems map:** An LLM judge is a classifier whether or not the
team treats it as one. Skipping train/dev/test splits and
precision/recall reporting does not make the judge less of a
classifier; it makes its error rate undocumented. A procurement review is another place the undocumented number can
become awkward.

**Transferable principle:** Any decision-maker priced in human
authority that gets delegated to an automated component must be
validated against ground truth on a labeled set, or its error rate
becomes structurally important and unknown. Example beyond LLM judges: rule
engines for fraud detection — a hand-coded rule that flags 2% of
transactions still needs a labeled holdout to report precision and
recall, or downstream chargeback rates surprise the team months
later.

**Falsification test:** Compare the judge with a cheap rule baseline
on held-out human labels. If it catches no more real failures at the
same false-block rate, do not pay for it as a release gate. Track
buyer questions separately; winning a sale does not validate a classifier.

**Adoption ladder:**

  - Minimum viable: pick one LLM judge in production; sit down for
    90 minutes; hand-label 50 historical responses; compute
    precision and recall against the judge's verdict; write the
    two numbers and their denominators in a doc; mark this a pilot.
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

**Evidence:** MTRX-W20-EARLY-05

---

**Confidence:** medium
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

Write the sentence that names your buyer; most product pages won't.
