---
id: DEC-CDCP-006-agents-md-as-coding-agent-contract
spec: specs/0010-cognitive-delivery-control-plane/
requirement: R-CDCP-006
date: 2026-05-24
status: approved
reversible: true
decision: |
  A single .agents/AGENTS.md file is the contract a coding agent
  (Claude Code, Codex, or other) reads first. The file names four
  load-bearing sections: coding style, domain decisions, workflow
  conventions, and cross-repo links. The file lives at one path so
  the agent's bootstrap rule has one target.
alternatives:
  - label: per-tool config (CLAUDE.md, CODEX.md, GEMINI.md)
    rejected_because: |
      Per-tool config drifts. A coding-style rule that lives only in
      CLAUDE.md gets stale the day a different agent runs. One file
      with one canonical body is the only stable target.
  - label: scattered docs (CONTRIBUTING.md + STYLE.md + docs/)
    rejected_because: |
      Three files mean three places to update on every convention
      change, and the agent has to crawl each one. AGENTS.md is the
      single entry; it links out to the deeper docs as needed.
  - label: no contract; let the agent infer the conventions
    rejected_because: |
      Inference produces drift across runs. The voice-lint banlist
      is the canonical example: a fresh agent infers "let's add a
      flashy adverb" every time without the contract. The contract
      names the rules once.
rationale: |
  The four-section shape comes from the cross-repo charter under
  athena-site/ops/control-plane.md. Coding style names the language
  rules. Domain decisions name the load-bearing technical calls
  (Apache 2.0 code, CC BY 4.0 briefs, voice-lint banlist, no antithetical
  reversals). Workflow conventions name the stash-pop-around-WIP
  rule, the gate sequence on every commit, and the spec-first
  cadence. Cross-repo links point at athena-site, procurement-
  negotiation-lab, and the live brief.

  One contract, one read, one drift surface to keep current.
evidence:
  - kind: spec
    ref: specs/0010-cognitive-delivery-control-plane/requirements.md
  - kind: doc
    ref: .agents/AGENTS.md
  - kind: doc
    ref: ../athena-site/ops/control-plane.md
rollback: |
  Delete .agents/AGENTS.md and move the four sections into
  CONTRIBUTING.md (or split per-tool). The bootstrap drift returns;
  no data loss. Existing rules stay in force via the gate scripts.
owner: editorial
---

## decision

A single `.agents/AGENTS.md` file is the coding-agent contract. The
file names four sections: coding style, domain decisions, workflow
conventions, and cross-repo links. One path, one canonical body.

## alternatives

- Per-tool config (CLAUDE.md, CODEX.md, GEMINI.md) — drifts.
- Scattered docs (CONTRIBUTING.md + STYLE.md + docs/) — three
  places to update; the agent crawls each.
- No contract — inference produces drift across runs.

## rationale

The four-section shape comes from the cross-repo charter. Coding
style names the language rules. Domain decisions name the
load-bearing technical calls (Apache 2.0 code, CC BY 4.0 briefs,
voice-lint banlist). Workflow conventions name the stash-pop rule,
the gate sequence, and the spec-first cadence. Cross-repo links
point at the sibling repos and the live brief. One contract, one
read, one drift surface.

## evidence

- `specs/0010-cognitive-delivery-control-plane/requirements.md` —
  R-CDCP-006 acceptance.
- `.agents/AGENTS.md` — the contract itself.
- `../athena-site/ops/control-plane.md` — the cross-repo charter.

## rollback

Delete `.agents/AGENTS.md`. Split the four sections across
CONTRIBUTING.md and per-tool config. Existing rules stay in force
via the gate scripts.
