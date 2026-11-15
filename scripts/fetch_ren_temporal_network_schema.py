from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen

USER_AGENT = "egwe-ren-q2-schema/1.0"

LOCKED_FILES = (
    {
        "name": "2_null_model_background_data.rar",
        "url": "https://zenodo.org/records/6519751/files/2_null_model_background_data.rar?download=1",
        "md5": "40d028ed6a72d35e37d06b1b5240a72d",
        "role": "primary_raw_network_and_source_code_package",
    },
    {
        "name": "3_span_1CV.rar",
        "url": "https://zenodo.org/records/6519751/files/3_span_1CV.rar?download=1",
        "md5": "6239f2eeebd4b7e7387cd6bde515c6ed",
        "role": "temporal_index_source_code_if_required",
    },
)


def _download(url: str) -> bytes:
    request = Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/octet-stream,*/*"},
    )
    with urlopen(request, timeout=180) as response:
        return response.read()


def _list_members(path: Path) -> list[str]:
    completed = subprocess.run(
        ["7z", "l", "-slt", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    members: list[str] = []
    for line in completed.stdout.splitlines():
        if not line.startswith("Path = "):
            continue
        value = line[len("Path = ") :].strip()
        if not value or value == path.name or value == str(path):
            continue
        members.append(value)
    return list(dict.fromkeys(members))


def discover(manifest_path: Path) -> dict:
    rows: list[dict] = []
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        for spec in LOCKED_FILES:
            payload = _download(str(spec["url"]))
            observed_md5 = hashlib.md5(payload).hexdigest()  # public archive digest verification
            if observed_md5 != spec["md5"]:
                raise RuntimeError(
                    f"MD5 mismatch for {spec['name']}: expected={spec['md5']} observed={observed_md5}"
                )
            path = root / str(spec["name"])
            path.write_bytes(payload)
            rows.append(
                {
                    "name": spec["name"],
                    "role": spec["role"],
                    "url": spec["url"],
                    "bytes": len(payload),
                    "md5": observed_md5,
                    "archive_members": _list_members(path),
                }
            )

    result = {
        "status": "archive_member_discovery_complete",
        "study_doi": "10.1111/ecog.06102",
        "dataset_doi": "10.5061/dryad.rv15dv484",
        "mirror_record": "https://zenodo.org/records/6519751",
        "files": rows,
        "inspection_boundary": (
            "Only public metadata, fixed archive bytes/digests, and archive member paths were inspected. "
            "No archived member was extracted; no source-code body, tabular header, matrix cell, interaction count, "
            "species persistence value, next-year outcome, effect direction, model fit, or score was read or computed."
        ),
        "next_gate": (
            "Use member names only to identify source-code and raw-network file roles. "
            "Any extraction step must remain response-blind and follow the preregistration before raw edge values are opened."
        ),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        default="artifacts/empirical/ren_temporal_network_schema.json",
    )
    args = parser.parse_args()
    result = discover(Path(args.manifest))
    print(
        json.dumps(
            {
                "status": result["status"],
                "files": {
                    row["name"]: row["archive_members"] for row in result["files"]
                },
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
