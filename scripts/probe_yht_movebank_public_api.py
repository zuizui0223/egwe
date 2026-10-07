from __future__ import annotations

import csv
import hashlib
import io
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

STUDY_ID = "897981076"
BASE = "https://www.movebank.org/movebank/service/direct-read"


def fetch(url: str, max_bytes: int = 2_000_000) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "egwe-yht-public-api-probe/1.0",
            "Accept": "text/csv,text/plain,application/json,text/html;q=0.5,*/*;q=0.1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read(max_bytes + 1)
            truncated = len(body) > max_bytes
            if truncated:
                body = body[:max_bytes]
            return {
                "ok": 200 <= response.status < 300,
                "status": response.status,
                "content_type": response.headers.get("Content-Type"),
                "bytes_captured": len(body),
                "truncated": truncated,
                "sha256_captured": hashlib.sha256(body).hexdigest(),
                "text": body.decode("utf-8", errors="replace"),
                "url": url,
            }
    except urllib.error.HTTPError as exc:
        body = exc.read(max_bytes)
        return {
            "ok": False,
            "status": exc.code,
            "content_type": exc.headers.get("Content-Type"),
            "bytes_captured": len(body),
            "truncated": False,
            "sha256_captured": hashlib.sha256(body).hexdigest(),
            "text": body.decode("utf-8", errors="replace"),
            "url": url,
        }
    except Exception as exc:
        return {
            "ok": False,
            "status": None,
            "content_type": None,
            "bytes_captured": 0,
            "truncated": False,
            "sha256_captured": None,
            "text": "",
            "url": url,
            "error": f"{type(exc).__name__}: {exc}",
        }


def summarize_csv(result: dict[str, Any]) -> dict[str, Any]:
    text = result.get("text", "")
    lines = [line for line in text.splitlines() if line.strip()]
    out = {k: result.get(k) for k in (
        "ok", "status", "content_type", "bytes_captured", "truncated",
        "sha256_captured", "url", "error"
    ) if k in result}
    out["looks_like_license_html"] = (
        "<html" in text.casefold()
        or "license terms" in text.casefold()
        or "accept" in text.casefold() and "license" in text.casefold()
    )
    if lines and not out["looks_like_license_html"]:
        try:
            rows = list(csv.reader(io.StringIO(text)))
            out["header"] = rows[0] if rows else []
            out["rows_captured"] = max(0, len(rows) - 1)
            out["first_data_row"] = rows[1] if len(rows) > 1 else None
        except Exception as exc:
            out["csv_parse_error"] = f"{type(exc).__name__}: {exc}"
    return out


def main() -> None:
    queries = {
        "study": {
            "entity_type": "study",
            "study_id": STUDY_ID,
        },
        "individuals": {
            "entity_type": "individual",
            "study_id": STUDY_ID,
        },
        "events_2024_09_15": {
            "entity_type": "event",
            "study_id": STUDY_ID,
            "sensor_type_id": "653",
            "timestamp_start": "20240915000000000",
            "timestamp_end": "20240916000000000",
            "attributes": "individual_local_identifier,timestamp,location_long,location_lat,visible",
        },
    }

    summary: dict[str, Any] = {
        "probe_id": "yht_movebank_public_api_probe_v1",
        "study_id": STUDY_ID,
        "status": "public_api_acquisition_probe_no_demographic_outcomes",
        "requests": {},
    }

    for name, params in queries.items():
        url = BASE + "?" + urllib.parse.urlencode(params, safe=",")
        summary["requests"][name] = summarize_csv(fetch(url))

    study = summary["requests"]["study"]
    inds = summary["requests"]["individuals"]
    ev = summary["requests"]["events_2024_09_15"]
    summary["decision"] = {
        "study_metadata_public_without_login": bool(study.get("ok") and not study.get("looks_like_license_html")),
        "individual_metadata_public_without_login": bool(inds.get("ok") and not inds.get("looks_like_license_html")),
        "event_data_public_without_login": bool(ev.get("ok") and not ev.get("looks_like_license_html") and ev.get("rows_captured", 0) > 0),
        "license_gate_detected": any(
            x.get("looks_like_license_html", False)
            for x in (study, inds, ev)
        ),
    }

    # Do not persist license text or raw event coordinates in the compact probe.
    for entry in summary["requests"].values():
        entry.pop("text", None)
        if entry.get("first_data_row") is not None:
            entry["first_data_row"] = ["<redacted>" for _ in entry["first_data_row"]]

    out = Path("artifacts/yht_spatial_warning/movebank_public_api_probe.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary["decision"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
