"""Fail-closed metadata-only admissibility audit for natural relational-state transfer.

No source downloads or outcomes are opened. A 'pass' is only valid when raw
archive bytes, patch-matched interaction and genetic states, forward function,
temporal joins and independent validation units have all been verified.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "artifacts/empirical/relational_source_scout_20261008.json"
REQUIRED = (
    "raw_bytes_inspected",
    "same_unit_genetic_or_parentage",
    "patch_resolved_effective_interaction",
    "patch_relational_join_verified",
    "subsequent_functional_endpoint",
    "forward_time_alignment_verified",
    "independent_holdout_units_verified",
)
VALID = {"pass", "fail", "unknown"}


def validate_registry(registry: dict) -> dict:
    assert registry["schema_version"] == 1
    assert tuple(registry["criterion_keys"]) == REQUIRED
    ids: set[str] = set()
    confirmed: list[str] = []
    holds: dict[str, list[str]] = {}

    for record in registry["records"]:
        identifier = record["id"]
        assert identifier and identifier not in ids, f"duplicate/empty source: {identifier}"
        ids.add(identifier)
        assert record.get("source_doi") or record.get("source_dois") or record.get("source_url")
        gates = record["gates"]
        assert set(gates) == set(REQUIRED), f"wrong gate keys: {identifier}"
        assert all(value in VALID for value in gates.values()), f"invalid gate: {identifier}"
        complete = all(gates[field] == "pass" for field in REQUIRED)
        if complete:
            confirmed.append(identifier)
            assert record["full_HR_classification"] == "ELIGIBLE_FULL_HR"
        else:
            assert record["full_HR_classification"] != "ELIGIBLE_FULL_HR"
            holds[identifier] = [key for key in REQUIRED if gates[key] != "pass"]

    assert len(confirmed) == registry["primary_full_HR_confirmed_count"], (
        "declared eligible-count does not match independent gate computation"
    )
    return {
        "metadata_screened": len(registry["records"]),
        "raw_archives_verified": sum(
            record["gates"]["raw_bytes_inspected"] == "pass"
            for record in registry["records"]
        ),
        "full_HR_confirmed": len(confirmed),
        "confirmed_ids": confirmed,
        "not_yet_passed_gates": holds,
    }


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    result = validate_registry(registry)
    print("RELATIONAL_SOURCE_GATE " + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
