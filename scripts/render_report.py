#!/usr/bin/env python3
"""Render a research Markdown report with one tested HTML template."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup, NavigableString, Tag
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "templates"
SOURCE_REF = re.compile(r"\[(S[1-9]\d*)\]")
SOURCE_ID = re.compile(r"^S[1-9]\d*$")
THEMES = {"light", "dark"}


def _slug(text: str, used: set[str]) -> str:
    base = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text.lower()).strip("-") or "section"
    candidate = base
    counter = 2
    while candidate in used:
        candidate = f"{base}-{counter}"
        counter += 1
    used.add(candidate)
    return candidate


def _markdown() -> MarkdownIt:
    return MarkdownIt("commonmark", {"html": False}).enable("table").enable("strikethrough")


def _replace_source_refs(soup: BeautifulSoup) -> set[str]:
    referenced: set[str] = set()
    occurrences: dict[str, int] = {}
    for node in list(soup.find_all(string=SOURCE_REF)):
        if not isinstance(node, NavigableString):
            continue
        parent = node.parent
        if isinstance(parent, Tag) and parent.name in {"a", "code", "pre", "script", "style"}:
            continue
        text = str(node)
        cursor = 0
        replacements: list[Tag | NavigableString] = []
        for match in SOURCE_REF.finditer(text):
            if match.start() > cursor:
                replacements.append(NavigableString(text[cursor : match.start()]))
            source_id = match.group(1)
            referenced.add(source_id)
            occurrences[source_id] = occurrences.get(source_id, 0) + 1
            anchor = soup.new_tag("a", href=f"#source-{source_id}")
            anchor["class"] = ["source-ref"]
            anchor["id"] = f"ref-{source_id}-{occurrences[source_id]}"
            anchor.string = f"[{source_id}]"
            replacements.append(anchor)
            cursor = match.end()
        if cursor < len(text):
            replacements.append(NavigableString(text[cursor:]))
        for replacement in replacements:
            node.insert_before(replacement)
        node.extract()
    return referenced


def _decorate_sources(soup: BeautifulSoup) -> set[str]:
    source_rows: set[str] = set()
    for row in soup.find_all("tr"):
        cells = row.find_all(["th", "td"], recursive=False)
        if not cells:
            continue
        source_id = cells[0].get_text(" ", strip=True)
        if not SOURCE_ID.fullmatch(source_id):
            continue
        if source_id in source_rows:
            raise ValueError(f"duplicate source row in Markdown source index: {source_id}")
        source_rows.add(source_id)
        row["id"] = f"source-{source_id}"
        cells[0]["class"] = list(cells[0].get("class", [])) + ["source-id"]
        back = soup.new_tag("a", href=f"#ref-{source_id}-1")
        back["class"] = ["source-back"]
        back["aria-label"] = f"返回正文第一次引用 {source_id}"
        back.string = "↩"
        cells[0].append(NavigableString(" "))
        cells[0].append(back)
    return source_rows


def _decorate_links(soup: BeautifulSoup) -> None:
    for link in soup.find_all("a", href=True):
        href = str(link["href"])
        if href.startswith(("http://", "https://")):
            link["target"] = "_blank"
            link["rel"] = ["noopener", "noreferrer"]


def _wrap_tables(soup: BeautifulSoup) -> None:
    for table in list(soup.find_all("table")):
        parent = table.parent
        if isinstance(parent, Tag) and "table-wrap" in parent.get("class", []):
            continue
        wrapper = soup.new_tag("div")
        wrapper["class"] = ["table-wrap"]
        table.wrap(wrapper)


def build_report_body(markdown_text: str) -> dict[str, Any]:
    soup = BeautifulSoup(_markdown().render(markdown_text), "html.parser")
    used: set[str] = set()
    toc: list[dict[str, Any]] = []
    title = "市场调研报告"
    first_h1 = soup.find("h1")
    if isinstance(first_h1, Tag):
        title = first_h1.get_text(" ", strip=True) or title
        first_h1.extract()
    for heading in soup.find_all(["h2", "h3"]):
        heading_text = heading.get_text(" ", strip=True)
        heading_id = _slug(heading_text, used)
        heading["id"] = heading_id
        toc.append({"level": int(heading.name[1]), "title": heading_text, "id": heading_id})

    referenced = _replace_source_refs(soup)
    source_rows = _decorate_sources(soup)
    missing_rows = sorted(referenced - source_rows)
    if missing_rows:
        raise ValueError(f"source references missing from Markdown source index: {missing_rows}")
    _decorate_links(soup)
    _wrap_tables(soup)
    return {
        "title": title,
        "toc": toc,
        "body_html": str(soup),
        "source_ids": sorted(source_rows),
    }


def render_report(markdown_text: str, theme: str = "light", generated_at: str | None = None) -> str:
    if theme not in THEMES:
        raise ValueError(f"theme must be one of {sorted(THEMES)}")
    report = build_report_body(markdown_text)
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("report.html.j2")
    return template.render(
        **report,
        theme=theme,
        generated_at=generated_at or date.today().isoformat(),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--theme", choices=sorted(THEMES), default="light")
    parser.add_argument("--generated-at", help="ISO date shown in the report footer")
    args = parser.parse_args()
    try:
        markdown_text = args.input.read_text(encoding="utf-8")
        rendered = render_report(markdown_text, args.theme, args.generated_at)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print(f"WROTE {args.output} ({args.theme})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
