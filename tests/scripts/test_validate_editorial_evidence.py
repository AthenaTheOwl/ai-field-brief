from copy import deepcopy
import importlib.util
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/validate_editorial_evidence.py"
spec = importlib.util.spec_from_file_location("editorial_evidence", SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def make_brief(tmp_path, cell=None, text="**Evidence:** CELL-1\n"):
    brief = tmp_path / "briefs/2026-W20"
    (brief / "matrix").mkdir(parents=True)
    (brief / "brief.md").write_text(text, encoding="utf-8")
    if cell is None:
        cell = {"id": "CELL-1", "faithfulness_status": "passed", "status": "verified", "content": "A bounded source claim.", "source_refs": [{"uri": "https://example.com/paper", "quote_or_span": "Section 2, the evaluated fixture."}]}
    (brief / "matrix/cells.yaml").write_text(yaml.safe_dump({"cells": [cell]}), encoding="utf-8")
    return brief


def change_cell(brief, key, value):
    path = brief / "matrix/cells.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    data["cells"][0][key] = value
    path.write_text(yaml.safe_dump(data), encoding="utf-8")


def test_legacy_format_can_keep_its_headings(tmp_path):
    brief = make_brief(tmp_path, text="## An original old-style heading\n\n**Evidence:** `CELL-1`.\n")
    assert gate.check_brief(brief) == []


@pytest.mark.parametrize("field,value,expected", [
    ("faithfulness_status", "not_checked", "not faithfulness-passed"),
    ("faithfulness_status", "failed", "not faithfulness-passed"),
    ("status", "rejected", "is rejected"),
    ("content", " ", "no content"),
    ("source_refs", [], "no source reference"),
    ("source_refs", [{"uri": "file:///private/source", "quote_or_span": "Section 2"}], "no public HTTP"),
    ("source_refs", [{"uri": "https://example.com", "quote_or_span": "TODO"}], "no usable source"),
    ("source_refs", [{"uri": "https://[broken", "quote_or_span": "Section 2"}], "no public HTTP"),
])
def test_rejects_unreviewed_or_empty_support(tmp_path, field, value, expected):
    brief = make_brief(tmp_path)
    change_cell(brief, field, value)
    assert any(expected in error for error in gate.check_brief(brief))


def test_rejects_missing_matrix(tmp_path):
    brief = make_brief(tmp_path)
    (brief / "matrix/cells.yaml").unlink()
    assert any("no matrix" in error for error in gate.check_brief(brief))


def test_historical_lifecycle_does_not_override_passed_faithfulness(tmp_path):
    brief = make_brief(tmp_path)
    change_cell(brief, "status", "created")
    assert gate.check_brief(brief) == []


@pytest.mark.parametrize("text,expected", [("No explicit reference.\n", "no explicit Evidence"), ("**Evidence:**\n", "empty Evidence"), ("**Evidence:** MISSING\n", "does not exist")])
def test_rejects_dangling_or_missing_references(tmp_path, text, expected):
    brief = make_brief(tmp_path, text=text)
    assert any(expected in error for error in gate.check_brief(brief))


def test_duplicate_id_cannot_replace_reviewed_record(tmp_path):
    brief = make_brief(tmp_path)
    path = brief / "matrix/cells.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    duplicate = deepcopy(data["cells"][0])
    duplicate["content"] = "Replacement claim."
    data["cells"].append(duplicate)
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    assert any("duplicate cell id" in error for error in gate.check_brief(brief))


def test_cli_fails_on_unresolved_reference(tmp_path):
    make_brief(tmp_path, text="**Evidence:** MISSING\n")
    result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(tmp_path)], capture_output=True, text=True)
    assert result.returncode == 1
    assert "does not exist" in result.stdout


