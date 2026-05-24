---
id: DEC-CDCP-009-dream-candidates-are-human-gated
spec: specs/0010-cognitive-delivery-control-plane/
requirement: R-CDCP-009
date: 2026-05-24
status: approved
reversible: false
decision: |
  Every dream candidate (memory update, generated test, skill
  patch, prompt patch, config patch, backlog item) carries
  human_review_required: true per the cross-repo
  dream-output.schema.json default. No CI job auto-applies a
  candidate. The agent contract .agents/AGENTS.md repeats the rule;
  the dream-candidates-require-human-approval policy enforces it.
alternatives:
  - label: auto-apply low-risk candidates (memory updates only)
    rejected_because: |
      A memory update changes what the next agent run does. A bad
      memory edit propagates silently. The risk on a memory edit is
      not low; it is delayed. Human review on every kind keeps the
      risk surface bounded.
  - label: human review per-kind (skill patches gated, others auto)
    rejected_because: |
      The per-kind exception list grows. Today memory updates seem
      low-risk; tomorrow a memory update breaks the voice-lint
      banlist via an undocumented edge case. One rule for every
      kind is the only stable contract.
  - label: trust the dream-orchestrator's confidence score
    rejected_because: |
      A confidence score is the orchestrator grading its own
      homework. The structural rule is the load-bearing one; the
      score is a hint, not a gate.
rationale: |
  The dream job is the offline-cognition layer. It proposes; it
  does not decide. The structural human-gate keeps the loop
  intact: an agent cannot self-promote a candidate it produced.

  The rule is reversible only by changing the schema default in
  athena-site, which would propagate across every repo on the
  operating model. The local enforcement (the AGENTS.md mention,
  the policy file) is reversible; the schema default is not. Hence
  status: approved with reversible: false.
evidence:
  - kind: spec
    ref: specs/0010-cognitive-delivery-control-plane/requirements.md
  - kind: doc
    ref: .agents/AGENTS.md
  - kind: doc
    ref: .agents/policies/dream-candidates-require-human-approval.yaml
  - kind: doc
    ref: ../athena-site/ops/schemas/dream-output.schema.json
  - kind: run
    ref: dreams/2026-W21/report.md
rollback: |
  Drop the dream-candidates-require-human-approval policy file. Edit
  the schema default in athena-site to auto_apply: true (this is the
  irreversible step; it propagates across every consumer). Remove
  the human-gate text from AGENTS.md. Existing candidates stay
  filed; future ones auto-apply.
owner: editorial
---

## decision

Every dream candidate carries `human_review_required: true` per the
cross-repo `dream-output.schema.json` default. No CI job auto-applies
a candidate. The agent contract `.agents/AGENTS.md` repeats the
rule; the `dream-candidates-require-human-approval` policy enforces
it.

## alternatives

- Auto-apply low-risk candidates — a bad memory edit propagates
  silently; risk is delayed, not low.
- Per-kind exceptions — the exception list grows.
- Trust the orchestrator's confidence score — agent grading its own
  homework.

## rationale

The dream job proposes; it does not decide. The structural
human-gate keeps the loop intact. The rule is reversible locally
(policy file, AGENTS.md text) but irreversible at the schema
default in athena-site, which would propagate across every consumer.

## evidence

- `specs/0010-cognitive-delivery-control-plane/requirements.md` —
  R-CDCP-009 acceptance.
- `.agents/AGENTS.md` — the agent contract repeats the rule.
- `.agents/policies/dream-candidates-require-human-approval.yaml` —
  the policy enforcement.
- `../athena-site/ops/schemas/dream-output.schema.json` — the
  schema default.
- `dreams/2026-W21/report.md` — first weekly dream run; every
  candidate filed with the flag set.

## rollback

Drop the policy file. Edit the schema default in athena-site (the
irreversible step). Remove the human-gate text from AGENTS.md.
Existing candidates stay filed.
