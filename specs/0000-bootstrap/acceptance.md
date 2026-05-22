# acceptance: bootstrap

## Phase 0 gates

- Repo initializes on `main`.
- Spec ledger exists.
- Root verify command exists, even if early tasks are placeholder checks.
- CI can install dependencies and run lint/typecheck/test/eval placeholders.
- Source schema fixture test exists before real connectors.
- Eval fixture test exists before real prompts.
- Workflow contract exists before real background jobs.
- Release ledger template exists before deploy.

## Done means

Phase 0 is done when a new agent can clone the repo, run one command, and see
which checks are real, which are placeholders, and which external accounts are
needed.

