#!/usr/bin/env python3
"""Run deterministic structure checks for the market-research skill package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REQUIRED_FILES = {
    "VERSION",
    "references/evidence-standard.md",
    "references/source-policy.md",
    "references/standard-research.md",
    "references/industry-onboarding.md",
    "references/report-writing.md",
    "scripts/validate_evidence.py",
    "scripts/render_report.py",
    "scripts/validate_report.py",
    "scripts/run_evals.py",
    "templates/report.html.j2",
    "companion-skills/sales-visit-prep/SKILL.md",
}
REQUIRED_SKILL_REFERENCES = {
    "references/evidence-standard.md",
    "references/source-policy.md",
    "references/standard-research.md",
    "references/industry-onboarding.md",
    "references/report-writing.md",
}
FORBIDDEN_PHRASES = {
    "不使用 Python 脚本渲染": "contradicts the canonical renderer",
    "第一版被用户批评": "leaks development conversation",
    "15000-40000": "hard-codes report length",
    "至少 20 个": "hard-codes company sample size",
    "Finding Cards": "exposes an internal artifact instead of a report",
}
FRONTMATTER = re.compile(r"\A---\n(?P<meta>.*?)\n---\n", re.DOTALL)
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def _frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        raise ValueError(f"{path.relative_to(ROOT)} is missing YAML frontmatter")
    meta = yaml.safe_load(match.group("meta")) or {}
    if not isinstance(meta, dict):
        raise ValueError(f"{path.relative_to(ROOT)} frontmatter must be a mapping")
    return meta, text[match.end() :]


def validate() -> list[str]:
    errors: list[str] = []
    if not SKILL.exists():
        return ["SKILL.md is missing"]

    for relative in sorted(REQUIRED_FILES):
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"required file is missing: {relative}")

    try:
        meta, body = _frontmatter(SKILL)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [str(exc)]
    if set(meta) != {"name", "description"}:
        errors.append("SKILL.md frontmatter must contain only name and description")
    if meta.get("name") != "market-research":
        errors.append("SKILL.md name must be market-research")
    description = meta.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("SKILL.md description is required")
    elif len(description) > 1024:
        errors.append("SKILL.md description exceeds 1024 characters")
    if body.count("\n") + 1 > 240:
        errors.append("SKILL.md exceeds 240 body lines; move detail to references")
    if len(body) > 20_000:
        errors.append("SKILL.md exceeds 20,000 body characters")

    for relative in REQUIRED_SKILL_REFERENCES:
        if relative not in body:
            errors.append(f"SKILL.md does not route to {relative}")

    package_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [SKILL, *sorted((ROOT / "references").glob("*.md"))]
    )
    for phrase, reason in FORBIDDEN_PHRASES.items():
        if phrase in package_text:
            errors.append(f"forbidden phrase {phrase!r}: {reason}")

    version_path = ROOT / "VERSION"
    if version_path.is_file():
        version = version_path.read_text(encoding="utf-8").strip()
        if not SEMVER.fullmatch(version):
            errors.append("VERSION must contain semantic version X.Y.Z")

    companion = ROOT / "companion-skills" / "sales-visit-prep" / "SKILL.md"
    if companion.is_file():
        try:
            companion_meta, _ = _frontmatter(companion)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(str(exc))
        else:
            if set(companion_meta) != {"name", "description"}:
                errors.append("sales-visit-prep frontmatter must contain only name and description")
            if companion_meta.get("name") != "sales-visit-prep":
                errors.append("companion skill name must be sales-visit-prep")

    eval_path = ROOT / "evals" / "evals.json"
    try:
        data = json.loads(eval_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid evals/evals.json: {exc}")
    else:
        entries = data.get("evals") if isinstance(data, dict) else None
        if not isinstance(entries, list) or not entries:
            errors.append("evals/evals.json must contain a non-empty evals list")
        else:
            ids: set[int] = set()
            for index, entry in enumerate(entries):
                label = f"evals[{index}]"
                if not isinstance(entry, dict):
                    errors.append(f"{label} must be a mapping")
                    continue
                required = {"id", "name", "prompt", "expected_output", "checks"}
                missing = required - set(entry)
                if missing:
                    errors.append(f"{label} missing fields: {sorted(missing)}")
                    continue
                if not isinstance(entry["id"], int) or entry["id"] in ids:
                    errors.append(f"{label}.id must be a unique integer")
                ids.add(entry["id"])
                checks = entry.get("checks")
                if not isinstance(checks, dict) or not checks.get("must_match"):
                    errors.append(f"{label}.checks.must_match must be a non-empty list")
                else:
                    for pattern in checks.get("must_match", []) + checks.get("must_not_match", []):
                        try:
                            re.compile(pattern)
                        except (TypeError, re.error) as exc:
                            errors.append(f"{label} has invalid regex {pattern!r}: {exc}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    meta, body = _frontmatter(SKILL)
    print("PASS: market-research skill package is structurally consistent")
    print(f"  version: {(ROOT / 'VERSION').read_text(encoding='utf-8').strip()}")
    print(f"  description chars: {len(meta['description'])}")
    print(f"  SKILL.md body lines: {body.count(chr(10)) + 1}")
    print(f"  progressive references: {len(REQUIRED_SKILL_REFERENCES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
