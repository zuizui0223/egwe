"""Inspect *only* archived CSV member names and first header lines for Brassica.

This is an outcome-blind source-schema gate. It does not open outcome values,
fit models, alter frozen protocols or turn a missing archive into a biology null.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import zipfile

DEFAULT_SOURCE = (
    "https://datadryad.org/api/v2/datasets/"
    "doi%3A10.5061%2Fdryad.tdz08kqdr/download"
)
MAX_BYTES = 25_000_000
MAX_NESTED_BYTES = 20_000_000
HEADER_FIELDS_TO_NOTE = ("site", "date", "doy", "batch", "id", "terr", "x", "y")
VISIT_KEYS = {
    "plantid", "plant_id", "plant", "plantnumber", "plant_number",
    "patch", "patchid", "patch_id", "subplots", "subplot", "quadrat",
    "terr", "territory", "x", "y", "donorid", "donor_id",
}


def fetch_public_zip(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "egwe-schema-only-source-gate/1.0"})
    with urlopen(request, timeout=50) as response:
        payload = response.read(MAX_BYTES + 1)
    if len(payload) > MAX_BYTES:
        raise ValueError("archive-exceeds-size-limit")
    return payload


def member_type(path: str) -> str | None:
    name = path.lower().replace("\\", "/")
    if not name.endswith(".csv"):
        return None
    if "pollinatorvisitationdatafiles/" in name:
        return "visitation"
    if "/phenotype data/brapap_" in name or "/phenotype_data/brapap_" in name:
        return "phenotype"
    if "/genetic data/brapag_" in name or "/genetic_data/brapag_" in name:
        return "genotype"
    if "/pedigree_assignment/pedigee_" in name:
        return "paternity"
    if name.endswith(("clump_coord.csv", "even_coord.csv")):
        return "coordinates"
    return None


def first_header(zipped: zipfile.ZipFile, member: zipfile.ZipInfo) -> list[str]:
    # Read a *single header line only*, never row-level biological measurements.
    with zipped.open(member) as raw:
        line = raw.readline(16384)
    if len(line) >= 16384:
        raise ValueError(f"overlong-header:{member.filename}")
    decoded = line.decode("utf-8-sig", errors="replace").rstrip("\r\n")
    dialect = csv.excel
    if ";" in decoded and decoded.count(";") > decoded.count(","):
        dialect = csv.excel
        return list(csv.reader([decoded], delimiter=";"))[0]
    return list(csv.reader([decoded], dialect=dialect))[0] if decoded else []


def inspect_archive(blob: bytes) -> dict:
    if not zipfile.is_zipfile(io.BytesIO(blob)):
        raise ValueError("download-not-zip")
    root_hash = hashlib.sha256(blob).hexdigest()
    with zipfile.ZipFile(io.BytesIO(blob)) as outer:
        archive = outer
        nested_blob: bytes | None = None
        inner_name: str | None = None
        zip_members = [m for m in outer.infolist() if not m.is_dir() and m.filename.lower().endswith(".zip")]
        target = [m for m in zip_members if "leventhal_et_al_2026.zip" in m.filename.lower()]
        if target:
            info = target[0]
            if info.file_size > MAX_NESTED_BYTES:
                raise ValueError("nested-archive-exceeds-size-limit")
            nested_blob = outer.read(info)
            inner_name = info.filename
            archive = zipfile.ZipFile(io.BytesIO(nested_blob))
        try:
            found = []
            for info in archive.infolist():
                kind = member_type(info.filename)
                if kind is None or info.is_dir():
                    continue
                found.append({
                    "path": info.filename,
                    "role": kind,
                    "header": first_header(archive, info),
                })
        finally:
            if nested_blob is not None:
                archive.close()

    visit = [entry for entry in found if entry["role"] == "visitation"]
    visit_columns = {name.lower().strip() for entry in visit for name in entry["header"]}
    return {
        "status": "RAW_HEADER_INDEX_OBTAINED",
        "raw_archive_sha256": root_hash,
        "archive_bytes": len(blob),
        "nested_member": inner_name,
        "member_count_by_role": {
            role: sum(entry["role"] == role for entry in found)
            for role in ("visitation", "phenotype", "genotype", "paternity", "coordinates")
        },
        "csv_headers": found,
        "visitation_has_plant_or_patch_key_by_column_name": bool(VISIT_KEYS & visit_columns),
        "possible_visitation_grain_fields": sorted(visit_columns & (VISIT_KEYS | set(HEADER_FIELDS_TO_NOTE))),
        "claim_ceiling": (
            "Columns only: IDs, temporal alignment, joins, independence and "
            "future prediction remain UNVERIFIED until separately gated."
        ),
        "outcome_values_opened": False,
    }


def run(source: str, offline_file: str | None) -> dict:
    try:
        blob = Path(offline_file).read_bytes() if offline_file else fetch_public_zip(source)
        result = inspect_archive(blob)
    except (HTTPError, URLError, OSError, ValueError, zipfile.BadZipFile) as exc:
        return {
            "status": "ACCESS_OR_SCHEMA_STOP",
            "error_type": type(exc).__name__,
            "error_detail": str(exc)[:240],
            "source": source,
            "outcome_values_opened": False,
            "claim_ceiling": "Not an ecological null or a verified dataset schema",
        }
    result["source"] = source
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=DEFAULT_SOURCE)
    parser.add_argument("--offline-zip", default=None)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = run(args.source, args.offline_zip)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("BRASSICA_SCHEMA_GATE " + json.dumps({
        "status": report["status"],
        "outcome_values_opened": report["outcome_values_opened"],
        "member_count_by_role": report.get("member_count_by_role"),
        "visitation_patch_key": report.get("visitation_has_plant_or_patch_key_by_column_name"),
        "error_type": report.get("error_type"),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
