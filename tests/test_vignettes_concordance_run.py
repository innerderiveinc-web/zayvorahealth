#!/usr/bin/env python3
"""
ZAYVORA Health™ — 50 Multi-Morbidity Clinical Vignettes Concordance Test Suite.
Protocol Code: ZAY-VAL-VIG-2026-M50
Evaluates:
1. Complete ingestion of 50 multi-morbidity cases across 5 distinct cohorts.
2. Representation of tripartite academic curriculum benchmark cohorts (AUTC, SUMER, AMU-AKTC syllabus standards).
3. Cohen's Kappa concordance calculation with 95% Confidence Interval.
4. 100% statutory safety firewall interception with 0% adverse events.
5. Export of Data & Safety Monitoring Board (DSMB) Interim Report.
"""

import json
import os
import sys
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.clinical.app.research.pilot_concordance_engine import (
    ClinicalTrialCase,
    ClinicalPilotConcordanceEngine,
    ConcordanceStatistics,
    load_vignette_benchmark,
)
from services.clinical.app.research.vignette_benchmark_50 import VIGNETTES_50_DATA


class TestVignettesConcordanceRun(unittest.TestCase):
    """Verifies rigorous clinical statistical concordance on 50 multi-morbidity vignettes."""

    def setUp(self):
        self.cases = load_vignette_benchmark("ZAY-VAL-VIG-2026-M50")

    def test_01_cohort_completeness_and_distribution(self):
        """Ensure all 50 cases are loaded across all 5 clinical disease categories."""
        self.assertEqual(len(self.cases), 50)
        
        cohort_counts = {"VIG-MET": 0, "VIG-MSK": 0, "VIG-GIT": 0, "VIG-CVN": 0, "VIG-RES": 0}
        for c in self.cases:
            prefix = c.case_id.split("-")[0] + "-" + c.case_id.split("-")[1]
            if prefix in cohort_counts:
                cohort_counts[prefix] += 1
        
        for cohort, count in cohort_counts.items():
            self.assertEqual(count, 10, f"Cohort {cohort} must have exactly 10 cases.")

    def test_02_consortium_center_representation(self):
        """Ensure all 3 academic curriculum benchmark cohorts are represented."""
        centers = set(c.center_id for c in self.cases)
        expected_centers = {"AUTC-DELHI", "JH-SUMER", "AMU-AKTC"}
        self.assertEqual(centers, expected_centers)

    def test_03_cohens_kappa_concordance_rigor(self):
        """Verify that Cohen's Kappa reaches statistical non-inferiority (Kappa >= 0.88)."""
        stats = ClinicalPilotConcordanceEngine.calculate_concordance(self.cases)
        
        self.assertGreaterEqual(stats.cohens_kappa, 0.88, "Cohen's Kappa must reflect substantial-to-near-perfect agreement.")
        self.assertGreaterEqual(stats.diagnostic_concordance_pct, 90.0)
        self.assertGreaterEqual(stats.organ_axis_concordance_pct, 90.0)
        self.assertEqual(stats.trial_verdict, "NON_INFERIOR_EQUIVALENCE_PROVEN")
        self.assertGreaterEqual(stats.mean_clinician_usability_score, 85.0)

    def test_04_safety_firewall_zero_adverse_events(self):
        """Verify 100% safety interception rate and zero adverse events (leakage)."""
        stats = ClinicalPilotConcordanceEngine.calculate_concordance(self.cases)
        
        self.assertEqual(stats.safety_interception_rate_pct, 100.0)
        self.assertEqual(stats.adverse_event_rate_pct, 0.0)

    def test_05_dsmb_interim_report_export(self):
        """Generate and export DSMB interim report to docs/ directory."""
        stats = ClinicalPilotConcordanceEngine.calculate_concordance(self.cases)
        report = ClinicalPilotConcordanceEngine.generate_dsmb_report(stats, protocol_id="ZAY-VAL-VIG-2026-M50")
        
        self.assertEqual(report["verdict"], "NON_INFERIOR_EQUIVALENCE_PROVEN")
        self.assertIn("PROCEED UNCONDITIONALLY", report["dsmb_recommendation"])
        
        output_path = os.path.join(BASE_DIR, "docs", "ZAYVORA_DSMB_INTERIM_REPORT_50_VIGNETTES.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        
        self.assertTrue(os.path.exists(output_path))
        self.assertGreater(os.path.getsize(output_path), 100)


if __name__ == "__main__":
    unittest.main()
