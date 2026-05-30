# frontier scout radar

This file is the review surface for sources that are useful before they
become obvious. Entries here are not promoted because they are obscure;
they are promoted because they expose a concrete mechanism that could
change a prompt, config, eval, workflow, tool policy, runtime adapter,
source registry, or architecture decision.

## promotion rule

A frontier-scout item earns a matrix cell only when it has all of:

- a verified source link
- a concrete shipped change, repo diff, product update, talk, paper,
  or reproducible example
- a named adoption surface
- a 30-90 minute test the reader can run
- a kill criterion that would demote the item to archive

Funding news, launch posts without technical detail, and broad market
claims stay in Archive notes unless they reveal a mechanism.

## scout lanes

| Lane | What to watch | Action surface |
|---|---|---|
| Agent sandboxes | persistent workspaces, filesystem tools, artifact stores, state snapshots | runtime-adapter, tool-policy |
| Browser automation | session replay, auth handoff, proxy controls, DOM/action traces | runtime-adapter, eval |
| Agent frameworks | typed tools, durable workflows, memory, handoffs, interrupts | architecture, agent-role |
| Human approval | leases, approvals, interrupts, escalation paths | tool-policy, workflow |
| Evals and observability | traces, span schemas, replay, prompt/version control | eval, software-control-plane |
| MCP directories | server categories, auth patterns, duplicated tools, risky surfaces | tool-policy, source-registry |
| Structured extraction | schema retries, provider portability, validation hooks | prompt, config |
| Model routing | provider failover, spend controls, audit logs, routing tests | config, eval |

## active scout sources

The first active set is now in `sources/registry.yaml` under
`lane: frontier-scout`:

- E2B, Browserbase: sandbox and browser execution.
- Pydantic AI, Mastra, HumanLayer: agent framework and approval loops.
- Braintrust, Langfuse, AgentOps: evals, tracing, and replay.
- Smithery, Glama, Composio: MCP and tool-surface discovery.
- DSPy, Instructor, LiteLLM: structured extraction, optimization, and
  provider routing.

## weekly review loop

1. Sweep the `frontier-scout` lane after the primary-source and
   fast-signal lanes.
2. Run `source_arbitrage` and `repo_project_scan` lenses before
   promotion; these lenses decide whether the item is early signal or
   just another tool announcement.
3. If promoted, write an Action packet in the weekly brief. The packet
   must name the target repo or working surface, proof metric, and kill
   criterion.
4. If the item is promising but not ready, place it in Scout radar with
   a revisit trigger.
5. If the item repeats a mainstream claim with no mechanism, archive it.

## calibration

The expected hit rate is low. A good week may promote one scout item and
archive twenty. That is acceptable if the promoted item leads to a real
repo change, eval case, prompt, policy, or experiment.

## 2026-05-30 — first scout run (run-scout-f23d443ff059)

5 frontier-scout sources fetched + 3 lenses applied = 15 cells, 15 verified.

Sources: e2b (sandboxes), pydantic-ai (typed agents), langfuse (LLM obs),
smithery (MCP registry), dspy (prompt programming).

Action packets:

- `e2b.md` — SandboxHandle artifact with E2B as default backend (prototype).
- `pydantic-ai.md` — port one lens to a Pydantic AI Agent with typed
  output_type (prototype).
- `langfuse.md` — wire Code Evaluators + Experiments CI into the
  run-evidence loop (prototype).
- `smithery.md` — CLI probe to test credential broker as a CDCP tool
  registry (prototype).
- `dspy.md` — GEPA-optimize one prompt-heavy chain (prototype).

Killed experiments:

- `dspy-framework-runtime.md` — adopting DSPy as a runtime framework is
  killed; only the GEPA optimizer survives as a build-time tool.

Artifacts live under `ops/scout-runs/run-scout-f23d443ff059/` (cells.yaml,
action-packets/, killed/). Contracted by DEC-MTRX-008.
