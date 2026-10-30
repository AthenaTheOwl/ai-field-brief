<!--
iso_week: 2026-W44
through_date: 2026-10-30
profile_id: personal
registry_version: 14
matrix_run_id: MTRX-W44-reported-success
-->

# A rejected prompt came back as a successful answer, with another customer's data in it.

**Week 44 through 2026-10-30 · Vol. 27**

## Field thesis

Cloudflare served GLM-5.3 with a 1,048,576-token context window on a prefill cache that held 681,280 tokens. It expected prompts past the cache to fail. Its long-context tests came back successful, so the gap looked harmless. Between August 27 and September 9, 155 responses to prompts over that size carried other customers' data. The October 26 disclosure leads this issue. Five smaller items this week share its outline, a reported state that differed from the actual one. Braintrust's tracing SDK began recording MCP tool results by default a day after it shipped MCP tracing with that off. Ai2 moved a novelty judge from 93.5 to 40.9 percent accuracy by rewording one prompt. Claude Code fixed blocked calls that read as if they ran in a collapsed tool group. Meta routes engineers only tests that already fail on their diff. Vercel's new model aliases drop provider-specific settings when the provider changes. The thread joining them is the editor's reading, not any source's claim: check the effect, and read the status line second.

This is the regular issue for Saturday, October 24 through Friday, October 30. W43 covers October 19 through 23, so items dated in that span stay out of the headline even where this week's leads repeated them. Every pick below was dated from its own page.

## Top signals

### 1. An over-length prompt returned a successful answer built from someone else's cache

