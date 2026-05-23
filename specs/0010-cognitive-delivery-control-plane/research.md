# research: cognitive-delivery-control-plane

Research checked 2026-05-22.

- The CDCP framing came out of a synthesis pass across athena-site and
  ai-field-brief: specs were already gated, decisions were not, and the
  weekly brief work showed an offline-cognition shape worth naming.
- The cross-repo schemas under `athena-site/ops/schemas/` (artifact,
  decision, dream-output, run, skill) just landed; this repo references
  them by URL and keeps a local cache copy for offline CI.
- Anthropic's published guidance on agent skills (March 2026) frames a
  skill as instructions plus optional scripts and evals, graduated from
  observed practice. The `skill.schema.json` shape in athena-site
  follows that pattern.
- The codex.md pattern in athena-site uses a declarative workflow YAML
  with named steps; we mirror that pattern in
  `control-plane/workflows/single-change.yaml`.
- The reset ledger pattern came from the procurement-negotiation-lab
  repo's audit-trail discipline; force-pushes get recorded in the same
  push so the trail survives the rewrite.
- The release ledger backfill covers nine commits from f126a87 (Phase 0
  bootstrap) through 992f3f2 (the public-deploy fix that landed the
  Vercel-hosted reader). Each entry names which gates the release
  passed.

## Why now

- Specs alone do not record why a path was chosen over alternatives.
  DEC files fill that gap.
- Skills graduate from playbooks once a pattern recurs; the existing
  `playbook/run-weekly-brief.md` has run twice without a graduation
  record. The SKILL.md lands the graduation.
- The weekly dream job is the offline-cognition pattern that turns
  postmortems and eval drift into promotion candidates. The README
  reserves the shape; the first output lands in a later pass.

## Alternatives considered

- Single ad-hoc `governance.md` file: skipped because it does not
  generate executable gates.
- Adopting a framework stack (LangGraph, CrewAI, Strands): skipped
  because frameworks turn over every six months; the records survive
  the framework.
- A 12-screen control-plane SaaS: deferred until artifact volume
  warrants a UI layer beyond the markdown ledgers.

## Open questions

- When does the first dream output land? Likely weekend 2 after this
  spec ships; the agent contract will name the trigger.
- Do we add a portfolio-audit script that reads cross-repo health? The
  athena-site repo owns that script; this repo only emits the records.
- How do we handle dream candidates that propose changes to gate
  scripts themselves? Treated as a skill patch, gated by human review.
