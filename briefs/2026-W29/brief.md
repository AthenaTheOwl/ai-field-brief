<!--
iso_week: 2026-W29
through_date: 2026-07-11
profile_id: builder-tpm
registry_version: 8
matrix_run_id: MTRX-W29-legible-harness
-->

# The harness stopped being a secret

**Week of 2026-07-11 - Vol. 11**

## Field thesis

Four disclosures landed this week that would have been internal documents a year ago. OpenAI priced its new model family as a three-tier menu and left the routing decision to the buyer. Anthropic published what 1.2 million Cowork sessions delegate. LangChain published the playbook it used to tune an open-weights model's harness, with scores. And the prompt-capture archives had GPT-5.6's working instructions on file within a day of launch. The operating layer around the models is becoming readable from outside the vendor wall, and a team that reads it can build routing tables, delegation ledgers, and harness diffs from evidence instead of guesswork.

## Top signals

### 1. GPT-5.6 shipped as a price ladder, and routing became the buyer's job

**Source:** [OpenAI, "GPT-5.6: Frontier intelligence that scales with your ambition"](https://openai.com/index/gpt-5-6/), [TechCrunch launch report](https://techcrunch.com/2026/07/09/openai-launches-its-new-family-of-models-with-gpt-5-6/)

**Payload:** GPT-5.6 launched July 9 in three tiers - Sol at $5 input / $30 output per million tokens, Terra at $2.50 / $15, Luna at $1 / $6. The generation number and the capability tier are now separate axes: 5.6 names the generation, Sol/Terra/Luna name tiers that advance on their own cadence. The Agents SDK shipped GPT-5.6 request controls in v0.18.1 within two days.

**Mechanism:** The vendor now publishes the cost structure of the routing decision instead of hiding it behind one flagship price. Luna costs one fifth of Sol on both input and output, so the break-even question - which tasks clear the quality bar on the cheap tier - moved from vendor marketing into the buyer's eval harness.

**Why it matters:** Teams that route every task to the top tier are now paying a visible 5x premium for the subset of tasks the small tier handles. The price list is an invitation to measure that subset.

**Reusable pattern:** A routing policy per task class: start on the cheapest tier, promote on gate failure, and log the tier that produced each accepted artifact.

**Action surface:** `config`, `eval`

**Try this week:** Take one recurring task, run ten cases on the cheapest tier behind your existing quality gate, and record how many cleared without escalation.

**Systems map:** task class -> tier policy -> gate check -> escalate or accept -> per-tier cost and pass-rate ledger.

**Transferable principle:** When a vendor exposes a price axis, build the measurement that tells you where on the axis each workload belongs. The same applies to context-window sizes and sandbox compute classes.

**Falsification test:** If a quarter of ledger entries show cheap-tier outputs failing gates and escalating anyway, the routing overhead is buying nothing and a flat top-tier policy is honest.

**Adoption ladder:**
  - Minimum viable: one task class pinned to the cheap tier behind a gate.
  - Mid: escalation on gate failure with the tier recorded per artifact.
  - Full: ledger-calibrated tier defaults per task class, reviewed monthly.
  - Monitoring: escalation rate, per-artifact cost, and gate pass-rate by tier.

**Confidence:** High.

**Evidence:** W29-OPENAI-001, W29-SDK-001.

### 2. Delegated work detached from the device

**Source:** [Anthropic, "Claude Cowork on web and mobile"](https://claude.com/blog/cowork-web-mobile), [Axios on ChatGPT Work](https://www.axios.com/2026/07/09/ai-openai-gpt-release)

**Payload:** Cowork reached web and mobile on July 7 with background and scheduled tasks that keep running after the laptop closes; a task started at a desk can be reviewed and redirected from a phone. OpenAI's ChatGPT Work, launched July 9, folds Codex into ChatGPT to produce documents, sites, and presentations for non-coders. Anthropic also published its session census: over 90 percent of Cowork usage is non-coding, with business operations at 33.4 percent and content creation at 16.4 percent.

**Mechanism:** The agent session stopped being a window you watch and became a queue you review. Once tasks run without a device attached, the operative unit shifts from conversation to standing grant: connectors, skills, schedules, and the permissions they carry.

**Why it matters:** A standing agent with inbox, file, and calendar connectors is a standing capability, and it stays live while nobody is looking at it. Approval, revocation, and action history become the safety surface, and the vendors are shipping the persistence faster than the audit tooling.

**Reusable pattern:** A standing-grant inventory per agent account: every connector, skill, schedule, and scope, with an owner and a revocation path.

**Action surface:** `tool-policy`, `security`

**Try this week:** List the standing grants on one agent account you run, then answer one question per grant: what would tell you it fired while you were offline?

**Systems map:** standing grant -> scheduled trigger -> background run -> action ledger -> review surface on any device.

**Transferable principle:** Persistence converts a UX feature into an access-control problem. The same shift happened when cron jobs got credentials.

**Falsification test:** If background runs ship with complete, exportable action ledgers by default across vendors this quarter, the audit gap named here closed on its own.

**Adoption ladder:**
  - Minimum viable: written inventory of standing grants.
  - Mid: per-grant activity review once a week.
  - Full: revocation drill plus alerting on first use of a dormant grant.
  - Monitoring: count grants nobody can explain, and time-to-revoke.

**Confidence:** High.

**Evidence:** W29-COWORK-001, W29-WORK-001.

### 3. The harness playbook went open-weights and got written down

**Source:** [LangChain, "Tuning the harness, not the model: a Nemotron 3 Ultra playbook"](https://www.langchain.com/blog/tuning-the-harness-not-the-model-nemotron-playbook), [LangChain, "Improving Agents is a Data Mining Problem"](https://www.langchain.com/blog/improving-agents-is-a-data-mining-problem)

**Payload:** A week after reporting a 52.8-to-66.5 Terminal Bench jump from harness changes on a fixed model, LangChain published the procedure itself as a playbook against NVIDIA's open-weights Nemotron 3 Ultra, alongside a companion post that frames agent improvement as mining a trace corpus for failure patterns. The NemoClaw blueprint adds a governed code-execution path for teams that cannot send code to a hosted model.

**Mechanism:** Harness tuning moved from a result you read to a procedure you can rerun: collect traces, mine failure classes, patch the harness, re-score. Running it against open weights removes the confound of silent vendor model updates - the model is pinned, so the delta is yours.

**Why it matters:** W28's claim was that harness beats model at fixed model quality. The written playbook makes that claim checkable on your own agent, and the open-weights target makes the baseline reproducible.

**Reusable pattern:** Treat every model swap as a harness re-tune, and keep the tuning procedure in the repo next to the harness it tunes.

**Action surface:** `eval`, `workflow`

**Try this week:** Re-run one harness change you made from trace analysis against a second model, and record whether the fix transfers or was model-specific.

**Systems map:** trace corpus -> failure mining -> harness patch -> pinned-model re-score -> playbook update.

**Transferable principle:** A published procedure beats a published score; you can audit a procedure. The same standard applies to eval claims in vendor launch posts.

**Falsification test:** If replaying the playbook on a different agent yields no measurable gain over ad-hoc prompt editing, the playbook was a writeup, and the W28 result stays a one-off.

**Adoption ladder:**
  - Minimum viable: store traces from one agent with failure labels.
  - Mid: one harness patch per mined failure class, re-scored.
  - Full: playbook file in-repo, rerun on every model swap.
  - Monitoring: score delta per patch, and patches that transfer across models.

**Confidence:** High.

**Evidence:** W29-LC-001, W29-LC-002.

### 4. The attack surface is the authorization boundary, and a guard has numbers

**Source:** [arXiv:2606.02240, "AgentRedBench: Dynamic Redteaming and Integration-Aware Defense for LLM Agents over SaaS Integrations"](https://arxiv.org/abs/2606.02240)

**Payload:** Across eight models and 24 enterprise SaaS integrations, injection attacks riding tool responses succeeded between 32 percent (Claude Sonnet 4.6) and 81 percent (Gemini 3 Flash) of the time. The benchmark includes 215 scenarios built on underspecified authorization - requests the tool policy permits but the user never meant. Their guard model, trained on integration-diverse adversarial tool responses, cut attack success from 69.9 to 2.4 percent at a 0.37 percent false-positive rate.

**Mechanism:** The failing boundary sits between what the user asked for and what the tools permit. Attacks live in tool-response content and in scope gaps, so a guard that sees only the user prompt misses both; the working defense reads the integration context around each tool response.

**Why it matters:** Most agent deployments gate the user input and trust the tool path. This benchmark puts numbers on how wrong that default is for SaaS-connected agents, and shows a deterministic pre-execution check earning its keep.

**Reusable pattern:** An authorization-boundary fixture in every agent eval suite: one request that passes tool policy while exceeding the user's ask, and one injection payload inside a tool response.

**Action surface:** `eval`, `security`

**Try this week:** Add one underspecified-authorization fixture to an agent you run and check whether any gate fires before the action executes.

**Systems map:** user intent -> tool policy scope -> tool response content -> guard check -> execute or block -> attack-rate metric.

**Transferable principle:** Test the gap between granted scope and stated intent, and treat everything arriving through a tool as attacker-reachable. The same fixture works for MCP servers and browser agents.

**Falsification test:** If the guard's numbers hold only on the paper's own scenario distribution and collapse on fixtures written after training, the 2.4 percent is memorization, and the boundary framing still stands on the attack side alone.

**Adoption ladder:**
  - Minimum viable: two adversarial fixtures in the agent eval suite.
  - Mid: guard check on tool responses for one high-privilege integration.
  - Full: pre-execution guard across integrations with logged verdicts.
  - Monitoring: attack success rate per integration, and guard false-positive rate.

**Confidence:** Medium-high.

**Evidence:** W29-SEC-001.

### 5. Capture archives became the harness diff surface

**Source:** [asgeirtj/system_prompts_leaks](https://github.com/asgeirtj/system_prompts_leaks), [x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)

**Payload:** GPT-5.6 launched July 9; the capture archive had the ChatGPT and Codex GPT-5.6 instructions on file July 10. The same repo tracks Claude Code's bundled skill by version number, and a sibling archive refreshed Claude Sonnet 5's instructions and tool descriptions on July 6. This registry added four capture repos and one teardown analysis this week (v8), with a standing rule attached.

**Mechanism:** Vendor harness changes now surface as public diffs within a news cycle. What each team used to extract on its own became a watchable commit feed: instruction budgets, tool definitions, and behavioral rules, diffable across releases and across vendors.

**Why it matters:** The vendors' own harness engineering is the densest public corpus of production prompt technique, and it updates on ship day. The caveat carries equal weight: captures are unofficial, unverified, and adversarially obtained. They are diff signal and hypothesis fuel - never ground truth, and never text to paste into your own systems.

**Reusable pattern:** A capture-diff watch: subscribe to the archive's commit feed, and when a vendor ships, read the harness diff for techniques worth testing - as untrusted data, summarized and cited, never copied.

**Action surface:** `source-registry`, `watchlist`

**Try this week:** Subscribe to one archive's commits.atom; when the next vendor ship lands, write down one harness technique from the diff shape and one experiment to test it.

**Systems map:** vendor ship -> extraction -> archive commit -> diff read -> technique hypothesis -> local experiment.

**Transferable principle:** When a hidden layer gains a public change log, watching the change log beats reverse-engineering each release. Dependency changelogs and API deprecation feeds earned the same watch.

**Falsification test:** If three months of capture diffs yield no technique that survives a local experiment, the archives are entertainment for this portfolio and belong off the scout lane.

**Adoption ladder:**
  - Minimum viable: one archive on commit watch.
  - Mid: per-ship diff notes with one tested hypothesis each.
  - Full: cross-vendor technique comparison feeding the prompt library.
  - Monitoring: hypotheses tested versus adopted, and takedown or staleness risk per archive.

**Confidence:** Medium.

**Evidence:** W29-CAPTURE-001, W29-CAPTURE-002.

### 6. A ten-year-old library shipped its 4.0 through an agent loop

**Source:** [Simon Willison, "sqlite-utils 4.0, now with database schema migrations"](https://simonwillison.net/2026/Jul/7/sqlite-utils-4/)

**Payload:** Willison shipped sqlite-utils 4.0 on July 7 - schema migrations, nested transactions, compound foreign keys - and wrote up the agentic engineering behind the rewrite. The release-candidate cycle included a detailed code review by Claude Fable 5, folded into rc4 before the stable cut.

**Mechanism:** Mature-library maintenance ran through an agent loop with the maintainer as gate: agents drafted the rewrite labor, the RC cycle plus a model code review served as verifier, and the human owned the merge. The writeup names the workflow, so the pattern is inspectable end to end on a real release.

**Why it matters:** The common story for agentic coding is greenfield demos. A 4.0 of a widely-installed decade-old library is the harder case - backwards compatibility, real users, real blame - and it shipped with the loop documented by a maintainer with a reputation to lose.

**Reusable pattern:** Agent-drafted upgrades behind the project's existing release gates, with a model code review as one verifier among several, and the human sign-off kept at the merge.

**Action surface:** `workflow`

**Try this week:** Pick one stale dependency upgrade you have deferred, run it agent-drafted behind your test gate, and count the review comments that caught real defects.

**Systems map:** maintainer intent -> agent draft -> test gate -> model code review -> RC cycle -> human merge.

**Transferable principle:** The verifier stack, and the human's position in it, matters more than which layer wrote the diff. The same holds for infra-as-code changes and data migrations.

**Falsification test:** If the post-release defect rate on 4.0 runs above the project's hand-written baseline, the loop optimized for shipping speed over the maintenance bar it claims to hold.

**Adoption ladder:**
  - Minimum viable: one agent-drafted dependency bump behind existing tests.
  - Mid: model code review added to the RC checklist.
  - Full: documented agent loop for routine maintenance releases.
  - Monitoring: post-release defect rate versus the pre-loop baseline.

**Confidence:** Medium-high.

**Evidence:** W29-SQLITE-001.

### 7. Wiki memory shipped as a product

**Source:** [LangChain, "Introducing OpenWiki Brains, general-purpose wiki memory for agents"](https://www.langchain.com/blog/introducing-openwiki-brains)

**Payload:** LangChain shipped OpenWiki Brains on July 10: a general-purpose, editable wiki that agents read and write as persistent memory. W27 scouted wiki memory as an early pattern; W28's watchlist asked whether memory governance would move from papers into tooling. This is a partial trigger fire - the substrate arrived, the governance fields have not.

**Mechanism:** Memory as a document store humans can read: pages, edits, and history instead of opaque embeddings. A wrong memory becomes a wrong sentence on a page - findable by reading, fixable by editing, revertible by history.

**Why it matters:** W28's governed-memory frame asked for provenance, review, and expiry on every durable write. Those controls need a substrate a reviewer can inspect, and a wiki is the first shipped memory product where review means reading.

**Reusable pattern:** Route durable agent memory through a reviewable document with edit history before reaching for a specialized memory stack.

**Action surface:** `personal-knowledge-base`, `architecture`

**Try this week:** Give one agent a wiki page as its durable memory for a week, then read the history and count the wrong entries you caught by eye.

**Systems map:** run output -> memory candidate -> wiki edit -> human-readable diff -> future context assembly.

**Transferable principle:** Reviewability comes from the storage format, and formats humans read get reviewed. Flat-file agent memory and AGENTS.md conventions bank on the same property.

**Falsification test:** If agents fill the wiki with confident stale claims faster than reading catches them, legibility without a review gate reproduced the corruption problem in a prettier format.

**Adoption ladder:**
  - Minimum viable: one agent, one wiki page, edit history on.
  - Mid: weekly human read of the diff, wrong entries tombstoned.
  - Full: provenance and expiry fields per entry, per the W28 governance frame.
  - Monitoring: stale-claim count per review, and time-to-correction.

**Confidence:** Medium.

**Evidence:** W29-MEM-001.

## Reusable patterns

- **Tier-routing ledger.** Where it applies: any vendor with a published price ladder; factory task routing. Caveats: needs a real quality gate first, or the cheap tier's failures arrive silently.
- **Standing-grant inventory.** Where it applies: background agents, scheduled tasks, connector-heavy accounts. Caveats: an inventory nobody reviews is a compliance document, and the review needs a calendar slot.
- **Harness playbook in-repo.** Where it applies: any agent with a trace corpus and a pinned model. Caveats: playbooks overfit to the model they were tuned on; re-verify on swap.
- **Authorization-boundary fixture.** Where it applies: SaaS-connected agents, MCP servers, browser agents. Caveats: two fixtures prove the gap exists, a distribution of fixtures proves the guard works.
- **Capture-diff watch.** Where it applies: prompt-library research, harness-engineering scouting. Caveats: unverified, adversarially sourced, and legally fragile; pointers and summaries only.

## Action queue

| Candidate | Surface | Effort | Risk | Test |
|---|---|---|---|---|
| Pin one factory task class to the cheapest GPT-5.6 tier behind gates | config | S | low | ten runs; record gate pass-rate and escalation count per tier |
| Write the standing-grant inventory for one agent account | tool-policy | S | low | every connector, skill, and schedule has an owner and a revocation path |
| Add two authorization-boundary fixtures to an agent eval suite | eval | M | medium | the tool-scope-exceeds-intent fixture is blocked before execution |
| Put one capture archive on commit watch with a diff-note template | source-registry | S | low | next vendor ship produces a dated diff note with one testable hypothesis |
| Run one deferred dependency upgrade agent-drafted behind tests | workflow | M | medium | upgrade merges with review comments logged and defect count tracked |

## Action packets

| Source | Target | Surface | Try | Proof metric | Rollback | Kill criterion |
|---|---|---|---|---|---|---|
| gpt-5.6-tiers | factory | config | Add per-tier routing with gate-failure escalation for one task class | ledger shows tier, cost, and pass-rate per artifact | pin the class back to the top tier | escalation rate above 25 percent after ten runs |
| cowork-grants | portfolio agent accounts | tool-policy | Write the standing-grant inventory and run one revocation drill | drill revokes a grant and the next scheduled run fails as expected | restore the grant from the inventory | inventory goes stale within two weeks |
| agentredbench | llm-evals | eval | Add the two-fixture authorization-boundary set to one suite | scope-exceeds-intent fixture blocked pre-execution | mark fixtures advisory | fixtures pass trivially against every model tested |
| capture-archives | prompt-library | source-registry | Add a capture-diff note template and file the GPT-5.6 diff as the first entry | one dated note with a tested hypothesis | drop the template, keep the watch | two ship cycles produce no testable hypothesis |
| openwiki-brains | ai-field-brief | personal-knowledge-base | Trial one wiki page as durable memory for the brief loop | wrong entries found by reading the weekly diff | export the page to flat notes | stale claims outrun the weekly read |

## Scout radar

| Item | Why it might matter early | What to watch | Revisit trigger |
|---|---|---|---|
| Microsoft Project Solara | An agent-first device platform moves the agent shell below the app layer. | Enterprise pilots converting to procurement; badge and kiosk reference devices. | A named customer deployment with seat counts. |
| Anthropic-TeraWulf 20-year lease | A frontier lab locking 400 MW for two decades is behaving like a hyperscaler. | Whether other labs sign multi-decade capacity or stay asset-light. | A second lab signs a comparable lease. |
| MaxText elastic training | Google reports TPU failure mid-training recovering in seconds as a catchable exception. | Whether elastic recovery reaches public training stacks beyond Pathways. | An open-source training run publishes recovery-time numbers. |
| Norm AI $120M raise | Compliance-as-agent is a wedge where regulation writes the eval criteria. | Whether shipped agents carry auditable decision trails regulators accept. | A regulator publicly accepts agent-produced compliance evidence. |
| LangGraph prebuilt deploy images | CLI 0.4.31 allows prebuilt images for deploys - runtime packaging is standardizing. | Whether agent deploys converge on container contracts like web apps did. | A second framework ships the same primitive. |
| Anthropic usage reflection | A vendor surface for reviewing your own Claude usage patterns. | Whether reflection data exports, and whether it reaches team plans. | An exportable usage ledger lands in the API. |

## Watchlist

- **Does tier routing survive contact with measured quality?** Revisit trigger: one cohort of ledger data showing cheap-tier pass-rates by task class.
- **Will background-agent vendors ship exportable action ledgers?** Revisit trigger: Cowork or ChatGPT Work documents a complete per-run action export.
- **Do AgentRedGuard's numbers replicate on unseen fixtures?** Revisit trigger: an independent eval reports the guard's attack-rate and false-positive numbers on new scenarios.
- **How long do capture archives stay up?** Revisit trigger: a DMCA takedown or license change hits any of the four registry entries.
- **Does China's model-access restriction land, and in what mechanism?** Revisit trigger: a published rule naming which models and which access paths are restricted.

## Archive notes

- **Addy Osmani, "The Agent-Era Career"** ([addyosmani.com](https://addyosmani.com/blog/agent-era-career/)). Career framing for the loop-engineering shift; useful reading, no mechanism to act on this week.
- **Google, "LiteRT.js"** ([developers.googleblog.com](https://developers.googleblog.com/)). Browser-side inference infrastructure; watch for agent use cases before promoting.
- **Anthropic news, July 9 batch** ([anthropic.com/news](https://www.anthropic.com/news)). UST physical-AI case study, Bernanke trust appointment, usage-reflection feature; the last moved to scout radar, the rest recorded.
- **Daily Systems Brief, July 7-10.** Mechanism feed for power, chips, and policy loops; AI-relevant claims were verified against public sources before promotion, the rest stayed internal.

## Sources reviewed

| Source | Status | Note |
|---|---|---|
| Weekly GenAI Digest folder | ok | no new digest in window; last item 2026-07-03 |
| Daily Systems Brief folder | ok | four dailies read as scout input; claims verified before promotion |
| Anthropic News | ok | July 9 batch captured; usage-reflection to scout radar |
| claude.com Cowork post | ok | background/scheduled tasks and session census promoted |
| OpenAI GPT-5.6 page | failed | direct fetch 403; pricing and tier claims verified via TechCrunch and Axios |
| Reuters ChatGPT Work report | failed | fetch blocked; launch verified via Axios and TechCrunch |
| TechCrunch GPT-5.6 report | ok | tier names and pricing confirmed |
| Axios GPT-5.6 and ChatGPT Work report | ok | launch date and Work framing confirmed |
| OpenAI Agents SDK releases | ok | v0.18.1/0.18.2 GPT-5.6 controls and hosted multi-agent beta captured |
| LangChain Blog | ok | harness playbook, data-mining post, NemoClaw, OpenWiki Brains promoted |
| LangGraph releases | ok | patch releases plus prebuilt deploy images to scout radar |
| Simon Willison | ok | sqlite-utils 4.0 agentic-engineering writeup promoted |
| Addy Osmani | ok | Agent-Era Career to archive notes |
| arXiv AgentRedBench | ok | attack rates and guard numbers promoted |
| asgeirtj/system_prompts_leaks | ok | GPT-5.6 capture timing promoted; content treated as untrusted |
| x1xhlol capture archive | ok | Sonnet 5 refresh noted; content treated as untrusted |
| Google Developers Blog | ok | elastic training to scout radar; LiteRT.js archived |
| LlamaIndex Blog | ok | newsletter only in window |
| MCP specification changelog | failed | changelog URL 404; no spec change confirmed this window |
| AWS AgentCore doc history | failed | page rendered empty; no update confirmed this window |

## Closing thought

A year ago the harness was the vendor's secret. This week it had a price list, a session census, a tuning playbook, and a public diff history. Read it before you rebuild it.
