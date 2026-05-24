# dream 2026-W21 — first weekly retrospective

**week of 2026-05-18 through 2026-05-24 · generated 2026-05-24 · model: claude-opus-4-7 · run by: learning.dream-orchestrator**

The first weekly dream pass against ai-field-brief. Twelve commits landed
on `main` between 2026-05-18 and 2026-05-24, covering Phase 0 bootstrap,
the Phase 1 foundation, the first published brief, three deploy fixes,
and the two-commit install of the Cognitive Delivery Control Plane
(spec 0010 and spec 0011). This pass runs three of the eight dream modes
against that window. The other five sit out v1 by design (see below).

The mode-by-mode shape:

- **memory_consolidation** — three candidates. Each one names a lesson
  that recurred across at least two commits and proposes a block of text
  for `.agents/AGENTS.md`. Recurrence is the threshold; novelty alone
  did not promote a candidate to the file.
- **skill_extraction** — one candidate. The CDCP install ran for the
  third time across the portfolio this week (athena-site and a sibling
  procurement repo carry the first two). Three repos with the same
  install shape is the dream's graduation threshold.
- **eval_generation** — two candidates. Each one pins a load-bearing
  behavior that today lives only in a code comment or a try/except
  block. Both target failure modes that do not throw, which is the
  hardest class of regression to catch by inspection.

## What recurred this week

Three patterns showed up across more than one commit, which is the
dream-orchestrator's working threshold for "promote to memory":

1. **voice_lint cleanup at push time.** Three commits (`c29b7ac`,
   `d2186d2`, `b4b9cf2`) named voice_lint as a verified gate in the
   commit body. Each push paid the cost of a late rewrite. Memory
   candidate `memory-001` proposes a `## Voice rules at commit time`
   block in `.agents/AGENTS.md` with the rewrite recipe for the three
   highest-frequency hit categories.
2. **Phase 2 WIP stash-pop dance.** Three agent runs (the brief
   generator, the CDCP install, and this dream pass) opened with the
   same seven-line `git stash push` command. The convention is mature
   enough to name. Memory candidate `memory-002` proposes a `## Phase
   2 WIP convention` block in `.agents/AGENTS.md` that captures the
   command and the exit condition.
3. **JSON Schema `$ref` over DNS.** `scripts/validate_schemas.py`
   carries a 24-line `build_registry()` that exists because the naive
   `jsonschema` pattern fetches `$ref` URLs over the wire, and CI runs
   offline. `scripts/validate_decisions.py` carries the matching
   remote-then-cache fallback for the cross-repo decision schema.
   Memory candidate `memory-003` promotes both patterns to a `## Cross-
   repo schema rule` block under `## Cross-repo links` in AGENTS.md.

## What graduated

One skill candidate. The CDCP install (`5b3b792` + `b4b9cf2`) ran for
the third time across the portfolio this week. The third install is the
dream's graduation threshold. Skill candidate `skill-001` proposes
`.agents/skills/install-cdcp-governance/SKILL.md`, with the playbook,
eval list, and DEC trail for promoting the install pattern from a
two-commit operation into a named skill. Without the graduation, the
fourth install re-discovers the steps from prior commits.

## What needs a test

Two regression-test candidates. Both target failure modes that compile
clean, type-check clean, and break silently.

- `eval-001` — js-yaml's `DEFAULT_SCHEMA` deserializes ISO-date strings
  into real `Date` objects, and React's reconciler throws at render
  time. The fix lives in one line of `apps/web/src/lib/briefs.ts` and
  one comment. A future refactor that loses the `{ schema:
  yaml.JSON_SCHEMA }` argument would break the production build with no
  unit-test signal. Proposed test: load `briefs/2026-W21/meta.yaml`
  through the production read path and assert no field is a `Date`
  instance.
- `eval-002` — `scripts/validate_decisions.py` carries an offline-
  fallback path that only runs when the remote schema fetch fails. CI
  has internet, so the fallback path stays dark; the next engineer who
  hits the path is the engineer for whom the network is already broken.
  Proposed test: force the remote URL to an unreachable host via an
  env-var override and assert the cache-fallback path validates a real
  DEC end-to-end.

