#!/usr/bin/env python3
"""Static checks for market-research skill structure."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(f"FAIL: PyYAML unavailable: {exc}")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"

REQUIRED_REFS = [
    "references/evidence-workflow.md",
    "references/methods.md",
    "references/reporting.md",
    "references/structure-patterns.md",
    "references/quality.md",
    "references/sales-visit-prep.md",
]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def main() -> None:
    if not SKILL.exists():
        fail("SKILL.md missing")
    text = SKILL.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        fail("missing YAML frontmatter")
    meta = yaml.safe_load(m.group(1)) or {}
    if meta.get("name") != "market-research":
        fail("frontmatter name must be market-research")
    desc = meta.get("description", "")
    if not desc or len(desc) > 500:
        fail(f"description length invalid: {len(desc)}")
    if any(term in desc for term in ["先校准", "证据地图", "Finding", "HTML 报告"]):
        fail("description appears to summarize workflow; keep it trigger-focused")

    body = text[m.end():]
    lines = body.count("\n") + 1
    words = len(re.findall(r"\S+", body))
    if lines > 500:
        fail(f"SKILL.md too long: {lines} lines; move detail to references")
    if words > 2200:
        fail(f"SKILL.md too wordy: {words} rough words")

    for rel in REQUIRED_REFS:
        p = ROOT / rel
        if not p.exists():
            fail(f"missing referenced file: {rel}")
        if p.stat().st_size < 500:
            fail(f"reference file too thin: {rel}")

    evals = ROOT / "evals" / "evals.json"
    if not evals.exists():
        fail("evals/evals.json missing")
    with evals.open(encoding="utf-8") as f:
        ev = json.load(f)
    if not isinstance(ev, dict) or "evals" not in ev:
        fail("evals/evals.json root must be dict with 'evals' key")
    if not isinstance(ev["evals"], list) or len(ev["evals"]) == 0:
        fail("evals/evals.json 'evals' must be a non-empty array")
    REQUIRED_EVAL_FIELDS = {"id", "name", "prompt", "expected_output", "assertions"}
    for i, entry in enumerate(ev["evals"]):
        missing = REQUIRED_EVAL_FIELDS - set(entry.keys())
        if missing:
            fail(f"eval[{i}] missing required fields: {missing}")
        if not isinstance(entry.get("assertions"), list) or len(entry["assertions"]) == 0:
            fail(f"eval[{i}] assertions must be a non-empty array")

    print("PASS: market-research skill structure looks good")
    print(f"  description chars: {len(desc)}")
    print(f"  SKILL.md lines: {lines}")
    print(f"  rough words: {words}")
    print(f"  references: {len(REQUIRED_REFS)}")


if __name__ == "__main__":
    main()
