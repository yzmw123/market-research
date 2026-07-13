#!/usr/bin/env python3
"""Validate report citations, evidence mappings, and rendered HTML."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml
from bs4 import BeautifulSoup

from render_report import SOURCE_REF, build_report_body
from validate_evidence import load_evidence, validate_evidence

SOURCE_ROW = re.compile(r"^\|\s*(S[1-9]\d*)\s*\|", re.MULTILINE)


def validate_report(markdown_text: str, evidence: dict, html_text: str | None = None) -> list[str]:
    errors = validate_evidence(evidence)
    source_by_id = {source["id"]: source for source in evidence.get("sources", []) if isinstance(source, dict) and "id" in source}
    refs = set(SOURCE_REF.findall(markdown_text))
    rows = set(SOURCE_ROW.findall(markdown_text))
    if not refs:
        errors.append("Markdown contains no [S1] style source references")
    if "来源索引" not in markdown_text:
        errors.append("Markdown is missing a 来源索引 section")
    for source_id in sorted(refs - source_by_id.keys()):
        errors.append(f"Markdown references unknown evidence source: {source_id}")
    for source_id in sorted(refs - rows):
        errors.append(f"Markdown reference is missing from source index: {source_id}")
    for source_id, source in source_by_id.items():
        if source_id in refs and source.get("url") not in markdown_text:
            errors.append(f"source index does not include evidence URL for {source_id}")

    try:
        expected = build_report_body(markdown_text)
    except ValueError as exc:
        errors.append(str(exc))
        expected = None

    if html_text is not None and expected is not None:
        soup = BeautifulSoup(html_text, "html.parser")
        if soup.find(string=re.compile(r"ref-\{c\}")) or "ref-{c}" in html_text:
            errors.append("HTML contains an unformatted citation anchor")
        content = soup.select_one(".report-content")
        if content is None:
            errors.append("HTML is missing .report-content")
        else:
            expected_text = BeautifulSoup(expected["body_html"], "html.parser").get_text(" ", strip=True)
            actual_text = content.get_text(" ", strip=True)
            if expected_text != actual_text:
                errors.append("HTML report body does not match Markdown content")
        for source_id in refs:
            if soup.find(id=f"source-{source_id}") is None:
                errors.append(f"HTML is missing source anchor for {source_id}")
            if soup.find("a", href=f"#source-{source_id}") is None:
                errors.append(f"HTML is missing source reference link for {source_id}")
        if not soup.select(".table-wrap > table"):
            errors.append("HTML tables are not wrapped for mobile overflow")
        if "@media (max-width: 840px)" not in html_text:
            errors.append("HTML is missing the mobile layout breakpoint")
        if "overflow-x: auto" not in html_text:
            errors.append("HTML is missing horizontal table overflow handling")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--html", type=Path)
    args = parser.parse_args()
    try:
        markdown_text = args.report.read_text(encoding="utf-8")
        evidence = load_evidence(args.evidence)
        html_text = args.html.read_text(encoding="utf-8") if args.html else None
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"FAIL: {exc}")
        return 1
    errors = validate_report(markdown_text, evidence, html_text)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: report, evidence, citations, and HTML are consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