def test_separate_current_review_file_resolves_without_rewriting_original(tmp_path):
    brief = make_brief(tmp_path, text="**Evidence:** REVIEW-1\n")
    original = (brief / "matrix/cells.yaml").read_bytes()
    data = yaml.safe_load(original)
    data["cells"][0]["id"] = "REVIEW-1"
    (brief / "matrix/editorial-review-2026-10-21.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")
    assert gate.check_brief(brief) == []
    assert (brief / "matrix/cells.yaml").read_bytes() == original
    field_spec = importlib.util.spec_from_file_location("brief_fields", SCRIPT.with_name("validate_brief_fields.py"))
    fields = importlib.util.module_from_spec(field_spec)
    field_spec.loader.exec_module(fields)
    assert fields.known_cell_ids(brief) == {"CELL-1", "REVIEW-1"}


def test_duplicate_id_across_review_files_is_rejected(tmp_path):
    brief = make_brief(tmp_path)
    (brief / "matrix/editorial-review-2026-10-21.yaml").write_bytes((brief / "matrix/cells.yaml").read_bytes())
    assert any("duplicate cell id" in error for error in gate.check_brief(brief))


def test_each_legacy_lead_signal_needs_its_own_binding(tmp_path):
    brief = make_brief(tmp_path, text=(
        "# Older issue\n\n## First concrete pick\n\nClaim one.\n\n"
        "**Evidence:** CELL-1\n\n## Second concrete pick\n\nClaim two.\n\n"
        "## Worth your time\n\n**Evidence:** CELL-1\n"
    ))
    errors = gate.check_brief(brief)
    assert any("Second concrete pick" in error and "no Evidence" in error for error in errors)
    assert not any("First concrete pick" in error for error in errors)


@pytest.mark.parametrize("week,count", [(20,5), (21,5), (22,7), (23,6), (24,7), (25,7), (26,7), (27,7)])
def test_all_eight_published_early_layouts_bind_every_pick(tmp_path, week, count):
    # Keep the historical major-heading layout and the later Top-signals
    # layout; unrelated packets, changelog headings and fenced runbooks
    # are intentionally present so they cannot borrow or demand evidence.
    if week in (20,21):
        text = "# Old issue\n\n"
        for number in range(1,count+1):
            text += f"## Pick {number}\n\nA concrete source claim.\n\n"
            if week == 21 and number == 2:
                text += "```markdown\n## Model-output incident\n**Evidence:** MISSING\n```\n\n"
            text += "**Evidence:** CELL-1\n\n"
        text += "## Worth your time\n\nA shorter note.\n" if week == 20 else "## Three more, in shorter form\n\nA shorter note.\n"
    else:
        text = "# Issue\n\n## Field thesis\n\nA narrow opening.\n\n"
        if week == 22:
            text += "## Vol. 4 to Vol. 5 changelog\n\nHistorical note.\n\n"
        if week == 27:
            text += "## Source refresh\n\nHistorical registry note.\n\n"
        text += "## Top signals\n\n"
        for number in range(1,count+1):
            text += f"### {number}. Pick {number}\n\nA concrete claim.\n\n**Evidence:** CELL-1\n\n"
        text += "## Action packets\n\n### Packet A: a proposed test\n\nNo result asserted.\n"
    brief = make_brief(tmp_path, text=text)
    if week != 20:
        target = brief.with_name(f"2026-W{week}")
        brief.rename(target)
        brief = target
    assert len(gate.signal_sections(text,brief.name)) == count
    assert gate.check_brief(brief) == []
    # Removing a single middle binding must fail even though every other
    # signal remains bound and a later section may contain example ids.
    broken = text.replace("**Evidence:** CELL-1", "No binding here.", 1)
    (brief / "brief.md").write_text(broken,encoding="utf-8")
    assert any("Top signal" in error and "no Evidence" in error for error in gate.check_brief(brief))


def test_fenced_binding_cannot_fill_a_real_signal_gap(tmp_path):
    brief = make_brief(tmp_path, text=(
        "## Top signals\n\n### 1. First\n\n**Evidence:** CELL-1\n\n"
        "### 2. Second\n\n```markdown\n**Evidence:** CELL-1\n```\n"
    ))
    assert any("Second" in error and "no Evidence" in error for error in gate.check_brief(brief))
