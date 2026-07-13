from __future__ import annotations

from run_evals import load_evals, score_output, validate_evals


def test_behavior_evals_have_executable_checks() -> None:
    evals = load_evals()
    assert validate_evals(evals) == []
    assert len(evals) >= 8


def test_scorer_returns_actionable_failures() -> None:
    case = {
        "checks": {
            "must_match": ["证据"],
            "must_not_match": ["编造"],
            "min_chars": 4,
        }
    }
    assert score_output(case, "证据地图")[0]
    passed, failures = score_output(case, "编造答案")
    assert not passed
    assert len(failures) == 2
