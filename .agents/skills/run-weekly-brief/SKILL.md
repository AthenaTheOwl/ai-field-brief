---
id: run-weekly-brief
version: 0.1.0
owner_guild: editorial
trigger:
  - weekly Friday cron
  - /dream-then-brief
  - "manual weekly brief pass"
instructions_file: playbook/run-weekly-brief.md
scripts:
  - name: voice_lint
    path: scripts/voice_lint.py
    description: voice rules the final brief markdown must pass
  - name: spec_check
    path: scripts/spec_check.py
    description: structural check across spec ledgers
evals: []
promotion_policy:
  requires:
    - human_approval
---

# skill: run-weekly-brief

This skill graduates the recurring weekly-brief pattern documented in
`playbook/run-weekly-brief.md`. The playbook ran twice without a
graduation record; this SKILL.md records the graduation.

## What it does

Drives one weekly pass: read the source registry, sweep new items,
triage into the four-bucket rubric, draft the brief against the
template, run voice-lint clean, publish under `briefs/YYYY-WNN/`.

## Trigger

- Weekly Friday cron job (lands when the dream job lands).
- Manual `/dream-then-brief` slash command from the operator.
- Operator-initiated weekly pass.

## Instructions

The full playbook lives at `playbook/run-weekly-brief.md`. Read it
top-to-bottom before starting. Key rules:

- One brief per ISO week. If the folder exists, halt and ask the
  human whether to overwrite or append.
- Source 403s and rate-limits land in `meta.yaml` as recorded
  failures; one bad source does not block the pass.
- The opening reflection names a pattern; the picks earn their
  place with comment, not link-dumps.
- Voice lint runs against the final brief and exits clean before
  publish.

## Scripts

- `scripts/voice_lint.py` — voice rules the final brief markdown
  must pass.
- `scripts/spec_check.py` — structural check across spec ledgers.

## Evals

None yet. A `passing_skill_eval` lands when the second brief output
gets a golden-case comparison. Until then, promotion past version
0.1.0 is gated on `human_approval` per the promotion_policy field.

## Promotion policy

- v0.1.0 ships under `human_approval`.
- v0.2.0 onward requires `passing_skill_eval` in addition to
  `human_approval`.
- A breaking change to the trigger surface or the script API requires
  a major version bump.

## Open items

- Add a golden-case eval that compares a generated brief against a
  reference brief on coverage, voice, and triage accuracy.
- Wire the Friday cron once the dream job ships.
- Decide whether the slash command lives in the agent runtime or as
  a repo script.
