#!/usr/bin/env python3
"""
ZAYVORA Health™ — Phase 8: Multi-Center Clinical Pilot Concordance & DSMB Test Suite.

Verifies:
1. Multi-center clinical trial case ingestion across AUTC, SUMER Center, and AMU AKTC.
2. Statistical inter-rater concordance (Cohen's Kappa >= 0.85).
3. 100% statutory safety firewall interception and zero adverse event leakage.
4. Automated Data & Safety Monitoring Board (DSMB) interim report generation.
5. Multi-tenant academic medical center isolation.
"""

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
)


class TestClinicalPilotConcordance(unittest.TestCase):
    """Verifies Phase 8 clinical pilot concordance and DSMB statistical rigor."""

    def setUp(self):
        # Generate representative cohort of 100 trial cases across 3 centers
        self.cases = []
        centers = ["AUTC-DELHI", "JH-SUMER", "AMU-AKTC"]
        humors = ["Damwi", "Safrawi", "Balghami", "Saudawi"]
        organ_axes = ["Kabid-Meda", "Qalb-Dimagh", "Kulyah-Masana", "Riya-Sadr"]

        for i in range(100):
            center = centers[i % 3]
            humor = humors[i % 4]
            organ = organ_axes[i % 4]

            # Simulate 92% direct concordance, 8% divergent cases
            if i % 12 != 0:
                z_humor = humor
                z_organ = organ
            else:
                z_humor = humors[(i + 1) % 4]
                z_organ = organ_axes[(i + 1) % 4]

            case = ClinicalTrialCase(
                case_id=f"CASE-{center}-{i:04d}",
                patient_pseudonym_id=f"SUBJ-PSEUDO-{i:04d}",
                center_id=center,
                tabeeb_panel_diagnosis=f"Su-e-Mizaj {humor}",
                zayvora_engine_diagnosis=f"Su-e-Mizaj {z_humor}",
                tabeeb_organ_axis=organ,
                zayvora_organ_axis=z_organ,
                tabeeb_nuskha_compounds=["Khamira Gaozaban", "Sharbat Deenar"],
                zayvora_suggested_compounds=["Khamira Gaozaban", "Sharbat Deenar"],
                safety_firewall_interceptions=1 if (i % 10 == 0) else 0,
                adverse_events_reported=0,  # Zero ADEs tolerated
                clinician_sus_score=88.5 + (i % 10),
            )
            self.cases.append(case)

    def test_01_cohort_case_ingestion(self):
        """Verify that 100 cases across all 3 university centers are loaded."""
        self.assertEqual(len(self.cases), 100)
        centers_represented = set(c.center_id for c in self.cases)
        self.assertEqual(centers_represented, {"AUTC-DELHI", "JH-SUMER", "AMU-AKTC"})

    def test_02_cohens_kappa_concordance_calculation(self):
        """Verify that Cohen's Kappa exceeds clinical threshold (>= 0.85)."""
        stats = ClinicalPilotConcordanceEngine.calculate_concordance(self.cases)
        self.assertGreaterEqual(stats.cohens_kappa, 0.85)
        self.assertGreaterEqual(stats.diagnostic_concordance_pct, 90.0)
        self.assertEqual(stats.trial_verdict, "NON_INFERIOR_EQUIVALENCE_PROVEN")
        self.assertGreaterEqual(stats.mean_clinician_usability_score, 85.0)

    def test_03_zero_tolerance_safety_interception(self):
        """Verify 100% safety interception rate and zero adverse events."""
        stats = ClinicalPilotConcordanceEngine.calculate_concordance(self.cases)
        self.assertEqual(stats.safety_interception_rate_pct, 100.0)
        self.assertEqual(stats.adverse_event_rate_pct, 0.0)

    def test_04_dsmb_interim_report_generation(self):
        """Verify generation and formatting of structured DSMB safety report."""
        stats = ClinicalPilotConcordanceEngine.calculate_concordance(self.cases)
        report = ClinicalPilotConcordanceEngine.generate_dsmb_report(stats, "ZAYVORA-PILOT-2026-A")
        self.assertEqual(report["protocol_id"], "ZAYVORA-PILOT-2026-A")
        self.assertIn("PROCEED UNCONDITIONALLY", report["dsmb_recommendation"])
        self.assertEqual(report["metrics"]["adverse_drug_reactions"], "0.0% (Zero Fatal/Severe)")

    def test_05_pilot_tenants_seeding_and_isolation(self):
        """Verify provisioning of university center tenant schemas."""
        from database.seed_pilot_tenants import seed_pilot_tenants
        test_db = os.path.join(BASE_DIR, "zayvora_test_pilot.db")
        res = seed_pilot_tenants(test_db)
        self.assertEqual(res["centers_seeded"], 3)
        self.assertEqual(res["trial_subjects_seeded"], 30)
        if os.path.exists(test_db):
            os.remove(test_db)


if __name__ == "__main__":
    unittest.main()
