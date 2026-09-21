<!--
iso_week: 2026-W38
through_date: 2026-09-18
profile_id: builder-tpm
registry_version: 14
matrix_run_id: MTRX-W38-the-ruler-outside-the-loop
-->

# Thirteen workers spent twelve days closing sixty-two percent of the gap to a model that already existed.

**Week 38 through 2026-09-18 - Vol. 21**

## Field thesis

Last week the thing outside the model got measured and did poorly. This week the thing outside the model is the only part that held. Every self-improvement result in the window put the ruler somewhere the agent could not reach it: a fixed bits-per-byte evaluator on a Git DAG that thirteen workers appended to for twelve days, a verifier agent kept separate from the actor, a replay simulator built from the search history instead of the live environment, a guardrail distilled from six hundred and forty-two recorded failures, a confidence score computed from graded past episodes, not from the model's own sampling. And every runtime change in the window moved a control out of the model and into the harness: a client that hands hostname resolution to the egress proxy, a fetch tool patched four ways in one release and a second vendor patching the same surface the same week, approvals keyed to validated arguments, a human's edit to a tool call recorded beside the model's original. The week's quietest item is the one this portfolio has waited for: the client now reads AGENTS.md when there is no CLAUDE.md, which turns a contract the portfolio wrote for itself into the default the tool reads.

## Top signals

### 1. The file the portfolio standardized on became the file the client reads

