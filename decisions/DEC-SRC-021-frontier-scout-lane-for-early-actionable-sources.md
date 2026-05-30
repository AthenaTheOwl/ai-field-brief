---
id: DEC-SRC-021-frontier-scout-lane-for-early-actionable-sources
spec: specs/0002-source-registry/
requirement: R-SRC-020
date: 2026-05-30
status: approved
reversible: true
decision: |
  Add a `frontier-scout` source lane for lesser-known repos, startups,
  projects, changelogs, videos, podcasts, and talks that may become
  useful before mainstream coverage catches up. The lane ships with 14
  active sources, three prompt lenses (`source_arbitrage`,
  `repo_project_scan`, `action_packet`), a scout-score overlay, a
  `frontier_scout` profile, and two new brief sections: Action packets
  and Scout radar.
alternatives:
  - label: fold the sources into fast-signal
    rejected_because: |
      Fast-signal tracks what happened this week. Frontier-scout tracks
      sources whose value is early discovery plus a testable adoption
      path. Mixing the two would let novelty compete with news volume
      and would hide the proof metric / kill-criterion discipline the
      scout lane needs.
  - label: keep the sources in candidates.md only
    rejected_because: |
      Candidate files are useful for human review, but the weekly run
      does not sweep them. The user asked for the brief to stay on top
      of repos, podcasts, videos, articles, projects, startups, and
      anything useful; that requires an active lane plus routing rules.
  - label: promote every interesting startup mention
    rejected_because: |
      Startup discovery without a mechanism becomes launch tracking.
      The brief needs actionability, so promotion requires a concrete
      artifact, proof surface, action surface, and kill criterion.
rationale: |
  The current registry is broad, but its lanes optimize for source
  authority, week-level signal, builder practice, and strategic framing.
  A separate lane is needed for source arbitrage: finding useful tools
  and projects before they appear in the common AI-news loop. The lane
  starts with agent sandboxes, browser automation, agent frameworks,
  approval loops, eval/tracing surfaces, MCP directories, structured
  extraction, and model routing. These categories map directly to the
  portfolio's current work: run evidence, MCP surface control, brief
  extraction, and agent workflow governance.
evidence:
  - kind: doc
    ref: sources/registry.yaml
  - kind: doc
    ref: sources/scout-radar.md
  - kind: doc
    ref: config/prompt_lenses.yaml
  - kind: doc
    ref: config/scoring_model.yaml
  - kind: doc
    ref: templates/weekly-brief.md
  - kind: run
    ref: scripts/validate_registry.py
rollback: |
  Remove the `frontier-scout` lane and retire the 14 scout sources.
  Remove `source_arbitrage`, `repo_project_scan`, and `action_packet`
  from `config/prompt_lenses.yaml`; remove the scout-score overlay and
  `frontier_scout` profile; drop Action packets and Scout radar from
  the weekly template. Delete R-SRC-020 and its traceability row.
owner: product.source-curator
systems_map: |
  Source arbitrage sits between discovery and adoption. A weak scout
  layer floods the brief with novelty; a strong one turns early signals
  into bounded tests with proof metrics and kill criteria.
transferable_principle: |
  Separate early discovery from evidence authority. The same principle
  applies to security tooling, procurement signals, and data pipelines:
  emerging sources need their own routing rules so they can be useful
  without lowering the proof bar.
falsification_test: |
  If the frontier-scout lane produces fewer than two Action packets that
  land as repo changes or validated experiments over the next four
  briefs, the lane is mostly noise and should be narrowed.
adoption_ladder:
  minimum_viable: |
    14 active scout sources, three scout lenses, and Action packet /
    Scout radar sections in the weekly template.
  mid_adoption: |
    One scout item per week becomes either an Action packet or Scout
    radar item with a concrete revisit trigger.
  full_adoption: |
    Scout items routinely graduate into promotions, eval cases, prompt
    changes, runtime adapters, or MCP/security review tasks.
  monitoring_signals:
    - "scout items promoted per week"
    - "Action packets that land as repo changes"
    - "Scout radar items demoted because kill criteria fired"
---

## decision

Add a `frontier-scout` source lane for lesser-known repos, startups,
projects, changelogs, videos, podcasts, and talks that may become useful
before mainstream coverage catches up. The lane ships with 14 active
sources, three prompt lenses (`source_arbitrage`, `repo_project_scan`,
`action_packet`), a scout-score overlay, a `frontier_scout` profile,
and two new brief sections: Action packets and Scout radar.

## alternatives

- Fold the sources into fast-signal: rejected because fast-signal tracks
  what happened this week, while frontier-scout tracks early discovery
  plus a testable adoption path.
- Keep the sources in `candidates.md` only: rejected because candidate
  files are useful for human review, but the weekly run does not sweep
  them.
- Promote every interesting startup mention: rejected because startup
  discovery without a mechanism becomes launch tracking.

## rationale

The current registry is broad, but its lanes optimize for source
authority, week-level signal, builder practice, and strategic framing.
A separate lane is needed for source arbitrage: finding useful tools and
projects before they appear in the common AI-news loop. The lane starts
with agent sandboxes, browser automation, agent frameworks, approval
loops, eval/tracing surfaces, MCP directories, structured extraction,
and model routing. These categories map directly to the portfolio's
current work: run evidence, MCP surface control, brief extraction, and
agent workflow governance.

## evidence

- `sources/registry.yaml` (`version: 5`, `last_curated: 2026-05-30`)
- `sources/scout-radar.md` (promotion and demotion loop)
- `prompts/lenses/source_arbitrage.md`
- `prompts/lenses/repo_project_scan.md`
- `prompts/lenses/action_packet.md`
- `config/scoring_model.yaml` (`scout_score`)
- `templates/weekly-brief.md` (Action packets + Scout radar)
- `specs/0002-source-registry/requirements.md#R-SRC-020`

## rollback

Remove the `frontier-scout` lane and retire the 14 scout sources. Remove
the three scout lenses, scout-score overlay, `frontier_scout` profile,
and the two template sections. Delete R-SRC-020 and its traceability row.