**Source:** [Cloudflare, "Cross-request KV cache exposure in the GLM-5.3 Workers AI model"](https://blog.cloudflare.com/kv-cache-exposure-remediation/), October 26

**Payload:** Cloudflare deployed GLM-5.3 with a 1,048,576-token context window and a prefill KV cache pool of 681,280 tokens. From August 27 to September 9, 155 responses, all to prompts longer than 681,280 tokens, contained data from other customers' requests to the same model. A researcher reported it on September 8, and the model was restored on September 9. Cloudflare found no evidence of deliberate exploitation. The incident is older than this issue; the coordinated disclosure with SGLang is dated October 26.

**Mechanism:** SGLang's disaggregated prefill/decode path marked the over-length prompt rejected, swapped in a one-token placeholder and carried on. Decode received "transfer complete" and generated over cache pages that still held earlier requests. Cloudflare had expected an error. Its long-context tests returned successful responses, and it read that as confirmation.

**Why it matters:** A test that accepts any successful response cannot catch a failure whose symptom is a successful response. Cloudflare now runs the pool at about 2.04 million tokens, roughly twice the context length, and also patched the rejection path to return its error, because pool size moves whenever quantization, parallelism or the model version changes. Operators of disaggregated SGLang should be on v0.5.22 or later. API customers cannot inspect a provider's pool; for them the transferable part is the test design.

**Reusable pattern:** At every declared limit, send one request just past it and fail the test on success.

**Action surface:** security

**Try:** For any self-hosted model config, assert the configured context length against measured cache capacity. Send one prompt just over capacity carrying a unique canary string and require an explicit error. Search later responses for the canary.

**Systems map:** advertised context exceeds cache capacity -> over-length prompt rejected internally -> placeholder transfer reports complete -> decode reads stale pages -> response succeeds with another tenant's data -> success-only tests pass.

**Transferable principle:** A limit is enforced only where crossing it produces an error that something checks. An upload endpoint that silently truncates files past its size cap fails the same way.

**Falsification test:** If an over-capacity canary prompt returns an explicit error on every run and its canary never appears in another request's output, the mismatch is not exposed on that deployment.

**Adoption ladder:**
  - Minimum viable: one config assertion and one over-capacity canary test per self-hosted model.
  - Mid: rerun both on every serving change to quantization, parallelism or model version.
  - Full: require the boundary test before a model goes public; Cloudflare now checks pool size against context length on every disaggregated deployment change.
  - Monitoring: over-capacity requests that succeed, canary strings in foreign responses, pool size against context length per deployment.

**Confidence:** high

**Evidence:** MTRX-W44-CFKV-source_gist, MTRX-W44-CFKV-mechanism_extraction, MTRX-W44-CFKV-risk_and_caveats, MTRX-W44-CFKV-adoption_action

### 2. A tracing SDK started recording MCP tool results by default, one day after adding MCP tracing

**Sources:** [Braintrust JS SDK 3.42.0](https://github.com/braintrustdata/braintrust-sdk-javascript/releases/tag/braintrust%403.42.0), October 29; [3.41.0](https://github.com/braintrustdata/braintrust-sdk-javascript/releases/tag/braintrust%403.41.0), October 28; [pull request 2690](https://github.com/braintrustdata/braintrust-sdk-javascript/pull/2690)

**Payload:** 3.41.0 added MCP server tracing with content capture off. 3.42.0 captures MCP tool arguments, prompt arguments, resource URIs, results and tool error text by default. The pull request says upgraders "will start recording MCP content unless they opt out", and notes the docs page still described the old default when it merged.

**Mechanism:** The SDK already recorded LLM prompts by default, and MCP content was brought in line. A minor version carries the change, so a caret range will pick it up on the next install; that last step is semver, not a Braintrust statement.

**Why it matters:** MCP results are where file contents, query rows and API responses come back. A trace store whose retention and access were set for prompts now holds those too, unless someone set the flag. The release changes what gets recorded. It reports no leak.

**Reusable pattern:** Set every capture flag explicitly, including the ones that match today's default.

**Action surface:** observability

**Try:** Pin the SDK. Call one MCP tool with a canary argument and a canary result, and search the exported spans for both strings. Upgrade and repeat. Then set `captureContent` to whatever the trace store is approved to hold.

**Systems map:** tracing ships with content off -> next minor flips the default -> caret range installs it -> tool results land in the trace store -> retention and access rules written for prompts now govern tool output.

**Transferable principle:** A default is a decision someone else can change in a minor release. A logging library whose new default level includes request bodies does the same thing to an application log.

**Falsification test:** If the canary strings stay out of spans on 3.42.0 without an explicit flag, or the trace store is already approved for tool results, the default change needs no action in that project.

**Adoption ladder:**
  - Minimum viable: canary search on the pinned and upgraded SDK in one service.
  - Mid: explicit capture flags in every service that traces MCP calls.
  - Full: a CI check that fails when a tracing dependency upgrade changes which canaries reach the exported spans.
  - Monitoring: canary hits in spans, trace-store size after upgrades, tracing SDK release notes that mention defaults.

**Confidence:** high

**Evidence:** MTRX-W44-BTMCP-source_gist, MTRX-W44-BTMCP-mechanism_extraction, MTRX-W44-BTMCP-risk_and_caveats, MTRX-W44-BTMCP-adoption_action

### 3. Rewording a judge's prompt moved its accuracy from 93.5 to 40.9 percent

**Source:** [Ai2, "Can we trust LLMs to judge whether a research idea is novel?"](https://huggingface.co/blog/allenai/novelty-bench), October 27

**Payload:** Ai2 tested six LLM novelty judges. On pairs of a top-10% ICLR idea and a generated idea, GPT-5.4 scored 93.5% with a prompt saying exactly one idea per pair was novel, and 40.9% with a prompt asking which idea was novel, changing more than half its verdicts. On human-only pairs the same switch moved GPT-5.4 about seven points and Claude Opus 4.6 by 21. Comparing two generators, a quarter to a third of verdicts flipped across prompt changes. A three-call Claude Opus 4.6 prompt scored 0.854 macro-F1 for $2.59 in total; two purpose-built evaluators scored 0.642 for $30.66 and 0.772 for $82.05.

**Mechanism:** A judge that looks stable on human-written work was asked to grade generated work, and its stability did not carry over. The 93.5% prompt also handed the judge the structure of the answer, which accounts for part of the gap.

**Why it matters:** Labels for the generated ideas are weak; Ai2 assumed them less novel than their human pairs. The flip rate needs no labels, which makes it the cheap number to compute for any judge already sitting in a pipeline. The task here is research novelty. Transfer to code-review or summary judges is a hypothesis.

**Reusable pattern:** Report a judge's verdict flip rate across reasonable prompt variants, on the items it grades in production.

**Action surface:** eval

**Try:** Pick one LLM judge already in use. Write a second reasonable prompt. Run both over 30 recent items of the kind it grades and report the share of flipped verdicts.

**Systems map:** judge validated on one distribution -> applied to generated items -> small prompt change -> verdicts flip -> ranking reflects the judge's prompt as much as the items.

**Transferable principle:** An instrument calibrated on one population needs recalibrating on another. A credit model fitted on salaried applicants and scored on gig workers has the same problem.

**Falsification test:** If two reasonable prompts agree on at least 90 percent of 30 production items, the judge is stable enough on that task for now. Rerun after any model or prompt change.

**Adoption ladder:**
  - Minimum viable: one judge, two prompts, 30 items, one flip rate.
  - Mid: flip rates for every judge in the pipeline, recorded beside its prompt version.
  - Full: block a judge prompt or model change when the flip rate against the previous version exceeds an agreed ceiling.
  - Monitoring: flip rate per judge, flip rate on generated versus human-written items, judge cost per decision.

**Confidence:** high

**Evidence:** MTRX-W44-NOVELTY-source_gist, MTRX-W44-NOVELTY-mechanism_extraction, MTRX-W44-NOVELTY-risk_and_caveats, MTRX-W44-NOVELTY-adoption_action

### 4. Two coding agents closed paths where a file nobody chose could widen permissions

**Sources:** [Claude Code 2.1.314](https://github.com/anthropics/claude-code/releases/tag/v2.1.314), October 30 UTC; [deepagents-code 0.2.2](https://github.com/langchain-ai/deepagents/releases/tag/deepagents-code%3D%3D0.2.2), October 26

**Payload:** Claude Code adds `permissions.blockWritesOutsideWorkingDirectories`: Write, Edit and NotebookEdit refuse paths outside the working directories in every permission mode. The same release fixes blocked shell and MCP calls reading as if they ran in a collapsed tool group, sandbox protections missing from a worktree entered by `claude -p --resume` or `--continue`, and a settings file excluded with `--setting-sources` still supplying auto mode rules and saved permission consents. LangChain's deepagents-code 0.2.2 stops a project `.env` file from setting extension, shell, plugin and skill trust, and allowlists Git options on auto mode's read-only fast path.

**Mechanism:** In each fix, a file or path the user had not picked as a policy source could change what the agent was allowed to do, or what the interface said it had done. Grouping the two tools is the editor's choice; the releases fix different code.

**Why it matters:** A reviewer skimming the collapsed view would have counted the blocked calls as executed. The notes place the bug in that display; they say nothing about the saved session record. Release notes record fixes, not how often the bugs fired. The write block arrives as a new named setting and the notes give no default, so treat it as off until a test says otherwise.

**Reusable pattern:** Confirm an agent's permission boundary from the file system, then compare with what the interface shows.

**Action surface:** tool-policy

**Try:** In a disposable repo on 2.1.314, enable the write block and ask the agent to edit a file one directory above the working directory. Check the file system. Then trigger a deny rule and confirm the collapsed tool group labels the call blocked.

**Systems map:** policy assembled from several files -> an excluded or repo-supplied file still contributes -> permissions widen or a call is mislabelled -> reviewer trusts the display.

**Transferable principle:** Every source that can contribute to policy is part of the policy. A CI job that reads deploy settings from a fork's config file has the same hole.

**Falsification test:** If the out-of-directory edit is refused on disk and every denied call is labelled blocked, including after a resume, these paths are closed on that version.

**Adoption ladder:**
  - Minimum viable: the two checks above in one disposable repo.
  - Mid: write block on in every repo where the agent has no reason to leave the working directory.
  - Full: a settings-source inventory per repo, with a test that an excluded file contributes nothing.
  - Monitoring: writes outside the working directory, display/file-system disagreements, permission rules whose origin file is unknown.

**Confidence:** high

**Evidence:** MTRX-W44-TRUST-source_gist, MTRX-W44-TRUST-mechanism_extraction, MTRX-W44-TRUST-risk_and_caveats, MTRX-W44-TRUST-adoption_action

### 5. Meta asks an engineer one question per catch: was this behavior change intended?

**Source:** [Meta Engineering, "Catching Bugs Before They Land"](https://engineering.fb.com/2026/10/29/security/catching-bugs-before-they-land-jittestings-human-on-the-loop-approach-at-full-scale/), October 29

**Payload:** Meta generates catching tests overnight for the previous day's risky diffs, built to fail on the diff's behavior change. An ensemble of LLM judges plus a deterministic rule-based assessor, RubFake, ranks the failures, and engineers are contacted only above a threshold. 589 engineers, 64% of those contacted, have engaged and report a 60% true-positive rate. Meta credits the system with a key role in catching 74 serious (SEV) privacy bugs at the diff stage in the first half of 2026, and with a 20% drop in privacy SEVs over that period.

**Mechanism:** A failing test is a concrete claim an engineer can confirm without reading test code. The deterministic assessor covers what the non-deterministic judges cannot verify. Humans set criteria and review outcomes in aggregate.

**Why it matters:** Reviewer attention is the scarce input once agents write most diffs. The 60% is engineer-reported with no denominator, and the 20% SEV drop has no control period, so both are Meta's account. The workflow shape travels better than the numbers.

**Reusable pattern:** Turn a review question into a test that must fail, and filter it with a deterministic check before a human sees it.

**Action surface:** workflow

**Try:** For ten recent agent-authored diffs, have a model write tests that pass on the parent commit and fail on the diff. Keep those that fail deterministically twice. Label each survivor intended change, real bug or noise.

**Systems map:** risky diff -> generated tests fail on its behavior change -> LLM judges and deterministic rules rank them -> engineer sees the top catches -> engineer confirms intent -> criteria adjusted from aggregate outcomes.

**Transferable principle:** A reviewer confirms a concrete observation faster than they can search for one. Data-quality alerts that attach the failing rows work the same way.

**Falsification test:** If fewer than one in ten surviving tests is labelled a real bug or unintended change, the generated tests cost more review time than they save on these diffs.

**Adoption ladder:**
  - Minimum viable: ten diffs, generated failing tests, three labels.
  - Mid: nightly run on agent-authored diffs above a size threshold, with a deterministic flakiness filter.
  - Full: engineers contacted only for ranked catches, with criteria tuned from the label counts.
  - Monitoring: real-bug share among surviving tests, review minutes per catch, flaky-test rate.

**Confidence:** medium

**Evidence:** MTRX-W44-JIT-source_gist, MTRX-W44-JIT-mechanism_extraction, MTRX-W44-JIT-risk_and_caveats, MTRX-W44-JIT-adoption_action

### 6. Vercel's model aliases keep fallbacks across a provider switch and drop provider options

**Source:** [Vercel, "Introducing Virtual Models on AI Gateway"](https://vercel.com/blog/ai-gateway-virtual-models), October 28

**Payload:** A virtual model is a task-level ID that carries the model, fallbacks, Zero Data Retention and tags. Edit it and every caller picks up the change without a deploy, and its settings override the same settings in a request. Vercel counts 125 new models from more than 10 labs on its gateway in the last 90 days. Provider options apply per provider, so an Anthropic-specific setting stops applying when the alias points at an OpenAI model.

**Mechanism:** On a switch, gateway-level settings move with the alias and provider-level settings stop applying. Vercel says to review provider options on every switch, to run evals against a second alias before moving production traffic, and to point the original back if quality drops.

**Why it matters:** Cheaper switches mean more of them. A dashboard edit also leaves no diff in the calling repository; that is the editor's inference, and the gateway does record requests, spend and success rate per alias. This is a launch post with no measured outcome.

**Reusable pattern:** On any model switch, diff the outgoing request's settings before and after.

**Action surface:** config

**Try:** In whatever routing layer a project uses, list each setting on the current model alias, mark the provider-specific ones, point a candidate alias at another provider and check which settings still appear on the outgoing request.

**Systems map:** task alias -> provider switch -> gateway settings persist and provider options drop -> request differs from what the config implies -> quality or cost changes with no code diff.

**Transferable principle:** An abstraction that hides the vendor also hides vendor-specific settings. An ORM that drops dialect-specific index hints during a database migration does the same.

**Falsification test:** If the request after a switch carries every setting the team intended, or the project uses no provider-specific options, nothing was lost.

**Adoption ladder:**
  - Minimum viable: one settings diff for one alias switched to one other provider.
  - Mid: a candidate alias evaluated before every production switch.
  - Full: switches logged with the before/after settings diff and the eval result.
  - Monitoring: settings dropped per switch, success rate and spend per alias after a switch.

**Confidence:** medium

**Evidence:** MTRX-W44-VMODEL-source_gist, MTRX-W44-VMODEL-mechanism_extraction, MTRX-W44-VMODEL-risk_and_caveats, MTRX-W44-VMODEL-adoption_action

## Reusable patterns

- **Fail the test on success past the limit.** Where it applies: context limits, upload caps, rate limits. Caveats: needs a canary to see the cross-tenant case. Evidence: MTRX-W44-CFKV-mechanism_extraction.
- **Pin defaults you depend on.** Where it applies: tracing, logging and retention flags in dependencies. Caveats: explicit flags drift from docs too. Evidence: MTRX-W44-BTMCP-mechanism_extraction.
- **Measure judges by disagreement.** Where it applies: any LLM judge without gold labels. Caveats: agreement can also be shared bias. Evidence: MTRX-W44-NOVELTY-mechanism_extraction.

## Action queue

| Candidate | Surface | Effort | Risk | Test |
|---|---|---|---|---|
| Over-capacity canary | security | S | low | Prompt just past cache capacity must return an error |
| Pin MCP capture flag | observability | S | low | Canary argument and result searched in spans across an upgrade |
| Judge flip rate | eval | S | low | Two prompts, 30 production items, share of flipped verdicts |
| Write-block check | tool-policy | S | low | Out-of-directory edit refused on disk; denied call labelled blocked |
| Failing-test triage | workflow | M | medium | Ten diffs, deterministic failing tests, labelled outcomes |
| Alias settings diff | config | S | low | Outgoing request settings before and after a provider switch |

## Action packets

| Source | Target | Surface | Try | Proof metric | Rollback | Kill criterion |
|---|---|---|---|---|---|---|
| Cloudflare disclosure | self-hosted inference config | security | Add the capacity assertion and canary test in 45 minutes | Over-capacity prompt errors on every run; canary never appears elsewhere | Remove the test | Stop if the project has no self-hosted inference |
| Braintrust 3.42.0 | tracing setup | observability | Canary search across one upgrade in 30 minutes | Canary presence matches the explicit flag on both versions | Revert the pin and flag | Stop if the project does not trace MCP calls with this SDK |
| Ai2 novelty judges | judge-backed pipeline | eval | Flip-rate run in 60 minutes | Flip rate recorded beside the judge's prompt version | Delete the variant prompt | Stop if the judge feeds no decision |
| Claude Code 2.1.314 | disposable repo | tool-policy | Write-block and deny-label checks in 30 minutes | Zero out-of-directory writes; every denied call labelled blocked | Remove the setting | Stop if a required cross-directory workflow breaks with no narrower rule |
| Meta catching tests | agent-authored diffs | workflow | Ten-diff failing-test trial in 90 minutes | Real-bug share among surviving tests | Discard generated tests | Stop below one real bug or unintended change per ten survivors |
| Vercel virtual models | model routing layer | config | One settings diff across a provider switch in 30 minutes | Settings present before and absent after | Delete the candidate alias | Stop if the project calls one provider |

## Framework-runtime scout

Release notes establish shipped changes. Dates are GitHub publication timestamps. The tests are proposals; none was executed for this issue.

| Primary source | Primitive changed | Why it matters | 30–90 minute test |
|---|---|---|---|
| [Codex rust-v0.166.0](https://github.com/openai/codex/releases/tag/rust-v0.166.0), Oct 29 | human approval | Keeps acknowledged approval and permission settings when a thread is resumed or forked | Resume a thread with a granted approval and check it is neither lost nor widened |
| [LangGraph 1.2.18](https://github.com/langchain-ai/langgraph/releases/tag/1.2.18), Oct 26 | artifact store | Delta snapshots now default to every 100 updates; the last checkpoint of an interrupted run is streamed | Compare checkpoint storage on a long thread before and after the upgrade |
| [LangGraph checkpoint 4.3.1](https://github.com/langchain-ai/langgraph/releases/tag/checkpoint%3D%3D4.3.1), Oct 26 | memory | Rejects NUL bytes in namespace labels | Write a namespace label with a NUL byte and expect a rejection |
| [Langfuse 4.72.0](https://github.com/langfuse/langfuse/releases/tag/v4.72.0), Oct 29 | observability | Attributes gateway spans to their API key; stops double counting cache-write TTL usage | Reconcile one day of cache-write cost against the provider invoice |
| [CrewAI 1.15.33](https://github.com/crewAIInc/crewAI/releases/tag/1.15.33), Oct 29 | observability | An env tracing value of `false` is now treated as off | Set tracing to `false` and confirm no spans export |
| [AgentCore SDK 1.25.1](https://github.com/aws/bedrock-agentcore-sdk-python/releases/tag/v1.25.1), Oct 27 | eval gate | Isolates custom simulation template rendering | Render two simulation templates in one run and check neither leaks into the other |

## Scout radar

| Item | Why it might matter early | What to watch | Revisit trigger |
|---|---|---|---|
| [Cloudflare Agents 0.31.0](https://github.com/cloudflare/agents/releases/tag/agents%400.31.0), Oct 27 | Browser Run can map up to 8 internal hostnames to an agent's own handlers, so the model can open a dev server in the browser it uses for the web | Whether internal hosts stay unreachable from outside pages | Upgrade after a fixture shows an external page cannot reach an internal host; demote if no portfolio agent uses Browser Run |
| [Microsoft Research synthetic enterprise evaluation](https://www.microsoft.com/en-us/research/blog/from-synthetic-enterprise-data-evaluations-to-real-microsoft-copilot-ai-confidence/), Oct 30 | Builds evaluation tenants from public occupational, job-posting and SEC data instead of customer data | Any reported result comparing synthetic-tenant scores with real usage | Upgrade when Microsoft publishes such a comparison; demote if none appears by W48 |

## Watchlist

- **Gemini 4 Carbon pricing at general availability.** Google lists an introductory $2 per million input tokens and $10 per million output tokens, the same as Argon, but access is limited to a subset of cyber defenders. Revisit trigger: developer API availability; reprice a fixed task set then.
- **Other disaggregated SGLang operators.** Cloudflare says GLM-5.3 was its only affected model and asks every operator to move to v0.5.22. Revisit trigger: another provider's disclosure or an SGLang security advisory for the same path.
- **Braintrust's MCP capture documentation.** The pull request flagged the docs as still describing the old default. Revisit trigger: the docs change, or a later release changes the default again.

## Archive notes

- Seventy of the 105 private-digest leads were dated outside this window by their own pages, 23 of them before October. The October 19–23 items among them, including Google's Agent Compute Engine, AWS's Infinity runtime, Anthropic's Agent Skills donation and formal-verification post, and Anthropic's UK AISI assessment, belong to W43's window and were not headlined here.
- openai.com returned HTTP 403 on every page requested, including four OpenAI posts the digests listed this week. Their dates could not be read from the pages, so none was used.
- Anthropic filed a Form S-1 on October 26 for a proposed Nasdaq listing under "ANT", with share count and price not yet set. Corporate news with no builder action this week.
- Mistral released Large 4 weights on October 29 with vendor benchmark claims only. Google DeepMind announced Genie 4 on October 27. Neither had a test a reader could run this week.
- Microsoft's Copilot harness post of October 28 sits on blogs.microsoft.com, which this pipeline cannot fetch reliably enough to carry a cell.
- Drew Breunig's October 24 talk on context engineering, Google Research's October 27 sleep framework and LangChain's October 24–29 posts were dated from their index pages and not read in full for cells.

## Sources reviewed

Discovery ran by script. Seven private daily digests and one weekly digest supplied 105 leads; each was dated from its own page, with 21 in window, 70 outside it and 14 undated (11 fetch failures, 3 pages with no readable date). A GitHub API scout over 32 framework repositories found 125 releases in window across 19 of them. A sweep of 38 registry feeds and indexes returned 35, with openai.com refusing all three of its surfaces, and produced 79 in-window leads. Thirty primary pages and 18 release bodies were fetched in full. Counts, dates and dispositions live in [the findings record](https://github.com/AthenaTheOwl/ai-field-brief/blob/main/ops/w44/findings.json). Digest text and private links are not reproduced.

The evidence matrix holds 24 cells under the personal profile. All 56 quoted spans matched their live sources verbatim. Each cell then received a same-author seven-question faithfulness reread; there was no independent reviewer. No proposed test was run.
