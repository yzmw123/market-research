#!/usr/bin/env python3
"""Validate the structured evidence contract used by market-research reports."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

SOURCE_ID = re.compile(r"^S[1-9]\d*$")
CLAIM_ID = re.compile(r"^C[1-9]\d*$")
SOURCE_TYPES = {"primary", "institutional", "secondary", "vendor", "community"}
CLAIM_TYPES = {"fact", "inference", "judgment", "recommendation"}
CONFIDENCE = {"high", "medium", "low"}


def _valid_date(value: Any) -> bool:
    if isinstance(value, date):
        return True
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _as_date(value: Any) -> date | None:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None


def _valid_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def load_evidence(path: str | Path) -> dict[str, Any]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("evidence root must be a YAML mapping")
    return data


def validate_evidence(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    research = data.get("research")
    if not isinstance(research, dict):
        errors.append("research must be a mapping")
        research = {}
    for key in ("question", "scope"):
        if not isinstance(research.get(key), str) or not research[key].strip():
            errors.append(f"research.{key} is required")
    for key in ("cutoff_date", "generated_at"):
        if not _valid_date(research.get(key)):
            errors.append(f"research.{key} must be an ISO date (YYYY-MM-DD)")
    cutoff_date = _as_date(research.get("cutoff_date"))
    generated_at = _as_date(research.get("generated_at"))
    if cutoff_date and generated_at and cutoff_date > generated_at:
        errors.append("research.cutoff_date cannot be after research.generated_at")

    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("sources must be a non-empty list")
        sources = []

    source_by_id: dict[str, dict[str, Any]] = {}
    for index, source in enumerate(sources):
        label = f"sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{label} must be a mapping")
            continue
        source_id = source.get("id")
        if not isinstance(source_id, str) or not SOURCE_ID.fullmatch(source_id):
            errors.append(f"{label}.id must match S1, S2, ...")
            continue
        if source_id in source_by_id:
            errors.append(f"duplicate source id: {source_id}")
        source_by_id[source_id] = source
        for key in ("title", "publisher", "independence_group"):
            if not isinstance(source.get(key), str) or not source[key].strip():
                errors.append(f"{source_id}.{key} is required")
        if not _valid_url(source.get("url")):
            errors.append(f"{source_id}.url must be an absolute HTTP(S) URL")
        published_at = source.get("published_at")
        if published_at is not None and not _valid_date(published_at):
            errors.append(f"{source_id}.published_at must be an ISO date or null")
        if not _valid_date(source.get("retrieved_at")):
            errors.append(f"{source_id}.retrieved_at must be an ISO date")
        published_date = _as_date(published_at)
        retrieved_date = _as_date(source.get("retrieved_at"))
        if published_date and retrieved_date and published_date > retrieved_date:
            errors.append(f"{source_id}.published_at cannot be after retrieved_at")
        if published_date and cutoff_date and published_date > cutoff_date:
            errors.append(f"{source_id}.published_at cannot be after research.cutoff_date")
        if retrieved_date and generated_at and retrieved_date > generated_at:
            errors.append(f"{source_id}.retrieved_at cannot be after research.generated_at")
        if source.get("source_type") not in SOURCE_TYPES:
            errors.append(f"{source_id}.source_type must be one of {sorted(SOURCE_TYPES)}")

    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("claims must be a non-empty list")
        claims = []

    claim_ids: set[str] = set()
    for index, claim in enumerate(claims):
        label = f"claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{label} must be a mapping")
            continue
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not CLAIM_ID.fullmatch(claim_id):
            errors.append(f"{label}.id must match C1, C2, ...")
            continue
        if claim_id in claim_ids:
            errors.append(f"duplicate claim id: {claim_id}")
        claim_ids.add(claim_id)
        if not isinstance(claim.get("statement"), str) or not claim["statement"].strip():
            errors.append(f"{claim_id}.statement is required")
        claim_type = claim.get("type")
        confidence = claim.get("confidence")
        if claim_type not in CLAIM_TYPES:
            errors.append(f"{claim_id}.type must be one of {sorted(CLAIM_TYPES)}")
        if confidence not in CONFIDENCE:
            errors.append(f"{claim_id}.confidence must be one of {sorted(CONFIDENCE)}")
        source_ids = claim.get("source_ids")
        if not isinstance(source_ids, list) or not source_ids:
            errors.append(f"{claim_id}.source_ids must be a non-empty list")
            source_ids = []
        elif len(source_ids) != len(set(source_ids)):
            errors.append(f"{claim_id}.source_ids must not contain duplicates")
        unknown = [source_id for source_id in source_ids if source_id not in source_by_id]
        if unknown:
            errors.append(f"{claim_id}.source_ids contains unknown ids: {unknown}")
        if claim_type in {"inference", "judgment", "recommendation"}:
            limitations = claim.get("limitations")
            if not isinstance(limitations, list) or not any(str(item).strip() for item in limitations):
                errors.append(f"{claim_id}.limitations is required for {claim_type}")
        if not isinstance(claim.get("decision_impact"), str) or not claim["decision_impact"].strip():
            errors.append(f"{claim_id}.decision_impact is required")
        if confidence == "high" and source_ids:
            referenced = [source_by_id[source_id] for source_id in source_ids if source_id in source_by_id]
            groups = {source.get("independence_group") for source in referenced}
            if len(groups) < 2:
                errors.append(f"{claim_id} high confidence requires two independent source groups")
            if not any(source.get("source_type") == "primary" for source in referenced):
                errors.append(f"{claim_id} high confidence requires at least one primary source")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    try:
        data = load_evidence(args.evidence)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"FAIL: {exc}")
        return 1
    errors = validate_evidence(data)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {args.evidence} satisfies the evidence contract")
    print(f"  sources: {len(data['sources'])}")
    print(f"  claims: {len(data['claims'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
