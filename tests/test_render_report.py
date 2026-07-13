from __future__ import annotations

from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from render_report import build_report_body, render_report

FIXTURE = Path(__file__).parent / "fixtures" / "sample-report.md"


def test_renderer_preserves_markdown_and_builds_links() -> None:
    html = render_report(FIXTURE.read_text(encoding="utf-8"), generated_at="2026-07-13")
    soup = BeautifulSoup(html, "html.parser")
    assert soup.select_one('a.source-ref[href="#source-S1"]')
    assert soup.select_one('#source-S1 a[href="https://example.com/policy"]')
    assert soup.select_one(".table-wrap > table")
    assert soup.select_one(".report-content ul li")
    assert soup.select_one('.toc-link[href="#执行摘要"]')
    external = soup.select_one('a[href="https://example.com/policy"]')
    assert external and external.get("target") == "_blank"
    assert set(external.get("rel", [])) == {"noopener", "noreferrer"}
    assert 'id="ref-{c}"' not in html


def test_light_and_dark_themes_are_real_variants() -> None:
    markdown = FIXTURE.read_text(encoding="utf-8")
    light = render_report(markdown, "light")
    dark = render_report(markdown, "dark")
    assert light != dark
    assert 'html lang="zh-CN" data-theme="light"' in light
    assert 'html lang="zh-CN" data-theme="dark"' in dark


def test_renderer_rejects_unindexed_reference() -> None:
    markdown = FIXTURE.read_text(encoding="utf-8").replace("[S1][S2]", "[S1][S3]")
    with pytest.raises(ValueError, match="S3"):
        build_report_body(markdown)


def test_renderer_rejects_duplicate_source_rows() -> None:
    markdown = FIXTURE.read_text(encoding="utf-8")
    duplicate = "| S1 | [重复来源](https://example.com/duplicate) | 原始来源 | 2026-01-10 |\n"
    markdown = markdown.replace(
        "| S2 | [制造业质量检测调查](https://example.org/survey) | 机构来源 | 2025-11-20 |\n",
        "| S2 | [制造业质量检测调查](https://example.org/survey) | 机构来源 | 2025-11-20 |\n" + duplicate,
    )
    with pytest.raises(ValueError, match="duplicate source row"):
        build_report_body(markdown)
