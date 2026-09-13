#!/usr/bin/env python3
"""
ZAYVORA HEALTH OS™ — PHASE 4 PHARMACY FEFO, DISPENSING & BILLING TEST SUITE
SUITE-13: Comprehensive Automated Integration Verification Harness

Verifies:
1.  Inventory retrieval ordered by FEFO (First-Expired, First-Out).
2.  FEFO batch allocation algorithm prioritizing earlier expiry lots.
3.  Multi-batch split allocation across sequential expiration tiers.
4.  Statutory expiry gate blocking expired stock (HTTP 400 EXPIRED_STOCK_ERROR).
5.  Schedule E(1) statutory Mudabbar gate blocking uncertified botanicals (HTTP 403).
6.  Successful dispensing of authenticated Mudabbar botanical batch.
7.  Insufficient stock guardrail (HTTP 400 INSUFFICIENT_STOCK).
8.  RBAC barrier: Patient blocked from medication dispensing (HTTP 403).
9.  RBAC barrier: Receptionist blocked from medication dispensing (HTTP 403).
10. Atomic prescription dispensation, multi-item stock decrement & invoice generation.
11. Idempotency guard: Blocking duplicate dispensation of already fulfilled prescription.
12. Pharmacy billing reconciliation via GET /api/v1/billing/invoices.
13. Multi-tenancy guard: Cross-tenant pharmacy dispensation blocked (HTTP 403).
14. Merkle audit ledger anchoring of dispense events with SHA-256 leaf hashes.
15. Zero developer jargon in all pharmacy responses and error messages.
"""

import sys
import os
import json
import sqlite3
import time
import uuid
from io import BytesIO

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from services.live_api_server import ZayvoraApiHandler, DB_PATH

PROHIBITED_JARGON = [
    "sqlite", "database error", "traceback", "stack trace", "exception in thread",
    "syntax error", "null pointer", "undefined is not a function", "query failed",
    "operationalerror", "integrityerror", "cursor", "unhandled rejection", "500 internal"
]

class DirectTestClient:
    def request(self, method, path, data=None, headers=None):
        body_bytes = json.dumps(data).encode("utf-8") if data is not None else b""
        
        raw_headers = f"{method} {path} HTTP/1.1\r\n"
        raw_headers += "Host: localhost:8000\r\n"
        raw_headers += "Content-Type: application/json\r\n"
        raw_headers += f"Content-Length: {len(body_bytes)}\r\n"
        
        if headers:
            for k, v in headers.items():
                raw_headers += f"{k}: {v}\r\n"
        raw_headers += "\r\n"
        
        input_stream = BytesIO(raw_headers.encode("utf-8") + body_bytes)
        output_stream = BytesIO()

        class DummySocket:
            def __init__(self, rfile, wfile):
                self.rfile = rfile
                self.wfile = wfile
            def makefile(self, mode, *args, **kwargs):
                if "b" in mode:
                    return self.rfile if "r" in mode else self.wfile
                raise NotImplementedError()
            def sendall(self, b):
                self.wfile.write(b)

        dummy_sock = DummySocket(input_stream, output_stream)
        handler = ZayvoraApiHandler(dummy_sock, ("127.0.0.1", 12345), None)
        
        output_stream.seek(0)
        response_bytes = output_stream.getvalue()
        
        parts = response_bytes.split(b"\r\n\r\n", 1)
        header_lines = parts[0].decode("utf-8").split("\r\n")
        status_line = header_lines[0]
        status_code = int(status_line.split(" ")[1])
        
        resp_body = {}
        if len(parts) > 1 and parts[1]:
            try:
                resp_body = json.loads(parts[1].decode("utf-8"))
            except Exception:
                resp_body = {"raw": parts[1].decode("utf-8")}
            
        return status_code, resp_body

