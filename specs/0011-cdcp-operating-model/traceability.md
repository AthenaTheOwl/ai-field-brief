# traceability: cdcp-operating-model

| Requirement | Owner role | Design surface | Planned proof |
|---|---|---|---|
| R-CDCP-011 | owner_role: control.coordinator | `.agents/roles/<id>/{role.yaml,instructions.md,tools.yaml,output.schema.json,gates.yaml}` for six roles | `python scripts/validate_roles.py` exits zero with six role files validated |
| R-CDCP-012 | owner_role: control.coordinator | `.agents/tools.yaml` + `scripts/validate_tools.py` + `ops/schemas-cache/tool.schema.json` | `python scripts/validate_tools.py` exits zero with 17 entries validated against the cross-repo schema |
| R-CDCP-013 | owner_role: control.coordinator | `.agents/policies/*.yaml` + `scripts/validate_policies.py` + `ops/schemas-cache/policy.schema.json` | `python scripts/validate_policies.py` exits zero with five policies plus the default-deny baseline confirmed |
| R-CDCP-014 | owner_role: control.coordinator | `.agents/workflows/{single-change,weekly-dream,incident-response}.yaml` + the `moved_to:` pointer at the old path | manual read against `ops/schemas-cache/workflow.schema.json`; future `validate_workflows.py` automates the check |
| R-CDCP-015 | owner_role: learning.dream-orchestrator | `ops/event-log/2026-05-24.jsonl` + `ops/schemas-cache/event.schema.json` | manual line-by-line parse against the schema; future `validate_events.py` automates the check |
| R-CDCP-016 | owner_role: learning.dream-orchestrator | `.agents/CATALOG.md` with 44 deferred roles + the promotion-rule header | manual review of the catalog count + the promotion-rule header |
