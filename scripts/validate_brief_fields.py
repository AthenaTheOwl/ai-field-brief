#!/usr/bin/env python3
"""Validate Top-signal field conformance for published briefs.

AGENTS.md states, per DEC-MTRX-007 and DEC-CDCP-020, that every Top signal
in a published digest must carry ``systems_map``, ``transferable_principle``,
``falsification_test``, and ``adoption_ladder``. The Brief OS digest format
in ``templates/weekly-brief.md`` additionally requires a ``Confidence`` label
and an ``Evidence`` line per pick, and ``AGENTS.md`` requires the action
surface to resolve against ``config/action_surface_taxonomy.yaml``.

Briefs 2026-W32 through 2026-W34 shipped without the last five of those, and
nothing caught it. This gate is that check. See DEC-PUB-013.

Rules, applied to every ``briefs/YYYY-WNN/brief.md`` not in ``LEGACY_BRIEFS``:

  1. A ``## Top signals`` section exists and holds at least one ``### `` pick.
  2. Each pick carries ``Source:`` or ``Sources:``.
  3. Each pick carries ``Action surface:``, and every surface named resolves
     against the taxonomy's ``surfaces`` list. Surfaces listed under the
     taxonomy's ``aliases`` key are reported as retired, not accepted.
  4. Each pick carries ``Systems map:``, ``Transferable principle:``,
     ``Falsification test:``, and ``Adoption ladder:``.
  5. The adoption ladder names all four rungs: a minimum-viable step, a mid
     step, a full step, and monitoring signals.
  6. Each pick carries ``Confidence:`` with a value in {high, medium, low}.
  7. Each pick carries ``Evidence:`` naming at least one cell id, and when
     ``matrix/cells.yaml`` sits beside the brief, every cited id resolves to
     a cell in that file.

``LEGACY_BRIEFS`` records the debt rather than hiding it. Removing a week
from that set is how the backfill lands.

Exit codes: 0 OK, 1 violations found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIEFS_DIR = ROOT / "briefs"
TAXONOMY_PATH = ROOT / "config" / "action_surface_taxonomy.yaml"

# Issues published before the gate existed. Each shipped without one or more
# of the fields below. Backfill a week, then delete its entry here.
LEGACY_BRIEFS = {
    "2026-W20",
    "2026-W21",
    "2026-W22",
    "2026-W22-rerun",
    "2026-W23",
    "2026-W24",
    "2026-W25",
    "2026-W26",
    "2026-W27",
    "2026-W28",
    "2026-W29",
    "2026-W30",
    "2026-W31",
    "2026-W32",
    "2026-W33",
    "2026-W34",
}

REQUIRED_FIELDS = (
    "Systems map",
    "Transferable principle",
    "Falsification test",
    "Adoption ladder",
)

LADDER_RUNGS = (
    ("minimum viable", re.compile(r"minimum[ -]viable", re.IGNORECASE)),
    ("mid", re.compile(r"^\s*[-*]\s*mid\b", re.IGNORECASE | re.MULTILINE)),
    ("full", re.compile(r"^\s*[-*]\s*full\b", re.IGNORECASE | re.MULTILINE)),
    ("monitoring", re.compile(r"monitoring", re.IGNORECASE)),
)

CONFIDENCE_VALUES = {"high", "medium", "low"}

FIELD_RE_CACHE: dict[str, re.Pattern[str]] = {}
HEADING_RE = re.compile(r"^(#{2,4})\s+(.*)$", re.MULTILINE)
CELL_ID_RE = re.compile(r"^\s*-\s*id:\s*(\S+)\s*$", re.MULTILINE)
WEEK_DIR_RE = re.compile(r"^\d{4}-W\d{2}")


def field_re(name: str) -> re.Pattern[str]:
    if name not in FIELD_RE_CACHE:
        FIELD_RE_CACHE[name] = re.compile(
            rf"^[ \t]*\*\*{re.escape(name)}:?\*\*:?[ \t]*(.*)$",
            re.MULTILINE | re.IGNORECASE,
        )
    return FIELD_RE_CACHE[name]


def load_taxonomy() -> tuple[set[str], dict[str, str]]:
    """Return (valid surface ids, retired alias -> replacement)."""
    if not TAXONOMY_PATH.is_file():
        return set(), {}
    text = TAXONOMY_PATH.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore[import-not-found]

        data = yaml.safe_load(text) or {}
        surfaces = {
            str(s["id"]) for s in data.get("surfaces", []) if isinstance(s, dict) and "id" in s
        }
        aliases = {str(k): str(v) for k, v in (data.get("aliases") or {}).items()}
        return surfaces, aliases
    except ImportError:
        # Line-level fallback so the gate runs on a bare Python install.
        surfaces = set(re.findall(r"^\s*-\s*id:\s*(\S+)\s*$", text, re.MULTILINE))
        aliases: dict[str, str] = {}
        in_aliases = False
        for line in text.splitlines():
            if line.startswith("aliases:"):
                in_aliases = True
                continue
            if in_aliases:
                match = re.match(r"^\s+(\S+):\s*(\S+)\s*$", line)
                if match:
                    aliases[match.group(1)] = match.group(2)
                elif line.strip() and not line.startswith(" "):
                    in_aliases = False
        return surfaces, aliases


def split_top_signals(text: str) -> list[tuple[str, str]]:
    """Return (pick heading, pick body) for each pick under ## Top signals."""
    headings = list(HEADING_RE.finditer(text))
    picks: list[tuple[str, str]] = []
    in_section = False
    for index, match in enumerate(headings):
        level, title = len(match.group(1)), match.group(2).strip()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        if level == 2:
            in_section = title.lower().startswith("top signal")
            continue
        if in_section and level == 3:
            picks.append((title, text[match.end() : end]))
    return picks


