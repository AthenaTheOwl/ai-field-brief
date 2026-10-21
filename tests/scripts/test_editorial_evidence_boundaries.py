"""Reference boundary regressions; no source fetches or DNS lookups."""
import importlib.util
from pathlib import Path

import pytest
import yaml

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/validate_editorial_evidence.py"
spec = importlib.util.spec_from_file_location("editorial_evidence_boundaries", SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def brief_fixture(tmp_path, text="**Evidence:** CELL-1\n", uri="https://example.com/paper"):
    brief = tmp_path / "briefs/2026-W20"
    (brief / "matrix").mkdir(parents=True)
    (brief / "brief.md").write_text(text, encoding="utf-8")
    cell = {
        "id": "CELL-1", "faithfulness_status": "passed", "status": "verified",
        "content": "A bounded claim.",
        "source_refs": [{"uri": uri, "quote_or_span": "Section 2"}],
    }
    (brief / "matrix/cells.yaml").write_text(yaml.safe_dump({"cells": [cell]}), encoding="utf-8")
    return brief


@pytest.mark.parametrize("host", [
    "localhost", "LOCALHOST.", "review.localhost", "localhost.localdomain",
    "127.0.0.1", "10.1.2.3", "172.16.0.1", "192.168.1.2",
    "169.254.169.254", "0.0.0.0", "[::1]", "[fc00::1]", "[fe80::1]",
    "[::ffff:127.0.0.1]", "224.0.0.1", "127.1", "2130706433", "0x7f000001",
])
def test_nonpublic_reference_cannot_pass_as_public(tmp_path, host):
    brief = brief_fixture(tmp_path, uri=f"https://{host}/paper")
    assert any("no public HTTP" in error for error in gate.check_brief(brief))


@pytest.mark.parametrize("host", ["example.com", "8.8.8.8", "[2606:4700:4700::1111]", "[::ffff:8.8.8.8]"])
def test_public_names_and_literal_addresses_do_not_need_dns(tmp_path, monkeypatch, host):
    import socket

    def no_lookup(*args, **kwargs):
        raise AssertionError("The reference gate must not resolve source hosts")

    monkeypatch.setattr(socket, "getaddrinfo", no_lookup)
    monkeypatch.setattr(socket, "gethostbyname", no_lookup)
    assert gate.check_brief(brief_fixture(tmp_path, uri=f"https://{host}/paper")) == []


@pytest.mark.parametrize("fence", ["```", "~~~", "````"])
def test_evidence_only_in_a_fence_is_not_public_support(tmp_path, fence):
    text = f"{fence}markdown\n**Evidence:** CELL-1\n{fence}\n"
    assert any("no explicit Evidence" in error for error in gate.check_brief(brief_fixture(tmp_path, text)))


def test_fenced_example_does_not_add_a_dangling_reference(tmp_path):
    text = "**Evidence:** CELL-1\n\n```markdown\n**Evidence:** MISSING\n```\n"
    assert gate.check_brief(brief_fixture(tmp_path, text)) == []


def test_shorter_fence_does_not_end_a_longer_code_block(tmp_path):
    text = "````markdown\n```\n**Evidence:** MISSING\n````\n**Evidence:** CELL-1\n"
    assert gate.check_brief(brief_fixture(tmp_path, text)) == []


def test_tilde_fence_can_be_indented_and_longer_at_close(tmp_path):
    text = "  ~~~markdown\n  **Evidence:** MISSING\n  ~~~~\n**Evidence:** CELL-1\n"
    assert gate.check_brief(brief_fixture(tmp_path, text)) == []
