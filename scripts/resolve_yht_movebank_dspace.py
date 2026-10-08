#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from pathlib import Path

REPO = "https://datarepository.movebank.org"
DEFAULT_DOI = "10.5441/001/1.5g4h5t6c"


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "egwe-yht-movebank-dspace-resolver/1.0",
            "Accept": "application/json, application/hal+json",
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def link(payload: dict, name: str) -> str:
    value = payload.get("_links", {}).get(name, {})
    return str(value.get("href", "")) if isinstance(value, dict) else ""


def embedded(payload: dict, name: str) -> list[dict]:
    value = payload.get("_embedded", {}).get(name, [])
    return [x for x in value if isinstance(x, dict)] if isinstance(value, list) else []


def checksum(bitstream: dict) -> tuple[str, str]:
    value = bitstream.get("checkSum") or bitstream.get("checksum") or {}
    if not isinstance(value, dict):
        return "", ""
    return (
        str(value.get("checkSumAlgorithm") or value.get("algorithm") or ""),
        str(value.get("value") or ""),
    )


def resolve(doi: str) -> dict:
    doi = doi.lower()
    urls = [
        f"{REPO}/server/api/pid/find?id={urllib.parse.quote(doi, safe='')}",
        f"{REPO}/server/api/pid/find?id={urllib.parse.quote('https://doi.org/' + doi, safe='')}",
    ]

    item = None
    pid_url = None
    errors: list[str] = []
    for url in urls:
        try:
            candidate = fetch_json(url)
            if link(candidate, "bundles"):
                item = candidate
                pid_url = url
                break
            errors.append(f"{url}: resolved object has no bundles link")
        except Exception as exc:
            errors.append(f"{url}: {type(exc).__name__}: {exc}")

    if item is None:
        return {
            "status": "pid_resolution_failure",
            "doi": doi,
            "errors": errors,
            "bitstream_contents_fetched": False,
        }

    bundles = fetch_json(link(item, "bundles"))
    files: list[dict] = []
    for bundle in embedded(bundles, "bundles"):
        bundle_name = str(bundle.get("name") or "")
        bitstreams_url = link(bundle, "bitstreams")
        if not bitstreams_url:
            continue
        bitstreams = fetch_json(bitstreams_url)
        for bitstream in embedded(bitstreams, "bitstreams"):
            algorithm, digest = checksum(bitstream)
            files.append(
                {
                    "bundle_name": bundle_name,
                    "bitstream_id": str(bitstream.get("uuid") or bitstream.get("id") or ""),
                    "filename": str(bitstream.get("name") or ""),
                    "size_bytes": bitstream.get("sizeBytes"),
                    "checksum_type": algorithm,
                    "checksum": digest,
                    "content_url": link(bitstream, "content"),
                }
            )

    files.sort(key=lambda row: (row["bundle_name"], row["filename"]))
    originals = [row for row in files if row["bundle_name"] == "ORIGINAL"]
    csvs = [row for row in originals if row["filename"].lower().endswith(".csv")]
    plausible_event_csvs = []
    for row in csvs:
        name = row["filename"].lower()
        if any(token in name for token in (
            "reference-data",
            "reference_data",
            "-acc",
            "_acc",
            "annotated",
            "code",
        )):
            continue
        plausible_event_csvs.append(row)

    return {
        "status": "resolved",
        "doi": doi,
        "pid_url": pid_url,
        "item_uuid": str(item.get("uuid") or item.get("id") or ""),
        "item_name": str(item.get("name") or ""),
        "files": files,
        "original_files": originals,
        "original_csvs": csvs,
        "plausible_event_csvs": plausible_event_csvs,
        "event_csv_selection_rule": (
            "ORIGINAL CSV excluding reference-data/reference_data, -acc/_acc, "
            "annotated, and code filenames; inherited from the outcome-blind "
            "Movebank source inventory used in zuizui0223/batter"
        ),
        "event_csv_selection_gate": (
            "unique_candidate" if len(plausible_event_csvs) == 1
            else "ambiguous_or_missing_candidate"
        ),
        "bitstream_contents_fetched": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doi", default=DEFAULT_DOI)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = resolve(args.doi)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))

    if result["status"] != "resolved":
        raise SystemExit(2)
    if not result["original_files"]:
        raise SystemExit("resolved item has no ORIGINAL files")


if __name__ == "__main__":
    main()
