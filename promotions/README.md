# promotions

The bridge between a weekly brief pick and an actual portfolio change.

## What a promotion candidate is

A promotion candidate is a brief move mature enough to land somewhere
concrete: a DEC record, a SKILL, a regression test, an AGENTS.md edit, a
spec, or a portfolio policy file. Not every pick promotes. Most picks
ask the reader to think; a few ask the reader to file an artifact. The
ones that ask for a filed artifact are the ones that show up here.

The candidate names the target repo, the artifact type, and the
acceptance signal. Filing one does not graduate it; a human still picks
it up and lands the change in the target repo.

## Lifecycle

```
proposed -> accepted -> landed -> archived
                    \-> rejected
```

- **proposed.** Filed by the brief author or an agent reviewing the
  brief. Default state for any new candidate.
- **accepted.** A maintainer in the target repo has agreed to take the
  change. The candidate stays here; the work happens upstream.
- **landed.** The change shipped in the target repo. `landed_commit`
  carries the upstream SHA.
- **rejected.** The maintainer in the target repo declined. The
  candidate stays here with a one-line reason.
- **archived.** The candidate aged out without resolution. The brief
  pick moved on; the file stays as a historical record.

## File format

One markdown file per candidate, named
`PROM-<WEEK>-<NNN>-<kebab-slug>.md`, under `promotions/<week>/`.

```yaml
---
id: PROM-W22-001
brief: 2026-W22
pick_slug: <short-slug-from-the-pick-heading>
target_repo: <repo name, e.g. athena-site>
target_artifact_type: <one of: dec, skill, spec, agents-md, regression-test, portfolio-policy>
date: <YYYY-MM-DD>
status: proposed
landed_commit: null
---

## What

One-line summary of the action the brief named.

## Why this earns a promotion

2-3 sentences. Why the pick's move belongs as a portfolio artifact and
not just a read.

## Where it would land

Specific repo path + artifact type.

## How we'd know it worked

One-line acceptance signal.

## Source

Brief pick: link to the relevant section of the brief.
```

## How to file one

Write the file. `scripts/list_promotions.py` picks it up on the next
run. No registry, no validator, no CI gate yet — the surface is
intentionally lightweight while the rollout settles.

## Graduation

For now, a maintainer in the target repo reads the candidate, lands the
change, and updates `status` + `landed_commit` here. Spec 0008
(action-backlog) will automate the round trip when the registry is
ready.
