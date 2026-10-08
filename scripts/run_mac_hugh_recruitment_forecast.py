from __future__ import annotations

import hashlib
import json
import urllib.parse
from pathlib import Path

from scripts.probe_mac_hugh_recruitment_code import PID, SERVER, get_bytes, get_json
from scripts.probe_mac_hugh_recruitment_schema import EXPECTED_SOURCE_MD5, TARGET, audit_schema
from eco_genetic_warning_extensions.mac_hugh_recruitment_forecast import audit_forecasts

OUT = Path("artifacts/mac_hugh_recruitment/temporal_result.json")


def main() -> None:
    meta = get_json(
        f"{SERVER}/api/datasets/:persistentId/?"
        + urllib.parse.urlencode({"persistentId": PID})
    )
    matching = [
        x["dataFile"]["id"]
        for x in meta["data"]["latestVersion"]["files"]
        if (x.get("label") or x["dataFile"].get("filename")) == TARGET
    ]
    if len(matching) != 1:
        raise RuntimeError("published source table was not uniquely identified")
    raw = get_bytes(f"{SERVER}/api/access/datafile/{matching[0]}")
    if hashlib.md5(raw).hexdigest() != EXPECTED_SOURCE_MD5:
        raise RuntimeError("published source table MD5 changed")
    schema = audit_schema(meta, raw)
    if not schema["required_source_fields_present"] or schema["candidate_time_field_names"] != ["Annee"]:
        raise RuntimeError("frozen source schema unexpectedly changed")

    result = audit_forecasts(raw.decode("utf-8-sig"))
    result["source_file_id"] = matching[0]
    result["source_md5"] = EXPECTED_SOURCE_MD5
    result["analysis_contract"] = "experiments/mac_hugh_recruitment_temporal_protocol.json"
    result["analysis_contract_frozen_before_outcomes"] = True
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
