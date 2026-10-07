from __future__ import annotations

import argparse
import csv
import hashlib
import json
import urllib.request
from collections import defaultdict
from datetime import datetime, time as dtime
from pathlib import Path
from zoneinfo import ZoneInfo

SOURCE_REPO = "robinm98/Spatial_Movement_Analysis"
SOURCE_REF = "main"
SOURCE_PATH = "Data/Ya Ha Tinda elk project, Banff National Park.csv"
SOURCE_BLOB_SHA = "2e67702781d73f8e0c018ecd4629c74c5662e424"
SOURCE_URL = (
    "https://raw.githubusercontent.com/robinm98/Spatial_Movement_Analysis/main/"
    "Data/Ya%20Ha%20Tinda%20elk%20project%2C%20Banff%20National%20Park.csv"
)
LOCAL_TZ = ZoneInfo("America/Edmonton")
REQUIRED = {"timestamp", "location-long", "location-lat", "individual-local-identifier"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(dest: Path) -> None:
    req = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "text/csv,*/*"},
    )
    with urllib.request.urlopen(req, timeout=900) as resp, dest.open("wb") as out:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)


def parse_timestamp(raw: str) -> datetime:
    value = raw.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(value)
    except ValueError:
        # Older Movebank exports often use M/D/YYYY H:M:S without a zone.
        for fmt in ("%m/%d/%Y %H:%M:%S", "%m/%d/%Y %H:%M"):
            try:
                dt = datetime.strptime(value, fmt)
                break
            except ValueError:
                continue
        else:
            raise
    # Diagnostic mirror only: the file is a direct Movebank-style export, but
    # timezone-naive timestamps are not authoritative enough for primary use.
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.astimezone(LOCAL_TZ)


def coverage(path: Path) -> dict:
    daily: dict[tuple[int, str], set[str]] = defaultdict(set)
    min_ts = None
    max_ts = None
    rows = 0
    ids = set()

    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fields = set(reader.fieldnames or [])
        missing = REQUIRED - fields
        if missing:
            raise RuntimeError(f"mirror missing required fields: {sorted(missing)}")

        for row in reader:
            rows += 1
            ident = (row.get("individual-local-identifier") or "").strip()
            if not ident:
                continue
            ids.add(ident)
            dt = parse_timestamp(row["timestamp"])
            if min_ts is None or dt < min_ts:
                min_ts = dt
            if max_ts is None or dt > max_ts:
                max_ts = dt
            md = (dt.month, dt.day)
            if not ((9, 15) <= md <= (11, 15)):
                continue
            noon = datetime.combine(dt.date(), dtime(12, 0), tzinfo=LOCAL_TZ)
            if abs((dt - noon).total_seconds()) / 3600.0 <= 6.5:
                daily[(dt.year, dt.date().isoformat())].add(ident)

    by_year: dict[int, list[int]] = defaultdict(list)
    for (year, _date), ids_day in daily.items():
        by_year[year].append(len(ids_day))

    years = []
    for year in sorted(by_year):
        counts = by_year[year]
        eligible = [n for n in counts if n >= 10]
        years.append({
            "year": year,
            "days_with_any_qualifying_fix": len(counts),
            "eligible_days_n_ge_10": len(eligible),
            "max_daily_individuals": max(counts),
            "mean_daily_individuals_on_eligible_days": (
                sum(eligible) / len(eligible) if eligible else None
            ),
            "eligible_year": len(eligible) >= 30,
        })

    eligible_years = [r["year"] for r in years if r["eligible_year"]]
    return {
        "status": "non_authoritative_public_mirror_coverage_diagnostic",
        "claim_boundary": (
            "Diagnostic only. This third-party GitHub mirror cannot replace the "
            "official Movebank DOI gate or authorize opening demographic outcomes."
        ),
        "source": {
            "repository": SOURCE_REPO,
            "ref": SOURCE_REF,
            "path": SOURCE_PATH,
            "blob_sha": SOURCE_BLOB_SHA,
            "downloaded_sha256": sha256(path),
        },
        "n_rows": rows,
        "n_unique_individuals": len(ids),
        "local_timestamp_min": min_ts.isoformat() if min_ts else None,
        "local_timestamp_max": max_ts.isoformat() if max_ts else None,
        "eligible_years": eligible_years,
        "n_eligible_years": len(eligible_years),
        "would_pass_primary_movement_gate_if_officially_confirmed": len(eligible_years) >= 11,
        "years": years,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ap.add_argument("--workdir", default="tmp/yht_public_mirror")
    args = ap.parse_args()
    work = Path(args.workdir)
    work.mkdir(parents=True, exist_ok=True)
    raw = work / "yht_mirror.csv"
    fetch(raw)
    out = coverage(raw)
    dest = Path(args.output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
