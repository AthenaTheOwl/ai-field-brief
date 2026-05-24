---
id: memory-002-stash-phase2-wip-before-agent-runs
target_kind: memory_update
target: .agents/AGENTS.md
human_review_required: true
status: promoted
promotion_date: 2026-05-24
evidence:
  - kind: commit
    ref: d2186d2 — added R-SRC-001..016 to the spec_check allowlist after Phase 2 WIP got re-surfaced from a stash and broke the gate
  - kind: file
    ref: specs/0002-source-registry/ + packages/sources/ — both untracked-on-main directories held in stash entries across three agent runs this week
  - kind: file
    ref: decisions/.spec-check-allowlist.yaml — 16 R-SRC-* entries deferred because the connector implementations sit in the stashed WIP
  - kind: doc
    ref: dreams/2026-W21/report.md — this dream run itself stashed the same files before starting (per the run instructions in the orchestrator prompt)
---

## proposal

Add a `## Phase 2 WIP convention` block to `.agents/AGENTS.md` that names the stash-before-agent-run pattern, the exact stash command, and the pop-after-finish requirement. The block sits under `## Workflow conventions`.

Proposed text (to be reviewed and edited by a human, not auto-applied):

```markdown
## Phase 2 WIP convention

Until the source-registry connectors land (specs/0002-source-registry/),
the working tree holds uncommitted Phase 2 WIP between agent sessions:

- `packages/sources/package.json` (modified)
- `packages/sources/src/` (untracked)
- `packages/sources/tsconfig.json` (untracked)
- `packages/sources/vitest.config.ts` (untracked)
- `specs/README.md` (modified)
- `specs/0002-source-registry/` (untracked)

Every multi-step agent run that touches gates, schemas, or commits
stashes the WIP first and pops it after:

```bash
git stash push --include-untracked -m "<job>: hold during run" -- \
  packages/sources/package.json packages/sources/src \
  packages/sources/tsconfig.json packages/sources/vitest.config.ts \
  specs/README.md specs/0002-source-registry
# ... do the work ...
git stash pop
```

The convention exits when each R-SRC-NNN ships its connector + DEC and
the allowlist entry in `decisions/.spec-check-allowlist.yaml` comes out.
```

## why it earns its keep

Three agent runs this week dealt with the same stash dance: the brief generator, the CDCP install, and this dream run. The pattern is mature enough to name. Without a documented convention, the next agent reasons from scratch about which files to stash, which is the kind of decision that loses files when it goes wrong.

The orchestrator prompt for this run had to spell out the seven-line stash command. That instruction belongs in the repo, not in the run prompt.

## evidence

- `d2186d2` — the spec_check allowlist commit shows the repo carrying R-SRC-001..016 as deferred. The deferment is the trace that the connector code lives in a stash and not on main yet.
- `packages/sources/` — directory exists locally in the agent's working tree but never lands in a commit on `main`. `git log -- packages/sources/` returns nothing.
- The orchestrator prompt that triggered this run names the stash command explicitly: a documented convention would let the prompt say "follow the Phase 2 WIP convention" instead.
- `decisions/.spec-check-allowlist.yaml` carries 16 R-SRC-* entries with the same closing line ("connector + DEC pending"). The pattern is repeated, which is the dream's signal to promote.

## promotion path

If approved, the change touches one file:

- `.agents/AGENTS.md` — add the new block under `## Workflow conventions`.

Reviewer checks:

1. The stash command in the block matches the exact file list currently uncommitted (run `git status` against a clean working tree to confirm).
2. The convention names the exit condition (per-R-SRC ship + DEC).
3. The block links to `specs/0002-source-registry/` so a reader can read the WIP's spec without hunting.

A second, lighter option: skip the AGENTS.md block and add a single `STASH-PHASE-2-WIP` note at the top of `specs/0002-source-registry/README.md` (if it exists; the spec dir is itself stashed today). The reviewer picks one or the other; both is duplication.

Owner role: `engineering.implementation`.

## risks if promoted blindly

- The exact file list ages out the moment a connector ships. The block needs a "last verified YYYY-WNN" footer so a stale list does not silently rot.
- Documenting the stash workflow on the contract surface risks signalling to a new agent that the convention belongs in the contract forever. The right end state is zero stashed WIP. A reviewer may want the block to lead with "temporary convention" so the reader does not adopt it as a pattern for new WIP.
- A future agent that follows the stash convention without checking `git stash list` first may pop the wrong stash. Reviewer should consider naming a stash-message prefix convention (`phase 2 WIP:`) so the pop is unambiguous.
