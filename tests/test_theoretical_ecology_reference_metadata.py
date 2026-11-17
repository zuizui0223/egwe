"""Offline regression tests for independent TE DOI metadata QA."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


MODULE = Path(__file__).resolve().parents[1] / "scripts" / "audit_theoretical_ecology_references.py"
spec = importlib.util.spec_from_file_location("te_refs", MODULE)
assert spec is not None and spec.loader is not None
te_refs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(te_refs)


class ReferenceMetadataTests(unittest.TestCase):
    def test_hyphenated_surname_is_not_false_mismatch(self):
        self.assertEqual(te_refs.normal("Kaiser-Bunbury"), te_refs.normal("Kaiser‐Bunbury"))
        self.assertEqual(te_refs.normal("Kaiser-Bunbury"), te_refs.normal("Kaiser‑Bunbury"))

    def test_publisher_family_metadata_does_not_false_fail(self):
        entry = {
            "doi": "10.1111/j.1461-0248.2009.01437.x",
            "first_author": "Kaiser-Bunbury",
            "year": 2010,
            "title": "The robustness of pollination networks to the loss of species and interactions: a quantitative approach incorporating pollinator behaviour",
            "volume": "13",
        }
        metadata = {
            "DOI": entry["doi"], "title": [entry["title"]],
            "author": [{"family": "Kaiser‐Bunbury"}],
            "published-print": {"date-parts": [[2010, 4]]},
            "volume": "13",
        }
        self.assertEqual(te_refs.judge(entry, metadata)["verdict"], "verified")

    def test_all_28_reference_entries_parse_locally(self):
        lines = te_refs.REFS.read_text(encoding="utf-8").split("\n\n", 1)[1].strip()
        records = [te_refs.parse_entry(x.strip()) for x in lines.split("\n\n") if x.strip()]
        self.assertEqual(len(records), 28)
        self.assertEqual(len({r["doi"] for r in records}), 28)
        self.assertEqual(records[15]["first_author"], "Kaiser-Bunbury")


if __name__ == "__main__":
    unittest.main()
