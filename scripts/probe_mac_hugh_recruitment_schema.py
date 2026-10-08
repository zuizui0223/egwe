from __future__ import annotations

import csv
import hashlib
import io
import json
import urllib.parse
from pathlib import Path

from scripts.probe_mac_hugh_recruitment_code import PID, SERVER, get_bytes, get_json

TARGET = "Dataset_migration_routes_and_recruitment.txt"
EXPECTED_SOURCE_MD5 = "3ac1d2d5c7f64b182567829c0f2e28ac"
REQUIRED_SOURCE_FIELDS = {"Recrutement", "Variance_long", "Moyenne_long", "Nb_femelle"}
DATE_FIELD_CANDIDATES = {"year", "annee", "année", "an", "year_migration"}
OUT = Path("artifacts/mac_hugh_recruitment/schema_only.json")


def audit_schema(metadata: dict, raw: bytes) -> dict:
    if not raw:
        raise RuntimeError("empty source dataset")
    latest = metadata["data"]["latestVersion"]
    files = latest["files"]
    matches = [
        x["dataFile"]
        for x in files
        if (x.get("label") or x["dataFile"].get("filename")) == TARGET
    ]
    if len(matches) != 1 or matches[0].get("restricted"):
        raise RuntimeError("source table missing, ambiguous or restricted")
    record = matches[0]
    digest = hashlib.md5(raw).hexdigest()
    if digest != record["md5"] or digest != EXPECTED_SOURCE_MD5:
        raise RuntimeError("source table MD5 mismatch")

    # Parse only the header. Outcomes and covariate rows are neither decoded
    # into records nor returned: no endpoint evaluation in this schema gate.
    first = raw.splitlines()[0].decode("utf-8-sig")
    header = next(csv.reader(io.StringIO(first), delimiter="\t"))
    header = [h.strip() for h in header]
    if any(not h for h in header):
        raise RuntimeError("invalid empty column name")
    if len(header) != len(set(header)):
        raise RuntimeError("duplicate source column name")
    rows = sum(bool(x.strip()) for x in raw.splitlines()[1:])
    present = set(header)
    year_fields = [x for x in header if x.strip().casefold() in DATE_FIELD_CANDIDATES]
    required_present = REQUIRED_SOURCE_FIELDS.issubset(present)

    return {
        "status": "author_source_schema_only_no_outcome_values_opened",
        "source": PID,
        "version": latest.get("versionNumber"),
        "file_id": record["id"],
        "file_name": TARGET,
        "verified_md5": digest,
        "raw_row_count_not_independent_year_count": rows,
        "header": header,
        "required_source_fields_present": required_present,
        "candidate_time_field_names": year_fields,
        "recruitment_row_values_parsed": 0,
        "forecast_models_fitted": 0,
        "claim_ceiling": (
            "A schema and raw-row count audit only. The number of independent "
            "annual outcomes and later-fate temporal validation remain untested."
        ),
    }


def main() -> None:
    url = (
        f"{SERVER}/api/datasets/:persistentId/?"
        + urllib.parse.urlencode({"persistentId": PID})
    )
    meta = get_json(url)
    matches = [
        x["dataFile"]["id"]
        for x in meta["data"]["latestVersion"]["files"]
        if (x.get("label") or x["dataFile"].get("filename")) == TARGET
    ]
    if len(matches) != 1:
        raise RuntimeError("source target not uniquely identified")
    raw = get_bytes(f"{SERVER}/api/access/datafile/{matches[0]}")
    result = audit_schema(meta, raw)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
