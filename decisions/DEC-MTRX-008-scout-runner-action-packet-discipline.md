---
id: DEC-MTRX-008-scout-runner-action-packet-discipline
spec: specs/0012-prompt-matrix-plane/
requirement: R-MTRX-019
date: 2026-05-30
status: approved
reversible: true
amends: DEC-SRC-021-frontier-scout-lane-for-early-actionable-sources
decision: |
  ai-field-brief operationalizes the frontier-scout lane via
  `scripts/scout_runner.py` plus the discipline that every
  `action_packet` lens cell produces either a promotion candidate
  (under `ops/scout-runs/<run-id>/action-packets/<source-id>.md`)
  or a killed experiment (under
  `ops/scout-runs/<run-id>/killed/<source-id>.md`). The first proof
  trail lives at `ops/scout-runs/run-scout-f23d443ff059/` with
  `cells.yaml` (15 verified cells), 5 promotion-candidate packets,
  and 1 killed experiment. DEC-SRC-021 added the lane declaratively;
  the runner (commit `c322c5a`) plus this DEC make the lane
  operational with a typed output contract.
alternatives:
  - label: keep the scout lane declarative and rely on weekly-brief authors to write Action packets ad hoc
    rejected_because: |
      Ad-hoc authoring under a weekly cadence reverts to prose
      discipline and drops the one-to-one cell-to-packet mapping
      that lets the proof-gate-runner audit the lane. Without the
      typed promotion-or-kill output per `action_packet` cell, the
      lane can run for weeks with zero artifacts and look healthy.
  - label: emit Action packets as a synthesis-time aggregation across cells
    rejected_because: |
      Synthesis-time aggregation hides which source produced which
      packet and breaks the cell-id reference chain the brief
      validator relies on. Per-cell packets keep the trace tight:
      one snapshot to one set of cells to one packet (or one kill
      note), readable from either direction.
  - label: "write killed experiments only on `disposition: reject`"
    rejected_because: |
      Restricting kills to explicit `reject` disposition under-counts
      the lane's actual decision rate. A source that lands a
      prototype but kills the framework-as-runtime adoption is a
      real boundary call worth recording; the kill captures the
      framework-soup risk the user flagged in portfolio memory.
rationale: |
  The scout lane only buys what DEC-SRC-021 claims if it routinely
  produces both raw evidence (snapshots plus matrix cells) and
  actionable artifacts (packets, killed experiments). The runner at
  `scripts/scout_runner.py` handles the raw-evidence side; this DEC
  contracts the actionable side. Every `action_packet` cell maps to
  one file under `action-packets/` (when disposition is `prototype`
  or `adopt_now`) or one file under `killed/` (when disposition is
  `reject` or when a sibling lens flags the source as
  framework-as-runtime risk). The first run gives the lane four
  weeks to clear the falsification bar.
evidence:
  - kind: decision
    ref: decisions/DEC-SRC-021-frontier-scout-lane-for-early-actionable-sources.md
  - kind: decision
    ref: decisions/DEC-MTRX-001-prompt-matrix-plane-install.md
  - kind: doc
    ref: scripts/scout_runner.py
  - kind: doc
    ref: sources/scout-radar.md
  - kind: doc
    ref: ops/scout-runs/run-scout-f23d443ff059/cells.yaml
  - kind: run
    ref: ops/run-records/run-scout-f23d443ff059.json
rollback: |
  Stop requiring a packet or kill file per `action_packet` cell.
  Remove the `ops/scout-runs/<run-id>/action-packets/` and
  `ops/scout-runs/<run-id>/killed/` directories from the runner
  contract. Retire `scripts/scout_runner.py` only if DEC-SRC-021
  also rolls back; otherwise leave the runner in place and revert
  to declarative-only scout entries.
owner: science.proof-gate-runner
systems_map: |
  Scout lane to runner to matrix cells to Action packets implements
  source-to-action at the lane level. The lane keeps discovery and
  authority separate; the runner freezes bytes; the cells carry
  faithfulness verdicts; the packets carry the bounded test that
  turns a signal into a repo change or a kill note.
