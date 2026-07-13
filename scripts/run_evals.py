#!/usr/bin/env python3
"""Validate and score market-research behavior evals."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVALS_PATH = ROOT / "evals" / "evals.json"
NONINTERACTIVE_PREFIX = (
    "这是自动评测环境，不能调用交互式澄清工具。需要澄清时，只能用一条文本集中提问并停止；"
    "信息足够时直接完成任务。\n\n"
)


def load_evals(path: Path = EVALS_PATH) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data.get("evals") if isinstance(data, dict) else None
    if not isinstance(entries, list) or not entries:
        raise ValueError("evals.json must contain a non-empty evals list")
    return entries


def validate_evals(evals: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen: set[int] = set()
    for index, case in enumerate(evals):
        label = f"evals[{index}]"
        required = {"id", "name", "prompt", "expected_output", "checks"}
        missing = required - set(case)
        if missing:
            errors.append(f"{label} missing fields: {sorted(missing)}")
            continue
        if not isinstance(case["id"], int) or case["id"] in seen:
            errors.append(f"{label}.id must be a unique integer")
        seen.add(case["id"])
        checks = case.get("checks")
        if not isinstance(checks, dict):
            errors.append(f"{label}.checks must be a mapping")
            continue
        if not isinstance(checks.get("must_match"), list) or not checks["must_match"]:
            errors.append(f"{label}.checks.must_match must be a non-empty list")
        for field in ("must_match", "must_not_match"):
            patterns = checks.get(field, [])
            if not isinstance(patterns, list):
                errors.append(f"{label}.checks.{field} must be a list")
                continue
            for pattern in patterns:
                try:
                    re.compile(pattern, re.IGNORECASE | re.DOTALL)
                except (TypeError, re.error) as exc:
                    errors.append(f"{label}.{field} invalid regex {pattern!r}: {exc}")
        for field in ("min_chars", "max_chars"):
            value = checks.get(field)
            if value is not None and (not isinstance(value, int) or value < 0):
                errors.append(f"{label}.checks.{field} must be a non-negative integer")
    return errors


def score_output(case: dict[str, Any], output: str) -> tuple[bool, list[str]]:
    checks = case["checks"]
    failures: list[str] = []
    flags = re.IGNORECASE | re.DOTALL
    for pattern in checks.get("must_match", []):
        if re.search(pattern, output, flags) is None:
            failures.append(f"missing required pattern: {pattern}")
    for pattern in checks.get("must_not_match", []):
        if re.search(pattern, output, flags) is not None:
            failures.append(f"matched forbidden pattern: {pattern}")
    minimum = checks.get("min_chars")
    maximum = checks.get("max_chars")
    if minimum is not None and len(output) < minimum:
        failures.append(f"output has {len(output)} chars; minimum is {minimum}")
    if maximum is not None and len(output) > maximum:
        failures.append(f"output has {len(output)} chars; maximum is {maximum}")
    return not failures, failures


def _find_case(evals: list[dict[str, Any]], eval_id: int) -> dict[str, Any]:
    for case in evals:
        if case["id"] == eval_id:
            return case
    raise ValueError(f"eval id {eval_id} not found")


def _print_cases(evals: list[dict[str, Any]]) -> None:
    print(f"market-research behavior evals ({len(evals)} total)")
    for case in evals:
        print(f"  [{case['id']}] {case['name']}: {case['prompt']}")


def _run_case(case: dict[str, Any], timeout: int) -> bool:
    prompt = NONINTERACTIVE_PREFIX + case["prompt"]
    print(f"RUN [{case['id']}] {case['name']}")
    try:
        result = subprocess.run(
            ["hermes", "chat", "-Q", "-q", prompt],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        print("FAIL: hermes CLI not found")
        return False
    except subprocess.TimeoutExpired:
        print(f"FAIL: hermes timed out after {timeout}s")
        return False
    output = result.stdout.strip()
    passed, failures = score_output(case, output)
    print(output)
    if result.stderr.strip():
        print(f"STDERR: {result.stderr.strip()}")
    if result.returncode != 0:
        failures.append(f"hermes exited with code {result.returncode}")
        passed = False
    if passed:
        print("PASS")
    else:
        for failure in failures:
            print(f"FAIL: {failure}")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true", help="validate eval schema and regex checks")
    parser.add_argument("--score-output", nargs=2, metavar=("ID", "FILE"))
    parser.add_argument("--run", help="run one eval ID or all through hermes")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    try:
        evals = load_evals()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        return 1
    errors = validate_evals(evals)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    if args.validate:
        print(f"PASS: {len(evals)} behavior evals have executable checks")
        return 0
    if args.score_output:
        eval_id = int(args.score_output[0])
        output_path = Path(args.score_output[1])
        try:
            case = _find_case(evals, eval_id)
            output = output_path.read_text(encoding="utf-8")
        except (OSError, ValueError) as exc:
            print(f"FAIL: {exc}")
            return 1
        passed, failures = score_output(case, output)
        if passed:
            print(f"PASS: output satisfies eval {eval_id}")
            return 0
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    if args.run:
        try:
            selected = evals if args.run == "all" else [_find_case(evals, int(args.run))]
        except ValueError as exc:
            print(f"FAIL: {exc}")
            return 1
        results = [_run_case(case, args.timeout) for case in selected]
        print(f"RESULT: {sum(results)}/{len(results)} passed")
        return 0 if all(results) else 1
    _print_cases(evals)
    return 0


if __name__ == "__main__":
    sys.exit(main())
