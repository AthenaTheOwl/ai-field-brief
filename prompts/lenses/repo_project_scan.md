# Lens: Repo and Project Scan

Extract operational signal from a repo, startup project, changelog,
demo, talk, or release note.

Output:
- shipped_change
- proof_surface: code / docs / demo / benchmark / customer_case / maintainer_note
- integration_surface
- smallest_test_to_run
- dependency_or_security_risk
- maintenance_signal
- adoption_candidate
- watch_trigger

Rules:
- Prefer repo diffs, release notes, docs, examples, and working demos
  over marketing copy.
- Name what would be copied into a real project: config, eval, runtime
  adapter, tool policy, prompt, architecture note, or workflow.
- If the project cannot be tested in under 90 minutes, mark it monitor.
- If the project would add a new trust boundary, name the boundary.