transferable_principle: |
  Any source-curation system should have lane-specific runners
  producing both raw evidence (snapshots plus cells) and actionable
  artifacts (packets, killed experiments). Declarative lane
  definitions without runners drift; runners without typed output
  contracts produce snapshots no one acts on.
falsification_test: |
  If the first 4 weeks of scout runs produce 0 promotions AND 0
  kills, retire the lane. The lane only earns its slot in the
  weekly loop if it routinely yields either a bounded prototype or
  an explicit kill note per source swept.
adoption_ladder:
  minimum_viable: |
    First run produces >=3 Action packets across promotions and
    killed experiments, with one `cells.yaml` per run-id.
  mid_adoption: |
    Weekly scout in playbook; the proof-gate-runner role validates
    that every `action_packet` cell has a matching packet or kill
    file before the brief renders.
  full_adoption: |
    Cron-scheduled scout runs with auto-renaming of the run-id
    folder; downstream repos open issues from the packet titles.
  monitoring_signals:
    - "scout runs per week"
    - "promotions landed per month"
    - "killed experiments recorded per month"
    - "action_packet cells without a matching packet or kill file"
---

## decision

ai-field-brief operationalizes the frontier-scout lane via
`scripts/scout_runner.py` plus the discipline that every
`action_packet` lens cell produces either a promotion candidate or a
killed experiment. The first proof trail lives at
`ops/scout-runs/run-scout-f23d443ff059/` with `cells.yaml`,
`action-packets/`, and `killed/` directories.

## alternatives

- Keep the scout lane declarative and rely on weekly-brief authors
  to write Action packets ad hoc. Rejected because ad-hoc authoring
  drops the one-to-one cell-to-packet mapping the proof-gate-runner
  needs to audit the lane.
- Emit Action packets as a synthesis-time aggregation across cells.
  Rejected because aggregation hides which source produced which
  packet and breaks the cell-id reference chain.
- Write killed experiments only on `disposition: reject`. Rejected
  because that under-counts the lane's actual decision rate; a
  source that lands a prototype but kills the framework-as-runtime
  adoption is a real boundary call worth recording.

## rationale

The scout lane only buys what DEC-SRC-021 claims if it routinely
produces both raw evidence and actionable artifacts. The runner at
`scripts/scout_runner.py` handles raw evidence; this DEC contracts
the actionable side. Every `action_packet` cell maps to one file
under `action-packets/` or one file under `killed/`. The first run
gives the lane four weeks to clear the falsification bar.

## evidence

- DEC-SRC-021 contracted the frontier-scout lane declaratively.
- DEC-MTRX-001 carries the matrix-plane install contract this DEC
  extends.
- `scripts/scout_runner.py` carries the runner (commit `c322c5a`).
- `sources/scout-radar.md` carries the promotion and demotion loop.
- `ops/scout-runs/run-scout-f23d443ff059/cells.yaml` carries the
  first 15 verified cells.
- `ops/run-records/run-scout-f23d443ff059.json` carries the first
  scout Run record.

## coverage

This DEC covers R-MTRX-019 through R-MTRX-022 on the
prompt-matrix-plane spec:

- R-MTRX-019: scout-runner produces a typed `cells.yaml` per run.
- R-MTRX-020: every `action_packet` lens cell maps to a packet or
  kill file.
- R-MTRX-021: the scout lane is owned by `science.proof-gate-runner`
  for the weekly audit pass.
- R-MTRX-022: scout runs carry the four-week falsification window.

## rollback

Stop requiring a packet or kill file per `action_packet` cell.
Remove the `ops/scout-runs/<run-id>/action-packets/` and
`ops/scout-runs/<run-id>/killed/` directories from the runner
contract. Retire `scripts/scout_runner.py` only if DEC-SRC-021
also rolls back; otherwise leave the runner in place and revert
to declarative-only scout entries.
