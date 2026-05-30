# Action packet: SandboxHandle artifact with E2B as default backend

- Source: `e2b` (https://github.com/e2b-dev/e2b)
- Snapshot: `ops/scout-snapshots/run-scout-f23d443ff059/e2b-github.html`
- Cell ids: MTRX-scout-run-scout-f23d443ff059-e2b-action_packet, MTRX-scout-run-scout-f23d443ff059-e2b-repo_project_scan
- Disposition: prototype
- Effort: small (one week)

## Hypothesis

Wrapping E2B behind a typed `SandboxHandle` artifact (create / exec / upload / download / close) lets CDCP tool-using roles request code execution through the policy engine without coupling role logic to any one runtime, and a one-line backend swap to local Docker keeps offline/CI viable.

## Test

In one active repo, add a `sandbox_handle.py` adapter implementing the interface against `e2b.Sandbox.create()`; route one existing tool-call site (a code-eval or shell-exec step) through it; run the same task end-to-end against both `backend=e2b` and a `backend=local-docker` stub.

## Success metric

Same task produces equivalent stdout/exit-code under both backends, and zero role code references `e2b` directly — only the handle. Achievable within one week.

## Risk

New trust boundary: code and possibly secrets leave the host for e2b.dev cloud. API-key blast radius. Per-sandbox cost if left to run. Mitigate by pinning SDK version, treating sandbox stdout as untrusted, and scoping the API key to one project.

## Kill criterion

Kill if the local-Docker stub cannot reach feature parity on stdout / exit-code shape within the prototype window, or if E2B pivots to a closed-source hosted-only model.
