<!--
iso_week: 2026-W41
through_date: 2026-10-09
profile_id: builder-tpm
registry_version: 14
matrix_run_id: MTRX-W41-clean-exit-failures
-->

# Agents flagged a plausible wrong value from a tool in fifty-nine percent of trials, and a problem that was not there in twenty-seven.

**Week 41 through 2026-10-09 - Vol. 24**

## Field thesis

2026-W40 found that a number belongs to a pair and gets credited to one half. This week the pairs were a check and the thing it checks, and in most of the readings the check was looking at something else. A fault-injection study found agents treated an explicit tool error as a problem in 91.3 percent of trials and a plausible wrong value in 58.8 percent, against 26.8 percent who flagged a problem when nothing was wrong, and a prompt line telling one model pair to check each result moved nothing. ThinkingBox, which grades agents on the database they leave behind, reached Hugging Face with a new comparison: Claude Opus 5.5 beat Opus 5 on a single attempt and passed the same number of tasks, 241, on all twenty. On the execution side, a Windows corpus of 47,828 shell calls found Claude Code's Bash launch changing 12.0 percent of the calls that carried a heredoc, a backslash pair or long text, and an LLM judge reading the transcripts blamed the model for 97 of 102 sampled failures, 56 of which the path had caused. Claude Code's own changelog spent the week on the same gap from inside: ten fixes where a Bash permission rule read a command differently from the shell, and eleven where a guard that was restarting, interrupted, overridden or handed truncated input let the call through. The fail-closed switch shipped on Thursday, as an option. Two cheaper items close the issue. The up-front budget for an MCP tool description doubled to 4,096 characters. Haiku 5.5 arrived 90 percent cheaper than Haiku 4.5 below 100,000 tokens and 50 percent cheaper above, with a 75 percent average weighted by the old model's traffic.

## Top signals

### 1. Agents noticed 91.3 percent of tool errors and 58.8 percent of plausible wrong values

