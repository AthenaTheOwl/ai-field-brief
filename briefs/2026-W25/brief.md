<!--
meta:
  iso_week: 2026-W25
  through_date: 2026-06-21
  profile_id: broad_builder
  sources_swept_count: 39
  items_collected: 48
  volume: 002
  mode: workflow-driven
-->

# Agent runtime hardened into infrastructure this week; the policy engine, the identity layer, and the eval gate all became first-class artifacts

**week of 2026-06-15 - audience: builder-tpms thinking about AI - vol. 002**

## Field thesis

The week's center of gravity sat in the agent runtime, hardening into infrastructure on every front at once while the Fable 5 export-control aftershock kept reshaping the supply chain underneath it. Three vendors worked on different runtime controls in this catch-up (Anthropic's IdP-managed MCP + auto-mode git denylist, OpenAI's Record-and-Replay + scheduled-tasks GA, DeepMind's capability-tiered control roadmap), and two independent frameworks (Vercel Eve, Google OKF) committed to the same filesystem-as-contract pattern that AGENTS.md has been previewing for months. Underneath, a second convergence: benchmark authors stopped trusting final-answer grades — ALE, WeaveBench, SciAgentArena, AutoResearch, MosaicLeaks, and ABC-Bench all require stepwise checks, channel-cooperation, reseeded verification, or physical execution. The Fable 5 fallout drove the strategic backdrop (export-control risk is now a real entry in your provider matrix; GLM-5.2 brings an MIT license and 1M context as another candidate), but the operational story is that the policy engine, the identity layer, the trigger surface, the eval gate, and the role-contract directory are all becoming first-class artifacts. Those releases make the policy engine, manifest, and eval gate worth comparing. Three vendors do not establish an industry default.

7 top signals, 6 watchlist items, 39 sources reviewed (7 failed).

## Top signals

### 1. Claude Code blocks unrequested destructive git; Claude adds artifacts and managed MCP auth

