---
id: DEC-CDCP-002-install-operating-model
spec: specs/0011-cdcp-operating-model/
requirement: R-CDCP-011
date: 2026-05-24
status: approved
reversible: true
decision: |
  Install the CDCP operating-model layer on top of the spec 0010 base:
  six worked-example role contracts under .agents/roles/, a tool
  registry at .agents/tools.yaml, five policies under
  .agents/policies/, three state machines under
  .agents/state-machines/, three workflows under .agents/workflows/, a
  44-role TODO ledger at .agents/CATALOG.md, and an append-only event
  log under ops/event-log/. Three new validators (validate_roles,
  validate_tools, validate_policies) ship under scripts/ and run on
  every push.
alternatives:
  - label: one mega-role contract instead of six
    rejected_because: |
      A single undifferentiated role hides the forbidden-action
      boundaries and the permission flags the policy engine relies
      on. Six worked examples is the smallest set that exercises the
      schema shape across guilds (control, product, engineering,
      science, learning) and runtime hints (claude_code, langgraph).
  - label: ship all 50 roles at once
    rejected_because: |
      Fifty role.yaml files plus instructions.md plus tools.yaml is
      weeks of writing without a single line of execution code that
      consumes the contracts. Six worked examples cover one end-to-end
      run (coordinator routes through spec-writer, implementation,
      reviewer, gate-runner, back to coordinator) plus the weekly
      dream loop. The other 44 stay tracked in CATALOG.md as TODO.
  - label: inline policies inside each role.yaml
    rejected_because: |
      An OPA-shaped policy set lives outside the role contract so a
      future policy daemon or evaluator can read the rules without
      parsing every role.yaml. The data-as-policy shape also lets one
      higher-priority rule deny across roles (the
      reviewer-cannot-edit-code priority 200 case).
  - label: skip state machines until an execution engine ships
    rejected_because: |
      The YAML files document the legal transitions the reviewer
      reads against, and the validators check the shape today. A
      future engine consumes the same files without a schema bump.
rationale: |
  The spec 0010 base named the records and the gates. Spec 0011 adds
  the runtime layer: who runs what, under which constraints, and how
  the work moves between roles. Without the layer, every coding agent
  is one undifferentiated actor; with the layer, the policy engine
  denies a tool call by role identity, not only by file path.

  Six worked roles cover the smallest end-to-end run plus the weekly
  dream loop. The other 44 stay in CATALOG.md so the team cannot
  claim "we shipped the operating model" while 88% of the catalog is
  vapor.

  The three new validators land alongside the data so the gates fail
  the build on any shape drift, the same pattern validate_decisions
  established in spec 0010.
evidence:
  - kind: spec
    ref: specs/0011-cdcp-operating-model/
  - kind: doc
    ref: ../athena-site/ops/control-plane.md
  - kind: doc
    ref: ../athena-site/ops/schemas/role.schema.json
  - kind: doc
    ref: ../athena-site/ops/schemas/tool.schema.json
  - kind: doc
    ref: ../athena-site/ops/schemas/policy.schema.json
  - kind: doc
    ref: ../athena-site/ops/schemas/workflow.schema.json
  - kind: doc
    ref: ../athena-site/ops/schemas/state-machine.schema.json
  - kind: doc
    ref: ../athena-site/ops/schemas/event.schema.json
rollback: |
  Delete this commit. The added directories (.agents/roles/,
  .agents/policies/, .agents/state-machines/, .agents/workflows/,
  .agents/tools.yaml, .agents/CATALOG.md, ops/event-log/,
  specs/0011-*) and the three new scripts can come out wholesale.
  The schemas-cache files added in this commit (role, tool, policy,
  workflow, state-machine, event) can come out with the scripts that
  read them. The spec_check.py extension that reads owner_role is
  additive; rolling it back means deleting the new code path and the
  roles_deferred allowlist section. No data loss: the cross-repo
  schemas remain in athena-site, and the six role contracts can land
  again in a later pass.
owner: control
---

## decision

Install the CDCP operating-model layer on top of the spec 0010 base.
Six role contracts ship as worked examples under `.agents/roles/`; the
other 44 stay tracked in `.agents/CATALOG.md`. A tool registry, five
policies, three state machines, three workflows, and an append-only
event log ship alongside. Three new validators (`validate_roles`,
`validate_tools`, `validate_policies`) join the gate suite.

## alternatives

- One mega-role contract — hides the forbidden-action and permission
  boundaries the policy engine reads.
- All 50 roles at once — weeks of writing without execution code
  consuming the contracts; CATALOG.md tracks the deferred 44.
- Inline policies inside role.yaml — blocks a future policy daemon
  from reading rules without parsing every role file.
- Skip state machines until an engine ships — the YAML documents the
  legal transitions the reviewer reads today and the engine
  consumes later.

## rationale

Spec 0010 named the records and the gates. Spec 0011 names who runs
what. Six worked roles cover one end-to-end run plus the dream loop;
the other 44 stay tracked. Three validators land with the data so the
gates fail the build on shape drift.

## evidence

- `specs/0011-cdcp-operating-model/` — the spec ledger this DEC
  resolves.
- `../athena-site/ops/control-plane.md` — the charter that names the
  twelve guilds and the 50-role catalog.
- `../athena-site/ops/schemas/{role,tool,policy,workflow,state-machine,event}.schema.json`
  — the six contracts the validators check.

## rollback

Delete this commit. Remove the new directories (`.agents/roles/`,
`.agents/policies/`, `.agents/state-machines/`, `.agents/workflows/`,
`.agents/tools.yaml`, `.agents/CATALOG.md`, `ops/event-log/`,
`specs/0011-*`) and the three new validator scripts. Remove the
schemas-cache files added in this commit. The `spec_check.py`
extension that reads `owner_role:` is additive; rolling it back means
deleting the new code path and the `roles_deferred:` allowlist
section. No data loss.