**Sources:** [Loud Failures, Quiet Failures](https://arxiv.org/abs/2610.10062), [ThinkingBox on Hugging Face](https://huggingface.co/blog/microsoft/thinkingbox), [ThinkingBox paper](https://arxiv.org/abs/2608.19741), [Claude Code 2.1.290](https://github.com/anthropics/claude-code/releases/tag/v2.1.290) and [Claude Code 2.1.292](https://github.com/anthropics/claude-code/releases/tag/v2.1.292)

**Payload:** Submitted 2026-10-07, a fault-injection study ran six models over 24 tasks of one function-calling benchmark for 1,920 trials. Agents treated an explicit tool error as a problem in 91.3 percent of trials, a plausible wrong value in 58.8 percent, and flagged a problem when nothing was wrong in 26.8 percent. A prompt line asking one model pair to check each result did not move detection, and two fault-free runs of the same task ended in the same state only 63.3 percent of the time. On 2026-10-03 Microsoft and Hugging Face put ThinkingBox on Hugging Face. It grades agents on the terminal backend state and side effects they leave, across 507 stateful business workflows each run 20 times, and 2026-W34 covered the paper behind it. The post adds a comparison the paper lacked: Claude Opus 5.5 beat Claude Opus 5 on the every-attempt average, 67.16 against 66.50 percent, and passed the same number of tasks on all 20 attempts, 241, while GPT-6 Astra kept 78 percent of its single-attempt rate and three open-weight models kept about 8 percent. The post also restates a result from that paper, first posted 2026-08-20: in a common-set ablation of 121,680 valid trials across 12 models, 79,853 attempts failed the executable checks, and 67.24 percent of those failures had terminated cleanly, invoked a state-changing tool and reported no error in the final tool response. The checks found wrong field values in 77.61 percent of all the failed attempts, unintended extra effects in 43.30 percent and missing required effects in 25.36 percent. In the same week Claude Code fixed four tool results that had been dropping data without saying so: WebFetch losing page text past 100,000 characters, Grep and Glob reporting no matches on a path they could not read, @-mentioned files over 256KB left out, and a PDF read with a list of pages returning only the first entry.

**Mechanism:** The agent and the grader read the same channel, and the channel is the error field. A run that writes the wrong value to the right record gets success back from every tool, so the agent reports success, the transcript reads as success, and a grader scoring tool calls agrees. The fault-injection numbers price the agent's half: an explicit error gets noticed nine times in ten, a well-formed wrong value about six in ten against a false-alarm rate near three in ten, and in the one model family tested, an instruction to check each result changed nothing. The ThinkingBox paper prices the grader's half: two-thirds of real failures passed a check that looks only for a clean finish, a write and no error in the last tool result. The Claude Code fixes are the tool-side version of the repair, four results that used to look complete and now say what they dropped.

**Why it matters:** 2026-W39 recorded three silent losses learning to announce themselves. This week puts a rate on what a silent loss does to the agent that receives it, beside the August rate for how often a failed run passes a check that reads only how it ended. W40's first pick asked for a repeat count before any comparison, and the 241-for-241 tie between two Opus versions is that argument made with a database. The factory scores runs on first-pass acceptance; whatever reads the run's own report to decide acceptance is reading the channel that looked clean in two-thirds of ThinkingBox's failures. The two papers are authors' benchmarks, the fault-injection result is one benchmark's 24 tasks, and the clean-exit share is six weeks older than this issue.

**Reusable pattern:** Grade the end state instead of the report, and test an agent with faults that keep the expected format.

**Action surface:** eval

**Try this week:** Pick one factory task with a checkable end state. Run it five times with one tool returning a well-formed wrong value at a fixed step, such as a stale file read or an empty grep on a file that exists, and count how many runs notice. Then grade the same five runs on the end state alone and compare with what each transcript claims.

**Systems map:** tool returns a well-formed wrong value -> no error field set -> agent continues and reports success -> transcript reads clean -> grader scoring tool calls agrees -> wrong value reaches the record -> repeat runs end in different states -> single-run pass rate overstates dependability.

**Transferable principle:** A check that reads the producer's own account of the work inherits the producer's blind spots, and a failure that keeps the expected format passes every check that only looks at the format. Audits that sample receipts instead of bank balances and monitoring that alerts only on exit codes fail the same way.

**Falsification test:** If five factory runs with an injected plausible wrong value all notice the fault, and end-state grading agrees with the transcript on every run, this pilot found no transcript/state disagreement. Keep the end-state check; one fault at one step does not establish transcript grading as adequate.

**Adoption ladder:**
  - Minimum viable: one task run five times with one injected well-formed wrong value, detections counted and end states checked.
  - Mid: an end-state check for every factory task class that has one, run beside the transcript verdict, with disagreements logged.
  - Full: explicit and plausible-wrong faults injected in the factory's eval suite, each task repeated enough times to report an every-attempt pass count beside pass@1.
  - Monitoring: transcript-pass and state-fail disagreements per week; detection rate by fault type; tasks passing every repeat.

**Confidence:** medium

**Evidence:** MTRX-W41-CLEAN-EXIT-FAILURES, MTRX-W41-REPEAT-DEPENDABILITY, MTRX-W41-QUIET-FAULT-DETECTION, MTRX-W41-RUN-TO-RUN-BASELINE, MTRX-W41-SILENT-TOOL-LOSSES

### 2. A judge reading transcripts blamed the model for 97 of 102 failures, and the path caused 56 of them

**Sources:** [Do Tool Calls Execute as Intended?](https://arxiv.org/abs/2610.04375), [Claude Code 2.1.290](https://github.com/anthropics/claude-code/releases/tag/v2.1.290) and [Claude Code 2.1.292](https://github.com/anthropics/claude-code/releases/tag/v2.1.292)

**Payload:** Submitted 2026-10-03, a study of intent-execution correspondence asks whether the shell command an agent emits is the command that runs. A call reaches its program through several hops, and any hop can change it without notice. On a Windows corpus of 47,828 shell calls that Claude Code and Codex ran through Git Bash and PowerShell 5.1 in 261 sessions by six developers at one company, Claude Code's Bash launch changed 12.0 percent of the 7,491 exposed calls, those carrying a heredoc, a backslash pair or at least 1,000 characters. The rate was 67.0 percent for calls with a backslash pair and 100 percent for calls of 8,000 characters or more. For 80.7 percent of the calls whose backslashes were changed, the wrong action ran with no reported error. All 10 measured harnesses changed a call. Two annotators labelled 102 production failures, sampled within each of the authors' protocol verdicts, and put 56 of them on the path. An LLM judge reading each whole trajectory attributed 97 of the 102 to the model, the 95.1 percent the abstract reports; two step-wise judges flagged the path in 49 and 45 of them but agreed with the labels no better than chance. On the authors' benchmark the path raised token cost per passed task 2.4 times, up to 12.3 times, and because a changing hop hides the changes after it, 55.1 percent of the failures on one path showed up only after its first hop was repaired. On the same benchmark the authors' fix recovers 79.2 percent of the failures with a changed call, 137 of 173; they also run it in an unnamed commercial product. Claude Code's changelog fixed two cousins from the inside: permission rules not applying after a PreToolUse hook rewrote a call's input (2.1.290), and plugin hooks seeing calls before misnamed parameters were repaired (2.1.292).

**Mechanism:** The model writes a command and something else runs it. Each hop between them has its own parser, and where two parsers disagree about a backslash or a line break, the executed action differs from the emitted one. The model then sees a failure it did not cause, retries the correct call, gets changed again, and pays tokens for every round, which is where the 2.4x comes from. A judge reading the trajectory sees the call the model wrote and the error that came back, and blames the model, because the transcript has no field for what the shell received. The measurement needs no model call: the authors keep the harness launch and swap only the program that would execute the command for one that reports the text it received, and for Bash that program is a file Bash sources before it runs the command string.

**Why it matters:** The portfolio's Claude Code sessions run on Windows through Git Bash, the launch the 12.0 percent was measured on, and Claude Code writes its commit messages through heredocs. A transcript records the call the model emitted and the result that came back, so triage that reads transcripts cannot see the path: of the paper's three transcript judges, one blamed the model almost every time and two split the blame at random. The corpus is one company's and the client version behind it is not stated in the passages read, so the rate may have moved since. The witness test answers that for the portfolio's own version in an afternoon.

**Reusable pattern:** Test the execution path hop by hop with a witness that reports what each hop received, and attribute a failure to the model only after the path is cleared.

**Action surface:** runtime-adapter

**Try this week:** On one Windows factory host, point `BASH_ENV` at a script that appends `$BASH_EXECUTION_STRING` to a log and exits before the command runs. Replay twenty recent Claude Code Bash calls that carry a heredoc, a backslash pair or more than 1,000 characters, and diff each logged string against the emitted call. Every difference is a changed call that no transcript shows.

**Systems map:** model emits a call -> wrapper re-quotes it or merges backslash pairs -> shell parses a different command -> wrong action runs, mostly with no error -> agent sees an unexpected result and retries the correct call -> same hop changes it again -> tokens per passed task rise -> transcript judge reads the emitted call and blames the model.

**Transferable principle:** When a request crosses several parsers, the request that executes is the one the last parser built, and a log written at the first hop records intent and not action. Shell quoting across SSH, CSV through a spreadsheet import, and SQL built through an ORM break the same way.

**Falsification test:** If the witness shows every replayed call reaching the shell byte-identical to what the model emitted, these twenty calls showed no path change on this host and version. Witness the failing call before assigning its cause.

**Adoption ladder:**
  - Minimum viable: twenty exposed Bash calls replayed through a `BASH_ENV` witness on one Windows host, with changed calls counted.
  - Mid: the witness run on every host and client version the factory uses, with heredocs and long commands written to a file and executed by path wherever the witness finds changes.
  - Full: a hop-level check in factory failure triage, so a failure is attributed to the model only after the executed command matches the emitted one.
  - Monitoring: changed calls per hundred exposed calls by host and version; failures reattributed from model to path; tokens per passed task before and after.

**Confidence:** medium

**Evidence:** MTRX-W41-HOP-CHANGE-RATE, MTRX-W41-MODEL-BLAMED, MTRX-W41-PATH-COST, MTRX-W41-WITNESS-METHOD, MTRX-W41-HOOK-REWRITE-FIXES

### 3. Ten Bash permission fixes in seven days, each one a command the checker read differently from the shell

**Sources:** [Claude Code 2.1.289 to 2.1.296](https://github.com/anthropics/claude-code/releases), [Codex rust-v0.162.0](https://github.com/openai/codex/releases/tag/rust-v0.162.0), [Codex rust-v0.161.0](https://github.com/openai/codex/releases/tag/rust-v0.161.0) and [langchain-core 1.6.8](https://github.com/langchain-ai/langchain/releases/tag/langchain-core%3D%3D1.6.8)

**Payload:** Between 2.1.289 on 2026-10-03 and 2.1.296 on 2026-10-09, ten Claude Code release-note lines fix a Bash deny or ask rule, a Bash permission check or a sandbox exemption pattern that missed a command, approved it unasked or let it out of the sandbox because the checker read the command differently from the shell, git or the filesystem. The spellings: an environment-variable prefix with an expanded value (the note's example is `TZ="$HOME" rm -rf build`), a bare variable assignment before the command, a name set as a prefix on `declare`, `typeset`, `export` or `readonly`, wildcards the shell still expands inside `rg` and `git grep` arguments, variable names zsh reads differently from bash, the short form of a `git clone` option, a wildcard inside an option value, an 8.3 or alternate Windows spelling of a home folder or drive, an assignment to `BASH_ARGV0`, and `rm -rf /c/Users/<name>` in Git Bash. Three more fixes close reads that returned a file outside what was approved through a link swapped mid-read. Codex rust-v0.162.0, on 2026-10-08, stops a ripgrep configuration from weakening deny-glob masks, after rust-v0.161.0 the day before let an approved filesystem escalation widen write access while keeping denied reads and network restrictions. langchain-core 1.6.8, also on 2026-10-08, hardens its SSRF checks against scoped and compatible IPv6 addresses. No note carries a severity.

**Mechanism:** A deny rule matches text and the shell executes a parse. Wherever the two disagree about what a command is, the rule and the shell are looking at different commands, and the rule loses. Each of the ten is one such disagreement: a prefix the checker treats as noise and the shell treats as an environment, a variable name zsh and bash resolve differently, a path with two spellings that reach one folder. The list cannot be finished from the matcher's side, because the shell grammar and the filesystem's aliases are larger than any pattern set. The link-swap fixes are the same gap in time: the path checked at approval and the path read a moment later were different files. Two of the ten applied only under sandbox auto-allow, where the sandbox still bounded what the command could reach, and that arrangement is the one that holds up: an OS-level boundary on what the process can touch, with text rules on top for convenience. The `git clone` fix cuts the other way: a text pattern decided which commands left the sandbox, so the boundary was only as tight as that pattern.

**Why it matters:** 2026-W38's second pick found a blocked domain reachable under another spelling in a fetch tool, and the IPv6 forms langchain-core hardened this week belong to the same family. Two of the ten spellings are Windows-specific, and the portfolio's hosts run Windows with Git Bash. Any Bash deny rule in the portfolio's Claude Code settings that stands alone between an agent and a destructive command depended on these ten readings until 2026-10-09, and on whichever spelling is found next after that.

**Reusable pattern:** Treat a text-matching deny rule as a speed bump, and put the enforcement where the effect lands: the sandbox, the filesystem permission, the network policy.

**Action surface:** security

**Try this week:** List every Bash deny or ask rule in the portfolio's Claude Code settings and mark, for each, whether a sandbox or filesystem permission would stop the same command if the rule missed. Upgrade every host to 2.1.296, then test the ten spellings in a disposable fixture with harmless witness commands against the rules marked unbacked. Unbacked rules are the exposure whether or not the spellings get through today.

**Systems map:** deny rule written as a command pattern -> agent emits the command in another spelling -> checker parses it one way -> shell parses it another -> rule misses or auto-approves -> command runs -> only an OS-level boundary limits the effect -> vendor ships a fix per spelling -> next spelling found.

**Transferable principle:** A filter that inspects a representation and an executor that interprets it are two parsers, and every disagreement between them is a bypass. Web application firewalls, SQL keyword blocklists and attachment filters keyed on file extensions have the same record.

**Falsification test:** If every Bash deny rule in the portfolio is backed by a sandbox or filesystem permission that stops the same command, the ten fixes were defence in depth here and the rules were never the boundary.

**Adoption ladder:**
  - Minimum viable: Bash deny and ask rules inventoried with a backed or unbacked mark, and every host on 2.1.296 or later.
  - Mid: every unbacked rule given an OS-level counterpart in sandbox write roots, deny-read paths or network policy, and the ten spellings kept as a regression test against the rules.
  - Full: destructive operations enforced at the sandbox or filesystem layer, text rules kept for prompts and convenience, and a release-note watch that adds each newly fixed spelling to the regression set.
  - Monitoring: unbacked rules; spellings in the regression set; denials by layer, rule against sandbox; hosts below the latest permission fix.

**Confidence:** high

**Evidence:** MTRX-W41-BASH-RULE-SPELLINGS, MTRX-W41-LINK-SWAP-READS, MTRX-W41-CODEX-DENY-GLOB, MTRX-W41-IPV6-SPELLING

### 4. Eleven fixes for a guard that let the call through, and fail-closed arrived as an option

**Sources:** [Claude Code 2.1.295](https://github.com/anthropics/claude-code/releases/tag/v2.1.295), [Claude Code 2.1.290 to 2.1.296](https://github.com/anthropics/claude-code/releases), [deepagents-code 0.1.81](https://github.com/langchain-ai/deepagents/releases/tag/deepagents-code%3D%3D0.1.81) and [LiteLLM 1.106.0-dev.1](https://github.com/BerriAI/litellm/releases/tag/v1.106.0-dev.1)

**Payload:** Claude Code 2.1.295, published 2026-10-08, adds `onFailure: "block"` for command and HTTP hooks: a hook that cannot start, times out or exits with an unexpected code blocks the action instead of letting it through. The note adds the setting and says nothing about the default. Around it, eleven release-note lines between 2.1.290 and 2.1.296 fix a guard or hook that let a call or prompt through. Tool calls were answered without the plugins' permission hooks while the hooks worker restarted. A hook that failed after an interrupt let the call through. A guard's catch was skipped for calls another mod made beneath it. A plugin's allow answer ran a tool that needed the user's answer. A deny was ignored because its reason ran past 4,096 characters. `prompt` and `agent` hooks written as instructions, such as "Block commands that...", allowed what they should block. A guard was handed a heavily nested tool input that had been cut short with no error. Calls made during a reload got past another mod's guard. An interrupt during a prompt hook let the unchecked prompt through. A user mod could make an organization's guard skip its check, and a busy hook's catch was skipped. Elsewhere, deepagents-code 0.1.81 (2026-10-06) makes hook execution fail closed when its context changes on resume, and a LiteLLM dev build (2026-10-07) makes one guardrail integration fail closed on a missing verdict.

**Mechanism:** A guard has two jobs, deciding and being there, and most of the eleven are failures of the second. A guard that is restarting, interrupted, overridden or handed half its input makes no decision at all, and the runner treated no decision as allow. For command and HTTP hooks the release now gives an explicit failure setting. The note does not establish the unset default; the drill below tests it. The prompt-hook fix is the odd one out and the more instructive: a guard written as an English sentence was judged by a model, and the model let through what the sentence said to block. A rule that can be written as code is safer written as code.

**Why it matters:** The portfolio's policy engine approves tool calls against declared targets, and any part of it that runs as a client hook inherits the hook runner's failure default. A gate that opens when its own process dies is a gate for the days nothing goes wrong. At least nine of the eleven fixes sit in Claude Code's plugin and mod hook layer, which is young and changing every release, so the count says as much about that surface as about hooks in general.

**Reusable pattern:** Decide what a guard does when it is missing, and make missing mean deny for anything that writes, spends or sends.

**Action surface:** governance

**Try this week:** Pick the one hook in the portfolio that gates the most consequential tool call. On a copy, make the hook script exit with an unexpected code and run the gated call twice, once with `onFailure: "block"` and once without. Record whether the call ran each time.

**Systems map:** guard registered -> hook runner restarts, times out, is interrupted or truncates the input -> guard returns no decision -> runner treats no decision as allow -> call runs ungated -> transcript shows no denial -> absence of a block reads as approval.

**Transferable principle:** A control's failure mode is part of the control, and a gate that opens when its power fails protects only while nothing goes wrong. Electronic door locks, circuit breakers and payment fraud checks that approve on timeout are each specified as fail-safe or fail-secure for this reason.

**Falsification test:** If a forced failure of a portfolio hook blocks the gated call without `onFailure` set, the runner already fails closed for that hook type and the setting changes nothing here.

**Adoption ladder:**
  - Minimum viable: one consequential hook tested with a forced failure, with and without `onFailure: "block"`, and the outcome recorded.
  - Mid: `onFailure: "block"` set on every hook that gates a write, a spend or an outbound send, and plain-language prompt hooks replaced by command hooks wherever the rule can be stated in code.
  - Full: a hook-failure drill in the factory's regression suite that kills, times out and truncates each gating hook and asserts the call is refused, with the client version pinned until the drill passes on a new release.
  - Monitoring: gating hooks without a fail-closed setting; drill failures per release; calls that ran while a hook reported an error.

**Confidence:** medium

**Evidence:** MTRX-W41-HOOK-ONFAILURE-BLOCK, MTRX-W41-GUARD-GAPS, MTRX-W41-FAIL-CLOSED-ELSEWHERE

### 5. The up-front budget for one MCP tool description doubled to 4,096 characters

**Sources:** [Claude Code 2.1.296](https://github.com/anthropics/claude-code/releases/tag/v2.1.296), [Claude Code 2.1.295](https://github.com/anthropics/claude-code/releases/tag/v2.1.295) and [Revamping Skills in Deep Agents](https://www.langchain.com/blog/revamping-skills-in-deep-agents)

**Payload:** Claude Code 2.1.296, published 2026-10-09, raises the default limit on MCP tool descriptions sent up front, and on MCP server instructions, from 2,048 to 4,096 characters, and adds `autoCompactWindow` to subagent definitions so a subagent can compact earlier than the main conversation. A day earlier 2.1.295 raised the cut for descriptions the model loads through tool search from 2,048 to 16,384 characters and capped subagent skill preloading at 32. On 2026-10-07 LangChain went the other way in Deep Agents: tools can be bound to a skill, so their schemas stay out of context until the agent reads that skill, and on models that accept tools mid-conversation, adding them keeps the prompt cache intact. A call to a bound tool before its skill is read fails as an unknown tool, and a reload that finds new skills changes the system prompt and invalidates the cache. LangChain reports enterprise skill registries growing to thousands of skills.

**Mechanism:** A tool description sent up front is paid on every request of the session, inside the cached prefix, and its length sets how many tools fit before the prefix crowds out the work. A higher per-description ceiling changes nothing for a server whose descriptions were already short, and lets a server whose descriptions were being cut send up to twice as much on every request. The tool-search change pulls the other way in the same week: descriptions loaded on demand can now run eight times longer, which rewards deferring. Deep Agents makes deferral structural. A schema bound to a skill costs nothing until the skill is read, and the price moves to two places: an unknown-tool error if the model reaches for it early, and a cache miss when the skill list changes.

**Why it matters:** Portfolio sessions connect several MCP servers, and their descriptions sit in every request's prefix. After 2.1.296 that prefix may have grown with no config change, which adds another moving input to the cache-hit measurement open since 2026-W36. The bound-tool pattern lands on the factory's skills, whose names and descriptions load at session start, and 2.1.295 put a 32-skill ceiling on what a subagent preloads.

**Reusable pattern:** Count the tool-description bytes in the prefix after every client upgrade, and move tools that serve one skill behind that skill.

**Action surface:** context

**Try this week:** Open one factory session with every usual MCP server connected, run `/context` at session start on 2.1.295 and again on 2.1.296, and record the MCP tools line both times. The difference is what the new default costs per request before caching. Then list which servers send descriptions longer than 2,048 characters.

**Systems map:** MCP servers connected -> descriptions sent up front in every request -> client raises the per-description ceiling -> longer descriptions pass uncut -> prefix grows -> fewer tokens left for work and more cache to write -> deferral through tool search or skill binding moves schemas out -> early calls fail as unknown tools and skill reloads miss the cache.

**Transferable principle:** A fixed per-request overhead scales with request count and not with use, so the cheapest description is the one loaded when it is needed. Eagerly loaded JavaScript bundles and ORM queries that join every relation pay the same tax.

**Falsification test:** If no connected server sends a description longer than 2,048 characters, the 2.1.296 change is inert for the portfolio and only the deferral half applies.

**Adoption ladder:**
  - Minimum viable: MCP description tokens at session start recorded on 2.1.295 and 2.1.296 for one session, with servers over 2,048 characters listed.
  - Mid: tools that serve one skill moved behind tool search or skill binding, and the up-front description budget recorded per session in the run record.
  - Full: an up-front tool-context budget per task class, checked at session start, with subagents given their own `autoCompactWindow` and preload lists under the cap.
  - Monitoring: description tokens per session; unknown-tool errors from deferred tools; cache misses after skill reloads; prefix share of request tokens.

**Confidence:** medium

**Evidence:** MTRX-W41-MCP-DESCRIPTION-BUDGET, MTRX-W41-SKILL-BOUND-TOOLS

### 6. Haiku 5.5 is 90 percent cheaper below 100,000 tokens and 50 percent cheaper above

**Sources:** [Claude Haiku 5.5](https://www.anthropic.com/claude-haiku-5-5), [Claude Haiku 5.5 (Simon Willison)](https://simonwillison.net/2026/Oct/7/claude-haiku-5-5/), [Claude Code 2.1.293](https://github.com/anthropics/claude-code/releases/tag/v2.1.293) and [Claude Code 2.1.296](https://github.com/anthropics/claude-code/releases/tag/v2.1.296)

**Payload:** Anthropic, 2026-10-07: Haiku 5.5 is priced 90 percent below Haiku 4.5 for requests up to 100,000 tokens and 50 percent below for requests over, at $0.10 and $0.50 per million input and output tokens up to 100k and $0.50 and $2.50 over. The headline of around 75 percent less on average is weighted by Haiku 4.5's traffic, 90 percent of which fell under 100,000 tokens, and accounts for an updated tokenizer that uses slightly more tokens per task. Simon Willison, the same day, counted one long prompt at around 1.25 times as many tokens on Haiku 5.5 as on Haiku 4.5, noted that reasoning cannot be switched off, and judged GPT-6 Luna the better deal above 100,000 tokens. Claude Code 2.1.293 made `claude-haiku-5-5` the default Haiku on the Anthropic API the same day. Anthropic also halved Sonnet 5.5 cache reads from $0.20 to $0.10 per million tokens, which it says cuts Sonnet 5.5's cost on most agentic tasks by around 20 percent because cache reads are a large share of consumption. Claude Code's local cost figures and `--max-budget-usd` moved to the new cache-read rate two days later, in 2.1.296.

**Mechanism:** A tiered price turns context length into a unit-cost switch. Below 100,000 tokens a Haiku token is priced at a tenth of what it was; above, half. An agent's context grows over a session, so the same subagent can cross the line mid-run, and its listed per-token rates rise fivefold at that point. The published average uses the old model's traffic, nine-tenths short prompts. Request share alone cannot reproduce the saving: long requests contribute more tokens and dollars. A different mix gets a different number, and the tokenizer multiplies every request's token count before any price applies. The Sonnet cut runs on the same arithmetic from the other side: cache reads make up a large share of a long agent's tokens, so the dollar effect of halving their price depends on the cache-read share of spend.

**Why it matters:** A Claude Code Anthropic-API session in the portfolio using the default Haiku changed model and price on 2026-10-07 with no config change. The model-routing ledger from W40 prices tiers per task class; its Haiku row needs the portfolio's own prompt-length split before the new price means anything, and its Sonnet rows move by each class's cache-read share. For two days after the price cut, local spend readings for Sonnet ran high, which is the rare meter error in the reader's favour.

**Reusable pattern:** Price a tiered model on your own request-length distribution instead of the vendor's average, and re-check model aliases after every launch.

**Action surface:** cost

**Try this week:** Pull one week of Haiku calls from the portfolio's logs and split them at 100,000 prompt tokens. Price the input, output, cache-read and cache-write tokens in each group at both models' rates; the request count alone cannot give the saving. Then count one representative prompt on both tokenizers, since the 1.25x is one author's single measurement.

**Systems map:** model launched with a price tier at 100,000 tokens -> alias moves to the new model -> agent context grows across a session -> step crosses the tier -> unit price rises fivefold -> vendor average weighted by the old request mix -> local saving differs from the headline -> tokenizer adds tokens before any discount applies.

**Transferable principle:** An average discount is a statement about someone else's distribution, and a tiered price makes the distribution the whole answer. Utility tariffs with consumption bands and cloud egress pricing read the same way.

**Falsification test:** If the portfolio's Haiku traffic sits almost entirely below 100,000 tokens and a re-count shows the tokenizer change near zero for its prompts, the short-prompt list-rate reduction is near 90 percent here. Check measured tokens per completed task before calling that a task-cost saving.

**Adoption ladder:**
  - Minimum viable: one week of Haiku calls split at 100,000 tokens, with one representative prompt counted on both tokenizers.
  - Mid: the routing ledger's Haiku row priced on the portfolio's own length split, Sonnet rows re-priced on cache-read share, and model aliases replaced by explicit model ids in agent configs.
  - Full: compaction thresholds for Haiku subagents set below 100,000 tokens where the task allows, with cost per completed task tracked by model and tier.
  - Monitoring: share of Haiku requests above 100,000 tokens; cost per completed task by model; alias resolutions changed by a client release.

**Confidence:** high

**Evidence:** MTRX-W41-HAIKU-PRICE-CLIFF, MTRX-W41-TOKENIZER-1-25X, MTRX-W41-HAIKU-DEFAULT-ALIAS, MTRX-W41-SONNET-CACHE-READ-CUT

## Framework-runtime scout

| Source | Primitive changed | Why it matters | 30-90 minute test |
|---|---|---|---|
| [Claude Code 2.1.292](https://github.com/anthropics/claude-code/releases/tag/v2.1.292) | tool gateway | Local stdio MCP servers now negotiate protocol version 2026-07-28 by default on every install, Bedrock, Vertex and Foundry included, with `MCP_PROTOCOL_NEGOTIATION=legacy` to opt out; a server that ignores the newer check is remembered for 7 days after one slow connect. The same release adds an `effort` parameter to the Agent tool | Connect each home-grown stdio MCP server on 2.1.292 or later and time the first connect; a slow one is mishandling the new handshake |
| [Codex rust-v0.161.0 and rust-v0.162.0](https://github.com/openai/codex/releases/tag/rust-v0.162.0) | config | Background tasks keep their originating turn's permissions (0.161.0), and Responses and WebSocket retries honour server `Retry-After` advice (0.162.0) | Start a background task from a restricted turn and confirm it cannot write where the turn could not |
| [MCP TypeScript SDK 2.3.1](https://github.com/modelcontextprotocol/typescript-sdk/releases/tag/v2.3.1) | agent identity | `requireBearerAuth` in `server-legacy` takes the optional `expectedResource` that `server` 2.3.0 added, accepting only tokens issued for this server; off unless set | Check whether the portfolio MCP server uses the legacy bearer helper, and set `expectedResource` if it does |
| [LiteLLM 1.106.0-dev.1](https://github.com/BerriAI/litellm/releases/tag/v1.106.0-dev.1) | tool gateway | Marked breaking: stdio MCP servers are disabled by default in the proxy. Dev pre-release only in the window | List stdio MCP servers registered on any LiteLLM proxy the portfolio runs, before this reaches a stable tag |
| [pydantic-ai 2.55.0](https://github.com/pydantic/pydantic-ai/releases/tag/v2.55.0) | observability | Each failed `FallbackModel` attempt is recorded with its model, timing, error and usage, rejected responses count in `RunUsage`, and default `run_id` stays stable across durable re-execution. Python 3.10 installs resolve to 2.54.0 | Compare `RunUsage` for one run that falls back, before and after the upgrade; the difference is spend the old count left out |
| [browser-use 0.13.11](https://github.com/browser-use/browser-use/releases/tag/0.13.11) | security | Sensitive-data redaction now reaches values nested below list boundaries in saved agent history | Grep saved browser-agent histories written before the upgrade for credentials inside lists |
| [CrewAI 1.15.27](https://docs.crewai.com/en/changelog) | runtime-adapter | Stops sending `stopSequences` to OpenAI GPT-6, GPT-5.6 and gpt-oss; the changelog line does not say what the parameter did to those requests | Send one request per model family through each framework adapter the portfolio uses and log which parameters reach the provider |
| [Vercel Sandbox](https://vercel.com/changelog/sandbox-create-waits-until-ready) | runtime-adapter | `Sandbox.create()` now resolves after snapshot restore, so startup failures reject at create; creation is about 50 ms longer at p50, more for uncached snapshots | Move sandbox timeout and error handling from the first command to the create call |
| [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) | cost | Ultrafast mode for GPT-6.1 Sol in the Responses API (2026-10-08) cuts the time between output tokens as a priced service tier | Price one latency-bound step at the Ultrafast tier before routing anything to it |

## Reusable patterns

- **Grade the end state, and inject faults that look like success.** Where it applies: eval suites, factory acceptance, regression tests for tool-using agents. Caveats: both results are authors' benchmarks, the fault-injection rates come from 24 tasks on one function-calling benchmark, and the clean-exit share dates from the ThinkingBox paper's August version.
- **Witness each hop before blaming the model.** Where it applies: shell tools, MCP servers, any wrapper between model output and execution. Caveats: the 12.0 percent is one company's Windows corpus on an unstated client version, and the 95.1 percent is one LLM judge on 102 sampled failures.
- **Put enforcement where the effect lands.** Where it applies: Bash deny rules, URL blocklists, file read rules. Caveats: the release notes carry no severity, and two of the ten Bash misses applied only where a sandbox still bounded the command.
- **Make a missing guard mean deny.** Where it applies: client hooks, guardrail services, approval gates on writes and spends. Caveats: the release adds a fail-closed setting without stating the unset default, and most counted fixes sit in a young plugin layer.
- **Price on your own distribution.** Where it applies: tiered model prices, cache-read discounts, any vendor average. Caveats: the 1.25x tokenizer figure is one prompt, and the over-100k price is labelled by prompt size without saying whether it applies to the whole request.

## Action queue

| Candidate | Surface | Effort | Risk | Test |
|---|---|---|---|---|
| Inject a plausible wrong value into five runs of one task and grade on end state | eval | S | low | Runs that notice; transcript verdicts the end state contradicts |
| Replay twenty exposed Bash calls through a `BASH_ENV` witness on a Windows host | runtime-adapter | S | low | Calls the shell received differently from how the model emitted them |
| Mark each Bash deny rule backed or unbacked and upgrade hosts to 2.1.296 | security | S | low | Count of deny rules with no OS-level counterpart |
| Force one gating hook to fail with and without `onFailure: "block"` | governance | S | low | Whether the gated call ran in each case |
| Record MCP description tokens at session start on 2.1.295 and 2.1.296 | context | S | low | Prefix growth per request from the new default |
| Split one week of Haiku calls at 100,000 prompt tokens | cost | S | low | Share above the tier and the saving it implies |

## Action packets

| Source | Target | Surface | Try | Proof metric | Rollback | Kill criterion |
|---|---|---|---|---|---|---|
| huggingface-blog | factory eval suite | eval | Five runs of one task with one injected well-formed wrong value, graded on end state | Detections out of five; transcript-pass and state-fail disagreements | Test harness only; production runs untouched | All five runs notice and end-state grading agrees with every transcript |
| arxiv-cs-ai | factory Windows hosts | runtime-adapter | `BASH_ENV` witness replay of twenty exposed Bash calls | Changed calls out of twenty | Unset `BASH_ENV`; read-only replay | Every replayed call reaches the shell unchanged |
| claude-code-changelog | Claude Code permission settings | security | Inventory Bash deny rules with a backed mark and upgrade hosts | Unbacked rules; hosts below 2.1.296 | Inventory is documentation; upgrade is a version pin revert | Every rule is backed by an OS-level control |
| claude-code-changelog | portfolio hook gates | governance | Forced hook failure with and without `onFailure: "block"` | Whether the gated call ran in each case | Setting is per hook and removable | The runner already blocks on failure without the setting |
| claude-code-changelog | factory session context | context | `/context` at session start on two client versions | MCP description tokens per session; servers over 2,048 characters | Read-only | No server sends a description over 2,048 characters |
| anthropic-news | model-routing ledger | cost | Split a week of Haiku calls at 100,000 tokens and re-count one prompt on both tokenizers | Share above the tier; tokenizer ratio on the portfolio's prompt | Ledger annotation only | Traffic sits almost entirely under the tier and the ratio is near one |

## Scout radar

| Item | Why it might matter early | What to watch | Revisit trigger |
|---|---|---|---|
| [Strands Box](https://aws.amazon.com/blogs/opensource/introducing-strands-box-ai-agent-sandboxes-powered-by-dogwood) | 2026-10-07, developer preview: an Apache-2.0 sandbox that pairs OS isolation with Dogwood policies evaluated on the requested action and the agent's recorded history, so a rule can say the agent may post to a channel no more than three times every 10 minutes | Whether history-aware policy holds up outside AWS's own examples; the post carries no enforcement benchmark | A third-party deployment or a measured overhead per decision |
| Spend gates on money-moving tools: [Restock](https://www.langchain.com/blog/agents-that-can-pay-with-stripe-link), [Vercel CLI domains](https://vercel.com/changelog/agents-can-now-buy-domains-with-the-vercel-cli) and [default hard budget caps](https://simonwillison.net/2026/Oct/3/default-hard-budget-caps/) | 2026-10-03 to 2026-10-09: LangChain's sample agent pays through a wallet that holds the credential, so the agent never sees a card and cannot spend above the amount the user approved; Vercel's CLI returns a structured error and next commands instead of buying a domain non-interactively; Simon Willison argues hard caps should be the default on usage-billed services | Whether any of this ships past samples and opinion; W40's scout radar already asked whether the portfolio's own spend caps are read-then-check | A portfolio agent gaining a tool that moves money or creates a paid resource |
| [AQuA](https://developers.googleblog.com/the-outer-loop-insights-first-an-ambient-quality-agent-that-diagnoses-your-production-agent/) | 2026-10-08: Google's open-source ambient quality agent runs beside a production agent, clusters failures from transcripts, and ties root causes to the deployed source snapshot, for the regressions where every infrastructure health check stays green | Whether it reports accuracy against labelled failures; the post gives none | A published precision figure, or a second team running it on its own agent |
| [ASCENT](https://arxiv.org/abs/2610.05303) | Submitted 2026-10-04: an agent distils its own verified trajectories into persistent LoRA weights during deployment, replacing retrieved text memory with weight updates, on ALFWorld, WebShop and AppWorld | Whether it holds outside three benchmarks, since the abstract gives no scores and the method needs trainable weights | Numbers on a coding or tool-use benchmark, or an open-weights deployment report |
| [AgentMonBench](https://arxiv.org/abs/2610.06406) | Submitted 2026-10-05: a training-free evidence graph that groups source-linked evidence into behaviours so a monitor can find consequential decisions in long agent traces | The abstract says it helps in most settings across eight models and gives no figures | Reported rates, or the graph applied to a trace format the portfolio already writes |
| [Confidence-based decision fallbacks](https://vercel.com/changelog/confidence-based-decision-fallbacks) | 2026-10-06: Vercel's AI Gateway escalates a decision request to a stronger model only when the primary answer trips a confidence condition, the same week OpenAI put a Decisions API in beta | Whether escalate-on-uncertainty beats a fixed tier on cost per correct decision | A published comparison against a fixed mid-tier default |
| [Query-time ACLs for retrieval](https://aws.amazon.com/blogs/machine-learning/rethinking-access-control-for-rag-with-amazon-quick-and-amazon-bedrock/) | 2026-10-07: AWS checks permissions against the source system at query time instead of replicating ACLs into the index on a periodic sync, where they can go stale | The added latency per query, which the post does not quantify | A latency figure, or a stale-ACL leak reported against a replicate-and-filter index |

## Watchlist

- **Does fail-closed become the default for hooks?** 2.1.295 shipped `onFailure: "block"` as an option. Revisit trigger: a release note changing the default hook failure behaviour, or the portfolio's own drill showing a call running on a failed hook.
- **Does the 12.0 percent survive on current clients?** The corpus behind it is one company's, on a client version the passages read do not name. Revisit trigger: the portfolio's witness replay, or a second corpus on a stated version.
- **Anthropic's usage policy takes effect on November 12.** The update adds controls for Claude taking physical actions autonomously and a new section on deceptive activity. Revisit trigger: 2026-11-12, against any portfolio agent that acts outside a sandbox.
- **Cyber work on Claude now runs through three access tiers.** Anthropic folded its two trusted-access programs into one Cyber Verification Program with Defense, Red Team and Specialized Access tiers, and Haiku 5.5's default safeguards still block penetration testing. Revisit trigger: a portfolio security agent hitting a cyber block.
- **Do Mistral Large 4's weights ship by the end of October?** A 1 trillion-parameter model with 52 billion active is on a preview API with weights promised by month-end. Revisit trigger: weights published under a stated license.
- **Does the cache-hit measurement finally land?** Open since 2026-W36. This week added a doubled up-front description budget and a halved Sonnet cache-read price, both moving inputs to the same number. Revisit trigger: ten sessions measured on 2.1.296 or later, prefix tokens and cache reads both logged.

## Archive notes

- **OpenAI customer stories** ([Asana](https://openai.com/index/asana-browser-agent), [LegalOn](https://openai.com/index/legalon-halves-codex-costs)). Dated 2026-10-09 and 2026-10-08 through the OpenAI news feed: Asana reports a browser agent 76 times cheaper and five times faster in tests, and LegalOn an estimated 65 percent cut in daily Codex cost from matching models to tasks. Both are vendor-published case studies with unstated baselines, and openai.com returns HTTP 403 to the quote fetcher, so neither is cited with a cell.
- **Microsoft Agent Lightning v1.0** ([Microsoft Research](https://www.microsoft.com/en-us/research/blog/agent-lightning-v1-0-a-3500-line-lightweight-agentic-rl-framework-for-training-agents-with-real-harnesses/)). Dated 2026-10-07: reinforcement learning with the deployed harness in the loop, reporting Qwen3.5-9B moving from 41.8 to 56.4 percent on SWE-bench Verified with about 6,000 samples. One model and one benchmark. The figures were read in a browser-agent fetch, but the blog returns HTTP 403 to the quote fetcher's user agent, so the item carries no cell.
- **NVIDIA's KDD Cup data agent** ([NVIDIA](https://developer.nvidia.com/blog/building-reliable-data-analytics-agents-lessons-from-the-kdd-cup/)). Dated 2026-10-08: second place with a small fixed model behind a harness that unified structured data into one SQL surface, exposed a small tool set and kept raw prose out of the main context. A useful design account with no ablation numbers.
- **Cursor Remote Control** ([Cursor](https://cursor.com/changelog/remote-control-local-agents)) and **Mistral Large 4** ([Mistral](https://mistral.ai/news/mistral-large-4/)). Dated 2026-10-06: Cursor's phone control of local agents is on by default for every organization except Enterprise, and Mistral's 1T-parameter model is on a preview API. The first is a default worth a settings check for non-Enterprise teams; the second is on the watchlist.
- **Discovery inputs found out of window.** Of 85 candidate URLs mined from the seven Daily Systems Brief issues, 54 were dated before 2026-10-03 by their primaries and 24 more were undated or off-topic; seven survived. Three of the out-of-window candidates were things this brief covered last week, presented again as news: the PACE preprint and the LangChain router post (2026-W40 picks) and the Clef decision models (a W40 scout row). The primary-source sweep found 13 more posts dated before the window, including posts whose feeds carried later dates than their pages and Agents SDK 0.23.1 (a W40 archive note), and one Cloudflare changelog entry dated 2026-10-10, after it.

## Sources reviewed

| Source | Status | Note |
|---|---|---|
| primary-source sweep (anthropic-news, openai-api-changelog, openai-news, huggingface-blog, langchain-blog, vercel-news, cursor-changelog, aws-ml-blog, aws-open-source-blog, google-developers-ai-blog, nvidia-dev-blog, mistral-news, crewai-docs, microsoft-research-blog and 28 more vendor and practitioner blogs) | partial | 42 sources attempted, 14 yielding 21 in-window findings; 3 top signal sources, 3 framework-runtime rows, 5 scout radar rows, 3 watchlist items, 4 archive notes. openai.com posts and the Microsoft Research blog return HTTP 403 to the quote fetcher, so nothing from them carries a cell |
| github-scout | ok | 98 releases read across claude-code, codex, MCP TypeScript SDK, langchain, deepagents, litellm, pydantic-ai, strands, browser-use and others; 16 in-window findings; 5 top signal source ids (Claude Code, Codex, langchain-core, deepagents-code, LiteLLM), 6 framework-runtime rows |
| daily-candidate route | ok | 85 candidate URLs from the seven Daily Systems Brief issues, each dated by its primary; 7 in-window findings; 4 top signal sources, 3 scout radar rows |
| Daily Systems Brief folder | ok | private discovery input, 2026-10-03 through 2026-10-09 |
| registry lane sweep | skipped | not run this cycle; no source in sources/registry.yaml was swept lane by lane |

## Closing thought

Every pick this week is a check reading a different object from the one that mattered. A grader read the transcript and the database disagreed. A reviewer read the emitted command and the shell ran another. A deny rule read a string and the shell read a parse. A guard went missing and the runner read its silence as yes. A price list read an average and the bill will read a distribution. None of the six actions needs a new tool, and the longest takes an afternoon.
