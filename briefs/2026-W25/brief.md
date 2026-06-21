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

The week's center of gravity sat in the agent runtime, hardening into infrastructure on every front at once while the Fable 5 export-control aftershock kept reshaping the supply chain underneath it. Three vendors shipped near-identical primitives in the same five days (Anthropic's IdP-managed MCP + auto-mode git denylist, OpenAI's Record-and-Replay + scheduled-tasks GA, DeepMind's capability-tiered control roadmap), and two independent frameworks (Vercel Eve, Google OKF) committed to the same filesystem-as-contract pattern that AGENTS.md has been previewing for months. Underneath, a second convergence: benchmark authors stopped trusting final-answer grades — ALE, WeaveBench, SciAgentArena, AutoResearch, MosaicLeaks, and ABC-Bench all require stepwise checks, channel-cooperation, reseeded verification, or physical execution. The Fable 5 fallout drove the strategic backdrop (export-control risk is now a real entry in your provider matrix; GLM-5.2 at MIT-license, 1M context, $0.06/task is the substitute), but the operational story is that the policy engine, the identity layer, the trigger surface, the eval gate, and the role-contract directory are all becoming first-class artifacts. The control plane the user has been arguing for is now the dominant industry shape — and the typed-artifact discipline (directories, manifests, stepwise gates) is winning over framework-driven registration.

7 top signals, 6 watchlist items, 39 sources reviewed (7 failed).

## Top signals

### 1. Claude Code auto-mode blocks destructive git, ships artifacts and IdP-managed MCP in the same week

