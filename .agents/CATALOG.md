# .agents/CATALOG.md

The 50-role catalog from `../athena-site/ops/control-plane.md` plus
one speculative graduation (`product.subscriber-experience`). Nine
roles ship as worked examples under `.agents/roles/`; 42 of the
original 50 remain tracked here as `not-installed`. Promotion of a role off this
list and into `.agents/roles/<id>/` requires a PR that lands the role
file set (`role.yaml`, `instructions.md`, `tools.yaml`,
`output.schema.json`, `gates.yaml`) plus a DEC and a CATALOG entry
removal in the same commit.

## Graduated

- 2026-05-24 — `learning.skill-curator` graduated. Originating
  evidence: R-CDCP-007 (spec 0010 traceability) plus the two
  existing skills under `.agents/skills/install-cdcp-governance/`
  and `.agents/skills/run-weekly-brief/` that landed before the role
  existed.
- 2026-05-24 — `security.threat-modeler` graduated. Originating
  evidence: R-BOOT-006 (spec 0000 traceability) — tenant and audit
  tests had been routing to `engineering.implementation` for lack
  of a graduated owner.
- 2026-05-24 — `product.subscriber-experience` graduated
  (speculative). Originating evidence: the deployed site
  `ai-field-brief.vercel.app` has visitors right now, the two
  published briefs (2026-W20 and 2026-W21) under `briefs/`, and no
  other role owns the comprehension surface.

## Installed (thirteen worked examples)

See `.agents/roles/` for the file sets.

- `control.coordinator` — routes a change from signal to release.
- `product.spec-writer` — turns intent into R-* specs.
- `product.subscriber-experience` — owns the read-only subscriber journey.
- `engineering.implementation` — writes code on assigned tickets.
- `engineering.code-reviewer` — blocks merges on quality or security smells.
- `science.proof-gate-runner` — runs the gate suite and reports green or blocking.
- `science.lens-designer` — curates the prompt-lens catalog and picks the lens set per matrix run. Graduated 2026-05-29 with the matrix plane install (DEC-MTRX-002).
- `science.matrix-runner` — runs lens × source-item fanout and writes matrix cells. Graduated 2026-05-29 with the matrix plane install (DEC-MTRX-002).
- `science.cell-verifier` — checks every cell against its source and marks pass/patch/fail. Graduated 2026-05-29 with the matrix plane install (DEC-MTRX-002).
- `science.matrix-synthesis-editor` — clusters verified cells into row summaries, themes, and action candidates. Graduated 2026-05-29 with the matrix plane install (DEC-MTRX-002).
- `security.threat-modeler` — drafts STRIDE passes on new external surfaces.
- `learning.dream-orchestrator` — weekly offline cognition; files candidates.
- `learning.skill-curator` — owns the skill registry and the graduation cadence.

The four new science roles cover the matrix-analysis loop named in
`.agents/workflows/matrix-analysis-loop.yaml`. The plan agent's
Phase 1 map called this guild `analysis`; the install lands them under
`science` because the cross-repo `role.schema.json` guild enum (control,
product, research, design, engineering, science, security, operations,
domain, learning, documentation, commercial) does not include
`analysis` and per DEC-CDCP-010 cross-repo schemas live in athena-site.
The matrix-plane work is evidence-grounded verification work, which
sits cleanly under the science guild today; a future
`analysis` guild can graduate via athena-site if and when other
analysis-flavored roles accumulate enough mass to justify the schema
amendment.

## Deferred (42 roles)

### Control guild (3 roles deferred)

- `control.escalation-lead` — picks up handoffs the coordinator cannot resolve. status: not-installed.
- `control.budget-watch` — tracks per-workflow spend against the budget and triggers throttle policies. status: not-installed.
- `control.scheduler` — owns cron triggers, dream-job cadence, and backpressure on the queue. status: not-installed.

### Product guild (4 roles deferred)

- `product.research-synthesizer` — clusters user research into requirement candidates. status: not-installed.
- `product.acceptance-author` — turns R-* IDs into structured acceptance-criteria fixtures. status: not-installed.
- `product.roadmap-curator` — maintains the cross-spec dependency graph and the phase ordering. status: not-installed.
- `product.backlog-grooming` — triages backlog items into work-now, work-later, and won't-do. status: not-installed.

