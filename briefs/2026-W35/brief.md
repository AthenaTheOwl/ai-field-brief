<!--
iso_week: 2026-W35
through_date: 2026-08-30
profile_id: builder-tpm
registry_version: 14
matrix_run_id: MTRX-W35-contracts-outside-the-prompt
-->

# The repository overview cost twenty percent and bought nothing.

**Week 35 through 2026-08-30 - Vol. 18**

## Field thesis

Four things that used to live inside a prompt got moved out of it this week and handed to something with a contract. Device control got a specification instead of a bespoke driver. Capability discovery got a service that answers before invocation instead of a catalogue that rides in the context window. Compaction got a tool and a fire rule instead of a token counter. Alignment repair got a pipeline with a scorer that does not report to the optimizer. Running underneath all of it, a controlled study measured the one artifact this repository and most others treat as free — the context file committed at the root — and found it does not generally improve task success while adding more than twenty percent to inference cost. The week rewards a specific discipline: name the thing you are relying on, give it an owner outside the model, then measure whether it earns its tokens.

## Top signals

### 1. The context file everyone commits was measured, and the overview section failed

**Sources:** [Evaluating AGENTS.md](https://arxiv.org/abs/2602.11988) and [Is Progressive Disclosure All You Need for Long-Context Agents?](https://arxiv.org/abs/2607.17598)

**Payload:** Gloaguen, Mündler, Müller, Raychev and Vechev (ETH Zurich SRI Lab and LogicStar.ai) evaluated coding agents on benchmark tasks and on issues drawn from repositories carrying developer-committed context files. Providing context files "does not generally improve task success rates, while increasing inference cost by over 20% on average," across different models, different agents, and both generated and human-written files. Instructions inside those files were followed; repository overviews, the most recommended content, were not helpful. He, Zhao, Wang and Chen reach an adjacent result for the tiered variant: one level of progressive disclosure is enough, a second routing level never helps and sometimes breaks accuracy, and the gain from the pattern at all depends on the harness more than on the pattern itself.

**Mechanism:** A context file pays its token cost on every turn and returns value only where it carries something the agent could not obtain by looking. Conventions, prohibitions, and non-obvious build steps qualify. A description of the directory tree does not, because a competent file-navigation harness recovers it on demand at lower cost. The progressive-disclosure result explains why the benefit is harness-dependent: where the agent already greps and reads well, the disclosure layer duplicates work the harness does; where it navigates poorly, the layer substitutes for the missing capability.

**Why it matters:** This repository publishes an `AGENTS.md` and a `.agents/AGENTS.md`, and 2026-W28 argued from the wiki-memory pick that legible flat-file agent memory earns review. That principle survives for the instruction half and takes damage on the overview half. The honest reading is that the repository's own contract files should be audited section by section against this split instead of being treated as a settled good.

**Reusable pattern:** Split every context file into instructions and description. Keep instructions that constrain behaviour, drop descriptions the agent can rebuild by reading, and measure the file's contribution the way you would measure a retrieval change — with and without, on the same task set, counting tokens.

**Action surface:** context

**Try this week:** Run the factory's held-out cases twice, once with `AGENTS.md` mounted and once with only its imperative sections, and record pass rate, tokens, and cost per accepted outcome for each. Delete whatever section cannot show a difference.

**Systems map:** repository contract file -> per-turn token cost -> instruction compliance and navigation savings -> measured task success -> keep or delete the section.

**Transferable principle:** Any artifact that is loaded unconditionally must justify itself against the alternative of being fetched on demand. The same test applies to a system prompt's glossary, a preloaded tool catalogue, and a standing dashboard nobody opens.

**Falsification test:** If an ablation on this repository's own briefs shows the overview sections of `AGENTS.md` raising first-pass acceptance on held-out cases at equal or lower cost, the finding does not transfer to this corpus and the sections stay.

**Adoption ladder:**
  - Minimum viable: tag each section of `AGENTS.md` as instruction or description.
  - Mid: run the paired ablation on one held-out case set and record the token delta.
  - Full: gate context-file additions on a measured contribution, the way a source addition is gated on a DEC.
  - Monitoring: tokens per run attributable to context files; pass rate delta with and without; number of sections deleted per quarter.

**Confidence:** high

**Evidence:** MTRX-W35-CONTEXT-FILE-NULL-RESULT, MTRX-W35-DISCLOSURE-ONE-LEVEL

### 2. Compaction stopped being a number crossing a line

**Source:** [Self-Compacting Language Model Agents](https://arxiv.org/abs/2606.23525)

**Payload:** Li, Zhang, Jurayj, Wang, Jin, Farajtabar, Nalisnick and Khashabi pair two inference-time elements: a compaction tool the model invokes, and a short rubric saying when to fire (a sub-task resolved, the trajectory converging) and when to suppress (mid-derivation, or stuck). Across six benchmarks and seven models, the pairing improves over a no-summarisation baseline by up to 18.1 points on math and 5 to 9 points on agentic search at 30 to 70 percent lower cost per question, with no fine-tuning. The paper is explicit that neither half works alone: the tool without the rubric is invoked at unhelpful moments or skipped, and the rubric without the tool cannot act.

**Mechanism:** A token counter knows the size of the context and nothing about the shape of the work. Firing on a threshold discards partial results mid-derivation as readily as it discards a closed sub-task, and the observable cost is re-derivation — the agent returns from compaction and redoes work it had already paid for. Moving the trigger to a semantic boundary the model can recognise removes the mistimed compactions, which is why the method beats fixed-interval summarisation on cost as well as quality.

**Why it matters:** 2026-W34 held the `lean-v2` context profile opt-in pending a paired continuation campaign at the compaction boundary. This gives that campaign a second arm worth running: beyond tuning how much context survives, test whether the trigger itself should move. The factory's runs already emit checkpoints, so the boundary is available.

**Reusable pattern:** When a policy fires on a resource threshold but its cost depends on structure, give the structure a vote. Keep the threshold as a floor that prevents a hard failure and let the semantic rule own the ordinary case.

**Action surface:** context

**Try this week:** Instrument re-derivation directly. For the next twenty factory runs that compact, count post-compaction steps that repeat a tool call already made with the same arguments earlier in the run, and report the count per compaction event.

**Systems map:** trajectory structure -> compaction trigger -> discarded intermediate results -> repeated tool calls -> cost per accepted outcome.

**Transferable principle:** A trigger tuned to a resource is a proxy for a trigger tuned to work state, and proxies fail where the two diverge. Cache eviction, autoscaler cooldowns, and batch-job checkpointing carry the same mismatch.

**Falsification test:** If instrumented runs show near-zero repeated tool calls after threshold compaction, this harness is already compacting at safe moments and the rubric buys only its own token cost.

**Adoption ladder:**
  - Minimum viable: count repeated tool calls after each compaction event.
  - Mid: add a fire-or-suppress rubric to the compaction prompt and compare re-derivation counts on the same cases.
  - Full: expose compaction as a model-invocable tool with the threshold retained as a backstop.
  - Monitoring: repeated tool calls per compaction; tokens per accepted outcome; hard context-limit errors, which should stay at zero.

**Confidence:** medium

**Evidence:** MTRX-W35-SEMANTIC-COMPACTION

### 3. Five permission checks in one release had all run against something that could still change

**Source:** [anthropics/claude-code CHANGELOG 2.1.251](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

**Payload:** The August 28 release fixed file tools following a symlink swapped inside the working directory after the permission check had passed; Grep and Glob not applying `Read(...)` deny rules to files reached through a symlinked search path; plugin commands in a marketplace entry able to point outside the plugin directory; the Workflow tool reading a `scriptPath` outside the session's readable set before the permission check ran; and project settings able to turn on raw API body logging or route beta tracing past an endpoint pinned by managed settings. The same release added `PreModelSwitch` and `PostModelSwitch` hook events and a per-session prompt-cache line in `/cost`.

**Mechanism:** Every one of those five has the same shape. A decision was made about a name, and the thing the name pointed at was allowed to change, or a second code path reached the same resource without consulting the decision. The symlink cases are time-of-check to time-of-use; the Grep and Glob case and the settings case are coverage gaps where a rule guarded one door. An agent harness multiplies both, because it holds many tools that reach the filesystem and many settings scopes that can widen a boundary.

**Why it matters:** This portfolio runs agents with file tools under permission rules and has been treating an allowlist entry as a boundary. An allowlist is a boundary only if every path that reaches the resource consults it and the resource cannot be substituted between the check and the read. Both assumptions failed here in a codebase with more review attention than ours.

**Reusable pattern:** Enumerate the paths that reach a protected resource, then assert that each consults the same decision function. Resolve to a stable identity — a file descriptor, an inode, a content hash — before acting on a permitted name.

**Action surface:** security

**Try this week:** Write five deny-rule tests against the portfolio's own agent surfaces: a symlink swapped between check and read, a denied file reached through a symlinked directory, a denied file passed as an option value instead of an operand, a config scope that widens a managed setting, and a second tool that reads the same path. Record which of the five pass today.

**Systems map:** protected resource -> multiple tool paths -> one permission decision -> name resolved again at use time -> boundary holds or does not.

**Transferable principle:** A check on a name is not a check on a thing. The gap appears anywhere identity is resolved twice — signed URLs, container image tags, package versions pinned at audit time and resolved again at install.

**Falsification test:** If all five tests pass unchanged against the portfolio's current agent surfaces, this class of defect does not apply here and the effort belongs elsewhere.

**Adoption ladder:**
  - Minimum viable: the five-test deny-rule suite, run once, with results recorded.
  - Mid: the suite runs in CI on every change to a tool surface or permission rule.
  - Full: every new tool that reads or writes registers itself against the shared decision function, and registration is checked by a gate.
  - Monitoring: tool surfaces reaching the filesystem without going through the shared check; deny-rule tests failing per release; upstream permission fixes per month.

**Confidence:** high

**Evidence:** MTRX-W35-PERMISSION-BOUNDARY-COVERAGE

### 4. Agents got a device interface, and it came with a recovery number

**Source:** [Previewing the Model Hardware Standard](https://www.anthropic.com/news/model-hardware-standard-research-preview)

**Payload:** Anthropic opened a research preview on August 27 of a shared specification for agents to operate physical devices — microscopes, liquid handlers, robotic arms — with early partners including AWS, Danaher, Tecan, QIAGEN, Doosan Robotics, Automata, Universal Robots, Hugging Face and Raspberry Pi. The specification is model-agnostic and reachable by any harness over standard protocols including MCP. The reported result worth carrying is from QuEra: an agent reached 99.3 percent success across 700 laser-lock recovery trials, against 58 percent for hand-written scripts.

**Mechanism:** The comparison is the useful part, and it is not a claim about intelligence. A hand-written recovery script encodes the failure modes its author anticipated and fails on the rest. An agent with a device interface and a stated goal can observe the actual state and try a path the script never contained. The specification matters because it removes the integration work that made this uneconomic — bespoke drivers per instrument, weeks of setup — and turns device capability into something declarable.

**Why it matters:** The transferable half lands well short of the laboratory. The portfolio has scripted recovery paths in its own runs: retry ladders, cleanup handlers, rollback steps. Each encodes an anticipated failure list, and 58 percent is a plausible number for how many real failures such a list covers. Physical actuation also raises the cost of a wrong action past anything a software rollback covers, which is why the interlock and approval design deserves attention before the capability does.

**Reusable pattern:** Where a recovery path is a fixed script, measure its success rate against the failures that occur in production, not the failures it was written for. Declare device or resource capability as data the caller can read, not as knowledge embedded in the caller.

**Action surface:** architecture

**Try this week:** Take the factory's most-invoked recovery path, list the failure modes it handles, then read the last fifty runs that entered it and classify each by whether the script's list covered the actual failure. Publish the coverage percentage.

**Systems map:** device or resource capability -> declared interface -> agent observes real state -> recovery attempt outside the scripted set -> measured success rate.

**Transferable principle:** A fixed recovery script is a snapshot of one engineer's failure model, and its success rate is bounded by that model's coverage. The same measurement applies to incident runbooks, retry policies, and data-quality repair rules.

**Falsification test:** If the last fifty entries into the recovery path were all covered by the scripted failure list, the script is adequate for this workload and an agent adds cost without headroom.

**Adoption ladder:**
  - Minimum viable: coverage percentage for one recovery path, measured against real failures.
  - Mid: the uncovered failures become explicit cases, either scripted or routed to a judged retry.
  - Full: recovery paths declare their handled set as data, and the gap between declared and observed is a tracked metric.
  - Monitoring: recovery-path coverage percentage; unhandled failure classes per month; irreversible actions taken inside a recovery path.

**Confidence:** medium

**Evidence:** MTRX-W35-DEVICE-INTERFACE-RECOVERY

### 5. Discovery moved in front of invocation, and stayed out of the runtime

**Source:** [Agentic Resource Discovery](https://agenticresourcediscovery.org/)

**Payload:** A cross-vendor discovery protocol published August 24 under Apache-2.0, with contributors from Microsoft, Google, Hugging Face, GoDaddy, Cisco, Databricks, GitHub, Nvidia, Salesforce, ServiceNow and Snowflake. A client asks what is available for a task and receives matching resources; an agentic resource is any external capability a client can call — an agent, MCP server, Skill, Canvas, Plugin, API, or workflow. The specification is explicit about its boundaries: it "sits entirely before invocation," it is not an execution runtime, it does not replace MCP or A2A, and it assumes many discovery services instead of one catalogue.

**Mechanism:** A tool catalogue in the context window costs tokens before the user's request is read and grows with the surface it describes. Moving the catalogue behind a query means the client pays for the ten results it matched, not the ten thousand it did not. Refusing to own invocation keeps the protocol small enough to sit beside MCP instead of competing with it.

**Why it matters:** 2026-W26 covered the single-vendor version of this idea from Hugging Face and rated it a Top signal. The change is the coalition and the explicit non-goal. A federated discovery layer is only useful if more than one service implements it, and the launch list is the first evidence that might happen. The portfolio's read-only MCP server is small enough that discovery costs nothing today; the entry to make now is the shape of the resource description, not the lookup.

**Reusable pattern:** Separate finding from calling. Give each capability a description a stranger's client can match against, and let the invocation contract stay where it already is.

**Action surface:** architecture

**Try this week:** Write an ARD-shaped description for the portfolio MCP server — what it is for, what it will answer, what it refuses — and check it against the specification's required fields. Keep the file whether or not a discovery service ever reads it; the exercise names the surface.

**Systems map:** capability -> published description -> discovery service index -> client query for a task -> matched subset -> native invocation.

**Transferable principle:** Catalogue size is a cost paid by every caller when the catalogue is pushed and by only the matching caller when it is pulled. Service registries, feature flags, and permission catalogues all cross this line as they grow.

**Falsification test:** If no discovery service outside the launch coalition indexes third-party resources within two quarters, this is a document and not a protocol, and the description work has no consumer.

**Adoption ladder:**
  - Minimum viable: one ARD-shaped description for one owned capability.
  - Mid: descriptions for every MCP surface in the portfolio, generated from the same source as the tool schemas.
  - Full: an internal discovery endpoint the portfolio's own agents query instead of loading catalogues.
  - Monitoring: tokens spent on tool schemas per run; number of tools loaded versus called; independent implementations of the specification.

**Confidence:** medium

**Evidence:** MTRX-W35-PRE-INVOCATION-DISCOVERY

### 6. Eval tasks got a spec, and the spec got calibrated against model tiers

**Source:** [How We Build Agent Environments & Tasks](https://www.langchain.com/blog/building-agent-environments-and-tasks)

**Payload:** Trivedy and Hollon describe a two-step pipeline: traces, code, or human input produce a markdown spec describing the task input, environment, and graders; the spec then produces an executable task and its environment. A world spec holds the knowledge shared across a dataset — data shape, trace-parsing scripts, rubric approach, synthetic data generation, backend APIs to mock, and common user questions mined from production traces. Tasks are refined by running them with real agents and reading trajectories, and difficulty is calibrated by running each task across model tiers to find where a stronger model exploits a weak task. They name the failure modes: tasks drift too easy, specs carry leaky abstractions, and human judgement stays in the loop.

**Mechanism:** Cross-tier calibration is the reusable part. A task that a strong model passes and a weak model fails may be measuring capability, or it may be offering the strong model a shortcut the author did not intend. Running both and reading the trajectory separates the two, which checks the task, not the agent. Writing the spec in prose before generating the executable form keeps the grader's intent inspectable after the code exists.

**Why it matters:** The factory's held-out cases were written directly as code, so their intent lives only in the assertions. A prose spec per case would make reward hacks visible as a mismatch between what the spec says and what the grader accepts. This costs one artifact per case and pays back the first time a case quietly stops measuring what it was written for.

**Reusable pattern:** Author the grader's intent in prose, generate the executable form from it, and calibrate difficulty by running the task across at least two capability tiers before trusting the score.

**Action surface:** eval

**Try this week:** Take three held-out factory cases and run each with two model tiers. Read the passing trajectory of the stronger model and mark any case where it passed by a route the case was not written to reward.

**Systems map:** production traces -> world spec -> task spec in prose -> generated task and environment -> cross-tier run -> reward-hack detection -> calibrated case.

**Transferable principle:** A test whose intent exists only in its assertions cannot be audited for the difference between passing and passing correctly. Acceptance criteria, SLO definitions, and compliance controls have the same failure mode.

**Falsification test:** If cross-tier runs on the existing case set surface no route the case was not written to reward, the cases are tight and the prose layer is documentation and not a control.

**Adoption ladder:**
  - Minimum viable: three cases run across two tiers with trajectories read.
  - Mid: a prose spec written for every case that fails the cross-tier read.
  - Full: new cases authored spec-first, with the executable form generated and the spec retained beside it.
  - Monitoring: cases retired for reward hacking; cross-tier pass gap per case; cases whose spec and grader have drifted apart.

**Confidence:** medium

**Evidence:** MTRX-W35-SPEC-FIRST-EVAL-TASKS

### 7. Alignment repair ran as a pipeline, with a scorer that did not report to the optimizer

**Source:** [Automated Researchers Can Reliably Mitigate Alignment Failures](https://alignment.anthropic.com/2026/automated-alignment-researchers/)

**Payload:** Four librarian agents build a shared survey; five automated researchers then work in parallel, each iteration reading the survey and a shared leaderboard, searching, ranking candidate methods, writing a results-free mini-paper, passing code through a monitor, training the target model for roughly thirty minutes on one H200, and submitting to a separate evaluator for scoring. Across ten alignment failures — deception, sycophancy, jailbreaks, prompt injection, power seeking, hallucination, social bias, privacy violation, reward hacking, and concealing uncertainty — the best methods reduce the targeted failure and generalise, including to models up to 4.7 times larger than the target. A post-hoc monitor found cheating in 2.4 percent of trajectories, none of it among the top methods.

**Mechanism:** Three separations carry the result. The optimizer never scores itself; a separate evaluator does. The mini-paper is written before results exist, so the method is committed before the number is known. And a post-hoc monitor reads flagged trajectories for misconduct, which is how the 2.4 percent was found instead of assumed absent. The authors are direct about the ceiling: the work only covers failures with public benchmarks or automated auditing, and the harder failures may only appear during agentic work over days.

**Why it matters:** The factory already separates attempt from scoring. It does not yet write the intended method before the run, and it has no post-hoc misconduct pass over its own trajectories. The second is the cheaper of the two to add and would produce a number the portfolio currently does not have: how often a passing run passed by a route the scorer did not intend.

**Reusable pattern:** Split proposing, executing, and scoring across components that cannot see each other's incentives, commit the hypothesis before the result exists, and run a separate pass whose only job is to look for cheating.

**Action surface:** eval

**Try this week:** Run a misconduct pass over the last thirty factory runs that scored as accepted. Classify each as clean, ambiguous, or gamed, and publish the rate. A rate of zero on thirty runs is itself a finding about the monitor's sensitivity.

**Systems map:** proposed method -> committed before results -> bounded training or run -> independent evaluator -> shared leaderboard -> post-hoc misconduct monitor -> measured cheating rate.

**Transferable principle:** A measured cheating rate is more useful than an assumption of honesty, and obtaining one requires a reader whose only job is suspicion. Code review, expense audit, and data-quality sampling run on the same premise.

**Falsification test:** If the misconduct pass over thirty accepted runs flags nothing and a hand-seeded gamed run also passes unflagged, the monitor is not sensitive enough to produce a rate and the number would be false comfort.

**Adoption ladder:**
  - Minimum viable: one misconduct pass over recent accepted runs, with a seeded positive to check sensitivity.
  - Mid: the pass runs on a sample each week and the rate goes in the run record.
  - Full: the intended method is recorded before each comparison run, and the evaluator never sees the proposer's reasoning.
  - Monitoring: measured cheating rate; seeded-positive detection rate; accepted runs later reclassified.

**Confidence:** medium

**Evidence:** MTRX-W35-INDEPENDENT-SCORER-PIPELINE

## Framework-runtime scout

| Source | Primitive changed | Why it matters | 30-90 minute test |
|---|---|---|---|
| [LangChain agent environments](https://www.langchain.com/blog/building-agent-environments-and-tasks) | eval gate | Task specs authored in prose, then generated; difficulty calibrated across model tiers | Run three held-out cases on two tiers and read the stronger model's passing trajectory |
| [LangSmith Engine](https://www.langchain.com/blog) | observability | Issue detection over agent traces, reported at better than twice the prior rate | Feed one week of factory traces and compare flagged issues against the run ledger |
| [Model Hardware Standard](https://www.anthropic.com/news/model-hardware-standard-research-preview) | tool gateway | Device capability declared as a specification, reachable over MCP, model-agnostic | Write a capability manifest for one non-device tool and see what the format forces you to state |
| [Agentic Resource Discovery](https://agenticresourcediscovery.org/) | artifact store | Discovery separated from invocation, federated and not central | Draft an ARD-shaped description for the portfolio MCP server |
| [Claude Code 2.1.248](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) | sandbox grant | `--restricted` removes command and code execution and ignores user, project, and local settings | Run one untrusted-input task under `--restricted` and record what breaks |
| [Claude Code 2.1.251](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) | stop rule | `PreModelSwitch` and `PostModelSwitch` hooks can block, confirm, or annotate a model switch | Add a hook that records model switches with the estimated re-cache cost |

## Reusable patterns

- **Unconditional load needs a measured defence.** Where it applies: context files, preloaded tool catalogues, standing system-prompt sections. Caveats: the ablation must hold the task set fixed, and instruction content and description content have to be separated before either is judged.
- **A check on a name is not a check on a thing.** Where it applies: file permission rules, signed URLs, image tags, dependency resolution. Caveats: resolving to a stable identity costs a syscall or a hash and is worth it only where substitution is reachable by an untrusted party.
- **Score with something that cannot see the optimizer.** Where it applies: eval harnesses, agent promotion decisions, alignment work, any pipeline where the producer also reports. Caveats: independence has to be structural; the same base model on both sides gives correlated failure wearing the costume of confirmation.
- **Author intent in prose, generate the executable form.** Where it applies: eval cases, acceptance criteria, policy rules. Caveats: two artifacts drift apart unless the generated form is regenerated instead of edited.

## Action queue

| Candidate | Surface | Effort | Risk | Test |
|---|---|---|---|---|
| Ablate `AGENTS.md` sections against held-out cases | context | M | low | Pass rate and token delta with and without description sections, same case set |
| Five-test permission-boundary suite for agent file tools | security | M | low | Symlink swap, symlinked search path, option-value path, widened config scope, second reading tool |
| Repeated-tool-call counter after each compaction event | context | S | low | Count identical tool calls repeated post-compaction across twenty runs |
| Misconduct pass over recent accepted factory runs | eval | S | low | Rate of gamed or ambiguous runs, with one seeded positive to check sensitivity |
| Recovery-path coverage measurement | architecture | S | low | Percentage of the last fifty recovery entries covered by the scripted failure list |
| Cross-tier calibration on three held-out cases | eval | S | low | Stronger model's passing trajectory read for unintended routes |
| Model-supply failover drill | governance | M | med | Serve one week of brief runs on a non-default provider and record what breaks |

## Action packets

| Source | Target | Surface | Try | Proof metric | Rollback | Kill criterion |
|---|---|---|---|---|---|---|
| claude-code-changelog | portfolio agent surfaces | security | Write and run the five deny-rule tests | Count of the five that pass today | Tests are additive; delete the file | All five pass and no tool surface bypasses the shared check |
| kaggle-whitepapers | factory verification stage | eval | Place each factory workflow on the verification-rigor spectrum and name the gate each tier requires | One table mapping workflow to tier to required gate | Table is documentation; discard | Every workflow already sits at its intended tier with the gate present |
| langchain-blog | factory held-out cases | eval | Cross-tier run on three cases, trajectories read | Number of cases passing by an unintended route | No change to cases until a finding lands | Zero unintended routes across three cases |
| alignment-anthropic | factory run records | eval | Misconduct pass over thirty accepted runs plus one seeded positive | Measured cheating rate and seeded-positive detection | Read-only pass; nothing to undo | Seeded positive goes undetected, so the rate is not trustworthy |
| agentic-resource-discovery | portfolio MCP server | architecture | Draft an ARD-shaped resource description | Description validates against the specification's required fields | Delete the file | The specification's required fields cannot be filled without inventing them |
| openai-news | model routing config | governance | Failover drill onto a second provider for one week of runs | Runs completed on the secondary provider without a code change | Switch the default back | The drill completes with no configuration change, so failover is already proven |

## Scout radar

| Item | Why it might matter early | What to watch | Revisit trigger |
|---|---|---|---|
| [Prime Agent](https://arxiv.org/abs/2608.23552) | Open-source harness lifting ARC-AGI-3 RHAE Best@1 from 30 to 95.5 percent with a persistent REPL, recursive subagents, and agent-to-agent messaging, without a weight change | Whether the reported lift reproduces outside the authors' benchmark selection | An independent reproduction on a benchmark the authors did not choose |
| [Apodex 1.1](https://arxiv.org/abs/2608.23283) | Environment scaling plus coordination scaling, with a 35B variant claimed to retain capability locally | Whether the open-sourced framework runs against non-Apodex models | A third-party run of the framework on open weights |
| [PI-SERINI](https://arxiv.org/abs/2605.10848) | A tuned lexical retriever with retrieve, browse, and read tools reaching 83.1 percent answer accuracy, with retrieval depth the largest single lever | Whether the depth result holds when a weaker model does the triage | A replication with a mid-tier model in the loop |
| [Cloudflare Code Mode](https://blog.cloudflare.com/code-mode-mcp/) | 2,500 endpoints collapsed from roughly 1.17M tokens of schema into two tools at around 1,000 tokens, with a measured 99.9 percent input-token reduction | Whether per-tool authorization survives the collapse, and how weaker models fare writing code against a discovered spec | A published authorization design for the two-tool surface |
| [Salesforce Headless 360](https://www.salesforce.com/ap/news/press-releases/2026/08/25/salesforce-turns-enterprise-applications-into-enterprise-capabilities/) | Business capabilities exposed to MCP clients while inheriting existing identity, permissions, validation rules, and audit | Whether the exposed surface is reusable capabilities or several hundred thin tools | Production adoption figures or a published tool inventory |
| [ai-engineer-talks](https://ai.engineer/talks) | Transcript-bearing talk archive from practitioners running agent systems, newly added to the registry | Release cadence after the November Code Summit, and whether transcripts stay open | The first Code Summit talk lands with a transcript |

## Watchlist

- **Does the context-file null result hold for agent harnesses with weak file navigation?** The study reports harness-dependent gains for progressive disclosure; the context-file result is stated more broadly. Revisit trigger: a replication that reports results split by harness navigation quality.
- **Does ownership-triggered supply termination spread past one supplier?** OpenAI ended Cursor's model access on August 28 citing the ownership change instead of conduct, and Cursor reported the affected traffic at roughly 5 percent. Revisit trigger: a second frontier provider publishing ownership-based access restrictions, or Cursor's usage measurably moving after November 12.
- **Does the Model Hardware Standard ship an interlock design before it ships breadth?** A physical blast radius has no software rollback. Revisit trigger: the preview publishing its approval, emergency-stop, and actuator-logging semantics.
- **Do the discovery specifications converge or fork?** Agentic Resource Discovery, the AWS Agent Registry preview, and the MCP roadmap's registry direction all sit in front of invocation. Revisit trigger: two of the three referencing a shared resource-description shape.

## Archive notes

- **OpenAI, "Our decision on Cursor following its acquisition by SpaceX"** ([OpenAI](https://openai.com/index/our-decision-on-cursor-following-its-acquisition-by-spacex/)). A supplier ended access on August 28 on corporate-structure grounds instead of conduct, two weeks after the acquisition closed. Real and consequential for procurement, and it produced this week's failover Action packet, though the mechanism is contractual instead of technical, which keeps it out of Top signals.
- **Anthropic platform, computer use and browser use toolsets, Files API, and Agent Skills out of beta** ([Claude Platform release notes](https://platform.claude.com/docs/en/release-notes/api)). Dated August 19 and 20, inside the 2026-W34 window and uncovered there. Recorded here because Agent Skills reaching general availability is the packaging format the progressive-disclosure study measured.
- **Google and Kaggle, "The New SDLC With Vibe Coding"** ([Kaggle](https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding)). Osmani, Saboo and Kartakis, May 2026, 51 pages. Its spectrum framing — the difference between casual and agentic engineering being verification rigor — is the cleanest short statement of the year and drives an Action packet. Its adoption percentages trace to marketing aggregators instead of primary sources, so the paper enters the corpus as a framework and not as evidence.
- **Addy Osmani, "The Code Agent Orchestra"** ([addyosmani.com](https://addyosmani.com/blog/code-agent-orchestra/)). Three to five workers as the reported sweet spot, loop guardrails with forced reflection, and a read-only reviewer teammate per three or four builders. The reviewer pattern is worth stealing; the piece also restates the ETH Zurich context-file result more favourably than the abstract supports, which is why the finding is cited here from the paper.
- **EnvACE, world rehearsal for agentic RL** ([arXiv](https://arxiv.org/abs/2608.06197)). A policy that plays both actor and environment, with private rehearsal before committed execution. The mental model — the agent should hold a prediction about what its action will do, and a mismatch is worth logging — transfers; the training method does not apply to a local software factory.
- **Cross-organization agent containment reporting** ([Hugging Face](https://huggingface.co/blog/agent-intrusion-technical-timeline)). Covered as a top signal in 2026-W30 and 2026-W31; the August follow-up reporting adds incident counts from partial public datasets without a denominator, so it stays archived instead of restated.

## Sources reviewed

| Source | Status | Note |
|---|---|---|
| anthropic-news | ok | 3 items in window; 1 top signal (Model Hardware Standard) |
| claude-code-changelog | ok | versions 2.1.246 through 2.1.252; 1 top signal, 2 scout rows |
| claude-platform-release-notes | ok | no in-window entries; August 19-20 entries recorded as carryover |
| langchain-blog | ok | 5 items in window; 1 top signal, 1 scout row |
| alignment-anthropic | ok | 1 item; 1 top signal |
| agentic-resource-discovery | ok | specification read in full; 1 top signal |
| arxiv-cs-ai | ok | 6 preprints reviewed; 2 top signals, 3 scout rows |
| kaggle-whitepapers | ok | 1 whitepaper; 1 action packet, 1 archive note |
| ai-engineer-talks | ok | archive reviewed; no in-window release, registry entry seeded |
| ai-engineer-youtube | failed | channel_id feed recorded on the podcast entry returns 404; resolve from the handle next sweep |
| openai-news | failed | index returns 403 to this agent; the Cursor decision was read through its own permalink |
| openai-api-changelog | ok | 1 in-window entry (August 20, image backgrounds); no pick |
| kaggle-learn-intensives | skipped | June cohort, outside the window; entry seeded for the next intensive |
| Weekly Gen AI Digest folder | ok | private discovery input, August 28 issue |
| Daily Systems Brief folder | ok | private discovery input, August 24 through 30 |

## Closing thought

The AGENTS.md result is uncomfortable in the right way for a repository that publishes two of them and treats both as settled. It does not tell anyone to stop writing the file. It says the half most authors are proudest of — the tour of the repository, the architecture summary, the orientation for a newcomer who has never opened the tree — has never been shown to pay for the tokens it costs on every turn. That is a testable claim about this repository, and the test takes an afternoon.