**Source:** [Anthropic / GitHub (Claude Code changelog)](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

**Payload:** Three Anthropic releases landed in five days: 2.1.183 blocks destructive git verbs in auto mode unless explicitly authorized, artifacts publish live versioned web pages from a Claude Code session, and MCP connectors now provision through Okta groups.

**Mechanism:** Safety enforcement moved from prompt to tool-policy gate (auto mode intercepts git reset --hard, force push, branch -D pre-execution); artifact delivery moved from chat transcript to its own URL with version history; MCP auth moved from per-user OAuth flow to IdP group mapping at admin time.

**Why it matters:** Confirms auto-mode is the default agent surface and that Anthropic is hardening it at three independent layers simultaneously — execution policy, delivery surface, and identity. Anyone running their own agent harness can copy the same three gates instead of inventing them.

**Reusable pattern:** Policy at the gate, not in the prompt

**Action surface:** tool-policy

**Try:** Copy the 2.1.183 destructive-git verb list into your own agent harness as an explicit-confirm denylist; publish one session's output as an artifact URL instead of a Slack writeup; tag each MCP connector as IdP-eligible.

**Systems map:** Three independent failure modes (irreversible action, ephemeral output, per-user auth burden) get pushed down to harness-level enforcement so the model never has to be trusted to follow a rule it could be argued out of.

**Transferable principle:** Move safety, delivery, and identity out of prompt instructions and into the harness — applies equally to any agent stack with shell access, ephemeral outputs, or OAuth-bound tools (e.g., your own CDCP role contracts gating tool calls via a policy engine rather than a system prompt).

**Confidence:** high

---

### 2. DeepMind's AI Control Roadmap treats internal agents as insider threats

**Source:** [Google DeepMind Blog](https://deepmind.google/blog/securing-the-future-of-ai-agents/)

**Payload:** Defense-in-depth framework with MITRE-ATT&CK-style tactics, trusted AI supervisors that can block actions pre-execution, and defenses scaled across a D1-D4 detection-evasion × R1-R3 harm-execution grid.

**Mechanism:** Live monitoring grounded in ~1M coding-agent trajectories where most flagged incidents trace to misinterpretation or overeagerness rather than adversarial intent; supervisor agents sit between the actor and the tool call and can veto pre-execution.

**Why it matters:** Provides a concrete capability-tiered taxonomy to borrow rather than invent; aligns directly with the role-contracts + policy-engine + event-ledger pattern. The empirical finding that overeagerness dominates adversariality changes what your detector should optimize for.

**Reusable pattern:** Capability-tiered control matrix instead of a single bar

**Action surface:** architecture

**Try:** Map your agent fleet to the D1-D4 / R1-R3 grid on one page; identify the highest D×R cell with zero supervisor coverage and decide whether you write a supervisor or remove the capability.

**Systems map:** A trusted-but-bounded second model wraps the actor model the same way an OS kernel mediates a user-mode process — the asymmetry is that the supervisor's job is narrower than the actor's, so it can be smaller and more verifiable.

**Transferable principle:** Pair every capable actor with a narrower verifier sitting on the action path — applies to code review (lint as actor-verifier), to financial controls (the four-eyes principle), and to any agent role contract where the action surface exceeds the trust budget.

**Confidence:** high

---

### 3. GLM-5.2 ships MIT-licensed at 1M context and crosses the price threshold below Opus

**Source:** [Simon Willison weblog](https://simonwillison.net/2026/Jun/17/glm-52/)

**Payload:** Z.ai released GLM-5.2, a 744B-MoE / 40B-active MIT-licensed model with 1M context that ranks #1 on Artificial Analysis's open-weight Intelligence Index and hits $2.40/task on AA-Briefcase vs Opus 4.8 at $10.40.

**Mechanism:** IndexShare sparse-attention reuses top-k indices across layer groups, cutting 1M-context inference cost ~2.9x; day-zero deployment in vLLM, SGLang, Ollama, OpenRouter, Cloudflare Workers AI, Baseten; Terminal-Bench 2.1 first open model over 80.

**Why it matters:** The pricing curve crossed the threshold where defaulting to Opus for agentic batch work is hard to justify, and arrived precisely as Fable 5 export controls created the substitute-demand vacuum. Open-weight share on OpenRouter moved from 40% to 60% in three months.

**Reusable pattern:** Architectural lever (IndexShare) plus license (MIT) plus day-zero ecosystem coverage is what makes an open model actually substitutable

**Action surface:** tool-policy

**Try:** Route one real coding task through GLM-5.2 via OpenRouter; log token cost and quality delta vs your current default and decide whether to add it as the fallback in a router config.

**Systems map:** When a serious open-weight model lands inside the existing inference-server ecosystem the same day it's announced, the switching cost collapses from weeks (adapter PRs, sandbox testing) to hours (model id change in the gateway).

**Transferable principle:** Lock-in to a closed model is only durable while either capability or ecosystem support is missing on the open side — same dynamic recently played out in vector DBs and is now playing out in frontier text models. Maintain a fallback path you've actually exercised, not just one you've drawn.

**Confidence:** high

---

### 4. Anthropic finds domain expertise, not coding background, predicts how much work Claude does

**Source:** [Anthropic Research](https://www.anthropic.com/research/claude-code-expertise)

**Payload:** Analysis of ~400k Claude Code sessions from ~235k users (Oct 2025–Apr 2026) decomposes each session into planning vs execution decisions: users contribute ~70% of planning, Claude ~80% of execution, and higher user domain expertise correlates with longer effective Claude turns per instruction.

**Mechanism:** Per-session decision attribution lets the team separate the 'who specifies' axis from the 'who types' axis; domain expertise turns out to be the variable that lengthens the productive Claude turn, not coding ability.

**Why it matters:** Directly reframes hiring and team composition for agent-using orgs: the bottleneck is people who can specify the right thing, not people who can type code. Maps cleanly onto role-contract design — the planner role is the scarce one.

**Reusable pattern:** Separate the planning role from the execution role and measure each

**Action surface:** agent-role

**Try:** For one repo, log who triggers each Claude Code session and rate planning specificity 1-5; over a week compare specificity score vs PR merge rate and look at whether the curve is monotonic.

**Systems map:** The agent absorbs execution decisions cheaply, which shifts the marginal value of the human upstream into specification — the same shift that happened when compilers absorbed register allocation.

**Transferable principle:** Whenever an agent reliably handles execution, the binding constraint moves to specification — applies to legal drafting (the brief, not the citation lookup), ops runbooks (the right question, not the right kubectl), and CDCP role design (the planner contract is where the scarce knowledge lives).

**Confidence:** high

---

### 5. Vercel Eve and Google OKF commit to filesystem-as-contract on the same axis

**Source:** [Vercel](https://vercel.com/changelog/introducing-eve-an-open-source-agent-framework)

**Payload:** Vercel released Eve at Ship 26 London, an Apache-2.0 TypeScript framework where every agent is a directory (instructions.md, tools/, skills/, connections/, channels/, schedules/, subagents/) compiled to a Vercel Function — and Google Cloud independently shipped OKF v0.1, a markdown-plus-YAML spec for portable agent context bundles.

**Mechanism:** Eve does build-time discovery from file paths and prepends instructions.md to every model call with no decorator-based registration; OKF requires only a 'type' field in YAML frontmatter and renders to an interactive graph via one self-contained HTML file; both treat the directory layout as the source of truth.

**Why it matters:** The AGENTS.md / skills / decisions / dreams directory pattern the user has been building toward is now the de facto industry convention for both runtime (Eve) and portable knowledge (OKF). Worth lifting both as references when finalizing CDCP role-contract directory layout.

**Reusable pattern:** Filesystem layout as the API surface, build-time discovery over runtime registration

**Action surface:** agent-role

**Try:** Clone github.com/vercel/eve, scaffold one agent with a single tool and a skills/onboarding.md, then diff its compiled manifest against an equivalent CDCP role contract to see what registration boilerplate disappears.

**Systems map:** A directory is diffable, reviewable, and grep-able in a way a runtime registry never is; making the directory authoritative converts framework state into git state, which makes the whole system more inspectable for free.

**Transferable principle:** When the framework's authoritative state lives in code rather than the filesystem, you've imported a parallel source-of-truth — same anti-pattern as ORM migrations diverging from schema or IaC diverging from console state. Push state to the filesystem and the diff tools you already have start working.

**Confidence:** high

---

### 6. Benchmark authors converge on stepwise verification, ditch final-answer grading

**Source:** [arXiv (cs.AI)](https://arxiv.org/abs/2606.12736)

**Payload:** Six independent agent benchmarks released in-window — ALE, WeaveBench, SciAgentArena, AutoResearch, MosaicLeaks, ABC-Bench — all reject single-score evaluation in favor of stepwise checks, trajectory audits, reseeded verification, channel cooperation, information-flow probes, or wet-lab execution.

**Mechanism:** SciAgentArena requires 3-5 checkpoint assertions per task; WeaveBench fails GUI-only or CLI-only agents (<3.5%) and audits full action sequences for fabricated screenshots; AutoResearch's audit layer requires seed-noise threshold, reseeded verification, and leave-one-out pruning before any improvement is credited; ABC-Bench validates one task on a physical OpenTrons robot.

**Why it matters:** Final-answer scoring is now the weak default. If your eval reports a single score per task, you're already behind the methodology curve — and you're vulnerable to agents that learn to fabricate the final answer without doing the work.

**Reusable pattern:** Verification gates per checkpoint, not per task

**Action surface:** eval

**Try:** Split one of your existing single-score evals into 3-5 checkpoint assertions; add a 'no result credited until reseeded' gate to any auto-tuning agent and log how many of its self-reported wins disappear.

**Systems map:** Final-answer grading creates an attack surface (Goodhart on the score) that stepwise verification closes by forcing the trajectory to be coherent at each checkpoint — same logic as why type systems catch more bugs than test suites alone.

**Transferable principle:** Wherever a metric can be optimized without the underlying behavior changing, replace it with a sequence of independent checks — applies to code review (CI matrix), to scientific results (preregistration + ablations), and to any agent eval where the agent could short-circuit the work.

**Confidence:** high

---

### 7. Fable 5 export controls reframe Anthropic dependency as a supply-chain risk with jurisdiction

**Source:** [Stratechery](https://stratechery.com/2026/the-state-of-fable-the-jailbreak-problem-spacex-acquires-cursor/)

**Payload:** Commerce's BIS export-control order on Fable 5 and Mythos 5 forced Anthropic into a global pull; The Information separately reports Commerce is not currently planning to extend the same action to OpenAI or Google.

**Mechanism:** The trigger was a manual multi-prompt sequence (Katie Moussouris clarified researchers used 'fix this code' prompting, not a universal jailbreak), meaning 'AI safety incident' classification can be triggered by routine prompt engineering — and the resulting export action operates on a few-days timeline.

**Why it matters:** Builders now have two new supply-chain fields to add per dependency: jurisdiction and owner. The Anthropic-specific scoping changes the timing of multi-vendor routing work (this quarter for Anthropic-heavy stacks, less urgent for others) but does not eliminate it.

**Reusable pattern:** Per-dependency jurisdiction + owner fields plus a pre-written 1-week-outage contingency

**Action surface:** tool-policy

**Try:** In your model/tool registry add 'jurisdiction' and 'owner' fields per dependency; tag Anthropic as 'active US export-control risk'; write a one-page contingency for (a) Claude frontier access disappearing for 72h and (b) Cursor's default routing changing to xAI under SpaceX ownership.

**Systems map:** Sovereign-policy actions on closed-weight models behave like sudden vendor deprecation, but with no migration period and no public roadmap — the only mitigation is a pre-exercised fallback path with a different jurisdiction and owner.

**Transferable principle:** Treat any single-jurisdiction closed-source critical dependency as a 72-hour outage risk and pre-build the swap — same playbook as cloud-region failover, payments-processor redundancy, or DNS-provider diversity. The premium is small until the day it's infinite.

**Confidence:** high

---

## Reusable patterns

- **Directory-as-contract beats decorator-as-registration** — Eve, OKF, agents.md-on-Spaces, and AGENTS.md routing all converge on filesystem layout as the source of truth for agent capability and context — registration boilerplate is the smell.
- **Tool-policy enforcement moves from prompt to runtime gate** — Claude Code's auto-mode git denylist, DeepMind's pre-execution supervisors, and Passport's short-lived-credential issuance all push safety from prompt instructions down into the harness layer that actually runs commands.
- **Evals must verify stepwise, not just finally** — SciAgentArena (checkpoints), WeaveBench (trajectory audits), AutoResearch (reseeded verification gates), MosaicLeaks (information-flow probes), and ABC-Bench (wet-lab closure) all reject the single-score grade — the artifact discipline has reached evaluation.
- **Supply-chain risk is now a per-dependency field, not a vibe** — Fable 5 export controls + SpaceX-acquires-Cursor mean 'jurisdiction' and 'owner' belong in your model/tool registry alongside latency and price, with one-week-outage contingencies pre-written for the high-D×R cells.

## Action queue

- **Add a 'Routing' section and an irreversible-action approval rule to AGENTS.md in your most-used repo; encode at least three task→mechanism mappings.**
  - surface: agent-role
  - rationale: Jason Liu's three-mechanism routing is the cheapest, highest-yield import this week — turns 'one agent does everything' into a policy artifact you can diff.
- **Stand up a fallback-router config with one open-weight primary (GLM-5.2) and one closed-weight premium, threshold on cost/capability, log which path each request took for a week.**
  - surface: tool-policy
  - rationale: Fable 5 fallout + GLM-5.2's $0.06-vs-$0.49 cost gap means single-vendor defaults are now a vendor-risk decision, not a default.
- **Audit every long-lived token in your agent harness; for each MCP/connector, mark IdP-eligible vs not and stub the short-lived-credential issuer that replaces it.**
  - surface: tool-policy
  - rationale: Anthropic enterprise-managed MCP and Vercel Passport landed in the same week — the runtime is moving to IdP-issued short-lived creds and your inventory is the prerequisite work.
- **Pick one MCP tool you depend on and write an eval that asserts a passed parameter actually changed the output; treat silent-ignore as a bug.**
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

**fast-signal**: Two patterns dominated the lane this week. First, the Fable 5 fallout deepened: the AI Daily Brief ran four consecutive episodes on the US export-control shutdown of Anthropic's Fable 5 and Mythos 5, with explicit framing that the trigger was Amazon researchers using a 'fix this code' prompt rather than a true jailbreak, and that ~200 orgs retained access via Project Glasswing. The crisis created competitive oxygen that immediately got consumed by GLM-5.2 (Z.ai, MIT-licensed, 744B MoE, 1M context with IndexShare sparse-attention), covered by Simon Willison, Smol AI across three issues, and Hacker News (#1 story June 17). Second, the practitioner conversation shifted from 'which model' to 'which integrated system': @_xjdr's Noumena Code argument that git breaks under concurrent agents, Vicki Boykis demonstrating local Gemma-4 + Pi + LM Studio is now production-adjacent, MCP zero-touch OAuth landing on HN, and Anjney Midha on Latent Space pushing horizontal compute pooling ('FLOPs flow like megawatts') while naming the sub-10% MFU at xAI. Dwarkesh's solo essay on the sample-efficiency 'data black hole' was the contrarian capability take of the week. Sources swept: Simon Willison, Latent.Space, AI Daily Brief, Dwarkesh, Smol AI, Hacker News. Failed: Charity Majors substack URL returned 404.

**builder-practice**: Thin week for long-form practitioner blogs (Hamel, Eugene Yan, Chip Huyen, Applied LLMs all silent in window; Jason Liu shipped one post). The volume sat in the OpenAI Cookbook, where four cookbook-side merges landed in five days, three of them clustered around Workspace Agents as a callable runtime: new API-trigger notebook, deployment-manager UI polish, and a grounded-answer simplification that publicly documents an MCP parameter being silently ignored. The throughline is operational: agents are being treated as named, triggerable, traceable services rather than as chat surfaces, and the lessons are about plumbing (auth tokens, idempotency keys, container names, MCP parameter trust) rather than prompting. Liu's post fits the same arc from the user side - routing tasks to the narrowest mechanism and codifying the rules in AGENTS.md. Anthropic Cookbook was quiet this window.

**strategy**: The lane this week was almost entirely the Fable 5 / Mythos 5 fallout. Thompson devoted three Stratechery pieces (Mon, Wed, Fri) to it, framing Anthropic's safety posture as the strategic root cause; Azhar tied it to a broader 'time to pause' alignment of the three frontier labs; The Information set the policy boundary by reporting Commerce will not (yet) extend the action to other labs. The second thread was AI org and capex shape: EV's data roundup put hard numbers on the 650x per-employee AI-spend gap and 40% AI-attributed May layoffs, and Platformer's Kuyda interview gave the matching org-design claim from a working founder ('no junior hires, 1,000x engineer'). A third smaller thread, agent commerce, surfaced through Thompson's Morton interview (ChatGPT checkout underperforming, Shopify durable) and the SpaceX-acquires-Cursor close, which together suggest the agentic surface is consolidating into platform owners (Musk/xAI, Shopify, Anthropic) faster than into the assistant chat layer. Benedict Evans published no essay in-window.

**frontier-scout**: The lane this week split cleanly into two patterns. First, directory-as-agent kept hardening as a convention: Vercel Eve shipped a framework where the agent literally IS a directory of files (Apache-2.0, github.com/vercel/eve), Google Cloud's OKF v0.1 standardized the same pattern for org knowledge bundles, Hugging Face extended it remotely with agents.md on Spaces, and the hf CLI added env-var detection so the same command renders differently for humans and agents. The convergence is on filesystem contracts over programmatic registration, which is the same direction the user's CDCP work favors. Second, the eval lane sharpened markedly: ALE (1000+ occupationally-grounded tasks, <1% pass rate), WeaveBench (forces GUI+CLI cooperation with trajectory audits), SciAgentArena (stepwise verification, agent-agnostic env), Every Eval Ever (unified JSON schema + 22k-model seed corpus on HF), PowerAgentBench-Dyn (simulation-budget constraints), AutoResearch (no-result-credited-without-audit gates), and ABC-Bench (wet-lab validated biosecurity). The throughline is that benchmark authors are no longer trusting final-answer grades — they're requiring stepwise checks, reseeded verification, channel-cooperation, or physical execution. Nothing this week looked like genuine agent-topology novelty; the action was in artifact formats and verification gates. Fable 5 fallout did not surface in primary frontier sources this week.
