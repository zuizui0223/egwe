"""Zenodo 7761289 schema-only reconnaissance.

The tool reads public record metadata, complete public README (non-data),
and at most the FIRST physical line of each CSV. No biological data rows,
genotype values, visit counts or fruit outcomes are inspected.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

API="https://zenodo.org/api/records/7761289"
REQUIRED={
    "floral.traits.csv",
    "fruits.and.mean.floral.traits.csv",
    "pollinator.census.csv",
    "relatedness.matrix.csv",
    "SNP.genotypes.csv",
    "README.md",
}
MAX_JSON=2_000_000
MAX_README=16_384
MAX_HEADER=65_536


def _url(url: str) -> None:
    p=urlparse(url)
    if p.scheme!="https" or p.hostname!="zenodo.org":
        raise ValueError("untrusted_zenodo_url")


def _request(url: str):
    _url(url)
    return urlopen(Request(url,headers={
        "User-Agent":"egwe-scientific-source-grain-audit/1.0",
        "Accept":"*/*",
    }),timeout=30)


def _metadata() -> dict:
    with _request(API) as rsp:
        payload=rsp.read(MAX_JSON+1)
    if len(payload)>MAX_JSON:
        raise ValueError("metadata_exceeds_cap")
    data=json.loads(payload)
    if not isinstance(data,dict):
        raise ValueError("metadata_not_object")
    return data


def _files(record: dict) -> list[dict]:
    files=record.get("files",[])
    if isinstance(files,dict):
        files=files.get("entries",files.get("files",[]))
    if isinstance(files,dict):
        files=[dict({"key":k},**v) for k,v in files.items() if isinstance(v,dict)]
    if not isinstance(files,list):
        raise ValueError("unexpected_file_inventory")
    return [v for v in files if isinstance(v,dict)]


def _download(file: dict) -> str:
    links=file.get("links") or {}
    value=links.get("content") or links.get("self") or links.get("download")
    if not isinstance(value,str):
        raise ValueError("file_has_no_content_link")
    _url(value)
    return value


def _first_line(url: str) -> tuple[str,str]:
    with _request(url) as rsp:
        line=rsp.readline(MAX_HEADER+1)
        content_type=rsp.headers.get("Content-Type","")
    if len(line)>MAX_HEADER:
        raise ValueError("csv_header_exceeds_cap")
    text=line.decode("utf-8-sig",errors="replace").rstrip("\r\n")
    if not text or text.lstrip().startswith("<"):
        raise ValueError("csv_response_not_tabular")
    return text, content_type


def _header(raw: str) -> tuple[list[str],str]:
    delim=max([",","\t",";"],key=lambda c:raw.count(c))
    return next(csv.reader([raw],delimiter=delim)),delim


def _readme(url: str) -> str:
    with _request(url) as rsp:
        payload=rsp.read(MAX_README+1)
    if len(payload)>MAX_README:
        raise ValueError("readme_exceeds_cap")
    text=payload.decode("utf-8-sig",errors="replace")
    if text.lstrip().startswith("<"):
        raise ValueError("readme_html_challenge")
    return text


def _source_excerpts(readme: str) -> list[str]:
    # Source descriptions only. Do not infer joins from field names.
    needles=("pollinat","census","flower","individual","plant","fruit",
             "site","sample","survey","genotyp","relatedness","id","location",
             "year","row","visit","seed")
    lines=readme.splitlines()
    return [line.strip()[:500] for line in lines
            if line.strip() and any(x in line.lower() for x in needles)][:35]


def probe() -> dict:
    receipt={
        "record_id":7761289,
        "status":"PENDING",
        "record_metadata_verified":False,
        "biological_outcome_rows_opened":False,
        "raw_row_join_performed":False,
        "full_HR_eligibility":False,
        "source_file_checksums_not_computed":True,
        "files":[],
    }
    try:
        metadata=_metadata()
        files=_files(metadata)
        receipt["record_metadata_verified"]=True
        receipt["title"]=metadata.get("metadata",{}).get("title")
        receipt["inventory_names"]=[x.get("key",x.get("filename")) for x in files]
        receipt["missing_expected_files"]=sorted(REQUIRED-set(receipt["inventory_names"]))
        for file in files:
            filename=file.get("key",file.get("filename"))
            if filename not in REQUIRED:
                continue
            report={
                "filename":filename,
                "declared_bytes":file.get("size"),
                "declared_checksum":file.get("checksum"),
                "status":"PENDING",
            }
            try:
                url=_download(file)
                if filename=="README.md":
                    readme=_readme(url)
                    report.update(status="README_READ",readme_sha256=hashlib.sha256(
                        readme.encode("utf-8")).hexdigest(),excerpts=_source_excerpts(readme))
                else:
                    line, content_type=_first_line(url)
                    cols,sep=_header(line)
                    report.update(status="HEADER_READ",header=cols,
                                  delimiter="tab" if sep=="\t" else sep,
                                  column_count=len(cols),
                                  header_sha256=hashlib.sha256(line.encode()).hexdigest(),
                                  response_content_type=content_type)
            except Exception as err:
                report.update(
                    status="ACCESS_OR_SCHEMA_STOP",
                    error_type=type(err).__name__,
                    http_status=err.code if isinstance(err,HTTPError) else None,
                    detail=str(err)[:160])
            receipt["files"].append(report)
        receipt["status"]="METADATA_AND_HEADER_AUDIT_COMPLETE"
    except Exception as err:
        receipt.update(status="SOURCE_METADATA_STOP",
                       error_type=type(err).__name__,
                       http_status=err.code if isinstance(err,HTTPError) else None,
                       detail=str(err)[:160])
    return receipt


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    report=probe()
    assert report["biological_outcome_rows_opened"] is False
    assert report["raw_row_join_performed"] is False
    assert report["full_HR_eligibility"] is False
    out=Path(args.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("ULEX_SCHEMA_GATE "+json.dumps({
        "status":report["status"],
        "inventory_names":report.get("inventory_names",[]),
        "files":[{"name":f["filename"],"status":f["status"],
                  "columns":f.get("column_count"),
                  "http":f.get("http_status")}
                 for f in report["files"]],
        "outcome_rows_opened":False,
    },ensure_ascii=False,sort_keys=True))


if __name__=="__main__":
    main()
