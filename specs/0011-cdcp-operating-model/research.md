# research: cdcp-operating-model

Research checked 2026-05-24.

- The CDCP base (spec 0010) shipped on 2026-05-22. The base defined
  the records (decisions, dreams, ledgers, agent contract) and the
  gates that hold them. The operating-model layer adds the runtime
  records (roles, tools, policies, state machines, workflows, events)
  on top.
- The cross-repo schemas under
  `https://raw.githubusercontent.com/AthenaTheOwl/athena-site/main/ops/schemas/`
  for role, tool, policy, workflow, state-machine, and event landed
  in athena-site between the 0010 ship and this spec. This repo
  references them by URL and keeps a cache copy under
  `ops/schemas-cache/` for offline CI.
- The 50-role catalog comes from the CDCP charter at
  `../athena-site/ops/control-plane.md`. Twelve guilds; the catalog
  enumerates the roles the charter names. Six worked examples ship
  here as the smallest set that covers one end-to-end run
  (coordinator → spec-writer → implementation → reviewer → gate-runner
  → coordinator → release) plus the weekly dream loop.
- The policy shape (data-as-policy, default-deny baseline,
  priority-sorted allows) follows the OPA pattern, but expressed as
  YAML the Python validator reads rather than Rego the OPA daemon
  reads. The validator is a small Python evaluator, not a daemon, at
  current artifact volume.
- The event log uses JSONL because append-only writes survive a crash
  mid-line, JSONL lines parse independently for partial-load reads,
  and one file per UTC day caps log-file growth without a rotation
  daemon.
- The runtime hints on each role.yaml (`claude_code`, `langgraph`)
  signal the planned execution surface. Today every role runs inside
  Claude Code; the langgraph hint on the dream orchestrator names
  the planned home once the run grows past one model call per mode.

## Why now

- Spec 0010 named the records and the gates. The operating-model
  layer names who runs what and under which constraints. Without the
  layer, "coding agent" stays a single undifferentiated actor; with
  the layer, the policy engine can deny a tool call by role rather
  than by file path.
- The cross-repo schemas just landed; the validators can ship now
  rather than after a schema-shape iteration.
- Six worked examples are the smallest set that exercises the schema
  shape across guilds and runtime hints. Shipping zero worked
  examples would leave the catalog as text without a built artifact;
  shipping all 50 would burn weeks of writing without a single line
  of execution code consuming the contracts.

## Alternatives considered

- One mega-role contract instead of six: rejected because a single
  role hides the forbidden-action and permission flag boundaries the
  policy engine relies on.
- Inline policies inside role.yaml instead of separate
  `.agents/policies/`: rejected because the OPA-shaped data lets a
  future policy daemon or evaluator read the rules without parsing
  every role.yaml.
- Skipping the state machines until an execution engine ships:
  rejected because the YAML files document the legal transitions the
  reviewer reads against, and the validators check the shape today.
- Putting the event log under `dreams/` instead of `ops/`: rejected
  because the log records cross-role workflow events, not weekly
  dream outputs.

## Open questions

- When does the merge-bot role land? Today the implementation role
  opens a PR and the reviewer approves; a human merges. The
  merge-bot stays deferred until the workflow shape stabilizes.
- Do we add a `validate_workflows.py` that cross-checks every
  workflow step's `role` field against the role catalog? Yes, in a
  later pass; today the manual read catches drift.
- How do we handle a role that gets removed from the catalog after a
  workflow references it? A future pass adds a hard fail in
  spec_check; today the manual read catches drift.
- How does the policy engine evaluate the `conditions` array? Today
  the strings document the predicate; a future Python evaluator
  reads `field`, `op`, and `value` against a request context.
