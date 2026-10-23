import unittest
import json
import base64
import os
from tests.test_audit_security_controls import DirectApiSimulator

class TestPatientAttachmentsApi(unittest.TestCase):
    def setUp(self):
        self.sim = DirectApiSimulator()
        self.sample_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\r\xef5\xc8\x00\x00\x00\x00IEND\xaeB`\x82'
        self.b64_img = 'data:image/png;base64,' + base64.b64encode(self.sample_png).decode('ascii')

    def test_upload_and_retrieve_patient_photo(self):
        # 1. Upload photo
        status, body, _ = self.sim.request('POST', '/api/v1/patient/attachments', data={
            'mrn': 'PAT-0816',
            'document_type': 'TONGUE_PHOTO',
            'file_name': 'lisan_exam_2026.png',
            'file_data': self.b64_img,
            'description': 'Lisan examination showing saburral phlegmatic coating'
        })
        self.assertEqual(status, 201)
        self.assertTrue(body.get('ok'))
        att = body.get('attachment', {})
        att_id = att.get('id')
        self.assertTrue(att_id.startswith('ATT-'))
        self.assertEqual(att.get('mrn'), 'PAT-0816')
        self.assertEqual(att.get('mime_type'), 'image/png')

        # 2. List attachments for PAT-0816
        status, list_body, _ = self.sim.request('GET', '/api/v1/patient/attachments?mrn=PAT-0816')
        self.assertEqual(status, 200)
        self.assertTrue(list_body.get('ok'))
        self.assertGreaterEqual(list_body.get('count', 0), 1)

        # 3. Serve binary media
        status, media_body, headers = self.sim.request('GET', f'/api/v1/media/{att_id}')
        self.assertEqual(status, 200)
        self.assertEqual(headers.get('content-type'), 'image/png')

    def test_unsupported_file_extension_blocked(self):
        status, body, _ = self.sim.request('POST', '/api/v1/patient/attachments', data={
            'mrn': 'PAT-0816',
            'file_name': 'exploit.sh',
            'file_data': 'data:application/x-sh;base64,ZWNobyAnSGFja2VkJw=='
        })
        self.assertEqual(status, 400)
        self.assertIn('Unsupported file format', body.get('error', ''))
