from __future__ import annotations

import csv
import io
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict
from pathlib import Path
from typing import Any

from eco_genetic_warning_extensions.yht_spatial_warning_coverage import (
    coverage_from_rows,
)

STUDY_ID = 897981076
SENSOR_TYPE_ID = 653
BASE = "https://www.movebank.org/movebank/service/direct-read"
CANDIDATE_YEARS = [2004, 2005, 2006, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
USER_AGENT = "egwe-yht-public-probe/1.0 (+https://github.com/zuizui0223/egwe)"


class AccessBoundary(RuntimeError):
    def __init__(self, status: str, detail: str) -> None:
        super().__init__(detail)
        self.status = status
        self.detail = detail


def _get(url: str, timeout: int = 120) -> tuple[int, str, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return (
                int(getattr(response, "status", 200)),
                str(response.headers.get("Content-Type", "")),
                response.read(),
            )
    except urllib.error.HTTPError as exc:
        body = exc.read() if exc.fp is not None else b""
        return int(exc.code), str(exc.headers.get("Content-Type", "")), body


def _looks_like_license_gate(body: bytes, content_type: str) -> bool:
    text = body[:100_000].decode("utf-8", errors="replace").casefold()
    return (
        "license terms" in text
        or "licence terms" in text
        or "license-md5" in text
        or ("text/html" in content_type.casefold() and "<html" in text)
    )


def _study_probe() -> dict[str, Any]:
    query = urllib.parse.urlencode(
        {
            "entity_type": "study",
            "study_id": STUDY_ID,
        }
    )
    status, content_type, body = _get(f"{BASE}?{query}", timeout=60)
    out: dict[str, Any] = {
        "http_status": status,
        "content_type": content_type,
        "bytes": len(body),
    }
    if status != 200:
        out["status"] = "study_metadata_http_error"
        out["body_prefix"] = body[:1000].decode("utf-8", errors="replace")
        return out
    if _looks_like_license_gate(body, content_type):
        out["status"] = "license_acceptance_required_or_html_gate"
        out["body_prefix"] = body[:1000].decode("utf-8", errors="replace")
        return out

    text = body.decode("utf-8-sig", errors="strict")
    rows = list(csv.DictReader(io.StringIO(text)))
    out["status"] = "study_metadata_csv_received"
    out["row_count"] = len(rows)
    if rows:
        keep = (
            "id",
            "name",
            "license_type",
            "suspend_license_terms",
            "i_can_see_data",
            "i_have_download_access",
            "number_of_individuals",
            "number_of_deployed_locations",
            "timestamp_first_deployed_location",
            "timestamp_last_deployed_location",
        )
        out["selected_fields"] = {k: rows[0].get(k) for k in keep if k in rows[0]}
    return out


def _event_url(year: int) -> str:
    # Deliberately request a slightly wider UTC interval than the local Sep15-Nov15
    # window. The frozen coverage function converts UTC to America/Edmonton and
    # applies the exact local-date window afterward.
    params = {
        "entity_type": "event",
        "study_id": STUDY_ID,
        "sensor_type_id": SENSOR_TYPE_ID,
        "timestamp_start": f"{year}0914000000000",
        "timestamp_end": f"{year}1118000000000",
        "attributes": (
            "individual_local_identifier,timestamp,location_long,"
            "location_lat,visible"
        ),
    }
    return f"{BASE}?{urllib.parse.urlencode(params)}"


def _fetch_year(year: int) -> tuple[list[dict[str, str]], dict[str, Any]]:
    status, content_type, body = _get(_event_url(year))
    meta: dict[str, Any] = {
        "year": year,
        "http_status": status,
        "content_type": content_type,
        "bytes": len(body),
    }
    if status in (401, 403):
        raise AccessBoundary(
            "anonymous_access_blocked",
            f"year={year} HTTP {status}",
        )
    if status != 200:
        raise AccessBoundary(
            "event_http_error",
            f"year={year} HTTP {status}: {body[:500]!r}",
        )
    if _looks_like_license_gate(body, content_type):
        raise AccessBoundary(
            "license_acceptance_required",
            f"year={year} returned licence/HTML gate; no acceptance attempted",
        )

    text = body.decode("utf-8-sig", errors="strict")
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        meta["raw_rows"] = 0
        return [], meta

    required = {
        "individual_local_identifier",
        "timestamp",
        "location_long",
        "location_lat",
        "visible",
    }
    missing = required - set(rows[0])
    if missing:
        raise AccessBoundary(
            "canonical_event_schema_incomplete",
            f"year={year} missing columns: {sorted(missing)}",
        )

    cleaned: list[dict[str, str]] = []
    invisible = 0
    missing_coordinate = 0
    for row in rows:
        visible = str(row.get("visible", "")).strip().casefold()
        if visible in {"false", "f", "0", "no"}:
            invisible += 1
            continue
        if visible not in {"true", "t", "1", "yes"}:
            raise AccessBoundary(
                "visible_flag_unparseable",
                f"year={year} encountered visible={row.get('visible')!r}",
            )
        lon = str(row.get("location_long", "")).strip()
        lat = str(row.get("location_lat", "")).strip()
        if not lon or not lat:
            missing_coordinate += 1
            continue

        ts = str(row["timestamp"]).strip()
        # Movebank API documentation: all dates are stored in UTC. direct-read
        # renders UTC timestamps without an explicit suffix, so make the
        # timezone semantics explicit before the frozen coverage function.
        if ts.endswith("Z") or "+" in ts[10:] or ts.endswith(" UTC"):
            normalized = ts.replace(" UTC", "+00:00")
        else:
            normalized = ts.replace(" ", "T", 1) + "+00:00"
        cleaned.append(
            {
                "timestamp": normalized,
                "individual_local_identifier": str(row["individual_local_identifier"]).strip(),
                "location_long": lon,
                "location_lat": lat,
            }
        )

    meta.update(
        {
            "raw_rows": len(rows),
            "visible_rows_with_coordinates": len(cleaned),
            "owner_flagged_invisible_rows": invisible,
            "visible_rows_missing_coordinates": missing_coordinate,
        }
    )
    return cleaned, meta


def run() -> dict[str, Any]:
    study = _study_probe()
    if study.get("status") == "license_acceptance_required_or_html_gate":
        return {
            "status": "license_acceptance_required",
            "study": study,
            "candidate_years": CANDIDATE_YEARS,
            "demographic_outcomes_opened": False,
            "license_acceptance_attempted": False,
        }

    all_rows: list[dict[str, str]] = []
    yearly_fetch: list[dict[str, Any]] = []
    try:
        for year in CANDIDATE_YEARS:
            rows, meta = _fetch_year(year)
            all_rows.extend(rows)
            yearly_fetch.append(meta)
    except AccessBoundary as exc:
        return {
            "status": exc.status,
            "detail": exc.detail,
            "study": study,
            "yearly_fetch": yearly_fetch,
            "candidate_years": CANDIDATE_YEARS,
            "demographic_outcomes_opened": False,
            "license_acceptance_attempted": False,
        }

    coverage = coverage_from_rows(
        all_rows,
        timestamp_col="timestamp",
        individual_col="individual_local_identifier",
    )
    return {
        "status": "anonymous_public_events_received_and_movement_coverage_evaluated",
        "study": study,
        "yearly_fetch": yearly_fetch,
        "candidate_years": CANDIDATE_YEARS,
        "coverage": coverage,
        "demographic_outcomes_opened": False,
        "license_acceptance_attempted": False,
        "raw_events_redistributed": False,
    }


def main() -> None:
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "artifacts/yht_movebank_public_probe/probe_summary.json"
    )
    result = run()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
