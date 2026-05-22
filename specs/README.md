# specs

The repo uses a six-file spec pattern:

- `requirements.md`
- `design.md`
- `tasks.md`
- `acceptance.md`
- `research.md`
- `traceability.md`

Active specs:

- `0000-bootstrap/requirements.md`
- `0000-bootstrap/design.md`
- `0000-bootstrap/tasks.md`
- `0000-bootstrap/acceptance.md`
- `0000-bootstrap/research.md`
- `0000-bootstrap/traceability.md`
- `0001-foundation/requirements.md`
- `0001-foundation/design.md`
- `0001-foundation/tasks.md`
- `0001-foundation/acceptance.md`
- `0001-foundation/research.md`
- `0001-foundation/traceability.md`

Development loop:

1. Add or update requirement IDs.
2. Design interfaces and failure modes before code.
3. Add fixtures/evals/golden cases before implementation.
4. Implement the narrowest traceable slice.
5. Run gates and record evidence.
6. Update traceability and status.

