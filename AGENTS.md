# Agent instructions

The contract a coding or research agent reads before acting on
ai-field-brief. This is the public-facing summary; the operating-model
detail lives at `.agents/AGENTS.md`.

## AI Brief OS — evidence-spine rules (non-negotiable)

No digest claim may be published unless it traces to one or more
verified matrix cells.

No matrix cell may be verified unless it has source references.

No action candidate may be promoted unless it has:

- source support (verified cell ids)
- action surface (from `config/action_surface_taxonomy.yaml`)
- test plan
- expected benefit
- risk
- disposition (one of `adopt_now`, `prototype`, `monitor`, `archive`,
  `reject`, `promote_to_os_candidate`)

Quality gates before publish:

- source link exists and resolves
- faithfulness pass completed for every cell that feeds the digest
- duplicate check completed
- no forced action angle — when a source has nothing actionable, it
  belongs in Archive notes, not Top signals
- confidence label present on every digest item (`high`, `medium`,
  `low`)
- source quality score present (per `config/scoring_model.yaml`)
- profile relevance score present (per `config/profiles.yaml`)
- every watchlist item has a revisit trigger

The rule is recorded under DEC-MTRX-001 and lives in
`docs/MATRIX_PLANE_DESIGN.md`. Amending the rule requires a new DEC.

## Three-pass note system

The Matrix Plane pipeline is the join key between sources and the
digest. Each pass maps onto lenses in `config/prompt_lenses.yaml` and
is gated by a role contract under `.agents/roles/`.

- **Pass 1 — Structured source note.** Extract title, source,
  source_type, published_at, url, one_sentence_gist, main_claims,
  mechanisms, implementation_details, contradictions, open_questions,
  risks, caveats, notable_terms. Lenses: `source_gist`,
  `claims_and_bets`, `mechanism_extraction`. Role:
  `science.matrix-runner`.
- **Pass 2 — Faithfulness audit.** For every Pass 1 cell, run the
  seven-question check in `prompts/cell_faithfulness.md`: unsupported
  claim, overstated certainty, missing caveat, invented consensus,
  wrong source span, too generic, action recommendation not supported
  by the source. Verdicts: `PASS`, `PATCH_CELL`, `FAIL_CELL`. Role:
  `science.cell-verifier`.
- **Pass 3 — Action extraction.** Produce reusable patterns plus
  action candidates with action_type, surface, proposed_action,
  test_plan, success_metric, risk, effort, confidence, disposition.
  Lenses: `reusable_pattern`, `adoption_action`, `risk_and_caveats`.
  Role: `science.matrix-synthesis-editor`.

## Scoring model

Defined in `config/scoring_model.yaml`. Every source item that
survives triage is scored on three axes (source_quality,
profile_relevance, actionability) with four penalties subtracted.
Final score gates promotion:

- `final_score >= 12` — eligible for Top signals
- `final_score in [9, 12)` — drops to Watchlist (with revisit trigger)
- `final_score < 9` — archived

Profile-level overrides land under `config/profiles.yaml` and are
resolved at run time.

## Profiles

Defined in `config/profiles.yaml`. The same corpus is scored under
multiple profiles to surface the difference. Seed profiles:

- `personal` — the user's working profile
- `broad_builder` — a generic builder profile used as a sanity check

A MatrixRun pins to one `profile_id` and records it in the run
record under `ops/run-records/`.

## Repo discipline

- Do not invent a source. Add a candidate to
  `sources/candidates.yaml`; a human promotes the entry into
  `sources/registry.yaml`.
- Voice rules in `scripts/voice_lint.py` are not optional. Every
  markdown file under the documented globs runs the lint and exits
  clean before commit. Banlist is hard-FAIL.
- The brief is the primary public artifact. The Matrix Plane outputs
  under `briefs/YYYY-WNN/matrix/` are the audit trail.
- A force-push, history rewrite, or rollback gets an entry in
  `ops/RESET_LEDGER.md` in the same push.

## Before commit

```powershell
python scripts/voice_lint.py
python scripts/check_no_bom.py
python scripts/spec_check.py
python scripts/validate_schemas.py
python scripts/validate_registry.py
python scripts/validate_decisions.py
python scripts/validate_roles.py
python scripts/validate_tools.py
python scripts/validate_policies.py
```

## Where to look

| If you want to | Read |
|---|---|
| run the weekly brief | `playbook/run-weekly-brief.md` |
| read the digest format | `templates/weekly-brief.md` |
| score a source item | `config/scoring_model.yaml` |
| score for a profile | `config/profiles.yaml` |
| pick an action surface | `config/action_surface_taxonomy.yaml` |
| inspect a matrix cell | `briefs/YYYY-WNN/matrix/` |
| read the operating-model contract | `.agents/AGENTS.md` |
| read a role contract | `.agents/roles/<id>/instructions.md` |
| audit a workflow event | `ops/event-log/YYYY-MM-DD.jsonl` |
| audit a run | `ops/run-records/<run-id>.json` |
