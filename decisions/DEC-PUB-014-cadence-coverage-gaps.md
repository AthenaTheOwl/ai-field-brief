---
id: DEC-PUB-014-cadence-coverage-gaps
spec: specs/0007-publishing/
requirement: R-PUB-031
date: 2026-10-18
status: approved
reversible: true
decision: |
  Extend cadence_check to report missing canonical weekly issues through
  the most recent Friday, reject future through-dates, ignore all suffixed
  reruns, and emit a JSON coverage report. Run its regression tests in CI.
alternatives:
  - label: check only the newest issue's age
    rejected_because: A new issue can hide an older missing week.
  - label: create empty folders for missing weeks
    rejected_because: A directory supplies neither an issue nor its metadata.
rationale: |
  The October 18 audit found W20 through W41 contiguous and W42 due. The
  existing gate checked only the newest folder. It also let listing that
  old published week in SKIPS suppress freshness forever. A skip now
  applies to the due week; internal missing weeks remain explicit.
evidence:
  - kind: doc
    ref: scripts/cadence_check.py
  - kind: doc
    ref: tests/scripts/test_cadence_check.py
  - kind: doc
    ref: playbook/run-weekly-brief.md
rollback: |
  Restore the previous cadence checker and its CI test list. No issue
  content or publication state changes when running this read-only gate.
owner: science.proof-gate-runner
---

Coverage runs from the first canonical issue, so the gate invents no
obligation for weeks before the publication started. An explicit skip
records a miss; it does not fabricate a historical issue.
