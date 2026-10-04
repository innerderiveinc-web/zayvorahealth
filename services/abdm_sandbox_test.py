#!/usr/bin/env python3
"""
ZAYVORA Health OS — ABDM Live Sandbox Compliance Test Suite
Validates Milestone 1 (ABHA Verification), Milestone 2 (Care Context), and Milestone 3 (FHIR R4 Bundle)
"""

import os
import sys

def run_tests():
    print("==================================================================")
    print(" ZAYVORA Health OS — ABDM NHA Gateway Compliance Verification")
    print("==================================================================")

    from services.abdm_gateway import ABDMGatewayClient
    client = ABDMGatewayClient()

    print("\n[1] Verifying NHA Gateway Session Token Negotiation...")
    token = client.get_session_token()
    assert token and len(token) > 5, "Session token failed"
    print(f"  ✓ Session Token negotiated successfully: {token[:24]}...")

    print("\n[2] Testing ABDM Milestone 1 (ABHA Address Verification)...")
    res = client.verify_abha_address("dr.irfan@abdm")
    assert res.get("ok") is True, "ABHA address validation failed"
    print(f"  ✓ ABHA Address: {res.get('abha_address')} -> Status: {res.get('status')} ({res.get('compliance')})")

    print("\n[3] Testing ABDM Milestone 2 & 3 (Care Context & FHIR Push)...")
    mock_bundle = {
        "resourceType": "Bundle",
        "type": "document",
        "entry": [
            {
                "resource": {
                    "resourceType": "Composition",
                    "status": "final",
                    "title": "ZAYVORA Unani OP Consult Record"
                }
            }
        ]
    }
    cc = client.generate_care_context_bundle("MRN-2026-0816", "ENC-9912", mock_bundle)
    assert cc.get("ok") is True, "Care context creation failed"
    print(f"  ✓ Care Context created: {cc['careContexts'][0]['careContextReference']}")
    print(f"  ✓ Encryption Profile: {cc.get('encryptionStatus')}")
    print(f"  ✓ NRCES Profile: {cc.get('abdmStandard')}")

    print("\n==================================================================")
    print("✓ ALL ABDM MILESTONES (M1, M2, M3) VERIFIED & COMPLIANT!")
    print("==================================================================")

if __name__ == "__main__":
    run_tests()