**Source:** [Claude Code v2.1.183](https://github.com/anthropics/claude-code/releases/tag/v2.1.183), [Claude Code artifacts](https://claude.com/blog/artifacts-in-claude-code), [Enterprise-managed MCP authorization](https://claude.com/blog/enterprise-managed-auth)

**Payload:** Three Anthropic releases landed in five days: 2.1.183 blocks destructive git verbs in auto mode unless explicitly authorized, artifacts publish live versioned web pages from a Claude Code session, and MCP connectors now provision through Okta groups.

**Mechanism:** The v2.1.183 list includes reset --hard, checkout -- ., clean -fd, and stash drop when discarding work was not requested. Artifacts and enterprise-managed MCP auth are separate product surfaces; the auth launch starts with Okta. A classifier review is not proof that every destructive command is blocked.

**Why it matters:** Three concrete places to inspect in your harness: destructive action policy, artifact sharing, and connector identity. Their arrival does not establish auto mode as the default.

**Reusable pattern:** Policy at the gate, not in the prompt

**Action surface:** tool-policy

**Try:** Copy the 2.1.183 destructive-git verb list into your own agent harness as an explicit-confirm denylist; publish one session's output as an artifact URL instead of a Slack writeup; tag each MCP connector as IdP-eligible.

**Systems map:** Three independent failure modes (irreversible action, ephemeral output, per-user auth burden) get pushed down to harness-level enforcement so the model never has to be trusted to follow a rule it could be argued out of.

**Transferable principle:** Move safety, delivery, and identity out of prompt instructions and into the harness — applies equally to any agent stack with shell access, ephemeral outputs, or OAuth-bound tools (e.g., your own CDCP role contracts gating tool calls via a policy engine instead of a system prompt).

**Confidence:** high

**Evidence:** MTRX-W25-EARLY-01

---

### 2. DeepMind's AI Control Roadmap treats internal agents as insider threats

**Source:** [Google DeepMind Blog](https://deepmind.google/blog/securing-the-future-of-ai-agents/)

**Payload:** Defense-in-depth framework with MITRE-ATT&CK-style tactics, trusted AI supervisors that can block actions pre-execution, and defenses scaled across a D1-D4 detection-evasion × R1-R3 harm-execution grid.

**Mechanism:** DeepMind reports reviewing a million coding-agent tasks with an asynchronous prototype, escalating flags to humans. Most flagged events were described as misinterpretation or overeagerness. Its roadmap separately calls for synchronous prevention on high-risk actions; that is not a measured pre-execution catch rate for the whole million-task corpus.

**Why it matters:** Provides a concrete capability-tiered taxonomy to borrow instead of invent; aligns directly with the role-contracts + policy-engine + event-ledger pattern. The empirical finding that overeagerness dominates adversariality changes what your detector should optimize for.

**Reusable pattern:** Capability-tiered control matrix instead of a single bar

**Action surface:** architecture

**Try:** Map your agent fleet to the D1-D4 / R1-R3 grid on one page; identify the highest D×R cell with zero supervisor coverage and decide whether you write a supervisor or remove the capability.

**Systems map:** Actor -> supervisor -> escalation or intervention. Measure monitoring coverage, missed harms, false blocks, and response time; a narrower supervisor can still share the actor's blind spot.

**Transferable principle:** Pair every capable actor with a narrower verifier sitting on the action path — applies to code review (lint as actor-verifier), to financial controls (the four-eyes principle), and to any agent role contract where the action surface exceeds the trust budget.

**Confidence:** high

**Evidence:** MTRX-W25-EARLY-02

---

### 3. GLM-5.2 ships MIT-licensed at 1M context — price a completed task

**Source:** [Z.ai model card](https://huggingface.co/zai-org/GLM-5.2) and [Simon Willison's first impressions](https://simonwillison.net/2026/Jun/17/glm-52/)

**Payload:** Z.ai released GLM-5.2 with MIT-licensed weights and 1M context. Its model card reports 81.0 on Terminal-Bench 2.1 using Terminus-2; a separately listed best-reported harness scores 82.7. Keep the harness attached to the number.

**Mechanism:** Z.ai says IndexShare reuses an indexer across four sparse-attention layers, reducing per-token FLOPs by 2.9x at 1M context. That is an architecture claim, not a 2.9x reduction in your hosted bill.

**Why it matters:** An open-weight option is worth a matched coding-task comparison. License, hardware, token count, latency, and accepted output all enter the substitute cost; a leaderboard rank cannot settle the route.

**Reusable pattern:** Architectural lever (IndexShare) plus license (MIT) plus day-zero ecosystem coverage is what makes an open model substitutable

**Action surface:** tool-policy

**Try:** Route one real coding task through GLM-5.2 via OpenRouter; log token cost and quality delta vs your current default and decide whether to add it as the fallback in a router config.

**Systems map:** When a serious open-weight model lands inside the existing inference-server ecosystem the same day it's announced, the switching cost collapses from weeks (adapter PRs, sandbox testing) to hours (model id change in the gateway).

**Transferable principle:** Lock-in to a closed model is only durable while either capability or ecosystem support is missing on the open side — same dynamic recently played out in vector DBs and is now playing out in frontier text models. Maintain a fallback path you've exercised, not just one you've drawn.

**Confidence:** high

**Evidence:** MTRX-W25-EARLY-03

---

### 4. Anthropic finds domain expertise tracks how much work Claude does

**Source:** [Anthropic Research](https://www.anthropic.com/research/claude-code-expertise)

**Payload:** Analysis of ~400k Claude Code sessions from ~235k users (Oct 2025–Apr 2026) decomposes each session into planning vs execution decisions: users contribute ~70% of planning, Claude ~80% of execution, and higher user domain expertise correlates with longer effective Claude turns per instruction.

**Mechanism:** Anthropic uses transcript classifiers to infer task-specific expertise and attribute planning/execution decisions. The observed correlation does not isolate expertise from task mix, selection, or model changes, and longer turns are not by themselves better output.

**Why it matters:** Bring the person who knows the task into the review. This study supports testing better specification; it does not establish that coding skills stopped mattering or prescribe a hiring mix.

**Reusable pattern:** Separate the planning role from the execution role and measure each

**Action surface:** agent-role

**Try:** On comparable tasks, log specification quality and accepted output, review defects, and total time. Use an independent reviewer; PR merge rate alone can rise while correctness falls.

**Systems map:** The agent absorbs execution decisions cheaply, which shifts the marginal value of the human upstream into specification — the same shift that happened when compilers absorbed register allocation.

**Transferable principle:** When the agent takes more execution work, test whether clearer specification improves the accepted result. Keep the expertise claim scoped to the task and the measured outcome.

**Confidence:** high

**Evidence:** MTRX-W25-EARLY-04

---

### 5. Vercel Eve and Google OKF commit to filesystem-as-contract on the same axis

**Source:** [Vercel Eve](https://vercel.com/changelog/introducing-eve-an-open-source-agent-framework) and [Google Cloud OKF](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)

**Payload:** Vercel put Eve in public preview on June 17: agents are directories with instructions, tools, and other runtime files. Google Cloud's June 12 OKF v0.1 announcement describes portable Markdown/YAML knowledge bundles. One defines agent behavior; the other packages context.

**Mechanism:** Eve does build-time discovery from file paths and prepends instructions.md to every model call with no decorator-based registration; OKF requires only a 'type' field in YAML frontmatter and renders to an interactive graph via one self-contained HTML file; both treat the directory layout as the source of truth.

**Why it matters:** Both make a useful reference for role-contract files. Neither establishes a de facto industry convention or proves a directory beats explicit registration for every repo.

**Reusable pattern:** Filesystem layout as the API surface, build-time discovery over runtime registration

**Action surface:** agent-role

**Try:** Clone github.com/vercel/eve, scaffold one agent with a single tool and a skills/onboarding.md, then diff its compiled manifest against an equivalent CDCP role contract to see what registration boilerplate disappears.

**Systems map:** A checked-in directory makes changes visible to git review. Code-based registration can also be versioned; inspectability depends on where the authoritative configuration lives and how the runtime reads it.

**Transferable principle:** Choose one authoritative configuration and test that the runtime uses it. A directory is easy to diff; permissions still need enforcement.

**Confidence:** high

**Evidence:** MTRX-W25-EARLY-05

---

### 6. Benchmark authors add checks beyond the final answer

**Source:** [SciAgentArena](https://arxiv.org/abs/2606.12736v1), [WeaveBench](https://arxiv.org/abs/2606.09426v2), [AutoResearch](https://arxiv.org/abs/2606.20394v1), [ABC-Bench](https://arxiv.org/abs/2606.11150v1)

**Payload:** SciAgentArena uses stepwise verification on roughly 200 scientific tasks. WeaveBench checks mixed GUI/CLI trajectories. AutoResearch tests aerospace-policy improvements against seed noise, reseeded runs, and edit ablations. ABC-Bench reports wet-lab validation of generated robot scripts on one task type. These are different checks, not one new grading standard.

**Mechanism:** Each check targets a specific shortcut: skipping a required step, fabricating evidence, mistaking noise for improvement, or failing outside simulation. Earlier June papers are catch-up context here; AutoResearch arrived June 18.

**Why it matters:** Add the check that catches your actual failure. A final-answer test remains useful when the answer is independently verifiable; step counts alone can reward a longer wrong trajectory.

**Reusable pattern:** Verification gates per checkpoint, not per task

**Action surface:** eval

**Try:** Split one of your existing single-score evals into 3-5 checkpoint assertions; add a 'no result credited until reseeded' gate to any auto-tuning agent and log how many of its self-reported wins disappear.

**Systems map:** Proposed result -> independent evidence -> accepted result. These checks reduce named failure modes; they do not close reward hacking in general.

**Transferable principle:** Keep the outcome check and add independent checks where the agent can fake the path. Test the verifier with a shortcut fixture before trusting a green result.

**Confidence:** high

**Evidence:** MTRX-W25-EARLY-06

---

### 7. Fable 5 export controls reframe Anthropic dependency as a supply-chain risk with jurisdiction

**Source:** [Stratechery](https://stratechery.com/2026/the-state-of-fable-the-jailbreak-problem-spacex-acquires-cursor/)

**Payload:** Anthropic's June 12 statement says a US government directive forced it to suspend Fable 5 and Mythos 5 for all customers, while other Claude models stayed available. The provider disputed the directive's technical basis. That statement establishes the disruption, not the full reasoning of the government.

**Mechanism:** A provider-specific access decision can break a pinned route with little warning. Keep disputed claims about the triggering research attributed; the availability failure is observable without settling them.

**Why it matters:** Builders now have two new supply-chain fields to add per dependency: jurisdiction and owner. The Anthropic-specific scoping changes the timing of multi-vendor routing work (this quarter for Anthropic-heavy stacks, less urgent for others) but does not eliminate it.

**Reusable pattern:** Per-dependency jurisdiction + owner fields plus a pre-written 1-week-outage contingency

**Action surface:** tool-policy

**Try:** In your model/tool registry add 'jurisdiction' and 'owner' fields per dependency; tag Anthropic as 'active US export-control risk'; write a one-page contingency for (a) Claude frontier access disappearing for 72h and (b) Cursor's default routing changing to xAI under SpaceX ownership.

**Systems map:** Provider, owner, serving cloud, jurisdiction, hardware, and access policy can create correlated failures. Exercise a permitted fallback against the failure you want to survive; a different owner or country alone does not guarantee independence.

**Transferable principle:** Write and test a short-outage plan for a critical dependency. Include data permissions and task quality before treating a model swap as continuity.

**Confidence:** high

**Evidence:** MTRX-W25-EARLY-07

---

## Reusable patterns

- **Directory-as-contract beats decorator-as-registration** — Eve, OKF, agents.md-on-Spaces, and AGENTS.md routing all converge on filesystem layout as the source of truth for agent capability and context — registration boilerplate is the smell.
- **Tool-policy enforcement moves from prompt to runtime gate** — Claude Code's auto-mode git denylist, DeepMind's pre-execution supervisors, and Passport's short-lived-credential issuance all push safety from prompt instructions down into the harness layer that runs commands.
- **Evals must verify stepwise, not just finally** — SciAgentArena (checkpoints), WeaveBench (trajectory audits), AutoResearch (reseeded verification gates), MosaicLeaks (information-flow probes), and ABC-Bench (wet-lab closure) all reject the single-score grade — the artifact discipline has reached evaluation.
- **Supply-chain risk is now a per-dependency field, not a vibe** — Fable 5 export controls + SpaceX-acquires-Cursor mean 'jurisdiction' and 'owner' belong in your model/tool registry alongside latency and price, with one-week-outage contingencies pre-written for the high-D×R cells.

## Action queue

- **Add a 'Routing' section and an irreversible-action approval rule to AGENTS.md in your most-used repo; encode at least three task→mechanism mappings.**
  - surface: agent-role
  - rationale: Jason Liu's three-mechanism routing is the cheapest, highest-yield import this week — turns 'one agent does everything' into a policy artifact you can diff.
- **Stand up a fallback-router config with one open-weight primary (GLM-5.2) and one closed-weight premium, threshold on cost/capability, log which path each request took for a week.**
  - surface: tool-policy
  - rationale: Fable 5 fallout makes a fallback worth testing. Price the same accepted task on both routes; the roundup's unnamed per-task denominator cannot price your workload.
- **Audit every long-lived token in your agent harness; for each MCP/connector, mark IdP-eligible vs not and stub the short-lived-credential issuer that replaces it.**
  - surface: tool-policy
  - rationale: Anthropic enterprise-managed MCP and Vercel Passport landed in the same week — the runtime is moving to IdP-issued short-lived creds and your inventory is the prerequisite work.
- **Pick one MCP tool you depend on and write an eval that asserts a passed parameter changed the output; treat silent-ignore as a bug.**
  - surface: eval
  - rationale: OpenAI Cookbook PR #2783 documents Parallel's MCP silently dropping source_policy.include_domains — assume your dependencies do the same until proven otherwise.
- **For one internal eval, split a single task into 3-5 checkpoint assertions and add a 'no result credited until reseeded' gate.**
  - surface: eval
  - rationale: SciAgentArena and AutoResearch independently converged on stepwise verification — final-answer scoring is now the weak default.
- **Map your agent fleet to DeepMind's D1-D4 / R1-R3 grid on one page and identify the highest D×R cell with zero supervisor coverage.**
  - surface: architecture
  - rationale: Cheaper to import DeepMind's taxonomy than to invent one; the gap-spotting exercise itself is the deliverable.

## Watchlist

- **Midjourney Scanner reconstruction model release vs proprietary hold**
  - revisit when: When Midjourney publishes (or pointedly does not publish) the reconstruction model weights, revisit — that signals whether frontier labs treat physical-world data acquisition as open infra or as moat.
- **Cursor default routing under SpaceX/xAI ownership**
  - revisit when: When Cursor announces any change to default model routing or pricing after the $60B SpaceX close, revisit dependency portability.
- **Every Eval Ever JSON schema adoption by harness authors**
  - revisit when: When a major harness (lm-eval, OpenAI Evals, Inspect) ships a built-in exporter to the EveryEvalEver schema, revisit — that's the moment the typed-artifact pattern wins the eval lane.
- **MCP enterprise-managed auth rollout to Slack and beyond Okta**
  - revisit when: When Slack lands in the IdP-managed connector list, or when Entra/Auth0 join Okta, revisit your MCP rollout plan — the gating constraint disappears.
- **GPT-5.6 launch and the sample-efficiency framing**
  - revisit when: When OpenAI ships the next frontier release, revisit Dwarkesh's data-black-hole thesis — if scaling delivers expected gains, the contrarian case weakens; if it underdelivers, expect a capital-allocation rethink.
- **AI Daily Brief and Stratechery coverage of Fable 5 / Project Glasswing access status**
  - revisit when: When ~200-org Project Glasswing access changes (revoked, expanded, or formalized), revisit provider-risk matrix and the urgency of the multi-vendor routing work.

## Sources reviewed

- Anthropic News
- Anthropic Research
- Anthropic / Claude.com
- Anthropic / GitHub (Claude Code changelog)
- Google DeepMind Blog
- OpenAI Help Center (release notes)
- OpenAI Cookbook
- OpenAI Cookbook (PR #2783)
- OpenAI Cookbook (PR #2670)
- Hugging Face Blog
- Hugging Face Blog (ServiceNow)
- Hugging Face
- Simon Willison weblog
- AI News by Smol AI
- Dwarkesh Patel
- latent.space
- The AI Daily Brief
- Hacker News (front page)
- Jason Liu (jxnl.co)
- Stratechery
- Exponential View
- Platformer
- The Information
- Vercel
- Vercel / The Register
- Google Cloud / MarkTechPost
- arXiv (cs.AI)

## Lane notes

**primary-source**: The week's primary-source signal clusters tightly around agent-runtime hardening on three vendors at once. Anthropic shipped artifacts inside Claude Code, IdP-managed MCP connectors, and a Claude Code patch that blocks destructive git in auto mode. DeepMind published a capability-tiered AI Control Roadmap that treats internal agents as insider threats with MITRE-ATT&CK-style tactics and trusted supervisors. OpenAI made scheduled tasks GA, sunset Pulse, and shipped Codex Record & Replay so a demonstrated workflow becomes a reusable skill. HuggingFace echoed the eval-discipline thread with two posts on tool-specific agent benchmarks and a MosaicLeaks adversarial information-flow suite. The only non-agent primary-source piece was Anthropic's Korean expansion (Seoul office, Naver/Samsung/LG deployments, MOU with KAISI), plus a paired research post arguing domain expertise, not coding background, predicts agent productivity. Meta AI blog was silent in window; OpenAI's own news page and several OpenAI URLs returned 403, so OpenAI items rely on the help-center release notes plus releasebot mirror.

**fast-signal**: Two patterns dominated the lane this week. First, the Fable 5 fallout deepened: the AI Daily Brief ran four consecutive episodes on the US export-control shutdown of Anthropic's Fable 5 and Mythos 5, with explicit framing that the trigger was Amazon researchers using a 'fix this code' prompt instead of a true jailbreak, and that ~200 orgs retained access via Project Glasswing. The crisis created competitive oxygen that immediately got consumed by GLM-5.2 (Z.ai, MIT-licensed, 744B MoE, 1M context with IndexShare sparse-attention), covered by Simon Willison, Smol AI across three issues, and Hacker News (#1 story June 17). Second, the practitioner conversation shifted from 'which model' to 'which integrated system': @_xjdr's Noumena Code argument that git breaks under concurrent agents, Vicki Boykis demonstrating local Gemma-4 + Pi + LM Studio is now production-adjacent, MCP zero-touch OAuth landing on HN, and Anjney Midha on Latent Space pushing horizontal compute pooling ('FLOPs flow like megawatts') while naming the sub-10% MFU at xAI. Dwarkesh's solo essay on the sample-efficiency 'data black hole' was the contrarian capability take of the week. Sources swept: Simon Willison, Latent.Space, AI Daily Brief, Dwarkesh, Smol AI, Hacker News. Failed: Charity Majors substack URL returned 404.

**builder-practice**: Thin week for long-form practitioner blogs (Hamel, Eugene Yan, Chip Huyen, Applied LLMs all silent in window; Jason Liu shipped one post). The volume sat in the OpenAI Cookbook, where four cookbook-side merges landed in five days, three of them clustered around Workspace Agents as a callable runtime: new API-trigger notebook, deployment-manager UI polish, and a grounded-answer simplification that publicly documents an MCP parameter being silently ignored. The throughline is operational: agents are being treated as named, triggerable, traceable services instead of as chat surfaces, and the lessons are about plumbing (auth tokens, idempotency keys, container names, MCP parameter trust) instead of prompting. Liu's post fits the same arc from the user side - routing tasks to the narrowest mechanism and codifying the rules in AGENTS.md. Anthropic Cookbook was quiet this window.

**strategy**: The lane this week was almost entirely the Fable 5 / Mythos 5 fallout. Thompson devoted three Stratechery pieces (Mon, Wed, Fri) to it, framing Anthropic's safety posture as the strategic root cause; Azhar tied it to a broader 'time to pause' alignment of the three frontier labs; The Information set the policy boundary by reporting Commerce will not (yet) extend the action to other labs. The second thread was AI org and capex shape: EV's data roundup put hard numbers on the 650x per-employee AI-spend gap and 40% AI-attributed May layoffs, and Platformer's Kuyda interview gave the matching org-design claim from a working founder ('no junior hires, 1,000x engineer'). A third smaller thread, agent commerce, surfaced through Thompson's Morton interview (ChatGPT checkout underperforming, Shopify durable) and the SpaceX-acquires-Cursor close, which together suggest the agentic surface is consolidating into platform owners (Musk/xAI, Shopify, Anthropic) faster than into the assistant chat layer. Benedict Evans published no essay in-window.

**frontier-scout**: The lane this week split cleanly into two patterns. First, directory-as-agent kept hardening as a convention: Vercel Eve shipped a framework where the agent IS a directory of files (Apache-2.0, github.com/vercel/eve), Google Cloud's OKF v0.1 standardized the same pattern for org knowledge bundles, Hugging Face extended it remotely with agents.md on Spaces, and the hf CLI added env-var detection so the same command renders differently for humans and agents. The convergence is on filesystem contracts over programmatic registration, which is the same direction the user's CDCP work favors. Second, the eval lane sharpened markedly: ALE (1000+ occupationally-grounded tasks, <1% pass rate), WeaveBench (forces GUI+CLI cooperation with trajectory audits), SciAgentArena (stepwise verification, agent-agnostic env), Every Eval Ever (unified JSON schema + 22k-model seed corpus on HF), PowerAgentBench-Dyn (simulation-budget constraints), AutoResearch (no-result-credited-without-audit gates), and ABC-Bench (wet-lab validated biosecurity). The throughline is that benchmark authors are no longer trusting final-answer grades — they're requiring stepwise checks, reseeded verification, channel-cooperation, or physical execution. Nothing this week looked like genuine agent-topology novelty; the action was in artifact formats and verification gates. Fable 5 fallout did not surface in primary frontier sources this week.
