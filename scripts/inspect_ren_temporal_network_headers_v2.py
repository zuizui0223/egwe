from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import shlex
import subprocess
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen

USER_AGENT = "egwe-ren-q2-header-v2/1.0"
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
    # `head -n 1` is the firewall: the Python process receives only row 1.
    cmd = (
        f"7z x -so {shlex.quote(str(archive))} {shlex.quote(member)} 2>/dev/null "
        "| head -n 1"
    )
    completed = subprocess.run(
        ["bash", "-lc", cmd],
        check=True,
        capture_output=True,
        timeout=30,
    )
    raw = completed.stdout
    if not raw:
        raise RuntimeError(f"no first row returned for {member}")
    if raw.count(b"\n") > 1:
        raise RuntimeError(f"row firewall failed for {member}")
    return raw.decode("utf-8-sig", errors="strict").rstrip("\r\n")


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
            members: list[dict] = []
            for member in spec["members"]:
                first = _first_line(archive, member)
                fields = [str(v).strip() for v in next(csv.reader(io.StringIO(first)))]
                members.append({"member": member, "row1_fields": fields})
            rows.append({"archive": name, "md5": observed, "members": members})

    result = {
        "status": "header_only_inspection_complete",
        "files": rows,
        "inspection_boundary": (
            "The extraction pipeline delivered only row 1 from each of the six preregistered CSV members. "
            "No row 2+, interaction value, persistence value, future outcome, effect direction, fit, or score was read by Python."
        ),
        "decision_rule": (
            "Proceed only if row-1 fields plus source definitions identify site, ordered time, plant, pollinator and year-specific edge state."
        ),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="artifacts/empirical/ren_temporal_network_headers_v2.json")
    args = parser.parse_args()
    result = inspect(Path(args.out))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
