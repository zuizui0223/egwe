from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "brassica_zip_header_probe", ROOT / "scripts/probe_brassica_dryad_schema.py"
)
assert SPEC and SPEC.loader
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


def zip_bytes(files: dict[str, str | bytes]) -> bytes:
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode="w") as zipped:
        for path, value in files.items():
            zipped.writestr(path, value)
    return data.getvalue()


def fixture_zip(visitation_header: str = "Site,DOY,Date,Batch,Total pollinator visits") -> bytes:
    prefix = "Leventhal_et_al_2026/"
    inner = zip_bytes({
        prefix + "data-raw/PollinatorVisitationDatafiles/PollinatorObservation_Comp&B30_editedForTimeSlices2.csv": (
            visitation_header + "\n" + "OUTCOME_SECRET" + "\n"
        ),
        prefix + "data-intermediate/phenotype data/BrapaP_B30.csv": (
            "id,terr,timevar,X,Y,ft,dur,tot_flwrs\nOUTCOME_SECRET\n"
        ),
        prefix + "data-intermediate/genetic data/BrapaG_B30.csv": (
            "id,A10A8a,A10A8b\nOUTCOME_SECRET\n"
        ),
        prefix + "data/pedigree_assignment/pedigee_bZ_B30.csv": (
            "P.1,P.2,P.3,prob\nOUTCOME_SECRET\n"
        ),
        prefix + "data-raw/clump_coord.csv": "id,X,Y\nOUTCOME_SECRET\n",
    })
    return zip_bytes({"Leventhal_et_al_2026.zip": inner})


def test_header_only_probe_never_exports_outcome_rows() -> None:
    result = PROBE.inspect_archive(fixture_zip())
    assert result["status"] == "RAW_HEADER_INDEX_OBTAINED"
    assert result["outcome_values_opened"] is False
    assert result["member_count_by_role"] == {
        "visitation": 1, "phenotype": 1, "genotype": 1,
        "paternity": 1, "coordinates": 1
    }
    assert result["visitation_has_plant_or_patch_key_by_column_name"] is False
    assert "OUTCOME_SECRET" not in json.dumps(result)


def test_patch_key_detection_requires_actual_visitation_column() -> None:
    result = PROBE.inspect_archive(fixture_zip("Site,Date,PlantID,Batch,Visits"))
    assert result["visitation_has_plant_or_patch_key_by_column_name"] is True
    assert "plantid" in result["possible_visitation_grain_fields"]


def test_bad_offline_payload_is_access_schema_stop(tmp_path: Path) -> None:
    path = tmp_path / "not_zip.bin"
    path.write_bytes(b"not zip data")
    result = PROBE.run("archive_fixture", str(path))
    assert result["status"] == "ACCESS_OR_SCHEMA_STOP"
    assert result["outcome_values_opened"] is False
    assert result["error_type"] == "ValueError"
