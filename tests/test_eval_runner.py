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


def test_sales_eval_scores_observable_behavior_not_internal_skill_name() -> None:
    case = next(case for case in load_evals() if case["id"] == 8)
    output = """在准备之前，请集中确认以下信息：
1. 哪家能源集团或具体客户单位？
2. 拜访目的，是初次见面、方案沟通还是需求调研？
3. 对方已知的数字化方向或业务痛点是什么？
确认后将准备近期动态、聊天话题和销售话术。"""
    assert score_output(case, output)[0]