**Source:** [Claude Code 2.1.277](https://github.com/anthropics/claude-code/releases/tag/v2.1.277)

**Payload:** The 2.1.277 release, published 2026-09-18, adds AGENTS.md support: in a project with no CLAUDE.md, Claude Code reads AGENTS.md instead, with the choice exposed under Project instructions in `/config`, and not yet on Bedrock, Vertex or Foundry. The same release adds `CLAUDE_GATEWAY_PROXY_IS_EGRESS_BOUNDARY=1` for Claude apps gateways whose only egress is a forward proxy: with it set, every outbound request hands the proxy the hostname instead of resolving it locally. A third item adds an optional `headers:` map on gateway upstreams for static headers to a proxy you run in front of a provider.

**Mechanism:** Project instructions are the one file the client loads unprompted, so whichever file the client picks is the contract that governs the session. Until this release the portfolio's AGENTS.md files were visible to every lane except the one that most often ran unattended, and the workaround was a CLAUDE.md shim that pointed at AGENTS.md or duplicated it. The release makes the shim unnecessary in repos that have no CLAUDE.md, and makes it dangerous in repos that have both, because the note says the fallback applies only when CLAUDE.md is absent. A shim that drifted from the contract it was meant to mirror is now the thing being read. The egress flag is the same move at the network layer: the client stops deciding where a hostname points and lets the proxy decide, which is where a destination policy can be enforced without trusting the client's resolver.

**Why it matters:** The portfolio carries AGENTS.md in every active repo and a July audit found the contracts invisible to the Claude lane. The gap closes on upgrade, but only for repos that never grew a CLAUDE.md; the rest need a decision per repo about which file is canonical, and a check that the two do not disagree. The egress flag matters for the factory's gateway sessions specifically: it is the first client-side switch that assumes the proxy is the boundary, which is the design 2026-W37's containment reading argued for and this week's fetch-tool advisories make concrete.

**Reusable pattern:** When a tool starts reading a contract file natively, remove the shim in the same change, or the shim becomes the contract.

**Action surface:** config

**Try this week:** List every portfolio repo that carries both AGENTS.md and CLAUDE.md. Diff the pair. Where they differ, decide which is canonical and delete or reduce the other to a one-line pointer.

**Systems map:** client reads AGENTS.md by default -> shim CLAUDE.md files become the only file read where both exist -> drifted shims override the contract -> repos with one file get the contract for free, repos with two get whichever drifted.

**Transferable principle:** A compatibility layer written for a tool that could not read the real artifact turns into a fork the day the tool learns to read it. Polyfills, adapter tables and mirrored schemas all age the same way.

**Falsification test:** If no portfolio repo carries both files, or every pair is byte-identical, the shim risk is zero and the upgrade is pure gain.

**Adoption ladder:**
  - Minimum viable: inventory of repos with both files and a diff of each pair.
  - Mid: one canonical instruction file per repo, the other removed or reduced to a pointer, with the choice recorded in decisions/.
  - Full: a gate that fails when a repo carries both files and they differ, and the factory's gateway sessions running with the egress-boundary flag set.
  - Monitoring: count of repos with two instruction files; count of diffs between them; sessions started with the egress flag set.

**Confidence:** high

**Evidence:** MTRX-W38-AGENTS-MD-DEFAULT, MTRX-W38-EGRESS-BOUNDARY-FLAG

### 2. Four holes in one release, and every one of them was reached through the fetch tool or the telemetry

**Source:** [pydantic-ai v2.44.0](https://github.com/pydantic/pydantic-ai/releases/tag/v2.44.0)

**Payload:** The 2.44.0 release, published 2026-09-17, fixes four security issues that the maintainers say were all reached through `web_fetch_tool` or OpenTelemetry instrumentation. The cloud-metadata and private-IP blocklists could be bypassed with an IPv6 zone identifier on a URL opted into local network access. `web_fetch` processed responses in superlinear time on the event loop, in both the HTML conversion and the charset decode, so a single attacker-chosen page could stall every agent in the process. The tool's domain lists were compared as written instead of in the form the resolver uses, so a blocked domain could be reached under another spelling. And with `InstrumentationSettings(include_content=False)`, spans still carried exceptions, error statuses, instructions and the output template. Two are rated moderate and two low; all four are backported to 1.107.6. Two days earlier, Gemini CLI v0.60.0 shipped a core fix titled improve destination validation and connection routing in web fetch utilities. The same week, Claude Code 2.1.273 fixed Bash commands the permission checker cannot fully analyze skipping the prompt under `permissions.blockReadsOutsideWorkingDirectories`, and a subshell hiding a dangerous `rm` in bypass mode.

**Mechanism:** A fetch tool is the one place where an agent's outbound request and an attacker's inbound content meet, so every weakness in how it names destinations or processes responses is an attack surface in both directions. Two of the four pydantic-ai issues are naming failures: a zone identifier the blocklist did not expect, and a spelling the resolver normalizes but the comparison did not. The third is a parser with no budget, trusting a page to be small. The fourth is the telemetry carrying what the operator had asked it not to carry. None of them is a model failure, and none of them would be fixed by a better prompt. Gemini CLI's fix reads as the same class from its title alone, and the Claude Code permission-checker fix is the shell-side twin: a command the checker cannot parse got the benefit of the doubt.

**Why it matters:** Two of the portfolio's agents fetch untrusted pages and one runs Bash under a permission policy. The pydantic-ai advisories name the exact checks to make elsewhere: does the blocklist normalize the destination the way the resolver does; does response processing have a size and time budget; does telemetry honour the content flag. The superlinear-parse issue is the one to test first, because it turns one hostile page into a denial of service for every agent sharing the process.

**Reusable pattern:** Compare destinations in the form the resolver uses, not the form the URL was written in, and put a budget on response processing before the parser sees the bytes.

**Action surface:** security

**Try this week:** Take the portfolio's fetch wrapper and feed it three inputs: a blocked domain in mixed case with a trailing dot, an IPv6 literal with a zone identifier, and a ten-megabyte page of nested tags. Record which of the three is refused, and how long the third takes.

**Systems map:** untrusted page -> fetch tool parses and resolves -> naming mismatch admits a blocked destination, or unbounded parse stalls the event loop -> every agent in the process waits -> telemetry records the instructions it was told to omit.

**Transferable principle:** Any allowlist compared in a different normal form from the one the enforcement point uses is a list of spellings, not of destinations. DNS blocklists, path allowlists and email domain rules fail the same way.

**Falsification test:** If the portfolio's fetch wrapper refuses all three probe inputs and telemetry with content disabled carries no instruction text, the four advisories describe someone else's code.

**Adoption ladder:**
  - Minimum viable: the three-input probe run once against the portfolio's fetch wrapper, with results recorded.
  - Mid: destination checks moved to resolver-normalized form and a size and time budget on response processing.
  - Full: the fetch wrapper behind an egress proxy that owns resolution, with the client's own blocklist treated as advisory, and a telemetry test that asserts what a content-disabled span may carry.
  - Monitoring: refused fetches by reason; parse time per response at the 99th percentile; span fields present when content is disabled.

**Confidence:** high

**Evidence:** MTRX-W38-FETCH-TOOL-ADVISORIES, MTRX-W38-FETCH-DESTINATION-VALIDATION, MTRX-W38-PERMISSION-CHECKER-SUBSHELL

### 3. The gateway can now be told what kind of turn it is billing

**Source:** [Claude Code 2.1.273](https://github.com/anthropics/claude-code/releases/tag/v2.1.273)

**Payload:** The 2.1.273 release, published 2026-09-15, adds `x-claude-code-request-class`, `x-claude-code-agent-type`, `x-claude-code-prev-tool-durations`, `x-claude-code-compaction` and `x-claude-code-context-compacted` request headers for LLM gateways, opt-in with `CLAUDE_CODE_GATEWAY_HINT_HEADERS=1`. The same release adds a notification when an MCP server disconnects mid-session and automatic reconnection gives up, pointing at `/mcp`.

**Mechanism:** A gateway sees tokens in and tokens out and nothing about why. Five headers change that: the request class says what kind of turn produced the call, the agent type says which role made it, the previous tool durations say how long the tools before it ran, and the two compaction headers say whether this request is a compaction or follows one. With those on the wire, a gateway can attribute cost to the turn type and split it by whether context had just been compacted, which is the split 2026-W36 and 2026-W37 both wanted and could not get from `/cost` alone.

**Why it matters:** The portfolio's open measurement is the prompt-cache hit ratio after 2.1.267, and 2026-W37 named eleven client-side causes that would have depressed any pre-upgrade number. The compaction headers isolate one more: a request that follows a compaction has a new prefix by construction, and until now it was indistinguishable at the gateway from a request whose cache was flushed by tool-list mutation. The MCP disconnect notification closes a smaller gap: a server that vanished mid-session used to be a silent loss of tools.

**Reusable pattern:** Put the reason for a request on the request, so the layer that sees the bill can group by cause without reading the transcript.

**Action surface:** observability

**Try this week:** Enable the flag on one factory session that runs through the gateway, and have the gateway log the five headers beside the token counts. Group cost by request class and by the compaction flag for one day of runs.

**Systems map:** turn type known only to the client -> gateway bills tokens without cause -> cost per outcome cannot be split by turn kind -> headers carry the cause -> cost grouped by class and by compaction -> cache-hit regressions attributable.

**Transferable principle:** Instrumentation that lives at the boundary can only group by what crosses the boundary; a system that wants cause-level accounting has to send the cause. Request IDs, trace parents and billing tags are the same idea in other stacks.

**Falsification test:** If the portfolio's sessions never run through a gateway, the headers are inert and the cache measurement has to come from `/cost` as before.

**Adoption ladder:**
  - Minimum viable: the flag enabled on one gateway session and the headers visible in the gateway's log.
  - Mid: cost grouped by request class and compaction flag over a week of factory runs.
  - Full: the cache-hit measurement from 2026-W36 re-run with post-compaction requests excluded and reported separately.
  - Monitoring: requests per class per day; share of requests marked compacted; cost per outcome by class.

**Confidence:** high

**Evidence:** MTRX-W38-GATEWAY-HINT-HEADERS

### 4. Six hundred and forty-two failure traces became a guardrail, and abnormal runs fell from sixty-nine to twenty-seven percent

**Source:** [AgentGuard: Learning Execution Guardrails from Anomalous Coding-Agent Trajectories](https://arxiv.org/abs/2609.16287)

**Payload:** Submitted 2026-09-14. AgentGuard extracts recurring execution failure patterns from 642 documented failure traces collected from real coding-agent executions across 382 repository tasks, generalizes them into instruction-level behavioural constraints, and organizes them as a lightweight guardrail skill that activates only the rules relevant to the current instruction. Reported effect on the held-out tasks: Abnormal Execution Rate from 69.0% to 26.7%, Successful Task Completion Rate from 21.7% to 35.0%.

**Mechanism:** The failure traces are the specification. A rule mined from what went wrong last time is more specific than any rule a person writes in advance, and activating only the rules that match the current instruction keeps the guardrail from becoming a second system prompt. The design is the trace-to-check loop the portfolio already runs, taken one step further: instead of freezing one failure into one eval case, the failures are clustered and turned into constraints that apply before the next run instead of after it.

**Why it matters:** The portfolio's harness freezes a failed run into a checked-in eval case so the same failure cannot ship twice. AgentGuard's numbers say the same traces can also feed forward. The gap between the two rates matters as much as either: abnormal executions fell by forty-two points while completion rose by thirteen, so most of what the guardrail stops was not going to succeed anyway, and the completion gain is the number to hold it to.

**Reusable pattern:** Cluster the failure traces, write the constraint per cluster, and scope each constraint to the instructions it matches.

**Action surface:** eval

**Try this week:** Take the portfolio's last fifty frozen failure cases, cluster them by hand into no more than eight patterns, and write one instruction-level constraint per pattern. Run the next ten factory tasks with the constraints injected only when the task matches.

**Systems map:** failure traces recorded -> patterns clustered -> constraints written per pattern -> constraint activated on matching instruction -> abnormal execution rate falls -> completion rate rises less than abnormal rate falls.

**Transferable principle:** A rule derived from recorded failures is a compressed test suite; the compression is only as good as the clustering, and a rule that fires on every instruction is a prompt, not a guardrail.

**Falsification test:** If the constraints written from the portfolio's own traces do not move completion on the next ten tasks, the traces were too few or too specific to generalize, and the frozen cases should stay as after-the-fact checks.

**Adoption ladder:**
  - Minimum viable: fifty frozen failure cases clustered into named patterns.
  - Mid: one constraint per pattern, injected only on matching tasks, with abnormal-run and completion rates recorded for ten tasks.
  - Full: the clustering and constraint generation run as a scheduled job over the run ledger, with each constraint carrying the trace IDs that produced it.
  - Monitoring: abnormal-run rate per task class; completion rate per task class; constraints active per task.

**Confidence:** medium

**Evidence:** MTRX-W38-AGENTGUARD-TRACES

### 5. Confidence from graded past episodes, and abstention on the least-confident tenth worth up to eight points

**Source:** [Confidence Comes from Experience: Experiential Confidence Estimation from Reasoning to Agents](https://arxiv.org/abs/2609.17708)

**Payload:** Submitted 2026-09-15. XConf estimates confidence from a record of the model's own graded past episodes. It beats or matches ten-sample self-consistency in discrimination (AUROC) on 23 of 24 comparisons, with much lower calibration error (ECE), at a tenth of the generation cost, and abstaining on the 10% least-confident episodes raises the delivered success rate by up to 8.7 points on agent tasks.

**Mechanism:** Self-consistency buys a confidence estimate by sampling the same problem ten times and measuring agreement, which costs ten generations and measures the model's agreement with itself. XConf replaces the ten samples with a lookup against graded history: episodes like this one went this way. The record is external to the model and grows with every graded run, so the estimate is a property of the operator's ledger, not of the model's mood on the day. Abstention then converts the estimate into a delivered number: refuse the tenth of episodes the record says are most likely to fail, and the success rate on what ships goes up.

**Why it matters:** The portfolio grades every factory run and keeps the grades in a ledger, which is the record XConf needs and most teams do not have. The 8.7-point figure is a maximum across the agent tasks reported, so the portfolio's own number will be lower, but the cost side is the point: a confidence estimate at a tenth of the cost of self-consistency changes whether it is worth computing at all.

**Reusable pattern:** Estimate confidence from graded history instead of resampling, and spend the estimate on abstention where a refused task costs less than a failed one.

**Action surface:** workflow

**Try this week:** For the last hundred graded factory runs, compute a nearest-neighbour confidence for each from the fifty runs before it, then check whether dropping the ten least-confident would have raised the pass rate on the remaining ninety.

**Systems map:** graded episodes accumulate in the ledger -> new episode matched against the record -> confidence assigned without resampling -> least-confident tenth abstained -> delivered success rate rises -> abstained tasks routed to a person or a stronger model.

**Transferable principle:** A record of graded outcomes is a calibration set; any system that grades its own work can price its confidence from history instead of from repetition. Credit scoring and clinical triage do this already.

**Falsification test:** If the ledger-derived confidence has no discrimination on the portfolio's own runs, the tasks are too heterogeneous for nearest-episode matching and self-consistency remains the only estimate.

**Adoption ladder:**
  - Minimum viable: retrospective confidence computed for one hundred graded runs from the fifty before each.
  - Mid: a live confidence field on each run record, with the least-confident tenth flagged for review before the result is accepted.
  - Full: abstention wired into the factory so flagged tasks route to a person or a stronger model, with delivered success reported with and without abstention.
  - Monitoring: AUROC of the confidence field against actual grades; share of tasks abstained; delivered success rate on shipped tasks.

**Confidence:** medium

**Evidence:** MTRX-W38-XCONF-ABSTENTION

### 6. Git was the shared memory of thirteen workers for twelve days

**Source:** [Agora: Git as Shared Memory for Collective AutoResearch](https://arxiv.org/abs/2609.18094)

**Payload:** Submitted 2026-09-16. Agora records research as an append-only directed acyclic graph stored in Git. In a run of nearly 12 days, 13 language-model workers on a weight-transfer problem published 1,703 contributions and drove the evaluator from 3.39 to 1.899 bits per byte, closing 62% of the gap to a trained GPT-2 124M. The abstract also reports a 145-commit ancestry, 15 accounts and 165 independent reproductions.

**Mechanism:** Every worker's contribution is a commit with parents, so the record of who tried what, on top of what, is the version history itself, and any worker can start from any node. The evaluator is a fixed bits-per-byte number on a fixed target, which is why the workers can search: the ruler is a file none of them can edit. The 62% figure is progress toward a model that already exists, which is the design, since the point was to test the coordination substrate and not to discover anything.

**Why it matters:** The portfolio runs one writer per repo per session, and the two-lane rule exists because two agents editing one working tree collide. Agora is the other answer: many writers, no shared working tree, an append-only DAG, and every contribution reproducible from its ancestry. The 165 independent reproductions are the number to notice, because they follow from the record being the DAG and not a transcript. The event ledger the portfolio already keeps is a flat log; the paper argues the log should have parents.

**Reusable pattern:** Make the shared memory an append-only DAG with a fixed external evaluator, and let workers branch from any node instead of serializing through one tree.

**Action surface:** architecture

**Try this week:** Take one factory task's run ledger and rewrite it as a DAG: each run's parent is the run whose output it started from. Count how many runs have no parent, which is the number of times a worker started from nothing when it could have started from a sibling.

**Systems map:** workers append commits with parents -> evaluator fixed and external -> any node reproducible from ancestry -> search proceeds in parallel without a shared tree -> coordination cost moves from locking to merging.

**Transferable principle:** A shared memory that records ancestry supports reproduction and branching for free; one that records only sequence supports replay and nothing else. Version control learned this before agents existed.

**Falsification test:** If the portfolio's run ledger already lets any run be reproduced from a named parent, the DAG is present in all but name and the change is cosmetic.

**Adoption ladder:**
  - Minimum viable: one task's ledger rewritten as a parent-child graph, with orphan runs counted.
  - Mid: a parent field on every run record, required when the run started from another run's output.
  - Full: workers permitted to branch from any recorded node, with the evaluator held outside the repo they write to.
  - Monitoring: share of runs with a parent; reproductions per node; evaluator score per branch over time.

**Confidence:** medium

**Evidence:** MTRX-W38-AGORA-GIT-MEMORY

### 7. Both self-improvement papers kept the verifier outside the loop, one as a replay simulator and one as an agent

**Source:** [Dream-RSI: Recursive Self-Improvement through Evolving Worlds](https://arxiv.org/abs/2609.14858) and [RSIAgent: Autonomous Exploration for Recursive Self-improvement in New Environments](https://arxiv.org/abs/2609.15364)

**Payload:** Both submitted 2026-09-14. Dream-RSI's key insight, in the authors' words, is that accumulated discovery history can serve as a replay simulator over the realized search space; dreaming in that simulator secures immediate, low-cost off-policy feedback to evaluate and refine exploration policies without invoking repetitive, expensive online evaluations, and across algorithm engineering, mathematical optimization and GPU kernel engineering the method achieves competitive or improved discovery quality while substantially reducing discovery cost in several settings. RSIAgent coordinates curriculum, actor, and verifier agents to continually explore the environment, validate outcomes, and retain environment-specific knowledge; on OSWorld-v2 and Agent's Last Exam the authors report Kimi-K3 and GLM-5.3 outperforming frontier closed-source models including GPT-6 once wrapped in it.

**Mechanism:** Two different answers to the same design question. Dream-RSI makes the search history into the environment: past discovery trees become a simulator, and the exploration policy is trained against replays of what already happened, which is off-policy evaluation applied to research. RSIAgent keeps the environment live and splits the roles instead: the actor explores, the verifier validates, the curriculum decides what to explore next. In both, the thing that scores the work is not the thing doing the work, and both papers are careful about what that buys. Dream-RSI's simulator can only score policies inside the region the history covered. RSIAgent's verifier is itself a model, so the separation is architectural, not independent.

**Why it matters:** The portfolio's replay tooling was built on exactly the Dream-RSI framing: replay a trajectory log against a simulated environment and score counterfactual mutations without paying for a live run. The paper is the first in-window evidence that the framing produces discovery-quality results in engineering domains and not only in benchmarks. RSIAgent's claim against closed-source models is the authors' own on two benchmarks with no scores at abstract level, and the brief carries it as a claim, not a result.

**Reusable pattern:** Score the work with something the worker cannot edit: a replay of history, or a separate role with its own instructions.

**Action surface:** experiment

**Try this week:** Take one factory task with at least twenty recorded runs and build the replay: for a proposed change to the task's exploration policy, score it against the twenty recorded trajectories before running it live. Record whether the replay score predicted the live score.

**Systems map:** discovery history accumulates -> history becomes a replay simulator -> policy refined off-policy at low cost -> refined policy redeployed live -> new history expands the simulator -> verifier stays outside the actor throughout.

**Transferable principle:** Off-policy evaluation turns a log into a laboratory, and the laboratory is only valid inside the region the log covered. Recommender systems and clinical trials from registry data carry the same caveat.

**Falsification test:** If replay scores on the portfolio's recorded trajectories fail to predict live scores for the next five policy changes, the history is too narrow for the simulator and live evaluation remains the only ruler.

**Adoption ladder:**
  - Minimum viable: one task's twenty recorded trajectories replayable against a proposed policy change.
  - Mid: replay score recorded beside live score for every policy change on that task.
  - Full: the replay run before any live run as a gate, with the verifier role's instructions held separately from the actor's.
  - Monitoring: replay-to-live correlation per task; live runs avoided per week; coverage of the replay pool.

**Confidence:** medium

**Evidence:** MTRX-W38-DREAM-RSI-REPLAY, MTRX-W38-RSIAGENT-VERIFIER

### 8. Two frameworks moved the approval record to the validated call

**Source:** [openai-agents-python v0.22.3](https://github.com/openai/openai-agents-python/releases/tag/v0.22.3) and [langchain 1.4.2](https://github.com/langchain-ai/langchain/releases/tag/langchain%3D%3D1.4.2)

**Payload:** openai-agents-python v0.22.3, published 2026-09-17, carries a core fix that aligns conditional approvals with validated tool arguments. langchain 1.4.2, published 2026-09-18, preserves model-generated tool calls in human-in-the-loop tool call edits and adds a notice to the ToolMessage. deepagents 0.7.15, published 2026-09-16, gave tool result offloads without IDs unique paths to avoid collisions.

**Mechanism:** An approval is a decision about a specific call. If the decision is computed on the raw arguments and the tool then runs on the validated ones, the human approved something other than what executed; aligning the two closes that gap. The langchain change is the audit side of the same problem: when a person edits a tool call before it runs, the record used to show only the edited call, so the model's original request was lost and the transcript read as if the model had asked for what the human chose. Keeping both, with a notice, makes the edit visible. The deepagents fix is smaller and belongs to the same family: an offloaded tool result with no ID could collide with another, so the agent could read back a result that was not the one it produced.

**Why it matters:** The portfolio's policy engine approves tool calls against declared targets, and a mismatch between what was approved and what ran is the failure that would pass every gate and still be wrong. The three notes are one-line release entries, so the mechanisms above are this brief's reading of the titles and the warnings on the matrix cells say so; the pattern across them is what carries.

**Reusable pattern:** Approve the call as it will execute, and when a human changes it, record both versions.

**Action surface:** tool-policy

**Try this week:** For the portfolio's policy engine, find the point where a tool call is approved and the point where its arguments are validated, and check they see the same object. Then check what the run record shows when a person edits a call before it runs.

**Systems map:** model proposes call -> arguments validated -> approval computed -> tool executes -> if approval saw raw arguments, the executed call differs from the approved one -> if the record keeps only the edited call, the audit trail loses what the model asked for.

**Transferable principle:** Authorization has to bind to the same representation the executor uses, and an edit to an authorized action has to leave both the original and the edit in the record. Change-control and financial approval systems learned this the expensive way.

**Falsification test:** If the portfolio's approval and validation steps already share one object and edited calls already record the original, the three fixes describe frameworks the portfolio does not run.

**Adoption ladder:**
  - Minimum viable: the approval and validation points located in the policy engine and compared.
  - Mid: approval bound to the validated call, with a test that a change to arguments after approval fails the run.
  - Full: run records that keep the model's original call beside any human edit, with a notice in the tool result.
  - Monitoring: runs where validated arguments differ from approved arguments; edited calls per week; run records missing an original.

**Confidence:** medium

**Evidence:** MTRX-W38-APPROVALS-VALIDATED-ARGS, MTRX-W38-HITL-EDIT-PRESERVE, MTRX-W38-OFFLOAD-ID-COLLISION

## Framework-runtime scout

| Source | Primitive changed | Why it matters | 30-90 minute test |
|---|---|---|---|
| [Claude Code 2.1.270 to 2.1.277](https://github.com/anthropics/claude-code/releases) | execution | Eight releases in the window: AGENTS.md fallback and the egress-boundary flag (2.1.277), gateway hint headers and the permission-checker fix (2.1.273), fast mode in remote sessions (2.1.271), a visible warning when memory usage is critical (2.1.274), gateway sign-in naming the signed-in account (2.1.275) | Upgrade one factory host, set the hint-header flag, and confirm the five headers reach the gateway |
| [pydantic-ai 1.107.6](https://github.com/pydantic/pydantic-ai/releases/tag/v1.107.6) | tool gateway | The four 2.44.0 security fixes backported to the v1 line, so pinned v1 users get the fetch and telemetry fixes without the v2 migration | Check which line the portfolio pins and whether it is past the fix |
| [deepagents-code 0.1.71](https://github.com/langchain-ai/deepagents/releases/tag/deepagents-code%3D%3D0.1.71) | tool gateway | MCP support moved onto FastMCP and `langchain.mcp`, which changes the client the portfolio's MCP server is talked to by | Run the portfolio MCP server against the new client and diff the tool listing |
| [Codex rust-v0.155.1](https://github.com/openai/codex/releases/tag/rust-v0.155.1) | runtime-adapter | New local TUI sessions leave reasoning summaries disabled by default, fixing request rejections; a default that changes what a transcript contains | Check whether any portfolio tooling reads reasoning summaries from Codex transcripts |
| [langchain 1.4.1](https://github.com/langchain-ai/langchain/releases/tag/langchain%3D%3D1.4.1) | tool gateway | Preserves open MCP object arguments, a fix to how tool schemas with open objects survive the call | Send one tool call with an open-object argument through the portfolio's MCP server and inspect what arrives |
| [Strands python/v1.56.0](https://github.com/strands-agents/sdk-python/releases/tag/python%2Fv1.56.0) | runtime-adapter | A minor release auto-drafted from conventional commits; 2026-W37 flagged Strands for shipping `feat!` in a minor, so the marker check applies again | Grep the release notes for a breaking-change marker before pinning |

## Reusable patterns

- **Remove the shim in the same change that makes it unnecessary.** Where it applies: instruction files, polyfills, adapter tables, mirrored schemas. Caveats: a repo that carries both files keeps the old one as canonical, so removal is per repo and needs a diff first.
- **Compare destinations in the resolver's normal form.** Where it applies: fetch allowlists, DNS blocklists, path rules, email domain checks. Caveats: normalization has to match the enforcement point exactly, and a proxy that owns resolution makes the client list advisory.
- **Send the cause with the request.** Where it applies: gateway cost accounting, trace attribution, billing tags. Caveats: only a gateway you operate can read the headers, and the value vocabularies are undocumented this week.
- **Score the work with something the worker cannot edit.** Where it applies: self-improvement loops, eval harnesses, review roles, replay simulators. Caveats: a replay is valid only inside the region the history covered, and a verifier that is itself a model is separated by architecture, not independence.
- **Approve the call as it will execute, and keep both versions of an edited one.** Where it applies: tool policy engines, human-in-the-loop edits, change control. Caveats: the three framework notes are one-line titles and the mechanisms are this brief's reading.

## Action queue

| Candidate | Surface | Effort | Risk | Test |
|---|---|---|---|---|
| Inventory repos with both AGENTS.md and CLAUDE.md and diff each pair | config | S | low | Count of repos with two files and count of differing pairs |
| Run the three-input probe against the portfolio's fetch wrapper | security | S | low | Which of a mixed-case blocked domain, an IPv6 zone literal, and a ten-megabyte page is refused, and the parse time of the third |
| Enable gateway hint headers on one factory session and group cost by request class | observability | S | low | Five headers visible in the gateway log; cost per class for one day |
| Cluster fifty frozen failure cases into patterns and write one constraint each | eval | M | low | Abnormal-run and completion rates on the next ten matching tasks |
| Compute retrospective ledger confidence for one hundred graded runs | workflow | M | low | Whether dropping the ten least-confident would have raised the pass rate on the rest |
| Rewrite one task's run ledger as a parent-child graph | architecture | S | low | Count of orphan runs that could have started from a sibling |
| Replay a proposed policy change against twenty recorded trajectories before running it live | experiment | M | low | Whether the replay score predicted the live score |
| Check that approval and validation in the policy engine see the same call object | tool-policy | S | low | Runs where validated arguments differ from approved ones; edited calls that lost the original |

## Action packets

| Source | Target | Surface | Try | Proof metric | Rollback | Kill criterion |
|---|---|---|---|---|---|---|
| claude-code-changelog | portfolio repos | config | List repos carrying both instruction files and diff each pair | Repos with two files; differing pairs | Read-only; nothing to undo | No repo carries both files |
| agent-frameworks | portfolio fetch wrapper | security | Feed the wrapper a mixed-case blocked domain, an IPv6 zone literal, and a ten-megabyte page | Which inputs are refused; parse time of the large page | Read-only against a test wrapper | All three refused and the large page parses within budget |
| claude-code-changelog | factory gateway sessions | observability | Set `CLAUDE_CODE_GATEWAY_HINT_HEADERS=1` on one session and log the headers beside token counts | Cost grouped by request class and compaction flag | Unset the flag | No session runs through a gateway |
| arxiv-cs-se | factory run ledger | eval | Cluster fifty frozen failures into patterns and inject one constraint per pattern on matching tasks | Abnormal-run rate and completion rate over ten tasks | Remove the constraints; frozen cases untouched | Completion unchanged after ten tasks |
| arxiv-cs-ai | factory run ledger | workflow | Compute nearest-episode confidence for one hundred graded runs from the fifty before each | Pass rate on the ninety kept versus all hundred | Read-only; retrospective | Confidence has no discrimination against actual grades |
| arxiv-cs-ma | factory run ledger | architecture | Add a parent field to one task's runs and count orphans | Orphan runs; reproductions per node | Field is additive; drop it | Every run already names a parent |
| arxiv-cs-ai | factory replay tooling | experiment | Score one policy change against twenty recorded trajectories before the live run | Replay score versus live score | Read-only; the live run happens anyway | Replay fails to predict live for five changes running |
| agent-frameworks | portfolio policy engine | tool-policy | Locate the approval and validation points and confirm they share one object; inspect the record of an edited call | Mismatched runs; records missing the original call | Documentation only until a change is made | Both already hold |

## Scout radar

| Item | Why it might matter early | What to watch | Revisit trigger |
|---|---|---|---|
| [ScienceIDE](https://arxiv.org/abs/2609.19134) | Submitted 2026-09-16: agents turn scientific code repositories into executable environments with task generation, execution and verification, guided by expert-defined cases and acceptance criteria, and the verified trajectories train a model family the authors report as gaining on held-out scientific-code repair | Whether repository-to-environment conversion works on code without expert acceptance criteria | A second group converting a repo the authors did not choose |
| [Benchmark Radar](https://arxiv.org/abs/2609.11115) | Revised 2026-09-13: a living catalogue of 1,283 source records from 4 benchmark catalogs and 12,916 numeric observations on 790 records, with daily discovery from 37 sources, aimed at the question of which settings sit behind a reported score | Whether harness version and extraction settings become catalogued fields, which is the gap 2026-W37 named | Scores in the catalogue carrying a harness identifier |
| [Agora's 165 reproductions](https://arxiv.org/abs/2609.18094) | The reproduction count follows from the DAG being the record; if it holds outside the authors' run it is a coordination result, not a research one | Whether anyone reproduces a node from the published ancestry alone | An independent reproduction from ancestry without author assistance |
| [Codex rust-v0.155.0 voice conversations](https://github.com/openai/codex/releases/tag/rust-v0.155.0) | Experimental `/voice` conversations with live transcripts on 2026-09-17; a new input channel into a coding agent, with the transcript as the record | Whether voice transcripts enter the same permission and audit path as typed input | A transcript-driven tool call appearing in a run record |

## Watchlist

- **Does the AGENTS.md fallback reach the hosted platforms?** The note says not yet on Bedrock, Vertex or Foundry. Revisit trigger: a release note naming one of the three.
- **Does a second framework publish an advisory against its fetch tool?** pydantic-ai published four in one release and Gemini CLI shipped a destination-validation fix the same week without an advisory. Revisit trigger: a CVE or GHSA against any agent framework's fetch or browse tool.
- **Does the gateway header vocabulary get documented?** Five header names shipped without value lists. Revisit trigger: documentation naming the request classes and agent types.
- **Does the cache-hit measurement move once compaction requests are excluded?** Open since 2026-W36, with eleven client causes named in 2026-W37 and a header to isolate one more this week. Revisit trigger: ten sessions measured with the compaction flag logged.
- **Does anyone reproduce AgentGuard's completion gain outside the authors' 382 tasks?** The abnormal-run drop is large and the completion gain is a third of it. Revisit trigger: a second trace corpus reporting both rates.

## Archive notes

- **OpenAI, Codex rust-v0.155.0 and 0.155.1** ([GitHub](https://github.com/openai/codex/releases/tag/rust-v0.155.1)). Voice conversations added on 2026-09-17 and reasoning summaries turned off by default for new local sessions on 2026-09-18. One scout row; no top signal.
- **Anthropic, anthropic-sdk-python 1.6.0 and 1.7.0** ([GitHub](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v1.7.0)). Two minor releases on 2026-09-15 and 2026-09-18 with changelog links only; no agent-systems mechanism to carry.
- **Microsoft, agent-framework python 1.19.0** ([GitHub](https://github.com/microsoft/agent-framework/releases/tag/python-1.19.0)). Generic vector-store support added on 2026-09-18. A storage primitive; no builder action this week.
- **CrewAI 1.15.22** ([GitHub](https://github.com/crewAIInc/crewAI/releases/tag/1.15.22)). Aliases as connection identifiers and recorded reasons for deployment creation failures, 2026-09-16. Kept searchable; no pick.
- **Discovery inputs found out of window.** Eleven items the daily briefs carried this week were rechecked against their primaries and dated outside 2026-09-12 to 2026-09-18: the Hugging Face intrusion timeline (July 27), the coding-agent sandbox escapes (July 20), OpenAI's cyber pacing post (August 18) and Hugging Face incident post (August 26), the GPT-6 Astra system card and the Nvidia acquisition of Hugging Face (both September 3), Gemini 3.8 Flash Cyber (September 2), Anthropic's advanced tool use post (November 2025), the Amazon Science compressibility post (September 10), and two practitioner posts on self-improvement and multi-turn evaluation (August 21 and July 27). None appears as a pick.

## Sources reviewed

| Source | Status | Note |
|---|---|---|
| claude-code-changelog | ok | 8 releases 2.1.270 to 2.1.277 dated by release timestamp; 3 top signals, 1 scout row |
| agent-frameworks | ok | 21 non-patch in-window releases across pydantic-ai, deepagents, langchain, openai-agents, Strands, CrewAI, ADK, agent-framework, LiteLLM and AI SDK; 2 top signals, 4 scout rows |
| google-agents | ok | Gemini CLI v0.60.0 and v0.61.0-preview.0; 1 top signal source |
| aws-agents | ok | 1 in-window agentcore SDK release; no pick |
| mcp-spec | ok | no in-window release in the specification, python-sdk or typescript-sdk repositories |
| arxiv-cs-ai / cs-se / cs-ma | ok | 7 verified in-window preprints by submission date; 5 top signals, 2 scout rows |
| huggingface-papers | ok | discovery route for the same preprints; overlap deduped |
| openai-news | failed | vendor pages returned 403 to the fetcher; RSS dated both candidate posts outside the window |
| anthropic-news | skipped | the September threat intelligence report's page carries no publication date the fetcher could read; not cited |
| practitioner-blogs | ok | 3 posts checked, all dated outside the window |
| ai-engineer-youtube | skipped | the YouTube feed endpoint returned 404 for a control channel as well as the registered one; the channel id was verified against the handle page and left unchanged |
| Daily Systems Brief folder | ok | private discovery input, 2026-09-12 through 2026-09-18; 105 candidate URLs mined, 11 found out of window on recheck |
| Weekly Gen AI Digest folder | ok | 2026-09-18 issue used as discovery; of its cited primaries only AgentGuard falls in the window |

## Closing thought

Last week ended with the measuring apparatus uninspected. This week every result that held put the apparatus where the worker could not reach it, and every runtime change moved a control to the layer that can enforce it. The fetch tool got four patches because names were compared in the wrong form. The gateway got five headers because it could not see why. The client learned to read the contract file the portfolio had been writing for months. None of it is a smarter model. All of it is a better ruler.
