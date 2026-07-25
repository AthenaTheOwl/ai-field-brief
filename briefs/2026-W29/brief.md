<!--
iso_week: 2026-W29
through_date: 2026-07-19
profile_id: builder-tpm
registry_version: 9
matrix_run_id: MTRX-W29-external-control
-->

# The control boundary moved outside the model

**Week 29 catch-up through 2026-07-19 - Vol. 12**

## Field thesis

This week's useful work happened at boundaries the model does not own. An authorization gateway checked identity and arguments before a tool call. A copy-on-write database let an agent work against real application state without touching the base rows. A repository carried specs between agent clients. Hugging Face kept a local model ready for incident evidence that hosted APIs would not process. Even Inkling's self-tuning demo placed a checkpoint and an eval between new weights and activation. A clear operating rule follows: give the model room to reason, then put authority, state, and promotion decisions in systems it cannot quietly rewrite.

## Top signals

### 1. A deceived model can still be denied authority

**Source:** [aiAuthZ: Off-Host, Identity-Bound Authorization for AI Agents](https://arxiv.org/abs/2607.05518)

**Payload:** The aiAuthZ technical report evaluated 15 models on eight attack scenarios and found refusal rates ranging from 100 percent to 38 percent. Its off-host gateway verifies signed caller identity, nonce freshness, role, and tool arguments before execution. The authors report zero residual dangerous calls in their tests and no more than 0.03 ms of policy-decision latency.

**Mechanism:** The gateway treats the agent's request as an untrusted proposal. A policy store outside the agent host decides whether the verified person may perform that exact action with those exact arguments, then records the decision in a hash-chained log. The model can follow an injected instruction and still fail to acquire permission.

**Why it matters:** Prompt defenses ask the same component that may be confused to recognize the confusion. An external authorization point supplies an independent invariant. The paper's own boundary matters: any built-in or alternate tool path that bypasses the gateway remains dangerous.

**Reusable pattern:** Route every consequential action through an identity-bound policy decision whose rules and signing keys are unavailable to the worker.

**Action surface:** `tool-policy`, `security`

**Try this week:** Put one write-capable factory tool behind a local policy function that checks actor, repository, allowed path, and argument shape. Add a test showing that a valid-looking call from the wrong actor fails.

**Systems map:** verified identity + single-use request -> off-host role and argument policy -> allow or deny -> signed receipt and audit record. Coverage depends on the absence of bypass paths.

**Transferable principle:** Put the final authority check in a component that cannot benefit from the proposed action. Payment approval and deployment promotion use the same separation.

**Falsification test:** If a worker can reach the same side effect through any ungated shell, SDK, or built-in tool path, the gateway adds ceremony without containment.

**Adoption ladder:**
  - Minimum viable: one high-impact tool behind an external argument check.
  - Mid: identity-bound signed requests with nonce and expiry.
  - Full: all consequential actions routed through the gateway with receipts.
  - Monitoring: bypass-path inventory, denied-call reasons, and policy latency.

**Confidence:** Medium. The design and code are public, while the performance and attack results are author-reported and need independent replication.

**Evidence:** MTRX-W29-AIAUTHZ-SECURITY.

### 2. Inkling put weight updates inside the agent loop

**Source:** [Thinking Machines Lab, "Inkling: Our Open-Weights Model"](https://thinkingmachines.ai/news/introducing-inkling/)

**Payload:** Thinking Machines released Inkling, a 975B-parameter mixture-of-experts model with 41B active parameters, a one-million-token context window, full weights, and a controllable effort setting. In the launch demo, Inkling wrote a fine-tuning objective and training job, ran it through Tinker, evaluated the result, staged the new checkpoint, and relaunched inside OpenCode.

**Mechanism:** The improvement loop gained a second actuator. A trace can now lead to a harness patch or a model-weight patch, and both can pass through the same proposal, eval, checkpoint, and promotion contract. The model's ability to stage its successor raises the value of a promotion boundary that the running model cannot approve.

**Why it matters:** Most agent loops stop at prompts and tool schemas. Open weights plus hosted post-training make weight updates operationally reachable for smaller teams. The cheapest unsafe version would let the worker define its own reward, judge its own result, and activate it.

**Reusable pattern:** Treat a weight update as an immutable candidate artifact with a pinned dataset, objective, grader, parent checkpoint, and explicit promotion verdict.

**Action surface:** `runtime-adapter`, `eval`

**Try this week:** Extend one run-evidence schema on paper with `parent_checkpoint`, `training_data_hash`, `objective_hash`, and `promotion_verdict`; verify that a reviewer could reconstruct why a candidate was activated.

**Systems map:** failure corpus -> objective and data candidate -> training job -> independent eval -> immutable checkpoint -> external promotion decision -> monitored rollout.

**Transferable principle:** Any self-modifying component needs a promotion boundary outside the component. Database migrations and auto-tuned policies follow the same rule.

**Falsification test:** If the fine-tuned checkpoint cannot beat a prompt or harness change on a held-out set at lower total cost, the weight-update path is unnecessary for that task.

**Adoption ladder:**
  - Minimum viable: record immutable checkpoint and evaluation references.
  - Mid: separate proposer and judge, with held-out cases.
  - Full: canary rollout plus automatic rollback on a pinned regression set.
  - Monitoring: accepted delta, rollback rate, drift by checkpoint, and training cost.

**Confidence:** Medium. The release and demo are primary-source evidence; benchmark and self-tuning results are vendor-reported.

**Evidence:** MTRX-W29-INKLING-RUNTIME.

### 3. The repository became the portable part of the agent system

**Source:** [Google Developers, "Evolving Spec-Driven Development: Conductor Now Supports Antigravity"](https://developers.googleblog.com/evolving-spec-driven-development-conductor-now-supports-antigravity/)

**Payload:** Google moved Conductor from a Gemini CLI extension into a plugin that can bundle skills, rules, MCP servers, and hooks. The project architecture, guidelines, specs, and plans remain versioned Markdown in the repository, allowing the same project state to move across supported agent clients.

**Mechanism:** Durable state lives in files with review history; the client compiles those files into whatever interaction surface it supports. Replacing the client no longer replaces the project memory. The plugin becomes an adapter around a repository-owned contract.

**Why it matters:** A factory that binds its operating model to one chat surface inherits that surface's lifecycle. Repository-owned contracts preserve review, diff, and replay when the worker family changes.

**Reusable pattern:** Keep source contracts vendor-neutral and compile client-specific prompts, skills, and hooks from them.

**Action surface:** `software-control-plane`, `architecture`

**Try this week:** Select one factory task and generate both Claude and Codex briefs from the same typed task object. Diff the requirements each worker receives; only client syntax should differ.

**Systems map:** versioned project contract -> client adapter -> worker interaction -> artifact and evidence -> contract update by reviewed commit.

**Transferable principle:** Stable state belongs below replaceable interfaces. Database schemas sit below API clients for the same reason.

**Falsification test:** If moving the same task between clients changes acceptance criteria or omits a constraint, the repository has failed as the source of truth and serves only as a document archive.

**Adoption ladder:**
  - Minimum viable: one typed task rendered for two worker clients.
  - Mid: shared skills, rules, and hook declarations generated from the contract.
  - Full: client conformance tests prove equivalent constraints and evidence.
  - Monitoring: adapter drift, omitted fields, and client-specific repair rate.

**Confidence:** High for the packaging and persistence design; Google's reported TerminalBench improvement is not independently reproduced here.

**Evidence:** MTRX-W29-CONDUCTOR-WORKFLOW.

### 4. Incident response needed a model the defender controlled

**Source:** [Hugging Face, "Security incident disclosure - July 2026"](https://huggingface.co/blog/security-incident-july-2026)

**Payload:** Hugging Face disclosed an autonomous-agent intrusion that began in dataset-processing code execution, escalated through credentials and clusters, and produced more than 17,000 recorded actions. Its response team used agents to reconstruct the attack in hours. Hosted frontier APIs blocked the exploit commands and command-and-control artifacts needed for analysis, so the team ran GLM 5.2 locally.

**Mechanism:** The attacker could send arbitrary offensive content through its own control loop. The defender's hosted model path applied general safety filters to incident evidence and rejected the work. A vetted local model restored both analytical capability and data locality.

**Why it matters:** A security response plan that first tests its analysis model during an incident has already lost time. The sensitive evidence may also contain active credentials that should never leave the environment.

**Reusable pattern:** Maintain a pre-vetted, isolated local analysis path for high-sensitivity evidence, with no outbound network and a practiced import/export procedure.

**Action surface:** `workflow`, `security`

**Try this week:** Run a tabletop on a synthetic attack log containing exploit strings and fake credentials. Confirm that the local path can ingest it, produce a timeline, and export only a redacted report.

**Systems map:** security telemetry -> isolated evidence store -> local analysis worker -> human-verified incident graph -> containment actions -> redacted disclosure.

**Transferable principle:** Emergency capability must be exercised under the same constraints that will exist during the emergency. Disaster recovery and offline signing use the same discipline.

**Falsification test:** If a hosted trusted-access path processes the full synthetic corpus without data egress concerns and meets response-time needs, maintaining local inference may cost more than it buys.

**Adoption ladder:**
  - Minimum viable: synthetic corpus and a documented local run command.
  - Mid: quarterly tabletop with redaction and export checks.
  - Full: isolated capacity, model pinning, evidence retention, and responder rotation.
  - Monitoring: time to first useful timeline, data-egress events, and analyst corrections.

**Confidence:** High for the incident and response account; attribution of the attacking model was unknown at disclosure time.

**Evidence:** MTRX-W29-HF-INCIDENT-SECURITY.

### 5. Protocols can connect agents without governing a group

**Source:** [Governance Gaps in Agent Interoperability Protocols](https://arxiv.org/abs/2606.31498)

**Payload:** A preprint compared MCP, A2A, ACP, ANP, and ERC-8004 across membership, deliberation, voting, dissent preservation, human escalation, and audit/replay. It found voting and dissent preservation absent across all five and argues that governed agent communities need an architectural layer above transport and tool protocols.

**Mechanism:** Interoperability answers how messages, identities, capabilities, and calls move. A governed group also needs rules for who participates, how conflicting proposals are retained, who decides, and when a person intervenes. Those semantics cannot be inferred from successful message delivery.

**Why it matters:** Multi-agent factories often mistake a fan-out plus a synthesizer for governance. Minority findings disappear, the synthesizer becomes an undeclared decision-maker, and escalation has no typed trigger.

**Reusable pattern:** Wrap multi-agent execution in a decision contract that records membership, proposals, dissent, verdict authority, and escalation.

**Action surface:** `agent-role`, `architecture`

**Try this week:** On one two-reviewer task, store each verdict separately and require the final handoff to name every unresolved disagreement before merge.

**Systems map:** membership rule -> independent proposals -> deliberation record -> verdict rule -> preserved dissent -> human escalation -> replayable decision.

**Transferable principle:** Communication infrastructure carries decisions; it does not supply decision rights. Message queues and board meetings share that distinction.

**Falsification test:** If an existing protocol extension expresses all six governance dimensions with interoperable implementations, a separate layer becomes optional.

**Adoption ladder:**
  - Minimum viable: preserve each review verdict and dissent.
  - Mid: typed quorum and escalation rules.
  - Full: replayable governance record independent of the worker runtime.
  - Monitoring: overridden dissent, unresolved conflicts, and escalation latency.

**Confidence:** Medium. The protocol reading is systematic but remains a two-author preprint without implementation testing.

**Evidence:** MTRX-W29-GOVERNANCE-ARCHITECTURE.

### 6. Copy-on-write scoring found the extra rows

**Source:** [Copy-on-Write Scoring: Application-Specific Agent Evaluations](https://arxiv.org/abs/2607.14336)

**Payload:** Copy-on-Write Scoring intercepts PostgreSQL writes into per-session change tables, compares an agent's final application state with a reviewed ground-truth session, and scores structure and content. In the Plane study, one agent produced 47 unrelated rows in one workflow and 44 in another. A vocabulary fix to the tool surface raised reported scores for two weaker models by 0.47 and 0.54.

**Mechanism:** The agent reads realistic application state while every write lands in an isolated overlay. The scorer compares desired and actual final state, so it catches missing, extra, and wrong writes even when the user-visible task appears complete.

**Why it matters:** Tool-call validity and final-answer quality can both pass while the application accumulates collateral changes. State-delta scoring measures the consequence the user inherits.

**Reusable pattern:** Evaluate a write-capable agent against an isolated state delta, with explicit allowed, required, and forbidden changes.

**Action surface:** `eval`, `runtime-adapter`

**Try this week:** For one file-editing factory fixture, compare the final changed-path set and content hashes against a reviewed golden result; fail on every unrelated file.

**Systems map:** shared base state -> per-run write overlay -> ground-truth delta and agent delta -> structural/content comparison -> tool-surface repair -> rerun.

**Transferable principle:** Score the state transition the system caused, not only the narrative it returned. Infrastructure plans and spreadsheet agents need the same check.

**Falsification test:** If ordinary diff-scoped gates catch every extra and missing change in the same fixture set, a storage-level copy-on-write layer is unnecessary there.

**Adoption ladder:**
  - Minimum viable: changed-path allowlist and golden content hashes.
  - Mid: isolated database or filesystem overlay with state-delta scoring.
  - Full: operation-level credit plus realistic production-shaped fixtures.
  - Monitoring: extra-write rate, missing-write rate, and score change after tool edits.

**Confidence:** Medium. The method is open and the study is detailed, while results come from one application and 20 workflows.

**Evidence:** MTRX-W29-COW-EVAL.

## Reusable patterns

- **External authority point.** Where it applies: write-capable tools, deployments, payments, and credential use. Caveats: every bypass path cancels the guarantee.
- **Candidate promotion contract.** Where it applies: model checkpoints, prompts, policies, and generated code. Caveats: proposer and promoter need independent evidence.
- **Repository-owned operating state.** Where it applies: multi-client agent work. Caveats: adapters need conformance tests or constraints drift silently.
- **State-delta evaluation.** Where it applies: agents that modify files, records, or configurations. Caveats: the golden state must represent the user's actual intent.
- **Incident-local analysis path.** Where it applies: sensitive logs, malware, exploit payloads, and regulated records. Caveats: local capacity must be patched, isolated, and exercised.

## Action queue

| Candidate | Surface | Effort | Risk | Test |
|---|---|---|---|---|
| Add actor, repo, path, and argument checks before one factory write tool | tool-policy | M | medium | wrong actor and out-of-scope path both fail before execution |
| Add a state-delta grader to one brownfield factory fixture | eval | M | low | unrelated files and missing expected changes each fail independently |
| Render one task contract for Claude and Codex, then compare constraints | software-control-plane | S | low | both briefs contain the same acceptance and forbidden-action sets |
| Run a synthetic incident-analysis tabletop on a local model | workflow | M | medium | timeline produced with no outbound network and no unredacted export |
| Preserve two reviewer verdicts and explicit dissent in one handoff | agent-role | S | low | unresolved disagreement appears in the final approval surface |

## Action packets

| Source | Target | Surface | Try | Proof metric | Rollback | Kill criterion |
|---|---|---|---|---|---|---|
| W29-AIAUTHZ | `mcp-security-lab` | tool-policy | add an identity-and-argument policy fixture around one dangerous tool | four deny cases and one allow case are deterministic | remove adapter and fixtures | any alternate path reaches the action without the check |
| W29-COW | `factory` | eval | score changed paths and file hashes against one reviewed brownfield result | unrelated change and omitted change both fail | keep current scoped-diff gate | no new defect class across ten held-out tasks |
| W29-CONDUCTOR | `factory` | software-control-plane | compare compiled Claude and Codex briefs for one task | required-field sets are equal | retain current worker-specific prompts | client syntax requires different acceptance semantics |
| W29-HF | `mcp-security-lab` | workflow | run a synthetic 200-event incident corpus through a local model | timeline recall and redaction precision recorded | preserve manual playbook | local path cannot meet the manual response time |
| W29-GOV | `trace-to-eval-harness` | architecture | add reviewer verdict and dissent fields to an example decision packet | replay reconstructs each reviewer and final authority | keep fields experimental | added fields cannot drive any gate or review decision |

## Scout radar

| Item | Why it might matter early | What to watch | Revisit trigger |
|---|---|---|---|
| [A2A Protocol v1.0](https://a2a-protocol.org/latest/announcing-1.0/) | signed Agent Cards, version negotiation, and multi-tenancy move cross-agent identity closer to an operational contract | independent SDK interoperability and key-rotation guidance | two vendors exchange signed cards across separate identity domains |
| [TREC RAG 2026](https://trec-rag.github.io/) | a shared retrieval track can expose whether local citation and faithfulness gains transfer beyond private fixtures | baseline release, submissions, and adjudication design | public baseline plus at least one reproducible run |
| [AI Agents Do Not Fail Alone](https://arxiv.org/abs/2607.14275) | context quality is framed as a leading indicator across instructions, tools, memory, retrieval, and guards | independent replication and criterion calibration | context score predicts held-out behavioral failures in a second system |
| [agent-cow-python](https://github.com/trail-ml/agent-cow-python) | the paper's state-delta method has an inspectable implementation | maintenance cadence, non-Postgres adapters, and fixture ergonomics | a filesystem or SQLite adapter lands |
| [Inkling-Small](https://thinkingmachines.ai/news/introducing-inkling/) | a 12B-active sibling may put controlled local customization within workstation reach | released weights, memory requirements, and fine-tuning cost | reproducible local eval and checkpoint workflow |

## Watchlist

- **Can off-host authorization survive a compromised worker with alternate network and shell paths?** Revisit trigger: an independent red-team evaluation of the released aiAuthZ implementation.
- **Will agent protocols add collective decision semantics or leave them to control planes?** Revisit trigger: an A2A, MCP, or ACP proposal for quorum, dissent, or human escalation.
- **Does copy-on-write scoring transfer beyond PostgreSQL applications?** Revisit trigger: a maintained filesystem, object-store, or SQLite implementation.

## Archive notes

- **Anthropic, "Evals for AI Agents: How Product Builders Get the Most Out of Every New Model"** ([webinar](https://www.anthropic.com/webinars/evals-for-ai-agents-how-product-builders-get-the-most-out-of-every-new-model)). Useful production-failure framing; the accessible page is a session description without a technical artifact.
- **OpenAI, "The US is advancing AI safety through state and federal action"** ([post](https://openai.com/index/advancing-ai-safety-through-state-and-federal-action/)). Relevant policy context; no direct implementation surface for this week's builder profile.

## Sources reviewed

| Source | Status | Note |
|---|---|---|
| Weekly Gen AI Digest | ok | discovery input; claims rechecked against public sources |
| Daily Systems Brief | ok | scout input; no prose copied |
| Thinking Machines Lab News | ok | Inkling release and self-tuning workflow included |
| Google Developers AI Blog | ok | Conductor Plugin included |
| arXiv aiAuthZ | ok | security signal included with bypass caveat |
| Hugging Face Blog | ok | incident and local-response path included |
| arXiv Governance Gaps | ok | governance-layer signal included as preprint |
| arXiv Copy-on-Write Scoring | ok | application-state eval signal included as preprint |
| A2A Protocol | ok | held in Scout radar pending interoperability evidence |
| TREC RAG 2026 | ok | held in Scout radar |
| Anthropic webinars | ok | archived; no technical artifact available on page |
| OpenAI News | ok | policy item archived |
| arXiv context-quality paper | ok | held in Scout radar pending replication |

## Closing thought

The safest component in an agent system may be the one that never needs to understand the agent's reasoning. It only needs to verify identity, scope, state, and proof before anything irreversible happens.
