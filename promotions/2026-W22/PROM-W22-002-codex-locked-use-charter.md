---
id: PROM-W22-002
brief: 2026-W22
pick_slug: codex-locked-use-long-running-agent-charter
target_repo: mcp-security-lab
target_artifact_type: dec
date: 2026-05-25
status: proposed
landed_commit: null
---

## What

File a long-running agent charter DEC in mcp-security-lab covering the
seven fields the brief enumerates (runs_in, maximum_session_duration,
allowed_credentials, disallowed_credentials, network_egress,
human_in_loop_triggers, kill_switch_path).

## Why this earns a promotion

mcp-security-lab is the portfolio repo whose charter readers care most
about. Codex Locked Use makes the screen-lock case concrete on macOS
today, and the security partner ask ("which long-running agents in our
stack hold credentials across a locked screen?") needs a written answer
before Q3. The charter shape lifts cleanly from the brief into a DEC.

## Where it would land

`mcp-security-lab/decisions/DEC-OPS-NNN-long-running-agent-charter.md`,
with the charter template stored alongside under
`mcp-security-lab/ops/long-running-agent-charter.md`.

## How we'd know it worked

Every existing long-running agent in mcp-security-lab has a filled-in
charter file by the W24 brief, and the AGENTS.md links to the
template.

## Source

Brief pick:
[briefs/2026-W22/brief.md - Codex Locked Use](../../briefs/2026-W22/brief.md#codex-locked-use--write-the-long-running-agent-charter-your-security-partner-will-ask-for).
