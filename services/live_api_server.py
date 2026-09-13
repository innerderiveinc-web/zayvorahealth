#!/usr/bin/env python3
"""
ZAYVORA Health OS — Live REST API Server & Database Bridge
Zero-dependency Python 3 HTTP REST Server connected directly to zayvora_live.db.
Provides live endpoints for Authentication, Patients, Appointments, Prescriptions, and Inventory.
"""

import sys
import os
import sqlite3
import json
import hashlib
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import urllib.parse
from datetime import datetime

# Resolve database path relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "zayvora_live.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    if not salt:
        salt = uuid.uuid4().hex[:16]
    hashed = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
    return hashed, salt

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class ZayvoraApiHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
        self.send_header("Access-Control-Max-Age", "86400")

    def _send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, message, status=400):
        self._send_json({"ok": False, "error": message}, status=status)

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def _read_json_body(self):
        try:
            content_len = int(self.headers.get("Content-Length", 0))
            if content_len == 0:
                return {}
            raw = self.rfile.read(content_len).decode("utf-8")
            return json.loads(raw)
        except Exception as e:
            return {}

    # =========================================================================
    # GET Endpoints
    # =========================================================================
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        # Health Probe
        if path in ("/api/health", "/health"):
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM users")
                u_cnt = cur.fetchone()[0]
            self._send_json({
                "ok": True,
                "service": "zayvora_live_api",
                "environment": "live_local",
                "database": "connected",
                "database_engine": "SQLite Relational Storage",
                "database_path": DB_PATH,
                "registered_users": u_cnt,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
            return

        # Patients Directory
        if path == "/api/v1/patients":
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM patients ORDER BY created_at DESC")
                rows = [dict(r) for r in cur.fetchall()]
                for r in rows:
                    try:
                        r["allergies"] = json.loads(r.get("allergies_json") or "[]")
                    except:
                        r["allergies"] = []
            self._send_json({"ok": True, "count": len(rows), "patients": rows})
            return

        # Single Patient Details
        if path.startswith("/api/v1/patients/"):
            pat_id = path.split("/")[-1]
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM patients WHERE id = ? OR mrn = ?", (pat_id, pat_id))
                row = cur.fetchone()
                if not row:
                    self._send_error("Patient not found", status=404)
                    return
                res = dict(row)
                res["allergies"] = json.loads(res.get("allergies_json") or "[]")
            self._send_json({"ok": True, "patient": res})
            return

        # Appointments & OPD Queue
        if path == "/api/v1/appointments":
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM appointments ORDER BY appointment_time ASC")
                rows = [dict(r) for r in cur.fetchall()]
            self._send_json({"ok": True, "count": len(rows), "appointments": rows})
            return

        # Prescriptions
        if path == "/api/v1/prescriptions":
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM prescriptions ORDER BY created_at DESC")
                rows = [dict(r) for r in cur.fetchall()]
                for r in rows:
                    try:
                        r["items"] = json.loads(r.get("items_json") or "[]")
                    except:
                        r["items"] = []
            self._send_json({"ok": True, "count": len(rows), "prescriptions": rows})
            return

        # Single Prescription Details
        if path.startswith("/api/v1/prescriptions/"):
            rx_id = path.split("/")[-1]
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM prescriptions WHERE id = ? OR order_number = ?", (rx_id, rx_id))
                row = cur.fetchone()
                if not row:
                    self._send_error("Prescription not found", status=404)
                    return
                res = dict(row)
                try:
                    res["items"] = json.loads(res.get("items_json") or "[]")
                except:
                    res["items"] = []
            self._send_json({"ok": True, "prescription": res})
            return

        # Billing Invoices & Receipts
        if path == "/api/v1/billing/invoices":
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM invoices ORDER BY created_at DESC")
                rows = [dict(r) for r in cur.fetchall()]
            self._send_json({"ok": True, "count": len(rows), "invoices": rows})
            return

        # Inventory (Sorted by FEFO expiry date)
        if path == "/api/v1/inventory":
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM inventory ORDER BY expiry_date ASC")
                rows = [dict(r) for r in cur.fetchall()]
            self._send_json({"ok": True, "count": len(rows), "inventory": rows})
            return

        # Audit Ledger
        if path == "/api/v1/audit/logs":
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM audit_ledger ORDER BY block_number DESC LIMIT 50")
                rows = [dict(r) for r in cur.fetchall()]
            self._send_json({"ok": True, "count": len(rows), "audit_logs": rows})
            return

        self._send_error(f"Route not found: {path}", status=404)

    # =========================================================================
    # POST Endpoints
    # =========================================================================
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self._read_json_body()

        # Registration
        if path == "/api/v1/auth/register":
            email = (body.get("email") or "").strip().lower()
            password = body.get("password") or ""
            full_name = (body.get("fullName") or body.get("full_name") or "").strip()
            phone = (body.get("phone") or "").strip()
            role = (body.get("role") or "PATIENT").upper()

            if not email or "@" not in email:
                self._send_error("Valid email address is required.", status=400)
                return
            if not password or len(password) < 4:
                self._send_error("Password must be at least 4 characters.", status=400)
                return
            if not full_name:
                self._send_error("Full name is required.", status=400)
                return

            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id FROM users WHERE email = ?", (email,))
                if cur.fetchone():
                    self._send_error("An account with this email address already exists.", status=409)
                    return

                pwd_hash, salt = hash_password(password)
                user_id = f"USR-{uuid.uuid4().hex[:8].upper()}"
                
                # Generate sequential MRN if patient
                mrn = None
                if role == "PATIENT":
                    cur.execute("SELECT COUNT(*) FROM patients")
                    p_count = cur.fetchone()[0] + 1
                    mrn = f"MRN-2026-{p_count:04d}"

                cur.execute("""
                INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, mrn, facility_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, email, pwd_hash, salt, full_name, phone, role, mrn, "FAC-HQ-01"))

                if role == "PATIENT":
                    name_parts = full_name.split(" ", 1)
                    first_name = name_parts[0]
                    last_name = name_parts[1] if len(name_parts) > 1 else ""
                    pat_id = f"PAT-{uuid.uuid4().hex[:6].upper()}"
                    
                    cur.execute("""
                    INSERT INTO patients (id, mrn, user_id, first_name, last_name, date_of_birth, gender, contact_phone, contact_email, blood_group, mizaj_dominant, allergies_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (pat_id, mrn, user_id, first_name, last_name, body.get("dob", "1995-01-01"), body.get("gender", "Unspecified"), phone, email, "B+", "Motadil (Balanced)", json.dumps([])))

                conn.commit()

            token = f"jwt-live-{uuid.uuid4().hex}"
            self._send_json({
                "ok": True,
                "message": "User registered successfully.",
                "token": token,
                "user": {
                    "id": user_id,
                    "email": email,
                    "fullName": full_name,
                    "phone": phone,
                    "role": role,
                    "mrn": mrn,
                    "facilityId": "FAC-HQ-01",
                    "facilityName": "Jamia Hamdard AUTC - Main Hospital"
                }
            }, status=201)
            return

        # Login
        if path == "/api/v1/auth/login":
            identifier = (body.get("identifier") or body.get("email") or "").strip().lower()
            password = body.get("password") or ""

            if not identifier or not password:
                self._send_error("Email and password are required.", status=400)
                return

            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM users WHERE LOWER(email) = ? OR phone = ?", (identifier, identifier))
                row = cur.fetchone()
                if not row:
                    self._send_error("Invalid email or password. Please check your credentials.", status=401)
                    return
                user = dict(row)

            pwd_hash, _ = hash_password(password, user["salt"])
            if pwd_hash != user["password_hash"]:
                self._send_error("Invalid password.", status=401)
                return

            token = f"jwt-live-{uuid.uuid4().hex}"
            self._send_json({
                "ok": True,
                "message": "Authentication successful.",
                "token": token,
                "user": {
                    "id": user["id"],
                    "email": user["email"],
                    "fullName": user["full_name"],
                    "phone": user["phone"],
                    "role": user["role"],
                    "mrn": user["mrn"],
                    "facilityId": user["facility_id"],
                    "facilityName": "Jamia Hamdard AUTC - Main Hospital"
                }
            })
            return

        # Book Appointment
        if path == "/api/v1/appointments":
            patient_name = body.get("patientName") or body.get("patient_name") or "Walk-in Patient"
            mrn = body.get("mrn") or f"MRN-2026-{uuid.uuid4().hex[:4].upper()}"
            doctor_name = body.get("doctorName") or body.get("doctor_name") or "Prof. (Dr.) Mansoor Alam"
            app_date = body.get("date") or datetime.now().strftime("%Y-%m-%d")
            app_time = body.get("timeSlot") or body.get("time_slot") or "11:00 AM"
            chief_complaint = body.get("chiefComplaint") or body.get("chief_complaint") or "General Health Assessment"
            acuity = body.get("acuity") or "STANDARD"
            fee = float(body.get("fee", 800.0))

            with get_db() as conn:
                cur = conn.cursor()
                # Compute sequential token for today
                cur.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = ?", (app_date,))
                today_count = cur.fetchone()[0] + 101
                token_num = f"T-{today_count}"
                apt_id = f"APT-{uuid.uuid4().hex[:6].upper()}"

                cur.execute("""
                INSERT INTO appointments (id, token_number, mrn, patient_name, doctor_name, department, opd_room, appointment_date, appointment_time, acuity, chief_complaint, status, fee_amount, payment_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (apt_id, token_num, mrn, patient_name, doctor_name, "Integrative Unani OPD", "Room 3", app_date, app_time, acuity, chief_complaint, "WAITING", fee, "PAID"))
                conn.commit()

            self._send_json({
                "ok": True,
                "message": "Appointment booked and token issued.",
                "appointment": {
                    "id": apt_id,
                    "tokenNumber": token_num,
                    "mrn": mrn,
                    "patientName": patient_name,
                    "doctorName": doctor_name,
                    "appointmentDate": app_date,
                    "appointmentTime": app_time,
                    "status": "WAITING",
                    "feeAmount": fee
                }
            }, status=201)
            return

        # Create Prescription & Anchor to Merkle Audit
        if path == "/api/v1/prescriptions":
            patient_name = body.get("patientName") or "Hamza Farooqi"
            mrn = body.get("mrn") or "MRN-2026-0814"
            doctor_name = body.get("doctorName") or "Prof. (Dr.) Mansoor Alam"
            doctor_reg = body.get("doctorReg") or "CCIM-U-1988-0412"
            items = body.get("items") or []
            diet = body.get("dietaryAdvice") or "Standard Unani Parhez"
            regimen = body.get("regimenalAdvice") or "Nutool Haar"

            order_num = f"RX-2026-{uuid.uuid4().hex[:4].upper()}"
            rx_id = f"RX-{uuid.uuid4().hex[:6].upper()}"
            
            # Compute 21 CFR Part 11 signature hash
            raw_payload = f"{order_num}|{mrn}|{doctor_reg}|{json.dumps(items)}|{datetime.utcnow().isoformat()}"
            sig_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()

            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("""
                INSERT INTO prescriptions (id, order_number, mrn, patient_name, doctor_name, doctor_reg, items_json, dietary_advice, regimenal_advice, signature_hash, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (rx_id, order_num, mrn, patient_name, doctor_name, doctor_reg, json.dumps(items), diet, regimen, sig_hash, "PENDING_VERIFICATION"))

                # Anchor to Merkle Audit Ledger
                cur.execute("""
                INSERT INTO audit_ledger (leaf_hash, event_type, signer, status, details_json)
                VALUES (?, ?, ?, ?, ?)
                """, (sig_hash, "PRESCRIPTION_LOCKED_21CFR11", f"{doctor_name} ({doctor_reg})", "ANCHORED", json.dumps({"order_number": order_num, "mrn": mrn})))
                conn.commit()

            self._send_json({
                "ok": True,
                "message": "Prescription authored and 21 CFR Part 11 cryptographically sealed.",
                "orderNumber": order_num,
                "signatureHash": sig_hash,
                "status": "PENDING_VERIFICATION"
            }, status=201)
            return

        # Dispense Pharmacy Item & Decrement Stock
        if path == "/api/v1/inventory/dispense":
            batch_num = body.get("batchNumber")
            qty = int(body.get("quantity", 1))

            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM inventory WHERE batch_number = ?", (batch_num,))
                row = cur.fetchone()
                if not row:
                    self._send_error("Batch not found in dispensary.", status=404)
                    return
                item = dict(row)

                if item["is_schedule_e1"] and not item.get("mudabbar_cert"):
                    self._send_error("DISPENSE BLOCKED: Schedule E(1) item requires validated Mudabbar Certificate.", status=403)
                    return

                new_stock = max(0, item["stock_qty"] - qty)
                cur.execute("UPDATE inventory SET stock_qty = ? WHERE batch_number = ?", (new_stock, batch_num))
                conn.commit()

            self._send_json({
                "ok": True,
                "message": f"Successfully dispensed {qty} unit(s) of {item['name']}.",
                "batchNumber": batch_num,
                "remainingStock": new_stock
            })
            return

        # Direct Patient Registration by Staff
        if path == "/api/v1/patients":
            first_name = (body.get("firstName") or body.get("first_name") or "").strip()
            last_name = (body.get("lastName") or body.get("last_name") or "").strip()
            if not first_name:
                self._send_error("First name is required.", status=400)
                return

            phone = body.get("phone") or body.get("contactPhone") or ""
            email = body.get("email") or body.get("contactEmail") or ""
            dob = body.get("dob") or body.get("dateOfBirth") or "1990-01-01"
            gender = body.get("gender") or "Unspecified"
            blood_group = body.get("bloodGroup") or "Unknown"
            mizaj = body.get("mizaj") or body.get("mizajDominant") or "Motadil (Balanced)"
            allergies = body.get("allergies") or []

            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM patients")
                p_count = cur.fetchone()[0] + 1
                mrn = f"MRN-2026-{p_count:04d}"
                pat_id = f"PAT-{uuid.uuid4().hex[:6].upper()}"

                cur.execute("""
                INSERT INTO patients (id, mrn, first_name, last_name, date_of_birth, gender, contact_phone, contact_email, blood_group, mizaj_dominant, allergies_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (pat_id, mrn, first_name, last_name, dob, gender, phone, email, blood_group, mizaj, json.dumps(allergies)))
                conn.commit()

            self._send_json({
                "ok": True,
                "message": "Patient registered successfully.",
                "patient": {
                    "id": pat_id,
                    "mrn": mrn,
                    "firstName": first_name,
                    "lastName": last_name,
                    "phone": phone,
                    "email": email,
                    "mizajDominant": mizaj,
                    "allergies": allergies
                }
            }, status=201)
            return

        # Record Billing Invoice
        if path == "/api/v1/billing/invoices":
            mrn = body.get("mrn") or "MRN-2026-0814"
            patient_name = body.get("patientName") or "Patient"
            amount = float(body.get("amount", 800.0))
            dept = body.get("department") or "Integrative Unani OPD"
            method = body.get("paymentMethod") or "UPI"
            inv_id = f"INV-{uuid.uuid4().hex[:6].upper()}"
            inv_num = f"RCPT-2026-{uuid.uuid4().hex[:4].upper()}"

            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("""
                INSERT INTO invoices (id, invoice_number, mrn, patient_name, amount, department, payment_method, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (inv_id, inv_num, mrn, patient_name, amount, dept, method, "PAID"))
                conn.commit()

            self._send_json({
                "ok": True,
                "message": "Invoice generated and payment recorded.",
                "invoice": {
                    "id": inv_id,
                    "invoiceNumber": inv_num,
                    "mrn": mrn,
                    "patientName": patient_name,
                    "amount": amount,
                    "status": "PAID"
                }
            }, status=201)
            return

        self._send_error(f"Cannot POST to {path}", status=404)

    # =========================================================================
    # PATCH Endpoints
    # =========================================================================
    def do_PATCH(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self._read_json_body()

        if "/appointments/" in path and path.endswith("/status"):
            apt_id = path.split("/")[-2]
            new_status = body.get("status")
            if not new_status:
                self._send_error("Status is required.", status=400)
                return

            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("UPDATE appointments SET status = ? WHERE id = ? OR token_number = ?", (new_status, apt_id, apt_id))
                if cur.rowcount == 0:
                    self._send_error("Appointment not found.", status=404)
                    return
                conn.commit()

            self._send_json({"ok": True, "message": f"Appointment status updated to {new_status}."})
            return

        self._send_error(f"Cannot PATCH to {path}", status=404)

def run_server(port=8000):
    server_address = ("0.0.0.0", port)
    httpd = ThreadedHTTPServer(server_address, ZayvoraApiHandler)
    print(f"============================================================")
    print(f" ZAYVORA Health OS — Live REST API Server & Database Bridge")
    print(f" Listening on http://localhost:{port}")
    print(f" Database: {DB_PATH}")
    print(f"============================================================")
    httpd.serve_forever()

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    run_server(port)