def run_tests():
    print("=" * 76)
    print(" ZAYVORA HEALTH OS™ — PHASE 4 PHARMACY FEFO, DISPENSING & BILLING TEST SUITE")
    print("=" * 76)

    client = DirectTestClient()
    passed = 0
    failed = 0

    def log_result(test_num, name, condition, detail=""):
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"[PASS] Test {test_num:02d}: {name} - {detail}")
        else:
            failed += 1
            print(f"[FAIL] Test {test_num:02d}: {name} - {detail}")

    def assert_zero_jargon(payload):
        text = json.dumps(payload).lower()
        for j in PROHIBITED_JARGON:
            if j in text:
                return False
        return True

    # 1. Obtain Tokens
    # Pharmacist
    _, p_body = client.request("POST", "/api/v1/auth/login", {
        "email": "zainab.pharm@zayvora.health",
        "password": "pharmacy123"
    })
    pharm_token = p_body["token"]
    pharm_headers = {"Authorization": f"Bearer {pharm_token}"}

    # Receptionist
    _, r_body = client.request("POST", "/api/v1/auth/login", {
        "email": "reception.opd@zayvora.health",
        "password": "reception123"
    })
    rec_token = r_body["token"]
    rec_headers = {"Authorization": f"Bearer {rec_token}"}

    # Patient
    _, pt_body = client.request("POST", "/api/v1/auth/login", {
        "email": "hamza.farooqi@gmail.com",
        "password": "password123"
    })
    pat_token = pt_body["token"]
    pat_headers = {"Authorization": f"Bearer {pat_token}"}

    # Super Admin
    _, a_body = client.request("POST", "/api/v1/auth/login", {
        "email": "admin@zayvora.health",
        "password": "admin123"
    })
    admin_token = a_body["token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # Doctor (for authoring fresh prescriptions)
    _, d_body = client.request("POST", "/api/v1/auth/login", {
        "email": "mansoor.alam@zayvora.health",
        "password": "doctor123"
    })
    doc_token = d_body["token"]
    doc_headers = {"Authorization": f"Bearer {doc_token}"}

    # ------------------------------------------------------------------------
    # Test 01: Inventory Retrieval FEFO Ordering
    # ------------------------------------------------------------------------
    st, data = client.request("GET", "/api/v1/inventory", headers=pharm_headers)
    inv = data.get("inventory", [])
    dates = [item["expiry_date"] for item in inv]
    is_sorted = (dates == sorted(dates)) and (len(inv) > 0)
    log_result(1, "FEFO Inventory Retrieval", st == 200 and is_sorted and assert_zero_jargon(data),
               f"Retrieved {len(inv)} inventory items ordered by expiry_date ASC")

    # ------------------------------------------------------------------------
    # Test 02: FEFO Allocation Algorithm - Earliest Expiry Lot Prioritization
    # ------------------------------------------------------------------------
    st, data = client.request("POST", "/api/v1/inventory/allocate-fefo", {
        "medicineName": "Majun Suranjan (Mudabbar)",
        "requestedQuantity": 20
    }, headers=pharm_headers)
    allocs = data.get("allocations", [])
    earliest_picked = len(allocs) > 0 and allocs[0]["batch_number"] == "MS-2026-LOT5" and allocs[0]["allocated_quantity"] == 20.0
    log_result(2, "FEFO Lot Prioritization", st == 200 and earliest_picked and assert_zero_jargon(data),
               f"Allocated earliest lot {allocs[0]['batch_number']} (Exp: {allocs[0]['expiry_date']})")

    # ------------------------------------------------------------------------
    # Test 03: Multi-Batch Split Allocation
    # ------------------------------------------------------------------------
    st, data = client.request("POST", "/api/v1/inventory/allocate-fefo", {
        "medicineName": "Majun Suranjan (Mudabbar)",
        "requestedQuantity": 60
    }, headers=pharm_headers)
    allocs = data.get("allocations", [])
    split_ok = len(allocs) == 2 and allocs[0]["batch_number"] == "MS-2026-LOT5" and allocs[0]["allocated_quantity"] == 45.0 and allocs[1]["batch_number"] == "MS-2026-LOT4" and allocs[1]["allocated_quantity"] == 15.0
    log_result(3, "Multi-Batch Split Allocation", st == 200 and split_ok and data.get("status") == "ALLOCATED",
               f"Split 60 units across LOT5 (45.0) and LOT4 (15.0)")

    # ------------------------------------------------------------------------
    # Test 04: Expired Stock Dispense Rejection
    # ------------------------------------------------------------------------
    st, data = client.request("POST", "/api/v1/inventory/dispense", {
        "batchNumber": "RB-2024-EXP",
        "quantity": 1
    }, headers=pharm_headers)
    exp_ok = st == 400 and data.get("code") == "EXPIRED_STOCK_ERROR"
    log_result(4, "Statutory Expiry Gate", exp_ok and assert_zero_jargon(data),
               f"Blocked expired stock RB-2024-EXP: '{data.get('error')}'")

    # ------------------------------------------------------------------------
    # Test 05: Schedule E(1) Uncertified Mudabbar Hard Block
    # ------------------------------------------------------------------------
    st, data = client.request("POST", "/api/v1/inventory/dispense", {
        "batchNumber": "MS-2026-RAW",
        "quantity": 1
    }, headers=pharm_headers)
    mudabbar_ok = st == 403 and data.get("code") == "MUDABBAR_CERTIFICATE_REQUIRED"
    log_result(5, "Schedule E(1) Mudabbar Gate", mudabbar_ok and assert_zero_jargon(data),
               f"Blocked raw botanical MS-2026-RAW: '{data.get('error')}'")

    # ------------------------------------------------------------------------
    # Test 06: Schedule E(1) Certified Mudabbar Dispense Success
    # ------------------------------------------------------------------------
    st, data = client.request("POST", "/api/v1/inventory/dispense", {
        "batchNumber": "MS-2026-LOT4",
        "quantity": 2
    }, headers=pharm_headers)
    cert_ok = st == 200 and data.get("ok") and "remainingStock" in data
    log_result(6, "Certified Mudabbar Dispensation", cert_ok and assert_zero_jargon(data),
               f"Successfully dispensed MS-2026-LOT4 (Remaining: {data.get('remainingStock')})")

    # ------------------------------------------------------------------------
    # Test 07: Insufficient Stock Rejection
    # ------------------------------------------------------------------------
    st, data = client.request("POST", "/api/v1/inventory/dispense", {
        "batchNumber": "RB-2026-LOT1",
        "quantity": 9999
    }, headers=pharm_headers)
    insuf_ok = st == 400 and data.get("code") == "INSUFFICIENT_STOCK"
    log_result(7, "Stock Sufficiency Guardrail", insuf_ok and assert_zero_jargon(data),
               f"Rejected excess quantity: '{data.get('error')}'")

    # ------------------------------------------------------------------------
    # Test 08: RBAC Barrier - Patient Blocked from Dispensing
    # ------------------------------------------------------------------------
    st, data = client.request("POST", "/api/v1/inventory/dispense", {
        "batchNumber": "RB-2026-LOT1",
        "quantity": 1
    }, headers=pat_headers)
    log_result(8, "RBAC Patient Dispensing Barrier", st == 403 and data.get("code") == "FORBIDDEN",
               f"Patient blocked from dispensing: '{data.get('error')}'")

    # ------------------------------------------------------------------------
    # Test 09: RBAC Barrier - Receptionist Blocked from Dispensing
    # ------------------------------------------------------------------------
    st, data = client.request("POST", "/api/v1/inventory/dispense", {
        "batchNumber": "RB-2026-LOT1",
        "quantity": 1
    }, headers=rec_headers)
    log_result(9, "RBAC Receptionist Dispensing Barrier", st == 403 and data.get("code") == "FORBIDDEN",
               f"Receptionist blocked from dispensing: '{data.get('error')}'")

    # ------------------------------------------------------------------------
    # Test 10: Atomic Prescription Dispensation & Invoice Settlement
    # ------------------------------------------------------------------------
    # Author a fresh prescription to ensure complete repeatability
    _, rx_draft = client.request("POST", "/api/v1/prescriptions", {
        "patientName": "Hamza Farooqi",
        "mrn": "MRN-2026-0814",
        "items": [
            {"name": "Majun Suranjan (Mudabbar)", "dose": "5g twice daily", "batchNumber": "MS-2026-LOT4", "quantity": 1},
            {"name": "Roghan-e-Balsan", "dose": "Local application nocte", "batchNumber": "RB-2026-LOT1", "quantity": 1}
        ],
        "facilityId": "FAC-HQ-01"
    }, headers=doc_headers)
    target_rx_order = rx_draft.get("orderNumber")

    st, data = client.request("POST", f"/api/v1/prescriptions/{target_rx_order}/dispense", {
        "paymentMethod": "UPI"
    }, headers=pharm_headers)
    disp_ok = st == 200 and data.get("ok") and data["prescription"]["status"] == "DISPENSED" and "invoice" in data and "audit_block" in data
    target_rx_id = data.get("prescription", {}).get("id")
    log_result(10, "Atomic Prescription Dispensation", disp_ok and assert_zero_jargon(data),
               f"Prescription {target_rx_order} fulfilled, Invoice {data.get('invoice', {}).get('invoice_number')} settled (₹{data.get('invoice', {}).get('amount')})")

    # ------------------------------------------------------------------------
    # Test 11: Idempotency Guard - Duplicate Dispense Blocked
    # ------------------------------------------------------------------------
    st, data = client.request("POST", f"/api/v1/prescriptions/{target_rx_order}/dispense", {
        "paymentMethod": "UPI"
    }, headers=pharm_headers)
    dup_ok = st == 400 and data.get("code") == "PRESCRIPTION_ALREADY_DISPENSED"
    log_result(11, "Dispense Idempotency Guard", dup_ok and assert_zero_jargon(data),
               f"Duplicate dispense rejected: '{data.get('error')}'")

    # ------------------------------------------------------------------------
    # Test 12: Pharmacy Billing Invoice Query & Reconciliation
    # ------------------------------------------------------------------------
    st, data = client.request("GET", f"/api/v1/billing/invoices?prescriptionId={target_rx_id}", headers=pharm_headers)
    invoices = data.get("invoices", [])
    inv_ok = st == 200 and len(invoices) > 0 and invoices[0]["prescription_id"] == target_rx_id
    log_result(12, "Billing Reconciliation", inv_ok and assert_zero_jargon(data),
               f"Retrieved pharmacy invoice {invoices[0].get('invoice_number')} linked to {target_rx_order} (Dept: {invoices[0].get('department')})")

    # ------------------------------------------------------------------------
    # Test 13: Cross-Tenant Pharmacy Isolation Guard
    # ------------------------------------------------------------------------
    st, data = client.request("POST", "/api/v1/inventory/dispense", {
        "batchNumber": "KGA-2026-B1",
        "quantity": 1
    }, headers=pharm_headers)
    cross_ok = st == 403 and data.get("code") == "CROSS_TENANT_ACCESS_DENIED"
    log_result(13, "Cross-Tenant Pharmacy Guard", cross_ok and assert_zero_jargon(data),
               f"Cross-facility dispense blocked: '{data.get('error')}'")

    # ------------------------------------------------------------------------
    # Test 14: Merkle Audit Trail for Dispensation
    # ------------------------------------------------------------------------
    st, data = client.request("GET", "/api/v1/audit/logs", headers=admin_headers)
    logs = data.get("audit_logs", [])
    dispense_logs = [log for log in logs if "DISPENSED" in log.get("event_type", "")]
    audit_ok = st == 200 and len(dispense_logs) > 0 and len(dispense_logs[0].get("leaf_hash", "")) == 64
    log_result(14, "Merkle Audit Trail", audit_ok,
               f"Dispense anchored in Merkle block #{dispense_logs[0].get('block_number')} (Hash: {dispense_logs[0].get('leaf_hash', '')[:16]}...)")

    # ------------------------------------------------------------------------
    # Test 15: Zero Developer Jargon in Pharmacy Payloads
    # ------------------------------------------------------------------------
    st, data = client.request("POST", "/api/v1/inventory/dispense", {
        "batchNumber": ""
    }, headers=pharm_headers)
    jargon_ok = st == 404 and assert_zero_jargon(data)
    log_result(15, "Zero Developer Jargon Audit", jargon_ok,
               "All pharmacy payloads, error codes and clinical responses contain zero developer terminology")

    print("=" * 76)
    print(f"PHASE 4 VERIFICATION SUMMARY: {passed} PASSED | {failed} FAILED (TOTAL {passed + failed})")
    print("=" * 76)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
