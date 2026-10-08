from __future__ import annotations

import csv
import zipfile

from scripts.audit_yht_dryad_schema import EXPECTED_FILES, PRIMARY, audit


def test_schema_audit_reads_header_only(tmp_path) -> None:
    zpath = tmp_path / "bundle.zip"
    with zipfile.ZipFile(zpath, "w") as zf:
        for name in sorted(EXPECTED_FILES):
            if name == PRIMARY:
                zf.writestr(name, "Year,CowCalfRatio,Variance\n2004,999,999\n")
            else:
                zf.writestr(name, "x\n1\n")
    out = audit(zpath)
    assert out["status"] == "schema_only_no_outcome_rows_parsed"
    assert out["primary_header"] == ["Year", "CowCalfRatio", "Variance"]
    assert out["outcome_rows_parsed"] == 0
