from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path

PRIMARY = "YHT_CalfCowRatioData.csv"
EXPECTED_FILES = {
    "YHT_AdultFemaleSurvivalDataRaw.csv",
    "YHT_AdultFemaleSurvivalRate.csv",
    "YHT_CalfCowRatioData.csv",
    "YHT_CowCalfObsData.csv",
    "YHT_MinimumCountWinterElkSurveys.csv",
    "YHT_PregnancyRate.csv",
}


def audit(zip_path: str | Path) -> dict:
    path = Path(zip_path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with zipfile.ZipFile(path) as zf:
        names = [name for name in zf.namelist() if not name.endswith("/")]
        basenames = {Path(name).name for name in names}
        missing = sorted(EXPECTED_FILES - basenames)
        if missing:
            raise RuntimeError(f"official Dryad bundle missing expected files: {missing}")
        matches = [name for name in names if Path(name).name == PRIMARY]
        if len(matches) != 1:
            raise RuntimeError(f"expected exactly one {PRIMARY}, found {matches}")
        with zf.open(matches[0]) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
            reader = csv.reader(text)
            try:
                header = next(reader)
            except StopIteration as exc:
                raise RuntimeError(f"{PRIMARY} is empty") from exc

    if not header or any(not str(x).strip() for x in header):
        raise RuntimeError("primary demographic CSV has an empty/invalid header")
    return {
        "status": "schema_only_no_outcome_rows_parsed",
        "source": "Dryad DOI 10.5061/dryad.6wwpzgmw7",
        "bundle_sha256": digest,
        "expected_file_basenames": sorted(EXPECTED_FILES),
        "primary_file": PRIMARY,
        "primary_header": header,
        "outcome_rows_parsed": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Schema-only audit of the official Ya Ha Tinda Dryad bundle."
    )
    parser.add_argument("--zip", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = audit(args.zip)
    dest = Path(args.output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
