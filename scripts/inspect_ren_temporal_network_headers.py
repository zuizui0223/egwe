from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import subprocess
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen

USER_AGENT = "egwe-ren-q2-header/1.0"
LOCKS = {
    "2_null_model_background_data.rar": {
        "url": "https://zenodo.org/records/6519751/files/2_null_model_background_data.rar?download=1",
        "md5": "40d028ed6a72d35e37d06b1b5240a72d",
        "members": [
            "2_null_model_background_data/pool.interactions.csv",
            "2_null_model_background_data/S48_network.csv",
        ],
    },
    "3_span_1CV.rar": {
        "url": "https://zenodo.org/records/6519751/files/3_span_1CV.rar?download=1",
        "md5": "6239f2eeebd4b7e7387cd6bde515c6ed",
        "members": [
            "3_span_1CV/all_ints_spatial.csv",
            "3_span_1CV/all_ints_temporal.csv",
            "3_span_1CV/ints_S_1CV_spatial.csv",
            "3_span_1CV/ints_S_1CV_temporal.csv",
        ],
    },
}


def _download(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/octet-stream,*/*"})
    with urlopen(req, timeout=180) as response:
        return response.read()


def _first_line(archive: Path, member: str) -> str:
    proc = subprocess.Popen(
        ["7z", "x", "-so", str(archive), member],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.stdout is not None
    raw = proc.stdout.readline(16384)
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=5)
    if not raw:
        stderr = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
        raise RuntimeError(f"no first line for {member}: {stderr}")
    return raw.decode("utf-8-sig", errors="strict").rstrip("\r\n")


def _parse_header(line: str) -> dict:
    # Source files use CSV naming and are inspected only at row 1 under the frozen Stage-A boundary.
    fields = next(csv.reader(io.StringIO(line)))
    fields = [str(x).strip() for x in fields]
    header_like = bool(fields) and all(field != "" for field in fields)
    return {"fields": fields, "header_like_nonempty": header_like}


def inspect(out_path: Path) -> dict:
    rows: list[dict] = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name, spec in LOCKS.items():
            payload = _download(spec["url"])
            observed = hashlib.md5(payload).hexdigest()
            if observed != spec["md5"]:
                raise RuntimeError(f"digest mismatch: {name}")
            archive = root / name
            archive.write_bytes(payload)
            members = []
            for member in spec["members"]:
                first = _first_line(archive, member)
                members.append({"member": member, **_parse_header(first)})
            rows.append({"archive": name, "md5": observed, "members": members})

    result = {
        "status": "header_only_inspection_complete",
        "files": rows,
        "inspection_boundary": (
            "Only row 1 of the six preregistered CSV members was read. No row 2+, interaction matrix cell, "
            "species persistence value, future interaction outcome, effect direction, fit, or score was read or computed."
        ),
        "decision_rule": (
            "Headers/source definitions must expose or unambiguously encode site, ordered time, plant, pollinator and year-specific edge state. "
            "If they do not, stop without reading data rows."
        ),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="artifacts/empirical/ren_temporal_network_headers.json")
    args = parser.parse_args()
    result = inspect(Path(args.out))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
