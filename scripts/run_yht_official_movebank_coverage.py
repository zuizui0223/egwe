from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import defaultdict
from datetime import datetime, time as dtime
from pathlib import Path
from zoneinfo import ZoneInfo

API = "https://datarepository.movebank.org/server/api"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
DOI = "10.5441/001/1.5g4h5t6c"
LOCAL_TZ = ZoneInfo("America/Edmonton")
REQUIRED = {"timestamp", "location-long", "location-lat", "individual-local-identifier"}


def get(url: str, accept: str = "application/json", retries: int = 5) -> bytes:
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
            with urllib.request.urlopen(req, timeout=900) as resp:
                return resp.read()
        except (urllib.error.URLError, ConnectionResetError, TimeoutError):
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
    raise AssertionError("unreachable")


def get_json(path: str, **params) -> dict:
    qs = urllib.parse.urlencode(params)
    return json.loads(get(f"{API}/{path}?{qs}").decode("utf-8"))


def meta(item: dict, key: str) -> list[str]:
    return [v["value"] for v in item.get("metadata", {}).get(key, [])]


def resolve_doi(doi: str) -> dict:
    page = get_json("discover/search/objects", query=f'"{doi}"', size=10, dsoType="item")
    objects = page["_embedded"]["searchResult"]["_embedded"]["objects"]
    for obj in objects:
        item = obj["_embedded"]["indexableObject"]
        if doi in meta(item, "dc.identifier.doi"):
            return item
    raise RuntimeError(f"DOI not found: {doi}")


def original_bitstreams(item: dict) -> list[dict]:
    bundles = get_json(f"core/items/{item['uuid']}/bundles")["_embedded"]["bundles"]
    out: list[dict] = []
    for bundle in bundles:
        if bundle["name"] != "ORIGINAL":
            continue
        out.extend(get_json(f"core/bundles/{bundle['uuid']}/bitstreams")["_embedded"]["bitstreams"])
    return out


def safe_extract(zpath: Path, out_dir: Path) -> list[Path]:
    extracted: list[Path] = []
    with zipfile.ZipFile(zpath) as zf:
        for member in zf.namelist():
            if member.startswith("__MACOSX/"):
                continue
            target = (out_dir / member).resolve()
            if not str(target).startswith(str(out_dir.resolve())):
                raise RuntimeError(f"unsafe zip member: {member}")
            zf.extract(member, out_dir)
            if target.is_file():
                extracted.append(target)
    return extracted


def parse_movebank_timestamp(raw: str) -> datetime:
    value = raw.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    # Movebank's canonical timestamp field is UTC. This assumption is allowed only
    # for data obtained directly from the official Movebank Data Repository.
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.astimezone(LOCAL_TZ)


def coverage(csv_path: Path) -> dict:
    daily: dict[tuple[int, str], set[str]] = defaultdict(set)
    with csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fields = set(reader.fieldnames or [])
        missing = REQUIRED - fields
        if missing:
            raise RuntimeError(f"missing required Movebank columns: {sorted(missing)}")
        for row in reader:
            ident = (row.get("individual-local-identifier") or "").strip()
            if not ident:
                continue
            dt = parse_movebank_timestamp(row["timestamp"])
            md = (dt.month, dt.day)
            if not ((9, 15) <= md <= (11, 15)):
                continue
            noon = datetime.combine(dt.date(), dtime(12, 0), tzinfo=LOCAL_TZ)
            offset_h = abs((dt - noon).total_seconds()) / 3600.0
            if offset_h <= 6.5:
                daily[(dt.year, dt.date().isoformat())].add(ident)

    by_year: dict[int, list[int]] = defaultdict(list)
    for (year, _date), ids in daily.items():
        by_year[year].append(len(ids))

    years = []
    for year in sorted(by_year):
        counts = by_year[year]
        eligible = [n for n in counts if n >= 10]
        years.append({
            "year": year,
            "days_in_window_with_any_qualifying_fix": len(counts),
            "eligible_days_n_ge_10": len(eligible),
            "max_daily_individuals": max(counts),
            "mean_daily_individuals_on_eligible_days": (
                sum(eligible) / len(eligible) if eligible else None
            ),
            "eligible_year": len(eligible) >= 30,
        })
    eligible_years = [x["year"] for x in years if x["eligible_year"]]
    return {
        "status": "official_movebank_movement_only_coverage_gate",
        "eligible_years": eligible_years,
        "n_eligible_years": len(eligible_years),
        "primary_temporal_replication_gate_passed": len(eligible_years) >= 11,
        "years": years,
    }


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ap.add_argument("--workdir", default="tmp/yht_movebank")
    args = ap.parse_args()

    work = Path(args.workdir)
    work.mkdir(parents=True, exist_ok=True)

    item = resolve_doi(DOI)
    files = original_bitstreams(item)
    manifest = [{
        "uuid": f["uuid"], "name": f["name"], "sizeBytes": f["sizeBytes"]
    } for f in files]

    downloaded: list[Path] = []
    for rec in files:
        name = rec["name"]
        if not name.lower().endswith((".csv", ".zip")):
            continue
        target = work / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(get(f"{API}/core/bitstreams/{rec['uuid']}/content", accept="*/*"))
        downloaded.append(target)

    candidates = list(downloaded)
    for path in list(downloaded):
        if path.suffix.lower() == ".zip":
            candidates.extend(safe_extract(path, work))

    csv_candidates: list[Path] = []
    for path in candidates:
        if path.suffix.lower() != ".csv":
            continue
        try:
            with path.open("r", encoding="utf-8-sig", newline="") as fh:
                header = set(next(csv.reader(fh)))
            if REQUIRED <= header:
                csv_candidates.append(path)
        except Exception:
            continue

    if len(csv_candidates) != 1:
        raise RuntimeError(
            f"expected exactly one official Movebank event CSV with required columns; "
            f"found {[str(x) for x in csv_candidates]}"
        )

    source = csv_candidates[0]
    result = coverage(source)
    result["source"] = {
        "doi": DOI,
        "item_uuid": item["uuid"],
        "title": meta(item, "dc.title"),
        "rights": meta(item, "dc.rights"),
        "animal_count": meta(item, "mdr.animal.count"),
        "location_count": meta(item, "mdr.location.count"),
        "original_bitstreams": manifest,
        "selected_event_file": source.name,
        "selected_event_file_sha256": sha256(source),
        "raw_locations_not_persisted_as_workflow_artifact": True,
    }
    dest = Path(args.output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
