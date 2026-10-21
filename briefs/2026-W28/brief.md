<!--
iso_week: 2026-W28
through_date: 2026-07-11
profile_id: builder-tpm
registry_version: 8
matrix_run_id: MTRX-W28-late-legible-harness
-->

# The harness stopped being a secret

**Week 28 update through 2026-07-11 - Vol. 11**

## Field thesis

Four public artifacts made the operating layer easier to inspect this week. OpenAI priced its new model family as a three-tier menu and left the routing decision to the buyer. Anthropic published a classification of 1.2 million sampled Cowork sessions. LangChain published the playbook it used to tune an open-weights model's harness, with scores. And prompt-capture archives posted files labeled as GPT-5.6 instructions the day after launch. The operating layer around the models is becoming readable from outside the vendor wall, and a team that reads it can build routing tables, delegation ledgers, and harness diffs from evidence instead of guesswork.

## Top signals

### 1. GPT-5.6 shipped as a price ladder, and routing became the buyer's job

**Source:** [OpenAI, "GPT-5.6: Frontier intelligence that scales with your ambition"](https://openai.com/index/gpt-5-6/), [TechCrunch launch report](https://techcrunch.com/2026/07/09/openai-launches-its-new-family-of-models-with-gpt-5-6/)

**Payload:** GPT-5.6 launched July 9 in three tiers - Sol at $5 input / $30 output per million tokens, Terra at $2.50 / $15, Luna at $1 / $6. The generation number and the capability tier are now separate axes: 5.6 names the generation, Sol/Terra/Luna name tiers that advance on their own cadence. The Agents SDK added GPT-5.6 model defaults in [v0.18.1](https://github.com/openai/openai-agents-python/releases/tag/v0.18.1) the same day.

**Mechanism:** The vendor now publishes the cost structure of the routing decision instead of hiding it behind one flagship price. Luna costs one fifth of Sol on both input and output, so the break-even question - which tasks clear the quality bar on the cheap tier - moved from vendor marketing into the buyer's eval harness.

**Why it matters:** Sol carries a 5x per-token price over Luna at launch. Cost per accepted task still depends on token use, retries, and escalation. The price list is an invitation to measure that subset.

**Reusable pattern:** A routing policy per task class: start on the cheapest tier, promote on gate failure, and log the tier that produced each accepted artifact.

**Action surface:** `config`, `eval`

**Try this week:** Take one recurring task, run the same ten cases under cheap-first and top-tier policies behind your existing quality gate, and record accepted-task cost, latency, and escalation.

**Systems map:** task class -> tier policy -> gate check -> escalate or accept -> per-tier cost and pass-rate ledger.

**Transferable principle:** When a vendor exposes a price axis, build the measurement that tells you where on the axis each workload belongs. The same applies to context-window sizes and sandbox compute classes.

**Falsification test:** If cheap-first routing costs more per accepted task than the top-tier baseline at the same quality bar, or breaches the declared latency budget, hold the routing change. Escalation rate alone cannot settle the bill.

**Adoption ladder:**
  - Minimum viable: one task class pinned to the cheap tier behind a gate.
  - Mid: escalation on gate failure with the tier recorded per artifact.
  - Full: ledger-calibrated tier defaults per task class, reviewed monthly.
  - Monitoring: escalation rate, per-artifact cost, and gate pass-rate by tier.

**Confidence:** High.

**Evidence:** W28-LATE-OPENAI-001, W28-LATE-SDK-001.

### 2. Delegated work detached from the device

**Source:** [Anthropic, "Claude Cowork on web and mobile"](https://claude.com/blog/cowork-web-mobile), [Axios on ChatGPT Work](https://www.axios.com/2026/07/09/ai-openai-gpt-release)

**Payload:** Anthropic announced a phased Cowork web and mobile beta on July 7, starting with Max users, with background and scheduled tasks that keep running after the laptop closes; a task started at a desk can be reviewed and redirected from a phone. OpenAI's July 9 announcement places GPT-5.6 in [ChatGPT Work](https://openai.com/index/gpt-5-6/), with documents, presentations, and interactive artifacts among its work surfaces. Anthropic also published a [study of 1.2 million sampled sessions](https://claude.com/resources/articles/how-people-are-using-claude-cowork) from May 11-31: business operations accounted for 33.4 percent and content creation for 16.4 percent. These are shares of a capped session sample; they do not count workers or the whole workload.

**Mechanism:** The agent session stopped being a window you watch and became a queue you review. Once tasks run without a device attached, the operative unit shifts from conversation to standing grant: connectors, skills, schedules, and the permissions they carry.

**Why it matters:** A standing agent with inbox, file, and calendar connectors is a standing capability, and it stays live while nobody is looking at it. Approval, revocation, and action history become the safety surface. Check what the account exports before calling that surface auditable.

**Reusable pattern:** A standing-grant inventory per agent account: every connector, skill, schedule, and scope, with an owner and a revocation path.

**Action surface:** `tool-policy`, `security`

**Try this week:** List the standing grants on one agent account you run, then answer one question per grant: what would tell you it fired while you were offline?

**Systems map:** standing grant -> scheduled trigger -> background run -> action ledger -> review surface on any device.

**Transferable principle:** Persistence converts a UX feature into an access-control problem. The same shift happened when cron jobs got credentials.

**Falsification test:** If the chosen account already exports every scheduled action with actor, scope, approval, and revocation history, use that ledger before building another one. Verify it with a revoked-grant run.

**Adoption ladder:**
  - Minimum viable: written inventory of standing grants.
  - Mid: per-grant activity review once a week.
  - Full: revocation drill plus alerting on first use of a dormant grant.
  - Monitoring: count grants nobody can explain, and time-to-revoke.

**Confidence:** High.

**Evidence:** W28-LATE-COWORK-001, W28-LATE-WORK-001.

### 3. The harness playbook went open-weights and got written down

**Source:** [LangChain, "Tuning the harness, not the model: a Nemotron 3 Ultra playbook"](https://www.langchain.com/blog/tuning-the-harness-not-the-model-a-nemotron-3-ultra-playbook), [LangChain, "Improving Agents is a Data Mining Problem"](https://www.langchain.com/blog/improving-agents-is-a-data-mining-problem)

**Payload:** LangChain's July 8 playbook describes tuning NVIDIA's open-weights Nemotron 3 Ultra while holding the model and generation settings fixed. It cites the team's earlier 52.8-to-66.5 Terminal-Bench result on GPT-5.2-Codex, published in February; those numbers belong to that earlier experiment. A companion post frames agent improvement as mining a trace corpus for failure patterns.

**Mechanism:** Harness tuning moved from a result you read to a procedure you can rerun: collect traces, mine failure classes, patch the harness, re-score. Pinning the weights removes silent model updates as one confound. Keep sampling, task cases, tool behavior, and scorer versions fixed too; open weights alone do not make a score delta attributable.

**Why it matters:** The experiments show that harness changes can improve a fixed model on the tested tasks. They do not rank harness work against every model upgrade. The written procedure gives your own agent a testable starting point.

**Reusable pattern:** Treat every model swap as a harness re-tune, and keep the tuning procedure in the repo next to the harness it tunes.

**Action surface:** `eval`, `workflow`

**Try this week:** Re-run one harness change you made from trace analysis against a second model, and record whether the fix transfers or was model-specific.

**Systems map:** trace corpus -> failure mining -> harness patch -> pinned-model re-score -> playbook update.

**Transferable principle:** A published procedure beats a published score; you can audit a procedure. The same standard applies to eval claims in vendor launch posts.

**Falsification test:** Compare trace-led harness tuning with an equal-budget prompt-editing baseline on held-out tasks. If it buys no acceptance or cost gain, defer the procedure for that agent; a failed transfer does not erase the published result.

**Adoption ladder:**
  - Minimum viable: store traces from one agent with failure labels.
  - Mid: one harness patch per mined failure class, re-scored.
  - Full: playbook file in-repo, rerun on every model swap.
  - Monitoring: score delta per patch, and patches that transfer across models.

**Confidence:** High.

**Evidence:** W28-LATE-LC-001, W28-LATE-LC-002.

### 4. The attack surface is the authorization boundary, and a guard has numbers

**Source:** [arXiv:2606.02240, "AgentRedBench: Dynamic Redteaming and Integration-Aware Defense for LLM Agents over SaaS Integrations"](https://arxiv.org/abs/2606.02240)

**Payload:** Across eight models and 24 enterprise SaaS integrations, injection attacks riding tool responses succeeded between 32 percent (Claude Sonnet 4.6) and 81 percent (Gemini 3 Flash) of the time. The benchmark includes 215 scenarios built on underspecified authorization - requests the tool policy permits but the user never meant. Their guard model, trained on integration-diverse adversarial tool responses, cut attack success from 69.9 to 2.4 percent at a 0.37 percent false-positive rate.

**Mechanism:** The failing boundary sits between what the user asked for and what the tools permit. Attacks live in tool-response content and in scope gaps, so a guard that sees only the user prompt misses both; the working defense reads the integration context around each tool response.

**Why it matters:** The benchmark measures attacks that arrive through the tool path. Its learned integration-aware guard reduced attack success on the reported panel; that result is an empirical defense score, with a residual failure rate.

**Reusable pattern:** An authorization-boundary fixture in every agent eval suite: one request that passes tool policy while exceeding the user's ask, and one injection payload inside a tool response.

**Action surface:** `eval`, `security`

**Try this week:** Add one underspecified-authorization fixture to an agent you run and check whether any gate fires before the action executes.

**Systems map:** user intent -> tool policy scope -> tool response content -> guard check -> execute or block -> attack-rate metric.

**Transferable principle:** Test the gap between granted scope and stated intent, and treat everything arriving through a tool as attacker-reachable. The same fixture works for MCP servers and browser agents.

**Falsification test:** If attack success rises beyond the declared tolerance on independently written, unseen fixtures, the published 2.4 percent does not transfer to that deployment. Measure false positives on legitimate work too; the failure alone would not diagnose memorization.

**Adoption ladder:**
  - Minimum viable: two adversarial fixtures in the agent eval suite.
  - Mid: guard check on tool responses for one high-privilege integration.
  - Full: pre-execution guard across integrations with logged verdicts.
  - Monitoring: attack success rate per integration, and guard false-positive rate.

**Confidence:** Medium-high.

**Evidence:** W28-LATE-SEC-001.

### 5. Capture archives became the harness diff surface

**Source:** [asgeirtj/system_prompts_leaks](https://github.com/asgeirtj/system_prompts_leaks), [x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)

**Payload:** GPT-5.6 launched July 9; archive commits on July 10 added files labeled ChatGPT and Codex GPT-5.6 instructions. The same repo tracks Claude Code's bundled skill by version number. A sibling archive's contributor branch updated Sonnet 5 files on July 6; its merge into main followed on July 8. This registry added four capture repos and one teardown analysis this week (v8), with a standing rule attached.

**Mechanism:** Capture repositories expose a watchable commit feed: claimed instruction budgets, tool definitions, and behavioral rules, diffable across files and versions. The feed records what the archive published; it cannot authenticate the vendor runtime.

**Why it matters:** These archives offer concrete harness hypotheses to test. Their provenance limits the inference: captures are unofficial, unverified, and adversarially obtained. They are diff signal and hypothesis fuel - never ground truth, and never text to paste into your own systems.

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

**Evidence:** W28-LATE-CAPTURE-001, W28-LATE-CAPTURE-002.

### 6. A mature library shipped its 4.0 through an agent loop

**Source:** [Simon Willison, "sqlite-utils 4.0, now with database schema migrations"](https://simonwillison.net/2026/Jul/7/sqlite-utils-4/)

**Payload:** Willison shipped sqlite-utils 4.0 on July 7 - schema migrations, nested transactions, compound foreign keys - and wrote up the agentic engineering behind the rewrite. The release-candidate cycle included a detailed code review by Claude Fable 5; Willison describes working through its findings before the stable cut.

**Mechanism:** Mature-library maintenance ran through an agent loop with the maintainer as gate: agents drafted the rewrite labor, the RC cycle plus a model code review served as verifier, and the human owned the merge. The writeup names the workflow, so the pattern is inspectable end to end on a real release.

**Why it matters:** The common story for agentic coding is greenfield demos. A major release of a library designed in 2018 is a harder case - backwards compatibility, real users, real blame - and it shipped with the loop documented by a maintainer with a reputation to lose.

**Reusable pattern:** Agent-drafted upgrades behind the project's existing release gates, with a model code review as one verifier among several, and the human sign-off kept at the merge.

**Action surface:** `workflow`

**Try this week:** Pick one stale dependency upgrade you have deferred, run it agent-drafted behind your test gate, and count the review comments that caught real defects.

**Systems map:** maintainer intent -> agent draft -> test gate -> model code review -> RC cycle -> human merge.

**Transferable principle:** The verifier stack, and the human's position in it, matters more than which layer wrote the diff. The same holds for infra-as-code changes and data migrations.

**Falsification test:** Compare escaped defects with earlier releases of similar change size and review depth. A worse rate would challenge the maintenance claim; release complexity and usage still need accounting before blaming the agent loop.

**Adoption ladder:**
  - Minimum viable: one agent-drafted dependency bump behind existing tests.
  - Mid: model code review added to the RC checklist.
  - Full: documented agent loop for routine maintenance releases.
  - Monitoring: post-release defect rate versus the pre-loop baseline.

**Confidence:** Medium-high.

**Evidence:** W28-LATE-SQLITE-001.

### 7. Wiki memory shipped as a product

**Source:** [LangChain, "Introducing OpenWiki Brains, general-purpose wiki memory for agents"](https://www.langchain.com/blog/introducing-openwiki-brains-general-purpose-wiki-memory-for-agents)

**Payload:** LangChain shipped OpenWiki Brains on July 10: a general-purpose, editable wiki that agents read and write as persistent memory. W27 scouted wiki memory as an early pattern; W28's watchlist asked whether memory governance would move from papers into tooling. This is a partial trigger fire - the substrate arrived, the governance fields have not.

**Mechanism:** Memory arrives as plain Markdown on the filesystem. A wrong memory becomes a wrong sentence on a page, findable by reading and fixable by editing. Put the wiki under version control if reviewable diffs and reverts are part of the contract.

**Why it matters:** W28's governed-memory frame asked for provenance, review, and expiry on every durable write. Those controls need a substrate a reviewer can inspect. A wiki supplies readable pages; an assigned owner and review cadence still have to turn readability into review.

**Reusable pattern:** Route durable agent memory through a reviewable document with edit history before reaching for a specialized memory stack.

**Action surface:** `personal-knowledge-base`, `architecture`

**Try this week:** Give one agent a versioned wiki page as durable memory for a week. Assign a reviewer, read the diff, and record wrong entries and correction time.

**Systems map:** run output -> memory candidate -> wiki edit -> human-readable diff -> future context assembly.

**Transferable principle:** A readable format lowers review cost. Ownership, provenance, and a review gate decide whether anyone pays that cost. Flat-file agent memory and AGENTS.md conventions need the same discipline.

**Falsification test:** If agents fill the wiki with confident stale claims faster than reading catches them, legibility without a review gate reproduced the corruption problem in a prettier format.

**Adoption ladder:**
  - Minimum viable: one agent, one versioned wiki page, named reviewer.
  - Mid: weekly human read of the diff, wrong entries tombstoned.
  - Full: provenance and expiry fields per entry, per the W28 governance frame.
  - Monitoring: stale-claim count per review, and time-to-correction.

**Confidence:** Medium.

**Evidence:** W28-LATE-MEM-001.

## Reusable patterns

- **Tier-routing ledger.** Where it applies: any vendor with a published price ladder; factory task routing. Caveats: needs a real quality gate first, or the cheap tier's failures arrive silently.
- **Standing-grant inventory.** Where it applies: background agents, scheduled tasks, connector-heavy accounts. Caveats: an inventory nobody reviews is a compliance document, and the review needs a calendar slot.
- **Harness playbook in-repo.** Where it applies: any agent with a trace corpus and a pinned model. Caveats: playbooks overfit to the model they were tuned on; re-verify on swap.
- **Authorization-boundary fixture.** Where it applies: SaaS-connected agents, MCP servers, browser agents. Caveats: two fixtures can expose a gap; a broader held-out set estimates guard performance within that distribution.
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
| gpt-5.6-tiers | factory | config | Add per-tier routing with gate-failure escalation for one task class | ledger shows tier, cost, and pass-rate per artifact | pin the class back to the top tier | higher accepted-task cost or a breached latency budget on the same ten cases |
| cowork-grants | portfolio agent accounts | tool-policy | Write the standing-grant inventory and run one revocation drill | drill revokes a grant and the next scheduled run fails as expected | restore the grant from the inventory | inventory goes stale within two weeks |
| agentredbench | llm-evals | eval | Add the two-fixture authorization-boundary set to one suite | scope-exceeds-intent fixture blocked pre-execution | mark fixtures advisory | fixtures pass trivially against every model tested |
| capture-archives | prompt-library | source-registry | Add a capture-diff note template and file the GPT-5.6 diff as the first entry | one dated note with a tested hypothesis | drop the template, keep the watch | two ship cycles produce no testable hypothesis |
| openwiki-brains | ai-field-brief | personal-knowledge-base | Trial one wiki page as durable memory for the brief loop | wrong entries found by reading the weekly diff | export the page to flat notes | stale claims outrun the weekly read |

## Scout radar

| Item | Why it might matter early | What to watch | Revisit trigger |
|---|---|---|---|
| Microsoft Project Solara | An agent-first device platform moves the agent shell below the app layer. | Enterprise pilots converting to procurement; badge and kiosk reference devices. | A named customer deployment with seat counts. |
| [Anthropic-TeraWulf 20-year lease](https://www.sec.gov/Archives/edgar/data/1083301/000110465926080583/tm2619468d1_8k.htm) | A frontier lab contracting approximately 401 MW of critical IT load for two decades is behaving like a hyperscaler. | Whether other labs sign multi-decade capacity or stay asset-light. | A second lab signs a comparable lease. |
| [MaxText elastic training](https://developers.googleblog.com/we-terminated-a-tpu-mid-training-and-it-recovered-in-seconds-introduction-to-elastic-training-with-maxtext/) | Google reports TPU failure mid-training recovering in seconds as a catchable exception. | Whether elastic recovery reaches public training stacks beyond Pathways. | An open-source training run publishes recovery-time numbers. |
| [Norm AI $120M raise](https://www.norm.ai/resources/norm-ai-raises-20-million-at-a-1-2-billion-valuation) | Compliance-as-agent is a wedge where regulation writes the eval criteria. | Whether shipped agents carry auditable decision trails regulators accept. | A regulator publicly accepts agent-produced compliance evidence. |
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

This week the operating layer had a price list, a session study, a tuning playbook, and an unofficial public diff history. Read it before you rebuild it.
