# Action packet: Smithery CLI probe — credential broker as 'tool registry' role in CDCP

- Source: `smithery` (https://smithery.ai/)
- Snapshot: `ops/scout-snapshots/run-scout-f23d443ff059/smithery-mcp-registry.html`
- Cell ids: MTRX-scout-run-scout-f23d443ff059-smithery-action_packet, MTRX-scout-run-scout-f23d443ff059-smithery-repo_project_scan
- Disposition: prototype
- Effort: small (2-4h: CLI install, 2 servers, write-up)

## Hypothesis

Smithery's CLI + Connect can serve as a drop-in reference implementation for the CDCP 'tool registry' role contract (publish manifest, broker credentials, emit usage events) — without us building a vault from scratch.

## Test

From a throwaway profile, run `npx smithery auth login`, then `npx smithery tool list` and `npx smithery tool call` against two verified servers (one read-only like Context7, one OAuth-bound like a Drive-style integration). Capture: (a) latency, (b) credential-flow UX, (c) whether the JSON tool-call surface is stable enough to wrap behind our policy engine, (d) what telemetry Smithery surfaces to the publisher.

## Success metric

Within one week, produce a 1-page note in `mcp-security-lab/decisions/` answering: 'Can Smithery Connect substitute for a self-hosted tool registry in CDCP? Y/N + 3 risks.' Plus a working repro script.

## Risk

Sending OAuth tokens through a third-party broker for any non-throwaway account; a verified badge does not equal an audited server. Mitigate by using burner accounts only.

## Kill criterion

Kill if (a) the CLI auth flow leaks tokens into shell history without warning, (b) the tool-call schema differs materially from the MCP spec, or (c) telemetry to publishers includes user-identifying data we cannot opt out of.
