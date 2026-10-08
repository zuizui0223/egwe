from __future__ import annotations

import csv
import io
import json
import urllib.parse
import urllib.request
from pathlib import Path

from scripts.probe_mac_hugh_recruitment_code import PID, SERVER, UA, get_json

TARGET = "Dataset_RSF_1994-2019.txt"
EXPECTED_FILE_ID = 984868
EXPECTED_SOURCE_MD5_FROM_MANIFEST = "82900917b0d53024209540df9aea2845"
MAX_HEADER_BYTES = 64 * 1024
OUTPUT = Path("artifacts/mac_hugh_recruitment/rsf_iid_schema_gate.json")

# This is a strict data-availability audit, not imputation or invention of
# synchronous trajectories. Source names are preserved verbatim in output.
ID_CANDIDATES = {"id", "elkid", "animalid", "individual", "individual_id", "animal_id"}
DATE_TIME_CANDIDATES = {"timestamp", "datetime", "date_time", "dateheure", "date_heure", "time", "date", "heure"}
YEAR_CANDIDATES = {"year", "annee", "année"}
X_CANDIDATES = {"longitude", "long", "lon", "location-long", "location.long", "x", "easting"}
Y_CANDIDATES = {"latitude", "lat", "location-lat", "location.lat", "y", "northing"}


def inspect_manifest_and_header(metadata: dict, raw_header: bytes) -> dict:
    files = metadata["data"]["latestVersion"]["files"]
    matches = [
        entry["dataFile"]
        for entry in files
        if (entry.get("label") or entry["dataFile"].get("filename")) == TARGET
    ]
    if len(matches) != 1:
        raise RuntimeError(f"{TARGET} not uniquely present in official manifest")
    record = matches[0]
    if record["id"] != EXPECTED_FILE_ID or record.get("md5") != EXPECTED_SOURCE_MD5_FROM_MANIFEST:
        raise RuntimeError("official source id/manifest digest mismatch")
    if b"\n" not in raw_header and b"\r" not in raw_header:
        raise RuntimeError("source header exceeds probe limit / missing newline")

    first_line = raw_header.splitlines()[0].decode("utf-8-sig")
    if "\t" in first_line:
        delimiter = "\t"
    elif "," in first_line:
        delimiter = ","
    else:
        raise RuntimeError("unsupported source field delimiter")
    fields = [s.strip() for s in next(csv.reader(io.StringIO(first_line), delimiter=delimiter))]
    if len(fields) != len(set(fields)) or any(not x for x in fields):
        raise RuntimeError("empty/duplicate header fields")

    canonical = {name.lower(): name for name in fields}
    def subset(keys: set[str]) -> list[str]:
        return [canonical[key] for key in sorted(keys & set(canonical))]
    id_fields = subset(ID_CANDIDATES)
    clock_fields = subset(DATE_TIME_CANDIDATES)
    year_fields = subset(YEAR_CANDIDATES)
    x_fields = subset(X_CANDIDATES)
    y_fields = subset(Y_CANDIDATES)
    has_candidate_sync_schema = bool(id_fields and clock_fields and x_fields and y_fields)
    return {
        "status": "rsf_source_schema_only_no_event_or_recruitment_rows_opened",
        "source_doi": PID,
        "source_file": TARGET,
        "source_file_id": record["id"],
        "manifest_md5_not_full_byte_verified": record["md5"],
        "declared_file_size_bytes": record.get("filesize"),
        "columns": fields,
        "delimiter": "tab" if delimiter == "\t" else "comma",
        "id_field_candidates": id_fields,
        "clock_field_candidates": clock_fields,
        "year_field_candidates": year_fields,
        "x_field_candidates": x_fields,
        "y_field_candidates": y_fields,
        "possible_same_time_IID_reconstruction": has_candidate_sync_schema,
        "source_data_rows_parsed": 0,
        "source_outcome_rows_parsed": 0,
        "claim_ceiling": (
            "This tests only the possibility of synchronous positional data from field names. "
            "Even a positive result would require independent validation of actual clock/ID "
            "resolution and yearwise sampling before Love-Otto IID CV is computable."
        ),
    }


def main() -> None:
    metadata = get_json(
        f"{SERVER}/api/datasets/:persistentId/?"
        + urllib.parse.urlencode({"persistentId": PID})
    )
    req = urllib.request.Request(
        f"{SERVER}/api/access/datafile/{EXPECTED_FILE_ID}",
        headers={"User-Agent": UA, "Accept": "text/plain", "Range": f"bytes=0-{MAX_HEADER_BYTES - 1}"},
    )
    with urllib.request.urlopen(req, timeout=180) as response:
        line = response.readline(MAX_HEADER_BYTES)
    result = inspect_manifest_and_header(metadata, line)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
