"""Outcome-blind published source-grain probe for Traine et al. (2026).

Dryad and Figshare metadata + at most one 12-MB public CSV payload per source.
Rows are neither parsed nor reported; headers, file hashes and HTTP errors only.
No genotype, visitation, fruit or seed outcome value is read for analysis.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import urllib.error
import urllib.request
from urllib.parse import urlparse
import re

DRYAD_BASE="https://datadryad.org"
DRYAD_DATASET="https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.2ngf1vj15"
FIGSHARE_API="https://api.figshare.com/v2/articles/31239511"
MAX_METADATA=2_000_000
MAX_DATA=12_000_000
# Header presence is only a source-schema gate, never a model-fit permission.
TRAINE_REQUIRED={"plant","matrix","cohort","temp_genotype","poll_genotype",
                 "flowers","bee_flower_visits","seed_number"}

def _fetch(url: str, maximum: int) -> bytes:
    req=urllib.request.Request(url,headers={
        "User-Agent":"EGWE source-schema audit/20261008",
        "Accept":"application/json" if "/api/" in url else "*/*"
    })
    with urllib.request.urlopen(req,timeout=35) as response:
        blob=response.read(maximum+1)
    if len(blob)>maximum:
        raise ValueError("source_exceeds_size_cap")
    return blob

def _json(url: str) -> dict:
    parsed=urlparse(url)
    if parsed.scheme!="https" or parsed.hostname not in ("datadryad.org","api.figshare.com"):
        raise ValueError("metadata endpoint not allowlisted")
    data=json.loads(_fetch(url,MAX_METADATA))
    if not isinstance(data,dict):
        raise ValueError("metadata_not_object")
    return data

def _header(blob: bytes) -> list[str]:
    # Only parse the first physical line. No next(csv.reader), no row values.
    line=blob.split(b"\n",1)[0]
    if len(line)>32768:
        raise ValueError("oversize_csv_header")
    return next(csv.reader([line.decode("utf-8-sig",errors="replace").rstrip("\r")]))

def _error(err: Exception) -> dict:
    return {"status":"ACCESS_OR_SCHEMA_STOP","error_type":type(err).__name__,
            "http_status":err.code if isinstance(err,urllib.error.HTTPError) else None,
            "detail":str(err)[:160]}

def _dryad_file_id(entry: dict) -> int:
    """Resolve a Dryad v2 file ID from advertised API relations, not only id."""
    if isinstance(entry.get("id"), int):
        return entry["id"]
    relations=entry.get("_links") or {}
    candidates=[v.get("href") for v in relations.values() if isinstance(v,dict)]
    for href in candidates:
        if not isinstance(href,str):
            continue
        matched=re.search(r"/(?:api/v2/files|downloads/file_stream)/(\d+)(?:/download)?(?:$|[?#])", href)
        if matched:
            return int(matched.group(1))
    raise ValueError("target_file_id_missing_from_api_relations")


def dryad() -> dict:
    report={"source":"Dryad Traine 2026","doi":"10.5061/dryad.2ngf1vj15",
            "outcome_rows_opened":False,"raw_verified":False}
    try:
        ds=_json(DRYAD_DATASET)
        link=ds.get("_links",{}).get("stash:version",{}).get("href")
        if not isinstance(link,str) or not link.startswith("/api/v2/versions/"):
            raise ValueError("missing_version_link")
        version=_json(DRYAD_BASE+link)
        files_link=version.get("_links",{}).get("stash:files",{}).get("href") or (link+"/files")
        if not files_link.startswith("/api/v2/versions/"):
            raise ValueError("unexpected_files_link")
        inventory=_json(DRYAD_BASE+files_link)
        files=inventory.get("_embedded",{}).get("stash:files",[])
        names=[{"name":f.get("path"),"size":f.get("size"),
                "link_paths":[urlparse(link.get("href","")).path
                              for link in (f.get("_links") or {}).values()
                              if isinstance(link,dict)]}
               for f in files if isinstance(f,dict)]
        report.update(status="METADATA_VERIFIED",version_path=link,inventory=names)
        target=next((f for f in files if str(f.get("path","")).endswith("data_local_adapt_traits.csv")),None)
        if not target:
            raise ValueError("target_csv_absent")
        identifier=_dryad_file_id(target)
        url=f"{DRYAD_BASE}/downloads/file_stream/{identifier}"
        blob=_fetch(url,MAX_DATA)
        expected_size=target.get("size")
        if not isinstance(expected_size,int) or len(blob)!=expected_size:
            raise ValueError(f"pinned_file_size_mismatch:{len(blob)} expected:{expected_size}")
        expected_digest=target.get("digest")
        if target.get("digestType")=="sha-256" and isinstance(expected_digest,str):
            if hashlib.sha256(blob).hexdigest().lower()!=expected_digest.lower():
                raise ValueError("pinned_sha256_mismatch")
        columns=_header(blob)
        missing=sorted(TRAINE_REQUIRED-set(columns))
        report.update(status="RAW_HEADER_VERIFIED" if not missing else "RAW_HEADER_INCOMPLETE",
                      file_id=identifier,sha256=hashlib.sha256(blob).hexdigest(),
                      bytes=len(blob),header=columns,
                      required_header_fields_missing=missing,raw_verified=True,
                      independent_matrix_units_verified=False)
    except Exception as exc:
        report.update(_error(exc))
    return report

def figshare() -> dict:
    report={"source":"Figshare Traine 2026 separate study",
            "article_id":31239511,"outcome_rows_opened":False,"raw_verified":False}
    try:
        article=_json(FIGSHARE_API)
        files=article.get("files",[])
        names=[{"name":f.get("name"),"size":f.get("size"),"id":f.get("id")}
               for f in files if isinstance(f,dict)]
        report.update(status="METADATA_VERIFIED",article_title=article.get("title"),files=names)
        csvs=[f for f in files if str(f.get("name","")).lower().endswith(".csv")
              and isinstance(f.get("size"),int) and f["size"]<=MAX_DATA]
        # Only one explicitly documented CSV file, never sample outcome rows.
        if csvs:
            f=sorted(csvs,key=lambda x:str(x.get("name","")))[0]
            url=f.get("download_url")
            parsed=urlparse(url or "")
            if parsed.scheme!="https" or parsed.hostname not in (
                "ndownloader.figshare.com","api.figshare.com","figshare.com"):
                raise ValueError("untrusted_figshare_file_url")
            blob=_fetch(url,MAX_DATA)
            report.update(status="RAW_HEADER_VERIFIED",sample_file=f.get("name"),
                          sha256=hashlib.sha256(blob).hexdigest(),
                          bytes=len(blob),header=_header(blob),raw_verified=True)
    except Exception as exc:
        report.update(_error(exc))
    return report

def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    a=p.parse_args()
    result={"schema_version":1,"outcome_rows_opened":False,
            "dryad":dryad(),"figshare":figshare(),
            "full_HR_validated":False,
            "interpretation":"Metadata/headers only. No source admitted to H-R or predictive modelling."}
    assert all(x["outcome_rows_opened"] is False for x in (result["dryad"],result["figshare"]))
    out=Path(a.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("TRAINE_SOURCE_GATE "+json.dumps({
        k:{"status":result[k]["status"],"raw_verified":result[k]["raw_verified"],
           "file_count":len(result[k].get("files",result[k].get("inventory",[]))),
           "http_status":result[k].get("http_status"),
           "column_count":len(result[k].get("header",[])),
           "missing_required_header_fields":result[k].get("required_header_fields_missing")}
        for k in ("dryad","figshare")},sort_keys=True))
if __name__=="__main__":
    main()
