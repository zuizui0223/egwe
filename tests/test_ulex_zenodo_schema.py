from __future__ import annotations

import importlib.util
from pathlib import Path
from urllib.error import HTTPError

import pytest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("ulex_schema",
    ROOT/"scripts/probe_ulex_zenodo_schema.py")
assert SPEC and SPEC.loader
MOD=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def test_expected_source_files_preserve_separate_grains() -> None:
    assert {"pollinator.census.csv","fruits.and.mean.floral.traits.csv",
            "relatedness.matrix.csv","SNP.genotypes.csv"} <= MOD.REQUIRED


def test_untrusted_file_link_never_fetched() -> None:
    with pytest.raises(ValueError,match="untrusted_zenodo_url"):
        MOD._download({"links":{"content":"https://elsewhere.example/data.csv"}})


def test_both_zenodo_file_inventory_shapes() -> None:
    newer={"files":[{"key":"pollinator.census.csv","links":{
        "self":"https://zenodo.org/api/records/7761289/files/pollinator.census.csv/content"
    }}]}
    older={"files":{"entries":{"pollinator.census.csv":{"size":100,
        "links":{"self":"https://zenodo.org/api/records/7761289/files/pollinator.census.csv/content"}
    }}}}
    assert MOD._files(newer)[0]["key"]=="pollinator.census.csv"
    assert MOD._files(older)[0]["key"]=="pollinator.census.csv"


def test_first_header_supports_csv_or_tab_separated() -> None:
    fields,delimiter=MOD._header("id,site,floral_trait")
    assert fields==["id","site","floral_trait"]
    assert delimiter==","
    fields,delimiter=MOD._header("id\tsite\tflower")
    assert fields==["id","site","flower"]
    assert delimiter=="\t"


def test_record_inspection_outputs_metadata_only(monkeypatch) -> None:
    metadata={
        "metadata":{"title":"Published Ulex data"},
        "files":[
            {"key":"README.md","size":70,"checksum":"md5:aaa","links":{
                "self":"https://zenodo.org/api/records/7761289/files/README.md/content"}},
            {"key":"pollinator.census.csv","size":400,"checksum":"md5:bbb","links":{
                "self":"https://zenodo.org/api/records/7761289/files/pollinator.census.csv/content"}},
            {"key":"fruits.and.mean.floral.traits.csv","size":500,
             "links":{"self":"https://zenodo.org/api/records/7761289/files/fruits.csv/content"}},
        ],
    }
    monkeypatch.setattr(MOD,"_metadata",lambda:metadata)
    monkeypatch.setattr(MOD,"_readme",lambda url:
        "site is the six sampled locations\npollinator visits are 3-minute flower censuses\n")
    monkeypatch.setattr(MOD,"_first_line",lambda url:
        ("site,visits,flower_count","text/csv") if "pollinator" in url
        else ("plant_id,fruit_count,flower_weight","text/csv"))
    report=MOD.probe()
    assert report["status"]=="METADATA_AND_HEADER_AUDIT_COMPLETE"
    assert report["biological_outcome_rows_opened"] is False
    assert report["raw_row_join_performed"] is False
    assert report["full_HR_eligibility"] is False
    assert len(report["files"])==3
    assert report["files"][1]["header"]==["site","visits","flower_count"]
    assert report["files"][0]["status"]=="README_READ"


def test_download_failure_does_not_become_biological_null(monkeypatch) -> None:
    metadata={"files":[{"key":"pollinator.census.csv",
        "links":{"self":"https://zenodo.org/api/records/7761289/files/pollinator.census.csv/content"}}]}
    monkeypatch.setattr(MOD,"_metadata",lambda:metadata)
    def denied(url):
        raise HTTPError(url,403,"Forbidden",None,None)
    monkeypatch.setattr(MOD,"_first_line",denied)
    result=MOD.probe()
    assert result["files"][0]["status"]=="ACCESS_OR_SCHEMA_STOP"
    assert result["files"][0]["http_status"]==403
    assert result["full_HR_eligibility"] is False
    assert result["biological_outcome_rows_opened"] is False


def test_real_header_shapes_forbid_plant_level_visitation_claim(monkeypatch) -> None:
    """Source-derived header names, entirely synthetic body-free fixture."""
    names=[
        "pollinator.census.csv",
        "fruits.and.mean.floral.traits.csv",
        "floral.traits.csv",
    ]
    md={"files":[{"key":name,"links":{
        "self":f"https://zenodo.org/api/records/7761289/files/{name}/content"}
        } for name in names]}
    headers={
        names[0]:"year,locality,flowers,tot.visits,Apis,Bombus,other,visits.flower,observations",
        names[1]:"site,ind,elev,weight,area,scars,fruits,nofruit",
        names[2]:"site,ind,flower,weight,area,elev",
    }
    monkeypatch.setattr(MOD,"_metadata",lambda:md)
    monkeypatch.setattr(MOD,"_first_line",lambda url: (
        headers[url.rsplit("/",2)[-2]],"text/csv"))
    r=MOD.probe()
    assert r["candidate_grain_decision"]=="NO_POLLINATOR_PLANT_ID_AT_SOURCE_HEADER"
    assert r["pollinator_plant_id_in_header"] is False
    assert r["fruit_trait_both_expose_ind"] is True
    assert r["full_HR_eligibility"] is False
    assert not r["biological_outcome_rows_opened"]


def test_snp_header_can_exceed_old_64k_without_reading_rows() -> None:
    assert MOD.MAX_HEADER>=100_000
    cols=[f"SNP_{n}" for n in range(10421)]
    fields, delim=MOD._header(",".join(cols))
    assert len(fields)==10421
    assert delim==","
