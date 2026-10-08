"""Outcome-blind Dryad transport diagnostic; prints HTTP status only.

Never read or print data rows. All requests are bound to datadryad.org.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from urllib.parse import urljoin, urlparse

BASE = "https://datadryad.org"
DOI = "doi%3A10.5061%2Fdryad.tdz08kqdr"
METADATA = f"{BASE}/api/v2/datasets/{DOI}"
DOWNLOAD = METADATA + "/download"


def fetch(url: str, *, json_only: bool = False) -> tuple[dict, dict | None]:
    if urlparse(url).hostname != "datadryad.org":
        raise ValueError("Unexpected remote host")
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (research data archive schema audit)",
        "Accept": "application/json" if json_only else "*/*",
    })
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            metadata = {
                "request_path": urlparse(url).path,
                "status": response.status,
                "final_host": urlparse(response.url).hostname,
                "content_type": response.headers.get("Content-Type"),
                "content_length": response.headers.get("Content-Length"),
            }
            if json_only and "json" in (response.headers.get("Content-Type") or ""):
                obj=json.load(response)
                return metadata, obj if isinstance(obj, dict) else None
            # Never read downloaded biological data.
            return metadata, None
    except urllib.error.HTTPError as e:
        return {
            "request_path": urlparse(url).path,
            "status": e.code,
            "error": e.reason if isinstance(e.reason,str) else type(e.reason).__name__,
        }, None
    except Exception as e:
        return {"request_path": urlparse(url).path,
                "error_type": type(e).__name__, "error": str(e)[:100]}, None


def main() -> None:
    results = []
    a, data = fetch(METADATA, json_only=True)
    results.append(a)
    if data:
        versions = data.get("_links",{}).get("stash:version",{}).get("href")
        print("DATASET_METADATA " + json.dumps({
            "identifier": data.get("identifier"),
            "curation_status": data.get("curationStatus"),
            "version_path": versions,
        }))
        if isinstance(versions,str) and versions.startswith("/api/v2/"):
            b, version_obj = fetch(urljoin(BASE,versions),json_only=True)
            results.append(b)
            link = version_obj.get("_links",{}).get("stash:files",{}).get("href") if version_obj else versions+"/files"
            if link and link.startswith("/api/v2/"):
                c, files_obj = fetch(urljoin(BASE,link),json_only=True)
                results.append(c)
                if files_obj:
                    members=files_obj.get("_embedded",{}).get("stash:files",[])
                    print("DATASET_FILE_INDEX " + json.dumps({
                        "count":len(members),
                        "files":[{"path":f.get("path"),"size":f.get("size"),
                                  "download":f.get("_links",{}).get("stash:download",{}).get("href")}
                                 for f in members if str(f.get("path","")).lower().endswith(".zip")],
                    }))
    d,_=fetch(DOWNLOAD)
    results.append(d)
    print("DRYAD_TRANSPORT " + json.dumps(results,sort_keys=True))
    # A published Dryad download can legitimately redirect to an object-storage
    # host. The diagnostic reports final_host without reading biological content.
    # Initial requests are still constrained to the documented Dryad API origin.


if __name__ == "__main__":
    main()
