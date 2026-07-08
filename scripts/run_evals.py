#!/usr/bin/env python3
"""
Minimal eval runner for market-research skill.

Reads evals/evals.json and prints each eval prompt + expected behavior
so a human can manually test or a Hermes session can be invoked per prompt.

Usage:
  python3 scripts/run_evals.py               # list all evals
  python3 scripts/run_evals.py --run 1       # run eval 1 via hermes chat -q (if available)
  python3 scripts/run_evals.py --run all     # run all evals sequentially
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals" / "evals.json"


def load_evals() -> list[dict]:
    with EVALS.open(encoding="utf-8") as f:
        data = json.load(f)
    return data["evals"]


def list_evals(evals: list[dict]) -> None:
    print(f"market-research evals ({len(evals)} total)\n")
    for e in evals:
        print(f"  [{e['id']}] {e['name']}")
        print(f"        {e['prompt'][:80]}...")
        print(f"        assertions: {len(e['assertions'])}")
        print()


def run_single(evals: list[dict], eval_id: int) -> None:
    evals_by_id = {e["id"]: e for e in evals}
    if eval_id not in evals_by_id:
        print(f"FAIL: eval id {eval_id} not found")
        sys.exit(1)
    e = evals_by_id[eval_id]
    print(f"Running eval [{e['id']}]: {e['name']}")
    print(f"  Prompt: {e['prompt']}")
    print(f"  Expected: {e['expected_output']}")
    print(f"  Assertions: {e['assertions']}")
    print()
    try:
        result = subprocess.run(
            ["hermes", "chat", "-Q", "-q", e["prompt"]],
            capture_output=True,
            text=True,
            timeout=300,
        )
        print("=== HERMES OUTPUT ===")
        print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
        if result.stderr:
            print(f"=== STDERR ===\n{result.stderr}")
        print(f"=== EXIT CODE: {result.returncode} ===")
    except FileNotFoundError:
        print("SKIP: hermes CLI not found in PATH")
    except subprocess.TimeoutExpired:
        print("SKIP: hermes timed out after 300s")


def main() -> None:
    evals = load_evals()
    if "--run" in sys.argv:
        idx = sys.argv.index("--run")
        if idx + 1 >= len(sys.argv):
            print("FAIL: --run requires an argument (id or 'all')")
            sys.exit(1)
        target = sys.argv[idx + 1]
        if target == "all":
            for e in evals:
                run_single(evals, e["id"])
                print("\n---\n")
        else:
            run_single(evals, int(target))
    else:
        list_evals(evals)


if __name__ == "__main__":
    main()