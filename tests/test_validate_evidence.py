from __future__ import annotations

import copy
from datetime import date
from pathlib import Path

from validate_evidence import load_evidence, validate_evidence

FIXTURE = Path(__file__).parent / "fixtures" / "sample-evidence.yaml"


def test_valid_evidence_contract() -> None:
    assert validate_evidence(load_evidence(FIXTURE)) == []


def test_yaml_native_dates_are_accepted() -> None:
    data = copy.deepcopy(load_evidence(FIXTURE))
    data["research"]["cutoff_date"] = date(2026, 7, 1)
    data["sources"][0]["published_at"] = date(2026, 1, 10)
    assert validate_evidence(data) == []


def test_unknown_published_date_is_accepted() -> None:
    data = copy.deepcopy(load_evidence(FIXTURE))
    data["sources"][0]["published_at"] = None
    assert validate_evidence(data) == []


def test_high_confidence_requires_independent_primary_evidence() -> None:
    data = copy.deepcopy(load_evidence(FIXTURE))
    data["sources"][0]["source_type"] = "secondary"
    data["sources"][1]["independence_group"] = data["sources"][0]["independence_group"]
    errors = validate_evidence(data)
    assert any("two independent source groups" in error for error in errors)
    assert any("at least one primary source" in error for error in errors)


def test_unknown_claim_source_is_rejected() -> None:
    data = copy.deepcopy(load_evidence(FIXTURE))
    data["claims"][0]["source_ids"] = ["S9"]
    assert any("unknown ids" in error for error in validate_evidence(data))


def test_impossible_evidence_chronology_is_rejected() -> None:
    data = copy.deepcopy(load_evidence(FIXTURE))
    data["sources"][0]["retrieved_at"] = "2026-07-14"
    errors = validate_evidence(data)
    assert any("after research.generated_at" in error for error in errors)
