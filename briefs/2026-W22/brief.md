# The agents outran the humans downstream

**week of 2026-05-25 · audience: builder-tpms thinking about AI · vol. 003**

Two stories from this week share a pattern that took a year to arrive.
Anthropic's first Project Glasswing update reports 10,000+ high- or
critical-severity vulnerabilities found by Claude Mythos Preview across
50 partner codebases in one month — and open-source maintainers have
asked Anthropic to slow the disclosure pace because they can't patch
fast enough. OpenAI shipped Codex Locked Use, which keeps a coding
agent operating on a Mac after the user locks the screen. The two
items aren't the same story, but they rhyme. The agent's output rate
has crossed the threshold where the human review loop downstream is
the bottleneck, and the operating questions for the rest of 2026 are
about that downstream — patch capacity, review queues, audit logs,
the humans who have to decide what to do with what the agent
produced.

If you only have time for one move from this brief: pull a list of
every place in your stack where an AI agent currently writes to a
queue (PRs, alerts, draft messages, tickets) and put a real number
next to the human review capacity that absorbs each queue. The
mismatch is the work for Q3.

---

## Project Glasswing 10,000-bug update — write a "queue overflow" policy this week

**What changed.** Anthropic published the first progress report on
Project Glasswing on May 22. About 50 trusted partners (AWS,
Cloudflare, Apple, JPMorgan, the Linux Foundation, others) got early
access to Claude Mythos Preview. In one month they collectively
identified more than 10,000 high- or critical-severity vulnerabilities
across systemically-important codebases. Cloudflare alone reports
2,000 bugs found, 400 high/critical, false-positive rate the team
considers better than human testers. Average patch time for a
critical bug surfaced this way: two weeks. Some open-source
maintainers have asked Anthropic to slow disclosure because the
patching pipeline can't keep up.
[anthropic.com/research/glasswing-initial-update](https://www.anthropic.com/research/glasswing-initial-update)

**Insight.** A vulnerability discovery rate that exceeds patching
capacity is a new operating condition for the security industry. The
1990s and 2000s ran the other way — bugs were rare, patches were
ready before the disclosure. For most of the last decade, the
constraint moved to disclosure coordination. Now the constraint is
patcher hours. The same shape will show up next quarter in any
workflow where an AI agent produces work items faster than humans
review them: customer-support tickets, code-review queues,
compliance flags, sales-call follow-ups. The work for builders this
quarter is to find those queues before they back up.

**Concrete move this week.** Pull a list of every queue an AI agent
writes to in your stack. For each one, fill the table below with two
real numbers: the agent's output rate and the human absorption rate
in the same unit. Anywhere the ratio exceeds 1.5x, write a queue
overflow policy before someone files the first complaint.

```
queue:                              agent output rate    human review rate    ratio    policy
AI-drafted PR comments              48/wk                20/wk                2.4x     batch + judge filter
LLM-flagged customer issues         210/day              90/day               2.3x     severity gate
auto-generated test cases           500/run              n/a (CI absorbs)     n/a      —
agent-written meeting summaries     35/day               unread by 60%        n/a      opt-in only
draft sales follow-ups              80/day               25/day               3.2x     human approval required
agent-found security findings       12/wk                4/wk                 3.0x     triage-bot first pass
```

Three concrete policy moves that take a ratio above 1.5x back down:

1. **Severity gate.** Drop everything below high; require explicit
   reviewer opt-in to see medium.
2. **Triage-bot first pass.** A small judge model groups, dedupes,
   and ranks before the human queue.
3. **Slow-mode flag.** The agent waits for queue depth to drop below
   N before producing more. This is the move the Glasswing
   maintainers asked Anthropic for.

The queue-overflow policy is one page. It belongs in your runbook
the week before the queue overflows, not the week after.

---

## Codex Locked Use — write the "long-running agent" charter your security partner will ask for

**What changed.** OpenAI shipped Codex Locked Use on May 21. With the
toggle on, an Apple authorization plug-in temporarily unlocks the Mac
while Codex runs Computer Use turns, then re-locks on local input.
Scopes are short-lived, the display stays covered, local typing
breaks the session. Unavailable in EEA, UK, and Switzerland at
launch.
[macworld coverage](https://www.macworld.com/article/3147024/openai-codex-can-now-run-with-locked-macbooks.html) · [developers.openai.com/codex/changelog](https://developers.openai.com/codex/changelog)

**Insight.** The product question Codex answered this week is "how
do you run a coding agent for six hours on a real GUI app you can't
script?" The answer is: keep the Mac unlocked behind the lock screen,
strictly scoped to the active turn. The security question that
follows is the one every CISO will ask next month: which long-running
agents in your stack hold credentials or session state across a
locked screen? The current honest answer for most teams is "I don't
know, let me check," because the controls weren't there until this
week.

**Concrete move this week.** Write a one-page long-running agent
charter that any team can use as the answer to "what is this agent
allowed to do while I'm offline?"

```markdown
# long-running-agent-charter.md — fill in per agent

agent_name: <name>
runs_in: [local-desktop | hosted-vm | ci-runner | mobile]
maximum_session_duration: <hours>
allowed_credentials:
  - read-only github token (scopes: <list>)
  - <other>
disallowed_credentials:
  - production database write access
  - billing / payments API keys
  - shared service-account tokens (require per-run rotation)
network_egress:
  - allowlisted hosts: <list>
  - block-by-default for: payments, identity provider
human_in_loop_triggers:
  - cost over $<N> per turn
  - file change in <protected paths>
  - any write to: prod database, github main branch, slack #public
audit_log_retention: <days>
kill_switch_path: <one-line how to halt this agent in 60 seconds>
review_cadence: monthly
owner: <name>
review_date: 2026-MM-DD
```

The charter forces three questions that are awkward to answer in the
abstract and concrete enough to act on per-agent. If you can't fill
in the kill-switch line in one sentence, that's the work for the
week.

---

## Anthropic widens the conversation — pick the two outside readers your AGENTS.md is missing

**What changed.** Anthropic published a piece on May 19 describing
dialogues with scholars, philosophers, clergy, and ethicists on the
formation of character in AI systems. The research artifact tucked
inside the post: Anthropic experimented with a tool Claude could call
mid-task that returned a brief reminder of its own ethical
commitments. The model reached for the tool right before consequential
actions, often flagging its own conflict of interest. Internal
alignment evaluations showed lower rates of misaligned behavior with
the tool in the decision loop.
[anthropic.com/news/widening-conversation-ai](https://www.anthropic.com/news/widening-conversation-ai)

**Insight.** Two threads worth pulling. First, the mid-task ethics
reminder is an architectural pattern any team can copy — a
self-callable tool that returns the agent's own constraints, used at
decision points. Second, the research method (engaging with readers
outside the AI subculture as a way to surface decisions a homogeneous
team would miss) maps onto something most builders already have but
underuse: the AGENTS.md or CLAUDE.md at the root of the repo. Most
versions are written by and for engineers. The two outside readers
who'd most improve it are the ones already on your team — finance and
legal — but their input rarely lands in the file.

**Concrete move this week.** Add two sections to your repo's
AGENTS.md (or create one if missing). Source the content from two
30-minute conversations with the two readers above.

```markdown
# Finance constraints (sourced from <name>, finance partner)
- Maximum unattended-run cost per agent session: $<N>.
- Any agent action with billing-API impact requires a human approve step.
- Monthly review of agent-driven cost line items; owner: <name>.
- The agent must not call APIs that incur per-request infra cost
  unless the request is in our cached allowlist.

# Legal / compliance constraints (sourced from <name>, legal)
- The agent must not draft outbound customer email without a human
  review step.
- Personal data classes the agent may not see: <list>.
- Records-retention obligations the agent must respect: <list>.
- Counsel-privilege boundary: the agent never writes to channels
  tagged #legal-* or summarizes content from them.

# Self-check pattern (from Anthropic's mid-task ethics-reminder result)
- The agent may call `ethics_check(action: str) -> str` before any
  consequential action. The tool returns this file's most relevant
  paragraph. Used at decision points; logged for audit.
```

The two outside-reader paragraphs are worth more than 100 lines of
engineering convention. The constraints they name are the ones
that get an agent in trouble; the engineering conventions are the
ones that get a PR rejected.

---

## KPMG Digital Gateway Powered by Claude — write your "consultancy-grade audit-log" answer this quarter

**What changed.** KPMG and Anthropic announced a global alliance on
May 19 launching KPMG Digital Gateway Powered by Claude. Scope:
276,000+ KPMG workforce on Claude; Tax & Legal first, expanding to
broader advisory; full implementation on Microsoft Azure by September
2026; Claude embedded in Digital Gateway so KPMG clients can build
agentic workflows directly. Anthropic names KPMG a preferred partner
for private equity.
[anthropic.com/news/anthropic-kpmg](https://www.anthropic.com/news/anthropic-kpmg) · [kpmg press release](https://kpmg.com/xx/en/media/press-releases/2026/05/kpmg-and-anthropic-sign-global-alliance-and-launch-digital-gateway-powered-by-claude.html)

**Insight.** This is the third consultancy headline in five weeks
(PwC W20, then Gates, now KPMG). The pattern is no longer
deployment-of-AI; it's AI as the delivery surface a consultancy resells
to its own clients. The audit-log question becomes second-order: when
KPMG runs a Claude-powered workflow on behalf of your portfolio
company, three audit logs exist — Anthropic's, KPMG's, and the
portfolio company's. The three rarely line up. The procurement
question your security partner has to answer this quarter is which
log governs when they disagree, and how fast a customer can get all
three pulled in a regulator-shaped event.

**Concrete move this week.** If you sell into firms that resell
AI-powered workflows (PE, consultancy, accounting, legal), add a
"reseller-audit" row to your security questionnaire. If you buy from
those firms, ask the four questions below.

```yaml
# reseller-audit-questions.yaml — drop into vendor review for any
# consultancy-resold AI workflow

vendor: <name>
review_date: 2026-MM-DD

audit_logs:
  vendor_log_pull_sla_hours: <int>       # vendor's own log
  reseller_log_pull_sla_hours: <int>     # consultancy's log
  upstream_provider_log_pull_sla_hours: <int>  # Anthropic / OpenAI / Google
  reconciliation_process: <named procedure or 'none documented'>

incident_path:
  who_calls_who_first: <vendor | reseller | upstream>
  customer_notification_sla_hours: <int>
  customer_can_request_all_three_logs: yes | no

data_flow:
  customer_data_visible_to_reseller: yes | no
  customer_data_visible_to_upstream_provider: yes | no
  training_carve_out_in_contract: yes | no  # required: yes

private_equity_carve_out:                # specific to KPMG-style PE work
  portfolio_company_data_segregation: yes | no
  cross_portfolio_use_blocked: yes | no  # required: yes
```

The four-question test catches the gap that opens up when a
consultancy resells an AI workflow. If any answer comes back as "no
documented procedure," it is the gap.

---

## OpenAI Deployment Company — re-read your "build vs partner" memo

**What changed.** OpenAI launched the OpenAI Deployment Company,
framed as an organization that helps businesses build and deploy AI
systems for their most important work. The framing is closer to a
consultancy than a sales team.
[openai.com/index/openai-launches-the-deployment-company](https://openai.com/index/openai-launches-the-deployment-company/)

**Insight.** Read alongside the KPMG news, this is the same week
where the two largest model labs both moved up the value chain into
white-glove deployment work. The product position OpenAI is staking is
"we'll send people, not just SDKs." For most builders the live
question this week: will the lab you depend on become your competitor
for white-glove deployment work inside your largest accounts? The build-vs-partner memo most teams
wrote in 2024 was about whether to build a model. The same memo in
2026 is about whether to build the deployment surface, and whether
your lab vendor will resell against you.

**Concrete move this week.** Pull the build-vs-partner memo your
team wrote at any point in the last two years. Re-score the four
rows below honestly. If two of four flipped, the memo needs a
rewrite this quarter.

```
                                            2024 score    2026 score
the lab will compete with us on deployment   no            <fill>
the lab will sell our buyer directly         no            <fill>
the lab's price reflects scarcity            yes           <fill>
our SLA depends on the lab's roadmap         partly        <fill>
```

Two flipped scores is the threshold for a fresh memo. One flipped is
worth a 30-minute conversation. Zero flipped is worth a sanity check
on whether the team is looking.

---

## Worth your time

**Simon Willison, *Datasette-Agent 0.1a4 + Datasette 1.0a30*** (May
24). Two coupled releases. Datasette 1.0a30 adds a `/`-triggered
"Jump to..." menu and exposes a new `jump_items_sql()` plugin hook so
extensions can register their own searchable items. Datasette-Agent
0.1a4 ships a "Start a new agent chat" entry that uses the hook. The
small-platform pattern worth copying: ship a plugin hook in the
platform release, then ship the first plugin that uses it in the
next release. The hook is the contract; the plugin is the proof.
Pick one place in your own platform where a feature is hard-coded and
make it a hook this sprint.
[simonwillison.net/2026/May/24/datasette-agent](https://simonwillison.net/2026/May/24/datasette-agent/)

**Armin Ronacher on issue quality** (via Simon, May 24). Ronacher's
complaint: AI-rewritten bug reports degrade open-source workflows
because the AI confidently adds analysis that wasn't in the original
human observation. His preferred shape is one paragraph, no
interpretation: "I ran this command. I expected this. This happened.
Here's the error." The applied move for any team that takes external
reports: add one sentence to your issue template asking submitters to
paste the literal command and the literal error before any AI summary.
The template change takes five minutes; it improves your bug funnel
for a year.
[simonwillison.net/2026/May/24/armin-ronacher](https://simonwillison.net/2026/May/24/armin-ronacher/)

**SpaceX S-1 confirms the Anthropic compute deal** (May 20, via
Simon). SpaceX's S-1 spells out the prior-week story in real numbers:
$1.25 billion per month, May 2026 through May 2029, COLOSSUS and
COLOSSUS II, 90-day termination clause either side, discounted
ramp-up pricing in May-June 2026. The number worth holding in your
head when reading next quarter's model price changes: $1.25B/month is
the new floor of Anthropic's compute cost line. The Flash 3.5 +
Haiku 4.5 price tables from W21 sit on top of cost lines like this
one. A 90-day termination clause in a deal at that scale is also a
signal — both sides are reserving optionality the public usually
doesn't see.
[simonwillison.net/2026/May/20/spacex-s1](https://simonwillison.net/2026/May/20/spacex-s1/)

---

## Watchlist

- **Of your security partner: when did we last test the queue-overflow
  case?** If an AI agent inside the stack starts writing 3x faster
  than the human queue absorbs, the first symptom is silent dropped
  work, not an alert. Pick one queue and run the drill this month.
- **Of your finance partner: do we hold any agent credential that
  survives a screen lock?** Codex Locked Use makes this question
  concrete on macOS today, and on hosted VMs by Q3.
- **Of your CEO or board: which of the four lab-relationship rows
  flipped this quarter?** The build-vs-partner memo from 2024 is now
  the wrong document for at least half its readers. Re-scoring is a
  one-hour exercise that catches an avoidable 2027 surprise.

---

## Closing thought

The week's quiet news, missing from the headlines, is in the
Glasswing footnote: maintainers asked the agent to slow down. The
slow-down request is the artifact. Builders who write the
slow-down switch into their own agent surfaces before a partner asks
for it have the seat next to the table when the policy gets
written.

---

## Postscript: the factory's own week

The two repos in the portfolio that ship procurement-side gates
landed the same operational discipline this week — schema-cache
freshness and owner-role coverage as executable checks instead of
documentation. The internal commits aren't news for outside readers.
The signal underneath them is: the gates you describe in your
playbook only count when they exit 1 in CI. If your AGENTS.md or
SECURITY.md or VENDOR-REVIEW.md is written but unenforced, the
sentence on the page is a suggestion. The next sprint's exercise is
to pick one written rule from any of those docs and make it an
executable check by Friday.
