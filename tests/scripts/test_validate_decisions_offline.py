"""eval-002 (promoted from 2026-W21 dream).

Regression: validate_decisions.py must work offline via
ops/schemas-cache/decision.schema.json.

If the remote schema fetch is unreachable AND the local cache holds
decision.schema.json, the script should validate every DEC successfully
without raising. The remote-fetch path runs every push under normal CI,
so the cache-fallback path stays dark; this test pins the behavior so
the next offline run does not surface as a silent break.

The script honors AI_FIELD_BRIEF_SCHEMA_URL_BASE as an override on the
default remote URL. Pointing it at an unresolvable host forces the
URLError -> load_cached_schema() path.
"""

import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CACHE = ROOT / "ops" / "schemas-cache" / "decision.schema.json"


def test_offline_cache_path_resolves():
    """Local decision.schema.json cache exists for the offline-fallback path.

    Covers: R-CDCP-002.
    """
    assert CACHE.exists(), (
        "ops/schemas-cache/decision.schema.json must exist for offline validation"
    )


def test_validate_decisions_succeeds_with_offline_env():
    """validate_decisions.py validates every DEC against the cached schema.

    Covers: R-CDCP-002, R-CDCP-010.
    """
    # Force the remote fetch to fail by pointing the script at a
    # non-resolvable host. The script should fall back to the cache.
    env = os.environ.copy()
    env["AI_FIELD_BRIEF_SCHEMA_URL_BASE"] = "https://invalid.invalid/missing.json"
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_decisions.py")],
        env=env,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"validate_decisions failed offline: stdout={result.stdout!r} "
        f"stderr={result.stderr!r}"
    )
