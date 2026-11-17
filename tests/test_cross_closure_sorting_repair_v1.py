"""Pre-outcome operator and protocol contract tests for cross-closure v1."""
from __future__ import annotations

import math
from random import Random
import unittest

from eco_genetic_warning_extensions.cross_closure_sorting_repair import (
    CLOSURES,
    allele_selected,
    auc_with_ties,
    binomial,
    check_matched_initial_marginals,
    ci_six_blocks,
    first_state,
    load_protocol,
    recruit_mass,
    seed,
)


class CrossClosureProspectiveTests(unittest.TestCase):
    def setUp(self):
        self.p = load_protocol(check_git_lock=False)

    def test_locked_factorial_and_matched_marginals(self):
        check_matched_initial_marginals(self.p)
        a, b = first_state(self.p, "AA"), first_state(self.p, "RR")
        self.assertEqual(a[1], b[1])
        self.assertEqual(a[4], b[4])
        self.assertEqual(sorted(a[2]), sorted(b[2]))
        self.assertEqual(sorted(a[3]), sorted(b[3]))
        self.assertEqual(len(CLOSURES), 2)
        self.assertEqual(self.p["replication"]["total_trajectories"], 7680)

    def test_allele_selection_matches_old_functional_multiplier_at_s_one(self):
        for p in (0.01, 0.2, 0.5, 0.8, 0.99):
            for q in (0.0, 0.3, 0.625, 1.0):
                w = 0.75 + 0.4 * q
                expected = p * w / (1.0 - p + p * w)
                self.assertAlmostEqual(allele_selected(p, q, 1.0), expected)
                self.assertAlmostEqual(allele_selected(p, q, 0.0), p)

    def test_trait_allele_recruitment_mismatch_contracts_by_h(self):
        for h in (0.25, 0.75):
            m, p = 0.20, 0.80
            self.assertAlmostEqual(recruit_mass(m, p, h) - p, h * (m - p))

    def test_binomial_extremes_and_reproducible_seed(self):
        rng = Random(17)
        self.assertEqual(binomial(rng, 100, 0.0), 0)
        self.assertEqual(binomial(rng, 100, 1.0), 100)
        self.assertEqual(binomial(Random(919), 40, 0.37),
                         binomial(Random(919), 40, 0.37))
        self.assertNotEqual(seed(901171, 2), seed(901171, 3))

    def test_auc_exact_rank_and_ties(self):
        self.assertAlmostEqual(auc_with_ties([(0, 0), (1, 1)]), 1)
        self.assertAlmostEqual(auc_with_ties([(1, 0), (0, 1)]), 0)
        self.assertAlmostEqual(auc_with_ties([(1, 0), (1, 1)]), 0.5)
        self.assertIsNone(auc_with_ties([(0.2, 1), (0.7, 1)]))

    def test_six_block_interval_no_fake_replicate_precision(self):
        x = ci_six_blocks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        self.assertEqual(x["n_blocks"], 6)
        self.assertAlmostEqual(x["mean"], 0.5)
        self.assertTrue(x["ci95"][0] < 0.5 < x["ci95"][1])
        with self.assertRaises(RuntimeError):
            ci_six_blocks([1, 2, 3])


if __name__ == "__main__":
    unittest.main()
