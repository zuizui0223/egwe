"""Offline tests: post-outcome diagnostic invariants, no real outcomes accessed."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import json
import unittest

PATH = Path(__file__).resolve().parents[1] / "scripts/audit_cross_closure_v1_diagnostics.py"
spec = importlib.util.spec_from_file_location("cc_diag", PATH)
assert spec and spec.loader
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)


class DiagnosticTests(unittest.TestCase):
    def test_fixed_factorial_count_and_no_replacement(self):
        self.assertEqual(len(d.CLOSURES) * len(d.ARRANGEMENTS) *
                         len(d.STRENGTHS) * len(d.REPAIR) *
                         len(d.MASTERS) * d.REPS, 15360)
        self.assertEqual(d.FREEZE_COMMIT, "efc3baa6868e705974235b35df70d1c3fee5b7a9")

    def test_known_dataset_small_sample_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # A structurally invalid fake artifact must fail closed.
            (root / "MANIFEST.json").write_text(json.dumps({
                "experiment_id": "cross_closure_sorting_repair_v1",
                "frozen_commit": d.FREEZE_COMMIT, "files_sha256": {}
            }))
            with self.assertRaises(ValueError):
                d.validate_manifest(root)

    def test_diagnostic_is_descriptive_not_inferential(self):
        dummy = {
            "original_primary_decision": "cross_closure_direction_not_established_no_retuning",
            "diagnostics": {
                d.CLOSURES[0]: {"cells": [{
                    "s": 1.0, "h": .25,
                    "RD_RR_minus_AA": 0.0,
                    "arrangements": {
                        "AA": {"n_loss": 3, "loss_rate": 3/960, "n_reappeared_after_first_loss": 0},
                        "RR": {"n_loss": 3, "loss_rate": 3/960, "n_reappeared_after_first_loss": 0},
                    }
                }]}
            }
        }
        md = d.render_markdown(dummy)
        self.assertIn("POST-OUTCOME", md)
        self.assertIn("3/960", md)
        self.assertIn("not species extinction", md.lower())


if __name__ == "__main__":
    unittest.main()
