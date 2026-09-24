"""Exhaustive tiny-plant meta-oracle tests."""
from __future__ import annotations

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from metaoracle import run_metaoracle  # noqa: E402


class MetaOracleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary = run_metaoracle(4)

    def test_declared_universe_is_exhausted(self):
        self.assertEqual(self.summary["plants_checked"], 486)
        self.assertEqual(self.summary["receipt_partitions_by_bound"],
                         {"0": 1, "1": 2, "2": 5, "3": 15, "4": 52})
        self.assertEqual(self.summary["receipt_partitions_checked"], 75)

    def test_generic_synthesizer_matches_bruteforce(self):
        self.assertEqual(self.summary["kernel_mismatches"], 0)
        self.assertEqual(self.summary["observer_mismatches"], 0)
        self.assertEqual(self.summary["greatest_contract_mismatches"], 0)
        self.assertEqual(self.summary["nonblocking_mismatches"], 0)

    def test_quantifier_and_eligibility_mutants_are_killed(self):
        self.assertGreater(self.summary["existential_mutant_counterexamples"], 0)
        self.assertGreater(self.summary["eligibility_mutant_counterexamples"], 0)
        self.assertIsNotNone(self.summary["first_existential_mutant_witness"])


if __name__ == "__main__":
    unittest.main()
