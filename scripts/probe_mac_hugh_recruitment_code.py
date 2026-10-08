from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

SERVER = "https://borealisdata.ca"
PID = "doi:10.5683/SP3/0ROESU"
TARGET = "Analyses_Recruitment.R"
UA = "egwe-mac-hugh-code-probe/1.0 (+https://github.com/zuizui0223/egwe)"


def get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def get_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def main() -> None:
    meta_url = (
        f"{SERVER}/api/datasets/:persistentId/?"
        + urllib.parse.urlencode({"persistentId": PID})
    )
    meta = get_json(meta_url)
    latest = meta["data"]["latestVersion"]
    files = latest["files"]

    manifest = []
    target_id = None
    for item in files:
        df = item["dataFile"]
        label = item.get("label") or df.get("filename")
        manifest.append({
            "id": df["id"],
            "label": label,
            "contentType": df.get("contentType"),
            "filesize": df.get("filesize"),
            "md5": df.get("md5"),
            "restricted": item.get("restricted", False),
        })
        if label == TARGET:
            target_id = df["id"]

    if target_id is None:
        raise RuntimeError(f"{TARGET!r} not found in dataset manifest")

    code = get_bytes(f"{SERVER}/api/access/datafile/{target_id}").decode("utf-8-sig")

    out = {
        "status": "author_recruitment_code_recovered_before_data_rows",
        "dataset_pid": PID,
        "dataset_version": latest.get("versionNumber"),
        "license": latest.get("license", {}),
        "file_manifest": manifest,
        "target_file_id": target_id,
        "target_file": TARGET,
        "recruitment_code": code,
        "data_rows_opened": False,
    }
    dest = Path("artifacts/mac_hugh_recruitment/code_probe.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(code)


if __name__ == "__main__":
    main()