### Research guild (4 roles deferred)

- `research.literature-scanner` — sweeps new arXiv papers and engineering blogs against the active question list. status: not-installed.
- `research.experiment-designer` — designs the smallest experiment that answers an open question. status: not-installed.
- `research.benchmark-builder` — builds a benchmark suite for a new capability claim. status: not-installed.
- `research.failure-analyst` — reads postmortems and clusters root causes for the dream job. status: not-installed.

### Design guild (3 roles deferred)

- `design.system-curator` — maintains the design-system tokens, components, and a11y rules. status: not-installed.
- `design.flow-mapper` — diagrams the user flow for a new feature before code lands. status: not-installed.
- `design.copy-editor` — owns voice across product surfaces, in step with voice_lint. status: not-installed.

### Engineering guild (6 roles deferred)

- `engineering.architecture` — owns the cross-package architecture record and the DEC for a structural change. status: not-installed.
- `engineering.platform` — owns the workspace tooling, the build, and the package boundaries. status: not-installed.
- `engineering.tests` — writes fixtures, golden cases, and snapshot suites against the spec acceptance criteria. status: not-installed.
- `engineering.migrations` — owns drizzle migrations and the migration roll-forward and rollback path. status: not-installed.
- `engineering.merge-bot` — the only role with merge_pr permission; reads the review and the gate report. status: not-installed.
- `engineering.release-bot` — the only role with deploy permission; reads the release ledger and the canary signal. status: not-installed.

### Science guild (4 roles deferred)

- `science.eval-author` — writes the eval suite for a new capability claim. status: not-installed.
- `science.benchmark-runner` — runs the benchmark suite on a candidate model or prompt change. status: not-installed.
- `science.fixture-curator` — owns the shared fixture set under tests and golden cases. status: not-installed.
- `science.regression-analyst` — diffs eval runs across model versions and flags a regression. status: not-installed.

### Security guild (3 roles deferred)

- `security.secret-scanner` — owns the gitleaks gate and the secret-rotation cadence. status: not-installed.
- `security.dep-auditor` — reads pnpm audit, npm advisories, and the SBOM for new findings. status: not-installed.
- `security.incident-responder` — owns the runbook for a confirmed breach and the disclosure timeline. status: not-installed.

### Operations guild (5 roles deferred)

- `operations.observability` — owns the trace pipeline, the dashboards, and the SLO definitions. status: not-installed.
- `operations.on-call` — first responder to a pager; owns the incident triage runbook. status: not-installed.
- `operations.cost` — reads the cloud bill and the LLM bill against the budget. status: not-installed.
- `operations.backup` — owns the backup cadence and the restore test. status: not-installed.
- `operations.access` — owns role grants in cloud consoles, the secret vault, and the source control. status: not-installed.

### Domain guild (4 roles deferred)

- `domain.editorial` — owns the weekly brief voice, the source curation rubric, and the human-in-the-loop call. status: not-installed.
- `domain.legal` — reads contract terms and license boundaries before a commit lands. status: not-installed.
- `domain.compliance` — owns the audit trail for a regulated workflow. status: not-installed.
- `domain.subject-matter-expert` — invoked per topic; gives a read on a draft brief or a research claim. status: not-installed.

### Learning guild (3 roles deferred)

- `learning.memory-curator` — reads promoted candidates and folds them into long-term memory files. status: not-installed.
- `learning.eval-promoter` — promotes a golden-case fixture from candidate to gated eval. status: not-installed.
- `learning.lesson-archivist` — reads dream reports and writes a quarterly lessons-learned digest. status: not-installed.

### Documentation guild (3 roles deferred)

- `documentation.contributor-guide` — owns CONTRIBUTING.md and the new-contributor onboarding. status: not-installed.
- `documentation.tutorial-author` — writes the worked-example tutorial for a new capability. status: not-installed.
- `documentation.release-notes` — drafts the release notes for the release-bot to ship. status: not-installed.
