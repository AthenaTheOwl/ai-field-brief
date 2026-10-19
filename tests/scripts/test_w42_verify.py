"""ops/w42/verify.py replays the CI script gates, cadence_check included."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _w42_gates() -> list[str]:
    spec = importlib.util.spec_from_file_location("w42_verify", ROOT / "ops" / "w42" / "verify.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.GATES


def test_w42_verify_replays_the_cadence_gate_it_changed() -> None:
    gates = _w42_gates()
    assert "cadence_check" in gates
    assert len(gates) == len(set(gates))
    assert [g for g in gates if not (ROOT / "scripts" / f"{g}.py").is_file()] == []
