<!--
iso_week: 2026-W42
through_date: 2026-10-18
profile_id: personal
registry_version: 14
matrix_run_id: MTRX-W42-execution-order
-->

# The instructions arrived after the tools had already run.

**Week 42 through 2026-10-18 · Vol. 25 · catch-up issue**

## Field thesis

Google loaded a skill and searched the docs in the same turn. The skill's instructions reached the agent on the next turn. The searches were already done. That small ordering bug earns this week's lead: a flattened trace makes it look like the agent ignored instructions it had never received. LangGraph's resume fixes and the Agents SDK's pending-approval fix give the same audit a second address. Anthropic supplies a limit on the cure: adversarial reviewers can add complexity for imaginary threats. DeepSeek closes the issue with a model comparison whose two benchmark rows use different harnesses. Keep the turn, the approval and the harness in the record. They explain more than another review pass.

This is a scoped catch-up from October 10 through October 18. Twenty public primary surfaces were checked, nineteen returned, and three private research briefs supplied leads. The 222-source registry was not swept. Older material in those leads stays dated in Archive notes.

## Top signals

### 1. A skill load and its dependent searches occupied the same turn

**Source:** [Google Cloud's four evaluation engineering lessons](https://cloud.google.com/blog/topics/developers-practitioners/four-eval-engineering-lessons), October 16

**Payload:** Google's plugin team found skill loading and two searches dispatched together. Full instructions arrived a turn later. Its first summary-based judge also failed three of eleven prompts whose tool logs showed success. Live and plan-only runs exposed different failures; in one example, permissions stopped the live run before the plan's governance omissions became visible.

**Mechanism:** Concurrent calls share the context available at dispatch. A sibling call cannot consume instructions that arrive in the next turn. Flattening the trace erases that dependency.

**Why it matters:** A portfolio refresh can fan out across independent repositories. Within one repository, reading its operating contract must finish before a dependent edit starts. The speed gain comes from independent work; ordering still applies. Google's account is one team's experience, with a small initial suite.

**Reusable pattern:** Preserve turn groups and instruction availability when reviewing a tool trajectory.

**Action surface:** eval

**Try:** Take five saved agent runs. Mark each skill load, the turn when its body entered context, and every dependent call dispatched before then. Grade one sandboxed task from the commands it executed, then compare that verdict with a judge given only its final summary.

**Systems map:** parallel dispatch -> guidance enters on a later turn -> dependent calls lack guidance -> flattened trace hides ordering -> reviewer attributes the failure to instruction following.

**Transferable principle:** A prerequisite must be available before its consumer starts. The same rule applies to loading configuration before a service accepts traffic.

**Falsification test:** If the full skill body was available before every dependent dispatch, ordering does not explain the observed failures; inspect the instructions and model behavior next.

**Adoption ladder:**
  - Minimum viable: label turn groups and skill-body availability in five existing traces.
  - Mid: pair live sandbox and plan-only cases for one task family; record their disagreements.
  - Full: retain turn groups in trace ingestion and block dependent dispatch until required guidance is available.
  - Monitoring: premature dependent calls, summary/trajectory verdict disagreements, and failures found only by one condition.

**Confidence:** medium

**Evidence:** MTRX-W42-GOOGLE-source_gist, MTRX-W42-GOOGLE-mechanism_extraction, MTRX-W42-GOOGLE-risk_and_caveats

### 2. Resume and compaction both need to preserve unfinished work

**Sources:** [LangGraph 1.2.16](https://github.com/langchain-ai/langgraph/releases/tag/1.2.16), October 16; [OpenAI Agents SDK 0.24.0](https://github.com/openai/openai-agents-python/releases/tag/v0.24.0), October 15; [Strands Python 1.61.1](https://github.com/strands-agents/sdk-python/releases/tag/python/v1.61.1), October 15

**Payload:** LangGraph fixes resumed updates applying more than once, completed subgraph tasks running again, and repeated pending writes. The Agents SDK defers automatic compaction while approvals are pending. Strands fixes a child stop reason being hidden behind a success result.

**Mechanism:** A restart, a context rewrite and a parent/child boundary each transform state. Losing the distinction between pending, applied and stopped work can repeat a write or turn a blocked child into an apparent success.

**Why it matters:** A handoff record needs an unresolved-action field and an authoritative outcome. These release notes describe fixes, with no incident frequency or portfolio reproduction. They justify regression cases; they do not establish that any particular local run was affected.

**Reusable pattern:** Carry unresolved approvals and effect status across every state transformation.

**Action surface:** runtime-adapter

**Try:** In a disposable fixture, interrupt a write task before approval, compact its context, resume it twice, and count applied effects. Separately make a child stop on a blocked tool and check that the parent reports the stop.

**Systems map:** unfinished action -> interrupt or compaction -> incomplete checkpoint -> replay repeats the effect or loses the approval -> parent summarizes a misleading success.

**Transferable principle:** Recovery must preserve both progress and permission. A payment worker needs the same distinction between authorized, attempted and settled.

**Falsification test:** If repeated resume applies exactly one effect, preserves the pending approval and reports the child stop, these failure modes are already covered in that fixture.

**Adoption ladder:**
  - Minimum viable: one interrupted write with an effect counter and a pending approval.
  - Mid: repeat the fixture across each runtime adapter used by the portfolio.
  - Full: require the fixture when changing checkpoint, compaction or child-result handling.
  - Monitoring: duplicate effects, lost approvals and parent-success/child-stop disagreements.

**Confidence:** medium

**Evidence:** MTRX-W42-RUNTIME-source_gist, MTRX-W42-RUNTIME-mechanism_extraction, MTRX-W42-RUNTIME-risk_and_caveats

### 3. An adversarial reviewer can sell you an unnecessary validation layer

**Source:** [Redesigning source control at Anthropic](https://www.anthropic.com/engineering/redesigning-source-control), October 13, updated October 15

**Payload:** Anthropic describes an adversarial review that treated an internal service too defensively and prompted excessive validation. Engineers intervened. The same account describes server-side repository queries and content-addressed fetches that avoid maintaining a full checkout for every question. Anthropic explicitly limits Scion's fit to enormous repositories and unusual token budgets.

**Mechanism:** Review without a stated trust boundary can manufacture a threat model. The author then pays to satisfy it. Narrow queries offer the opposite economy: retrieve only what the decision needs.

**Why it matters:** An adversarial reviewer without a stated trust boundary can multiply findings before anyone establishes whether the underlying risk exists. A reviewer should name the violated contract, reachable path and evidence. This is a design lesson from a company account, not a measured defect-reduction result.

**Reusable pattern:** Give reviewers the actual trust boundaries, and disposition each finding before implementing it.

**Action surface:** workflow

**Try:** Review one small change with a written boundary map. Classify each finding as fix, decline with evidence, or escalate. Record review time and accepted findings; compare with the same task's existing review process.

**Systems map:** unstated boundary -> reviewer assumes hostile input -> author adds defensive machinery -> extra branches and tests increase maintenance -> human reconstructs the original boundary.

**Transferable principle:** A control earns its cost by addressing a reachable failure. Procurement checks should likewise distinguish an external supplier from an authenticated internal transfer.

**Falsification test:** If every added check covers a reachable failure and no finding depends on an invented boundary, this review has no demonstrated over-engineering problem.

**Adoption ladder:**
  - Minimum viable: supply one review with the trust boundary and required evidence.
  - Mid: record finding dispositions and implementation time across five changes.
  - Full: route reviews by consequence and require explicit disposition before fixes expand scope.
  - Monitoring: accepted findings per review minute, declined speculative findings and post-change defects.

**Confidence:** medium

**Evidence:** MTRX-W42-SCION-source_gist, MTRX-W42-SCION-mechanism_extraction, MTRX-W42-SCION-risk_and_caveats

### 4. DeepSeek's benchmark table names two harnesses and its free tools name an expiry

**Sources:** [DeepSeek's October 17 release](https://api-docs.deepseek.com/news/news261017/) and [model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017)

**Payload:** DeepSeek reports Terminal-Bench 4.0 at 42.3 versus 31.2 for the preceding release and DeepSWE v1.1 at 77.0 versus 74.2. The card assigns Claude Code to the former and Mini-SWE-V2 to the latter. Search and Fetch each cost $0.75 per thousand calls; qualifying server-side calls are free until billing begins October 31 at 16:00 UTC. The weights carry MIT licensing.

**Mechanism:** Harness and tool prices are inputs to the result. A comparison that records only a model name loses both the execution conditions and the future bill.

**Why it matters:** Treat these vendor-selected scores as a candidate for a paired evaluation. They establish neither accepted-patch performance here nor the cost of serving the weights locally. Record the expiry when estimating API experiments.

**Reusable pattern:** Pin model, harness, tool tariff and effective date in every comparison row.

**Action surface:** cost

**Try:** Prepare ten repository tasks with fixed acceptance checks. Compare two model/harness pairs under the same time and spending ceilings. Report accepted patches, corrections, elapsed time and total cost. Show the post-promotion tool tariff beside the temporary one.

**Systems map:** release improves a vendor benchmark -> harness conditions differ -> temporary tool discount lowers observed spend -> unqualified model comparison overstates transfer and understates later cost.

**Transferable principle:** A price comparison needs the conditions under which the price applies. Cloud credits and introductory freight rates create the same accounting trap.

**Falsification test:** If the gain survives fixed acceptance checks and budgets, and repricing after October 31 leaves the decision unchanged, the result supports adoption for those tasks.

**Adoption ladder:**
  - Minimum viable: add harness, tariff and expiry columns to the comparison fixture.
  - Mid: run ten paired tasks after credential and budget setup is approved.
  - Full: rerun the accepted-patch suite whenever model, harness or tariff changes.
  - Monitoring: cost per accepted patch, correction count and expiring discounts.

**Confidence:** medium

**Evidence:** MTRX-W42-DEEPSEEK-source_gist, MTRX-W42-DEEPSEEK-mechanism_extraction, MTRX-W42-DEEPSEEK-risk_and_caveats

## Reusable patterns

- **Dependencies precede fan-out.** Parallelize repositories after reading their contracts; keep instruction loading ahead of governed calls. Evidence: MTRX-W42-GOOGLE-mechanism_extraction.
- **Unfinished work survives handoff.** Preserve approvals, effect counts and child stop reasons through restart and compaction. Evidence: MTRX-W42-RUNTIME-mechanism_extraction.
- **Review findings need a disposition.** A role's title supplies no proof that its proposed fix is necessary. Evidence: MTRX-W42-SCION-adoption_action.

## Action queue

| Candidate | Surface | Effort | Risk | Test |
|---|---|---|---|---|
| Retain turn groups | eval | S | low | Audit five traces for premature dependent dispatch |
| Preserve pending effects | runtime-adapter | S | medium | Resume one mocked write twice; effect count remains one |
| Bound critic scope | workflow | S | low | Five reviews with finding dispositions and time recorded |
| Pin comparison conditions | cost | S | low | Reprice a fixture at the post-promotion tariff |

## Action packets

| Source | Target | Surface | Try | Proof metric | Rollback | Kill criterion |
|---|---|---|---|---|---|---|
| Google eval lessons | trace-to-eval-harness | eval | Audit five saved traces in 60 minutes | Count premature dependent calls and verdict disagreements | Keep the original trace files | Stop if the trace cannot establish instruction availability |
| Runtime release cluster | agent-notary-layer | runtime-adapter | Exercise a mocked approval/resume fixture in 60 minutes | Exactly one effect; approval and child stop survive | Remove the isolated fixture | Stop before any real outbound write or credential use |
| Scion review account | review-queue | workflow | Add a boundary map to one review in 45 minutes | Findings with evidence and explicit dispositions | Remove optional review fields | Stop if review time rises without a useful finding |
| DeepSeek release/card | modelswap-replay | cost | Add tariff expiry and harness columns in 30 minutes | Fixture reprices reproducibly after expiry | Revert the fixture addition | Stop before paid evaluation without an approved ceiling |

## Framework-runtime scout

Release notes establish shipped changes. The tests below are proposals; none was executed for this issue.

| Primary source | Primitive changed | Why it matters | 30–90 minute test |
|---|---|---|---|
| [LangGraph 1.2.16](https://github.com/langchain-ai/langgraph/releases/tag/1.2.16) | execution | Resume fixes affect duplicate updates and completed subgraphs | Resume a mocked write twice and count effects |
| [Agents SDK 0.24.0](https://github.com/openai/openai-agents-python/releases/tag/v0.24.0) | human approval | Compaction waits for pending approvals | Force compaction with an unresolved mocked approval |
| [Google ADK 2.12.0](https://github.com/google/adk-python/releases/tag/v2.12.0) | human approval | Adds workflow-node confirmation | Assert no node effect occurs before confirmation |
| [Strands Python 1.61.1](https://github.com/strands-agents/sdk-python/releases/tag/python/v1.61.1) | stop rule | Surfaces a child's stop reason | Block a child and inspect the parent result |
| [LangSmith 0.14.9](https://github.com/langchain-ai/langsmith-sdk/releases/tag/v0.14.9) | eval gate | Fixes comparative scores when concurrent runs are randomized | Shuffle labelled mock runs and assert scores stay attached |
| [E2B 2.56.0](https://github.com/e2b-dev/E2B/releases/tag/e2b%402.56.0) | sandbox grant | Raises the Node requirement and changes concurrency controls | Check the pinned SDK against the actual host version |

## Scout radar

| Item | Why it might matter early | What to watch | Revisit trigger |
|---|---|---|---|
| [Cloudflare Agents 0.28.1](https://github.com/cloudflare/agents/releases/tag/agents%400.28.1) | Adds gateway route and key options | Permission and billing behavior | Upgrade after a scoped fixture verifies the required route; demote if no portfolio runtime uses it |
| [Langfuse 4.63.0](https://github.com/langfuse/langfuse/releases/tag/v4.63.0) | Attributes gateway errors by origin | Diagnostic accuracy | Upgrade after injected-origin errors stay distinguishable; demote if the trace already records this |

## Watchlist

- **Approval across context rewrite.** Revisit trigger: a local fixture loses an approval or repeats an effect; then promote the runtime test into a required gate.
- **Paid comparisons after a free-tool period.** Revisit trigger: October 31 at 16:00 UTC, when DeepSeek says billing starts; reprice before interpreting a later cost comparison.
- **Review-finding overhead.** Revisit trigger: five comparable changes with review time and accepted findings recorded; keep the boundary map only if it improves the measured outcome.

## Archive notes

- The October 16 research digest includes August context-compaction work and September harness, multi-agent and auditor papers. Those dates are part of the evidence. They were not promoted as October releases.
- The October 18 systems briefs disagree on their main AI story. One emphasizes persistent-agent and reward-hacking material; the other leads with DeepSeek's October 17 release. This issue uses their public links as leads and checks the selected claims against the primary pages.
- MCP TypeScript SDK, LlamaIndex, Braintrust SDK and AgentOps returned no in-window release among the five latest entries checked. That is a bounded release-index observation, not proof of inactivity elsewhere.

## Sources reviewed

Twenty public surfaces: four selected primary pages; LangChain Blog, Google Developers AI and the AgentCore tag page; thirteen framework release indexes. The AgentCore tag returned HTTP 404. All other requests returned. The checked URLs, release publication timestamps and fetch failures live in [the sweep record](https://github.com/AthenaTheOwl/ai-field-brief/blob/main/ops/w42/source-sweep.json). Three private briefs supplied discovery leads; their text and private URLs are excluded from this public issue.

The evidence matrix contains 36 cells, scored under the personal profile. Each received a same-author seven-question faithfulness reread against the fetched primary. An independent reviewer then reread the four Top signals against live primaries and passed their factual claims; the [review record](https://github.com/AthenaTheOwl/ai-field-brief/blob/main/ops/w42/independent-review.json) preserves the scope and caveats. No live agent benchmark ran. The proposed actions remain experiments.
