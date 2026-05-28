---
id: DEC-PUB-004-faithfulness-audit-before-publish
spec: specs/0007-publishing/
requirement: R-PUB-002
date: 2026-05-25
status: approved
reversible: true
decision: |
  Every brief draft passes a faithfulness audit between drafting and
  voice-lint. The audit asks five questions: did we overstate; did we
  drop caveats; does every claim have a source link; did we invent
  consensus; did we mistake hype for mechanism.
alternatives:
  - label: skip the audit and rely on voice-lint alone
    rejected_because: |
      Voice-lint catches AI cadence and banned phrases. It does not
      verify claim faithfulness. Three published briefs in, the most
      common drift is overstatement that voice-lint cannot see.
  - label: LLM-as-judge faithfulness scoring
    rejected_because: |
      Premature. The brief author is the judge for now. Move to
      LLM-as-judge when corpus + audit volume justify the per-pick
      cost, and after the judge itself is validated against human
      labels (see DEC-PUB-003 of trace-to-eval-harness when filed).
  - label: post-publish audit or errata page
    rejected_because: |
      Too late. The published brief is the artifact subscribers read.
      An errata page is honest but does not prevent the drift; the
      pre-publish audit does.
rationale: |
  Three published briefs in, the most common drift is overstatement:
  a source said X about Y; the brief writes it as "everyone's doing
  Y." A 10-15 minute self-audit between draft and lint catches this
  before publish. Cost is low; the alternative is errata-after-the-fact
  or quiet credibility loss. The audit sits in the playbook as a
  named step so the next agent or co-author reads it before they ship.
evidence:
  - kind: doc
    ref: playbook/run-weekly-brief.md
  - kind: doc
    ref: briefs/2026-W20/brief.md
  - kind: doc
    ref: briefs/2026-W21/brief.md
  - kind: doc
    ref: briefs/2026-W22/brief.md
rollback: |
  Remove the faithfulness-audit step from playbook/run-weekly-brief.md.
  The other passes (voice-lint, gates, meta log) continue unchanged.
  Future briefs would no longer carry the discipline; published briefs
  remain as-is.
owner: science.proof-gate-runner
---

## decision

Every brief draft passes a faithfulness audit between drafting and
voice-lint. The audit asks five questions: did we overstate; did we
drop caveats; does every claim have a source link; did we invent
consensus; did we mistake hype for mechanism.

## alternatives

- Skip the audit; rely on voice-lint alone. Rejected because voice-lint
  catches AI cadence and banned phrases but does not verify claim
  faithfulness.
- LLM-as-judge faithfulness scoring. Rejected as premature; the brief
  author is the judge for now. Move to LLM-as-judge when corpus + audit
  volume justify.
- Post-publish audit or errata. Rejected because the published brief
  is the artifact; an errata page is honest but does not prevent drift.

## rationale

Three published briefs in, the most common drift is overstatement: a
source said X about Y; the brief writes it as "everyone's doing Y."
A 10-15 minute self-audit between draft and lint catches this before
publish. The cost is low, the alternative is credibility loss the
brief cannot afford this early in its life.

## evidence

- `playbook/run-weekly-brief.md` step 5 carries the five-question
  audit.
- First brief subject to the audit: 2026-W23 (next Friday).
- Three published briefs without the audit: W20, W21, W22.

## rollback

Remove the step from `playbook/run-weekly-brief.md`. The other passes
(voice-lint, gates, meta log) continue unchanged. Future briefs would
no longer carry the discipline; published briefs remain as-is.