def known_cell_ids(brief_dir: Path) -> set[str] | None:
    cells_path = brief_dir / "matrix" / "cells.yaml"
    if not cells_path.is_file():
        return None
    return set(CELL_ID_RE.findall(cells_path.read_text(encoding="utf-8")))


def check_pick(
    label: str,
    body: str,
    surfaces: set[str],
    aliases: dict[str, str],
    cell_ids: set[str] | None,
    violations: list[str],
) -> None:
    if not field_re("Source").search(body) and not field_re("Sources").search(body):
        violations.append(f"{label}: no Source or Sources line")

    surface_match = field_re("Action surface").search(body)
    if not surface_match:
        violations.append(f"{label}: no Action surface line")
    elif surfaces:
        named = [s.strip().strip("`") for s in re.split(r"[,/]| and ", surface_match.group(1))]
        for surface in [s for s in named if s]:
            if surface in aliases:
                violations.append(
                    f"{label}: action surface '{surface}' is retired; "
                    f"use '{aliases[surface]}'"
                )
            elif surface not in surfaces:
                violations.append(
                    f"{label}: action surface '{surface}' is not in "
                    f"config/action_surface_taxonomy.yaml"
                )

    for name in REQUIRED_FIELDS:
        if not field_re(name).search(body):
            violations.append(f"{label}: missing required field '{name}'")

    ladder_match = field_re("Adoption ladder").search(body)
    if ladder_match:
        ladder = body[ladder_match.end() :]
        stop = re.search(r"^\s*\*\*(?:Confidence|Evidence)", ladder, re.MULTILINE)
        if stop:
            ladder = ladder[: stop.start()]
        for rung, pattern in LADDER_RUNGS:
            if not pattern.search(ladder):
                violations.append(f"{label}: adoption ladder does not name a '{rung}' rung")

    confidence_match = field_re("Confidence").search(body)
    if not confidence_match:
        violations.append(f"{label}: no Confidence label")
    else:
        value = confidence_match.group(1).strip().strip(".").lower()
        if value not in CONFIDENCE_VALUES:
            violations.append(
                f"{label}: Confidence '{value}' is not one of high, medium, low"
            )

    evidence_match = field_re("Evidence").search(body)
    if not evidence_match:
        violations.append(f"{label}: no Evidence line")
        return
    cited = [c.strip() for c in evidence_match.group(1).split(",") if c.strip()]
    if not cited:
        violations.append(f"{label}: Evidence line names no cell id")
        return
    if cell_ids is not None:
        for cell in cited:
            if cell not in cell_ids:
                violations.append(f"{label}: Evidence cell '{cell}' is not in matrix/cells.yaml")


def check_brief(brief_dir: Path, surfaces: set[str], aliases: dict[str, str]) -> list[str]:
    violations: list[str] = []
    brief_path = brief_dir / "brief.md"
    rel = brief_path.relative_to(ROOT).as_posix()
    text = brief_path.read_text(encoding="utf-8")

    picks = split_top_signals(text)
    if not picks:
        violations.append(f"{rel}: no Top signals section, or no picks inside it")
        return violations

    cell_ids = known_cell_ids(brief_dir)
    for title, body in picks:
        check_pick(f"{rel}: '{title}'", body, surfaces, aliases, cell_ids, violations)
    return violations


def main() -> int:
    if not BRIEFS_DIR.is_dir():
        print("validate_brief_fields OK (no briefs/ directory yet)")
        return 0

    surfaces, aliases = load_taxonomy()
    if not surfaces:
        print("validate_brief_fields: taxonomy unreadable; surface names not checked")

    violations: list[str] = []
    checked = 0
    skipped = 0
    for brief_dir in sorted(BRIEFS_DIR.iterdir()):
        if not brief_dir.is_dir() or not WEEK_DIR_RE.match(brief_dir.name):
            continue
        if not (brief_dir / "brief.md").is_file():
            continue
        if brief_dir.name in LEGACY_BRIEFS:
            skipped += 1
            continue
        checked += 1
        violations.extend(check_brief(brief_dir, surfaces, aliases))

    if violations:
        print(f"validate_brief_fields FAILED ({len(violations)} violation(s)):")
        for line in violations:
            print(f"  - {line}")
        return 1

    print(
        f"validate_brief_fields OK ({checked} brief(s) checked, "
        f"{skipped} legacy brief(s) skipped)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
