from __future__ import annotations

from pathlib import Path

from render_report import render_report
from validate_evidence import load_evidence
from validate_report import validate_report

FIXTURES = Path(__file__).parent / "fixtures"


def test_report_evidence_and_html_stay_consistent() -> None:
    markdown = (FIXTURES / "sample-report.md").read_text(encoding="utf-8")
    evidence = load_evidence(FIXTURES / "sample-evidence.yaml")
    html = render_report(markdown, generated_at="2026-07-13")
    assert validate_report(markdown, evidence, html) == []


def test_missing_source_url_is_detected() -> None:
    markdown = (FIXTURES / "sample-report.md").read_text(encoding="utf-8")
    markdown = markdown.replace("https://example.org/survey", "https://invalid.example/survey")
    evidence = load_evidence(FIXTURES / "sample-evidence.yaml")
    assert any("does not include evidence URL for S2" in error for error in validate_report(markdown, evidence))
