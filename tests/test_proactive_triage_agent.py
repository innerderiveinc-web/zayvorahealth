import unittest
import json
from tests.test_audit_security_controls import DirectApiSimulator

class TestProactiveTriageAgent(unittest.TestCase):
    def setUp(self):
        self.sim = DirectApiSimulator()

    def test_proactive_pre_consult_brief_generation(self):
        status, body, _ = self.sim.request('POST', '/api/v1/clinical/agent/pre-consult-brief', data={
            'mrn': 'PAT-0816',
            'patient_name': 'Hamza Farooqi',
            'age': 48,
            'gender': 'Male',
            'vitals': {
                'bp': '138/88',
                'pulse': '76',
                'temp': '98.4',
                'spo2': '98',
                'bmi': '27.4'
            },
            'chief_complaint': 'Osteoarthritis (Knee) with morning joint stiffness',
            'mizaj': 'Barid Balghami',
            'allopathic_meds': ['Atorvastatin 10mg']
        })
        self.assertEqual(status, 200)
        self.assertTrue(body.get('ok'))
        self.assertIn('brief', body)
        
        brief = body['brief']
        # 1. Vitals & Triage evaluation
        self.assertIn('vitals_analysis', brief)
        self.assertEqual(brief['vitals_analysis']['blood_pressure_grade'], 'STAGE_1_HTN')
        self.assertFalse(brief['vitals_analysis']['hypoxia_flag'])

        # 2. Humoral Pathology & Organ Axis inference
        self.assertIn('humoral_pathology', brief)
        self.assertEqual(brief['humoral_pathology']['predominant_humor'], 'Balgham')
        self.assertEqual(brief['humoral_pathology']['axis'], 'Mafasil-Dam (Musculo-Skeletal)')

        # 3. Proposed Staged Regimen
        self.assertIn('proposed_regimen', brief)
        regimen = brief['proposed_regimen']
        self.assertIn('Joshanda Munzij-e-Balgham', str(regimen['suggested_medicines']))
        self.assertIn('Majoon Suranjan', str(regimen['suggested_medicines']))
        self.assertTrue(len(regimen['suggested_medicines']) >= 2)

        # 4. Dietary Parhez & Tadbeer
        self.assertIn('dietary_parhez', regimen)
        self.assertIn('lifestyle_tadbeer', regimen)

    def test_pre_consult_brief_get_by_mrn(self):
        status, body, _ = self.sim.request('GET', '/api/v1/clinical/agent/pre-consult-brief?mrn=PAT-0816')
        self.assertEqual(status, 200)
        self.assertTrue(body.get('ok'))
        self.assertEqual(body['brief']['patient_mrn'], 'PAT-0816')
