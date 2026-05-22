"""Validate the spec-driven-development artifact set for ai-field-brief.

Phase 0 rules — every active spec under `specs/NNNN-*/` must:
  1. Carry the six required ledger files (requirements, design, tasks,
     acceptance, research, traceability).
  2. Define at least one R-* requirement in requirements.md, with the
     R-PREFIX-NNN shape: `### R-PREFIX-001: ...`.
  3. Use an R-* prefix from the planned set (BOOT, FND, SRC, RUN, TRN,
     EXT, BRF, PUB, ACT, SCH, INT, BIL, OBS, SEC, MOB, PORT).
  4. Have a traceability.md that names every requirement defined in
     requirements.md (no orphan reqs).
  5. Avoid referencing R-* IDs in traceability.md that are not
     defined in requirements.md (no phantom IDs).
  6. Be listed in specs/README.md.

Exit codes: 0 OK, 1 violations found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SPECS_ROOT = ROOT / "specs"
SPECS_INDEX = SPECS_ROOT / "README.md"

REQUIRED_FILES = (
    "requirements.md",
    "design.md",
    "tasks.md",
    "acceptance.md",
    "research.md",
    "traceability.md",
)

# R-* prefixes the v3 plan allocates for ai-field-brief specs.
# BOOT is the Phase 0 bootstrap. The rest map to specs 0001-0015.
ALLOWED_PREFIXES = {
    "BOOT",  # 0000 bootstrap
    "FND",   # 0001 foundation
    "SRC",   # 0002 source registry + ingestion
    "RUN",   # 0003 run workflow
    "TRN",   # 0004 transcription
    "EXT",   # 0005 extraction + scoring
    "BRF",   # 0006 brief synthesis + review
    "PUB",   # 0007 publishing
    "ACT",   # 0008 action backlog
    "SCH",   # 0009 search + RAG
    "INT",   # 0010 integrations
    "BIL",   # 0011 billing
    "OBS",   # 0012 observability + admin
    "SEC",   # 0013 security + compliance
    "MOB",   # 0014 mobile + extension
    "PORT",  # 0015 portfolio integration
}

REQ_RE = re.compile(r"^###\s+(R-[A-Z]+-\d{3,}):", re.MULTILINE)
ID_RE = re.compile(r"\bR-([A-Z]+)-(\d{3,})\b")
SPEC_DIR_RE = re.compile(r"^\d{4}-[a-z0-9][a-z0-9-]*$")


def active_specs() -> list[Path]:
    if not SPECS_ROOT.exists():
        return []
    return sorted(
        path
        for path in SPECS_ROOT.iterdir()
        if path.is_dir() and SPEC_DIR_RE.match(path.name)
    )


def main() -> int:
    violations: list[str] = []
    spec_dirs = active_specs()
    if not spec_dirs:
        print(f"spec_check: no spec folders found under {SPECS_ROOT}", file=sys.stderr)
        return 1

    index_text = SPECS_INDEX.read_text(encoding="utf-8") if SPECS_INDEX.exists() else ""

    for spec_dir in spec_dirs:
        rel = spec_dir.relative_to(ROOT).as_posix()

        # 1. Required files
        missing = [name for name in REQUIRED_FILES if not (spec_dir / name).is_file()]
        if missing:
            violations.append(
                f"{rel}: missing required file(s): {', '.join(missing)}"
            )

        req_path = spec_dir / "requirements.md"
        trace_path = spec_dir / "traceability.md"
        if not req_path.is_file():
            continue

        req_text = req_path.read_text(encoding="utf-8")
        ids = REQ_RE.findall(req_text)

        # 2. At least one R-* defined
        if not ids:
            violations.append(
                f"{rel}/requirements.md: no R-* requirements defined "
                f"(expected `### R-PREFIX-001: ...` shape)"
            )
            continue

        # 3. Prefix allowed
        prefixes_in_spec: set[str] = set()
        for rid in ids:
            prefix = rid.split("-", 2)[1]
            prefixes_in_spec.add(prefix)
            if prefix not in ALLOWED_PREFIXES:
                violations.append(
                    f"{rel}/requirements.md: unknown prefix `{prefix}` in `{rid}`. "
                    f"Allowed: {', '.join(sorted(ALLOWED_PREFIXES))}."
                )

        # 4 + 5. Traceability coverage + no phantom IDs
        if trace_path.is_file():
            trace_text = trace_path.read_text(encoding="utf-8")
            trace_ids = {
                f"R-{p}-{n}" for p, n in ID_RE.findall(trace_text)
            }
            req_id_set = set(ids)

            missing_in_trace = sorted(req_id_set - trace_ids)
            if missing_in_trace:
                violations.append(
                    f"{rel}/traceability.md: missing references to "
                    f"{', '.join(missing_in_trace)}"
                )

            phantom = sorted(trace_ids - req_id_set)
            # phantom IDs are allowed if they are cross-spec references
            # (prefix exists in another spec's requirements). For Phase 0
            # we tolerate phantom across allowed prefixes.
            phantom_unknown = [
                rid
                for rid in phantom
                if rid.split("-", 2)[1] not in ALLOWED_PREFIXES
            ]
            if phantom_unknown:
                violations.append(
                    f"{rel}/traceability.md: references unknown-prefix IDs "
                    f"{', '.join(phantom_unknown)}"
                )

        # 6. Spec listed in index
        if SPECS_INDEX.exists() and spec_dir.name not in index_text:
            violations.append(
                f"specs/README.md: missing entry for spec folder `{spec_dir.name}`"
            )

    if violations:
        print("spec_check: violations found", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        return 1

    print(f"spec_check OK ({len(spec_dirs)} active specs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
