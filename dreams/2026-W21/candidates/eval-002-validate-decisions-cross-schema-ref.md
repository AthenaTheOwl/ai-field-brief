---
id: eval-002-validate-decisions-cross-schema-ref
target_kind: test_generation
spec_id: specs/0010-cognitive-delivery-control-plane
test_path: tests/scripts/test_validate_decisions_offline.py
human_review_required: true
status: promoted
promotion_date: 2026-05-24
evidence:
  - kind: file
    ref: scripts/validate_decisions.py — fetches the cross-repo decision.schema.json from athena-site and falls back to ops/schemas-cache/decision.schema.json
  - kind: file
    ref: scripts/validate_schemas.py lines 84–107 — build_registry() exists to keep $ref-by-URL resolvable offline
  - kind: file
    ref: ops/schemas-cache/decision.schema.json — the cached cross-repo schema the validator falls back to
  - kind: file
    ref: decisions/DEC-CDCP-001-install-cdcp-governance.md, decisions/DEC-CDCP-002-install-operating-model.md — real DEC files that exercise the front-matter path
---

## proposal

Add a regression test under `scripts/test_validate_decisions_cross_ref.py` that runs `validate_decisions` against a fixture DEC file whose front-matter uses every required field plus the optional `alternatives` array, with the network-fetch path forced to fail. The test asserts the cache-fallback path resolves the schema and validates the DEC. The test pins the offline-CI contract.

Proposed test skeleton (to be written and reviewed by a human, not auto-applied):

```python
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_validate_decisions_offline():
    """Fixture DEC validates against the cached schema with no network."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        (repo / "decisions").mkdir()
        (repo / "ops" / "schemas-cache").mkdir(parents=True)
        shutil.copy(
            ROOT / "ops" / "schemas-cache" / "decision.schema.json",
            repo / "ops" / "schemas-cache" / "decision.schema.json",
        )
        # Copy a real DEC as the fixture so the test exercises the
        # actual front-matter shape, not a hand-rolled one.
        shutil.copy(
            ROOT / "decisions" / "DEC-CDCP-001-install-cdcp-governance.md",
            repo / "decisions" / "DEC-CDCP-001-install-cdcp-governance.md",
        )
        # Force the remote fetch to fail (no network) by overriding the
        # validator's URL to an unreachable host.
        env = {**os.environ, "DECISIONS_SCHEMA_URL": "http://127.0.0.1:1/missing"}
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_decisions.py")],
            cwd=repo,
            env=env,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr

if __name__ == "__main__":
    test_validate_decisions_offline()
    print("ok")
```

(Note: the proposed test depends on `validate_decisions.py` honoring a `DECISIONS_SCHEMA_URL` env var override. Today the URL is a module constant; the promotion adds the env-var override as part of the same change. The reviewer may prefer a different injection point — argparse flag, monkey-patch — and should pick whichever fits the script's style.)

## why it earns its keep

The validator's offline-fallback path is the kind of code that does not run in CI under normal conditions: CI has internet, so the remote fetch succeeds and the cache path stays dark. The cache path only runs when the network is down — which is exactly when the engineer who would notice the breakage is not watching.

`validate_schemas.py` carries the same shape (`build_registry()` is the offline-fallback for schema `$ref` resolution). Both paths are load-bearing and both are silent until they fail. One regression test per script keeps the fallback honest.

A second value: the test doubles as documentation. Reading the test tells the next agent how the script is meant to behave when the remote schema is unreachable. Today that behavior lives in a comment and a try/except block.

## evidence

- `scripts/validate_decisions.py` lines 32–46 — `load_remote_schema()` catches `URLError, TimeoutError, JSONDecodeError, OSError` and returns `None`. The fallback path runs only when one of those four exceptions fires.
- `scripts/validate_decisions.py` lines 49–56 — `load_cached_schema()` raises `SystemExit` if the cache is missing, which is the right behavior in production but is exactly the path the regression test pins.
- `ops/schemas-cache/decision.schema.json` — the cache file. The test asserts the file is enough to validate a real DEC end-to-end.
- `decisions/DEC-CDCP-001-install-cdcp-governance.md` — a real DEC that uses every documented front-matter field including the `alternatives` array and the multi-line `decision`, `rationale`, and `consequences` fields. Using a real DEC as the fixture catches schema drift the moment a new field gets added.
- `scripts/validate_schemas.py` `build_registry()` lines 84–107 — sibling pattern. A future eval candidate may extend the same shape to that script.

## promotion path

If approved, the promotion lands one new test plus one tiny script change:

- `scripts/test_validate_decisions_cross_ref.py` — the new test file.
- `scripts/validate_decisions.py` — add a `DECISIONS_SCHEMA_URL` env-var override on the module constant `REMOTE_URL`.
- `.github/workflows/ci.yml` — add a step that runs the new test (or roll it into an existing `pytest` step if one exists).

Reviewer checks:

1. The test fails today (without the env-var override) because the validator hard-codes the URL. The change to add the override is small and reviewable.
2. The test passes when CI has no internet (simulate by blocking egress).
3. The fixture DEC is a real DEC; if the test author wrote a minimal hand-rolled DEC, the test would not catch real-world drift.
4. The test runs in under one second so it can stay in the every-push set.

Owner role: `science.proof-gate-runner`.

## risks if promoted blindly

- The env-var override is one of several reasonable injection points. A reviewer who prefers argparse should push back; the dream candidate is one shape, not the shape.
- The test depends on `subprocess.run`, which means a Python-version mismatch between the script and the test runner produces a confusing failure. Reviewer may want the test to import the validator's `main()` directly and call it with a chdir context manager.
- The test pins the cache path, which means a deliberate removal of the cache file (intended deprecation) breaks the test in a way the next agent has to read carefully. The test name and assertion message should call out the cache-path dependency.
- A test that uses a real DEC as the fixture breaks if the DEC schema gains a required field that the seed DEC does not carry. Reviewer should consider auto-pinning the fixture (commit the test's expected DEC) instead of reading the live file.