## What the dream did not surface this week

Five of the eight dream modes sit out v1 by design. Each one gets a
one-line reason so a later pass can pick the mode up when the input
volume justifies the cost:

- **failure_clustering** — only one CI failure in the week's window
  (the 03:24 run before the vercel monorepo detection fix landed at
  `11efda1`). One failure does not cluster. Reopen when the failure
  count crosses three per week.
- **adversarial_simulation** — no known-fragile parser, regex, or
  prompt path is named in the spec ledger yet. The right input is a
  list of "things we are afraid will break" from the spec authors;
  that list does not exist. Reopen when spec 0003 (run workflow) lands
  the first inference path.
- **counterfactual** — counterfactual replay needs a baseline run with
  recorded inputs, outputs, and cost. The current brief generator is
  manual; nothing to replay. Reopen when the inngest workflow tables
  ship in spec 0003 and a brief run carries a run_id.
- **architecture_drift_detection** — the spec ledger and the file
  tree match cleanly this week (specs 0000, 0001, 0010, 0011 all
  shipped with their declared files). The 16 R-SRC-* deferrals in the
  spec_check allowlist are deliberate, not drift. Reopen when the
  allowlist holds a deferral older than three weeks.
- **prompt_patch_generation** — no prompt files exist in the repo
  yet. Reopen when the brief generator's prompt graduates from the
  playbook into a versioned prompt file.

## Open items for the next human review

The reviewer of this dream picks which candidates to promote. Each
candidate carries `human_review_required: true` and a `promotion path`
section that names the files to edit and the checks to run. The dream
job does not auto-apply any candidate.

Six candidates, one report. The candidate files:

- `candidates/memory-001-voice-lint-pre-commit-discipline.md`
- `candidates/memory-002-stash-phase2-wip-before-agent-runs.md`
- `candidates/memory-003-jsonschema-ref-needs-registry.md`
- `candidates/skill-001-install-cdcp-governance.md`
- `candidates/eval-001-js-yaml-no-date-objects-to-react.md`
- `candidates/eval-002-validate-decisions-cross-schema-ref.md`

## Handoff

This dream pass hands off to `control.coordinator` per the weekly-dream
workflow (`.agents/workflows/weekly-dream.yaml` step `human-review`).
The coordinator routes each picked candidate to the role that owns the
target file: `engineering.implementation` for the three memory updates
and the js-yaml test, `science.proof-gate-runner` for the validate-
decisions test, `control.coordinator` for the install-cdcp-governance
skill graduation. No candidate moves to its target file without the
human approval the coordinator gates.

## Costs

This run produced six candidate files and one report. The dream-job
event lands in `ops/event-log/2026-05-24.jsonl` with the run id, the
modes run, the candidate count, and the cost line.

## Promotion record

The 2026-05-24 promotion pass moved all six candidates to their target
files. Each candidate file carries `status: promoted` and
`promotion_date: 2026-05-24` in its front-matter; the
`human_review_required: true` field stays as the audit trail of the
review record.

| Candidate ID | Promoted on | Target file |
|---|---|---|
| memory-001-voice-lint-pre-commit-discipline | 2026-05-24 | `.agents/AGENTS.md` (under `## Lessons promoted from weekly dreams`) |
| memory-002-stash-phase2-wip-before-agent-runs | 2026-05-24 | `.agents/AGENTS.md` (under `## Lessons promoted from weekly dreams`) |
| memory-003-jsonschema-ref-needs-registry | 2026-05-24 | `.agents/AGENTS.md` (under `## Lessons promoted from weekly dreams`) |
| skill-001-install-cdcp-governance | 2026-05-24 | `.agents/skills/install-cdcp-governance/SKILL.md` |
| eval-001-js-yaml-no-date-objects-to-react | 2026-05-24 | `apps/web/src/lib/briefs.date-safety.test.ts` |
| eval-002-validate-decisions-cross-schema-ref | 2026-05-24 | `tests/scripts/test_validate_decisions_offline.py` + env-var override in `scripts/validate_decisions.py` |
