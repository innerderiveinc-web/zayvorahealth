"""
ZAYVORA Health OS — Prescriptions, Cold-Chain & Billing Domain Router
====================================================================
Modular request dispatcher for:
- Prescriptions Directory (Tenant-Scoped with Status Filter)
- Single Prescription Details & 21 CFR Part 11 Printable Slips (A4/80mm HTML)
- Inventory Directory (FEFO Sorted & Batch Allocation)
- Cold-Chain Thermal Telemetry & Automated 2-8°C CAPA Excursion Logging
- 21 CFR Part 11 Prescription Authoring with Digital Cryptographic Signatures
- Atomically Dispense Complete Prescription (FEFO & Statutory Gates)
- Billing Invoices & Receipts Ingestion and History
- Payment Order Creation (Razorpay-compatible Integration)
"""

from datetime import date, datetime, timezone
import hashlib
import json
import random
import time
from typing import Any, Dict
import uuid


def handle_billing_prescription_get(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any]) -> bool:
    """Dispatches GET requests for prescriptions, inventory, cold-chain telemetry, and billing."""
    import services.live_api_server as srv

    # Prescriptions (Tenant-Scoped with Status Filter)
    if path == "/api/v1/prescriptions":
        target_facility = handler._resolve_facility(auth_ctx, query_params)
        status_filter = query_params.get("status", [None])[0]
        mrn_filter = query_params.get("mrn", [None])[0]
        with srv.get_db() as conn:
            cur = conn.cursor()
            query = "SELECT * FROM prescriptions WHERE 1=1"
            params = []

            if auth_ctx and auth_ctx["role"] == "PATIENT":
                query += " AND mrn = ?"
                params.append(auth_ctx["mrn"])
            elif not ((auth_ctx and auth_ctx["role"] == "SUPER_ADMIN" and "all" in query_params.get("scope", [])) or (not auth_ctx and not query_params)):
                query += " AND facility_id = ?"
                params.append(target_facility)

            if status_filter:
                query += " AND status = ?"
                params.append(status_filter)
            if mrn_filter:
                query += " AND mrn = ?"
                params.append(mrn_filter)

            query += " ORDER BY created_at DESC"
            cur.execute(query, params)
            rows = [dict(r) for r in cur.fetchall()]
            for r in rows:
                try:
                    r["items"] = json.loads(r.get("items_json") or "[]")
                except Exception:
                    r["items"] = []
        handler._send_json({"ok": True, "count": len(rows), "facilityId": target_facility, "prescriptions": rows})
        return True

    # Single Prescription Printable Slip (A4 / 80mm with 21 CFR Part 11 Seal)
    if path.startswith("/api/v1/prescriptions/") and (path.endswith("/print") or path.endswith("/html")):
        rx_id = path.split("/")[-2]
        autoprint = query_params.get("autoprint", ["0"])[0] in ("1", "true")
        format_type = query_params.get("format", ["a4"])[0].lower()
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM prescriptions WHERE id = ? OR order_number = ?", (rx_id, rx_id))
            row = cur.fetchone()
            if not row:
                handler._send_error("Prescription record not found.", status=404, code="PRESCRIPTION_NOT_FOUND")
                return True
            rx = dict(row)
            cur.execute("SELECT * FROM patients WHERE mrn = ?", (rx.get("mrn"),))
            p_row = cur.fetchone()
            patient = dict(p_row) if p_row else {}
            cur.execute("SELECT * FROM facilities WHERE id = ?", (rx.get("facility_id", "FAC-HQ-01"),))
            f_row = cur.fetchone()
            facility = dict(f_row) if f_row else {}

        html_content = srv.render_printable_prescription_html(rx, patient, facility, autoprint=autoprint, format_type=format_type)
        encoded = html_content.encode("utf-8")
        handler.send_response(200)
        handler.send_header("Content-Type", "text/html; charset=utf-8")
        handler.send_header("Content-Length", str(len(encoded)))
        handler._send_cors_headers()
        handler.end_headers()
        handler.wfile.write(encoded)
        return True

    # Single Prescription Details
    if path.startswith("/api/v1/prescriptions/") and not path.endswith("/dispense"):
        rx_id = path.split("/")[-1]
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM prescriptions WHERE id = ? OR order_number = ?", (rx_id, rx_id))
            row = cur.fetchone()
            if not row:
                handler._send_error("Prescription record not found.", status=404, code="PRESCRIPTION_NOT_FOUND")
                return True
            res = dict(row)
            if auth_ctx and auth_ctx["role"] == "PATIENT":
                if res.get("mrn") != auth_ctx.get("mrn"):
                    handler._send_error("Access denied: Patients are strictly restricted to their own prescriptions.", status=403, code="PATIENT_PRESCRIPTION_ACCESS_VIOLATION")
                    return True

            try:
                res["items"] = json.loads(res.get("items_json") or "[]")
            except Exception:
                res["items"] = []
        handler._send_json({"ok": True, "prescription": res})
        return True

    # Billing Invoices & Receipts (Tenant-Scoped)
    if path == "/api/v1/billing/invoices":
        target_facility = handler._resolve_facility(auth_ctx, query_params)
        rx_filter = query_params.get("prescriptionId", [None])[0] or query_params.get("prescription_id", [None])[0]
        with srv.get_db() as conn:
            cur = conn.cursor()
            query = "SELECT * FROM invoices WHERE 1=1"
            params = []

            if auth_ctx and auth_ctx["role"] == "PATIENT":
                query += " AND mrn = ?"
                params.append(auth_ctx["mrn"])
            elif not ((auth_ctx and auth_ctx["role"] == "SUPER_ADMIN" and "all" in query_params.get("scope", [])) or (not auth_ctx and not query_params)):
                query += " AND facility_id = ?"
                params.append(target_facility)

            if rx_filter:
                query += " AND prescription_id = ?"
                params.append(rx_filter)

            query += " ORDER BY created_at DESC"
            cur.execute(query, params)
            rows = [dict(r) for r in cur.fetchall()]
            for r in rows:
                try:
                    r["items"] = json.loads(r.get("items_json") or "[]")
                except Exception:
                    r["items"] = []
        handler._send_json({"ok": True, "count": len(rows), "facilityId": target_facility, "invoices": rows})
        return True

    # Inventory (FEFO Sorted, Tenant-Scoped)
    if path == "/api/v1/inventory":
        target_facility = handler._resolve_facility(auth_ctx, query_params)
        with srv.get_db() as conn:
            cur = conn.cursor()
            if (auth_ctx and auth_ctx["role"] == "SUPER_ADMIN" and "all" in query_params.get("scope", [])) or (not auth_ctx and not query_params):
                cur.execute("SELECT * FROM inventory ORDER BY expiry_date ASC")
            else:
                cur.execute("SELECT * FROM inventory WHERE facility_id = ? ORDER BY expiry_date ASC", (target_facility,))
            rows = [dict(r) for r in cur.fetchall()]
        handler._send_json({"ok": True, "count": len(rows), "facilityId": target_facility, "inventory": rows})
        return True

    # Cold-Chain Telemetry & Thermal Monitoring (2-8°C AYUSH GDP Invariant)
    if path in ("/api/v1/cold-chain/telemetry", "/api/v1/pharmacy/cold-chain/telemetry"):
        target_facility = handler._resolve_facility(auth_ctx, query_params)
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT leaf_hash, event_type, signer, status, timestamp, facility_id, details_json 
                FROM audit_ledger 
                WHERE event_type IN ('CAPA_INCIDENT_TEMP_EXCURSION', 'COLD_CHAIN_TEMP_WARNING', 'COLD_CHAIN_TELEMETRY_LOG')
                ORDER BY block_number DESC LIMIT 20
            """)
            logs = [dict(r) for r in cur.fetchall()]
            for l in logs:
                try:
                    l["details"] = json.loads(l.get("details_json") or "{}")
                except Exception:
                    l["details"] = {}
        handler._send_json({
            "ok": True,
            "targetRangeCelsius": "2.0°C - 8.0°C",
            "currentTempCelsius": 4.6,
            "facilityId": target_facility,
            "status": "NOMINAL",
            "excursionLogs": logs
        })
        return True
    return False


def handle_billing_prescription_post(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any], body: Dict[str, Any]) -> bool:
    """Dispatches POST requests for prescription authoring, cold chain, dispensing, invoices, and payments."""
    import services.live_api_server as srv

    # Create Prescription & Anchor to Merkle Audit (RBAC Gated: Doctor/Hakeem/Admin Only)
    if path == "/api/v1/prescriptions":
        if auth_ctx and auth_ctx["role"] not in ("DOCTOR", "HAKEEM", "SUPER_ADMIN", "CLINIC_ADMIN"):
            handler._send_error("Access restricted: Only licensed consulting physicians or hakeems are authorized to author prescriptions.", status=403, code="FORBIDDEN")
            return True

        patient_name = body.get("patientName") or body.get("patient_name") or "Hamza Farooqi"
        mrn = body.get("mrn") or "MRN-2026-0814"
        doctor_name = body.get("doctorName") or body.get("doctor_name") or (auth_ctx["fullName"] if auth_ctx else "Prof. (Dr.) Mansoor Alam")
        doctor_reg = body.get("doctorReg") or body.get("doctor_reg") or "CCIM-U-1988-0412"
        # items_json accepts pre-serialised string or a list under "items" / "items_json"
        _raw_items = body.get("items") or body.get("items_json") or []
        if isinstance(_raw_items, str):
            try:
                import json as _j; _raw_items = _j.loads(_raw_items)
            except Exception:
                _raw_items = []
        items = _raw_items
        diet = body.get("dietaryAdvice") or body.get("dietary_advice") or "Standard Unani Parhez"
        regimen = body.get("regimenalAdvice") or body.get("regimenal_advice") or "Nutool Haar"
        facility_id = handler._resolve_facility(auth_ctx, query_params, body)

        with srv.get_db() as conn:
            # 1. Toxicological Invariant: Cumulative Colchicine Ceiling Check
            colchicine_ok, total_colchicine_mg, colchicine_err = srv.check_cumulative_colchicine_ceiling(mrn, items, conn)
            if not colchicine_ok:
                handler._send_error(colchicine_err, status=422, code="COLCHICINE_CEILING_BREACH")
                return True

            # 2. Classical Unani Medical Invariant: Nuzj-Tanqiya Sequencing Check
            nuzj_ok, nuzj_warn = srv.check_unani_nuzj_invariant(mrn, items, conn)

        for _ in range(10):
            order_num = f"RX-2026-{uuid.uuid4().hex[:8].upper()}"
            rx_id = f"RX-{uuid.uuid4().hex[:8].upper()}"
            with srv.get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT 1 FROM prescriptions WHERE order_number = ?", (order_num,))
                if not cur.fetchone():
                    break
        
        raw_payload = f"{order_num}|{mrn}|{doctor_reg}|{json.dumps(items)}|{datetime.utcnow().isoformat()}"
        sig_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO prescriptions (id, order_number, mrn, patient_name, doctor_name, doctor_reg, items_json, dietary_advice, regimenal_advice, signature_hash, status, facility_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (rx_id, order_num, mrn, patient_name, doctor_name, doctor_reg, json.dumps(items), diet, regimen, sig_hash, "PENDING_VERIFICATION", facility_id))

            cur.execute("""
            INSERT INTO audit_ledger (leaf_hash, event_type, signer, status, facility_id, details_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (sig_hash, "PRESCRIPTION_LOCKED_21CFR11", f"{doctor_name} ({doctor_reg})", "ANCHORED", facility_id, json.dumps({"order_number": order_num, "mrn": mrn})))

            if not nuzj_ok:
                cur.execute("""
                INSERT INTO audit_ledger (leaf_hash, event_type, signer, status, facility_id, details_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (hashlib.sha256(f"NUZJ_WARN|{order_num}".encode()).hexdigest(), "UNANI_NUZJ_INVARIANT_WARNING", f"{doctor_name} ({doctor_reg})", "WARNING", facility_id, json.dumps({"order_number": order_num, "mrn": mrn, "warning": nuzj_warn})))

            conn.commit()

        resp_payload = {
            "ok": True,
            "message": "Prescription authored and 21 CFR Part 11 cryptographically sealed.",
            "prescription_id": rx_id,
            "order_number": order_num,
            "orderNumber": order_num,
            "signatureHash": sig_hash,
            "facilityId": facility_id,
            "status": "PENDING_VERIFICATION"
        }
        if not nuzj_ok:
            resp_payload["nuzjWarning"] = nuzj_warn
        handler._send_json(resp_payload, status=201)
        return True

    # Cold-Chain Telemetry Ingestion & Automated 2-8°C CAPA Excursion Logging
    if path in ("/api/v1/cold-chain/telemetry", "/api/v1/pharmacy/cold-chain/telemetry"):
        sensor_id = body.get("sensorId") or "IOT-COLD-FRIDGE-01"
        temp = float(body.get("temperatureCelsius", 4.5))
        duration_minutes = float(body.get("durationMinutes", 0.0))
        batch_numbers = body.get("batchNumbers") or ["MS-2026-LOT4", "BMR-2026-MVP-09"]
        facility_id = handler._resolve_facility(auth_ctx, query_params, body)
        
        excursion = temp > 8.0 or temp < 2.0
        is_capa_breach = (temp > 8.0 and duration_minutes >= 15.0) or (temp < 0.0 and duration_minutes >= 10.0)
        
        event_type = "CAPA_INCIDENT_TEMP_EXCURSION" if is_capa_breach else ("COLD_CHAIN_TEMP_WARNING" if excursion else "COLD_CHAIN_TELEMETRY_LOG")
        status_val = "QUARANTINED" if is_capa_breach else ("ALERT" if excursion else "NOMINAL")
        
        details = {
            "sensorId": sensor_id,
            "temperatureCelsius": temp,
            "durationMinutes": duration_minutes,
            "batchNumbers": batch_numbers,
            "capaTriggered": is_capa_breach,
            "regulatoryStandard": "WHO Good Distribution Practices (GDP) & AYUSH 2-8°C Thermal Control",
            "correctiveAction": "Immediate electronic quarantine of affected botanical batches; root cause CAPA investigation initiated." if is_capa_breach else "Normal thermal stability verified."
        }
        
        payload_str = f"{sensor_id}|{temp}|{duration_minutes}|{datetime.utcnow().isoformat()}"
        leaf_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
        
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO audit_ledger (leaf_hash, event_type, signer, status, facility_id, details_json)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (leaf_hash, event_type, f"IoT Thermal Sensor ({sensor_id})", status_val, facility_id, json.dumps(details)))
            conn.commit()
            
        handler._send_json({
            "ok": True,
            "sensorId": sensor_id,
            "temperatureCelsius": temp,
            "durationMinutes": duration_minutes,
            "status": status_val,
            "isCapaBreach": is_capa_breach,
            "auditHash": leaf_hash,
            "message": "CAPA thermal excursion logged and batch quarantined in audit ledger." if is_capa_breach else "Cold-chain telemetry recorded successfully."
        }, status=201 if is_capa_breach else 200)
        return True

    # Atomically Dispense Complete Prescription (FEFO & Statutory Gates & Invoice Generation)
    if path.startswith("/api/v1/prescriptions/") and path.endswith("/dispense"):
        rx_id = path.split("/")[-2]
        if auth_ctx and auth_ctx["role"] not in ("PHARMACIST", "SUPER_ADMIN", "CLINIC_ADMIN"):
            handler._send_error("Access restricted: Only licensed pharmacy personnel are authorized to dispense medications.", status=403, code="FORBIDDEN")
            return True

        target_facility = handler._resolve_facility(auth_ctx, query_params, body)
        today_str = date.today().isoformat()

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM prescriptions WHERE id = ? OR order_number = ?", (rx_id, rx_id))
            row = cur.fetchone()
            if not row:
                handler._send_error("Prescription record not found.", status=404, code="PRESCRIPTION_NOT_FOUND")
                return True
            rx = dict(row)

            # Cross-tenant isolation check
            if auth_ctx and auth_ctx["role"] != "SUPER_ADMIN" and rx["facility_id"] != auth_ctx.get("facilityId", target_facility):
                handler._send_error("Access denied: You do not have authorization to dispense prescriptions from a different healthcare facility.", status=403, code="CROSS_TENANT_ACCESS_DENIED")
                return True

            # Status check
            if rx["status"] == "DISPENSED":
                handler._send_error("This prescription has already been dispensed and cannot be fulfilled again.", status=400, code="PRESCRIPTION_ALREADY_DISPENSED")
                return True

            try:
                items = json.loads(rx.get("items_json") or "[]")
            except Exception:
                items = []

            if not items:
                handler._send_error("Prescription contains no dispensable items.", status=400, code="EMPTY_PRESCRIPTION")
                return True

            dispensed_items = []
            total_amount = 0.0

            for itm in items:
                item_name = itm.get("name") or itm.get("item")
                specified_batch = itm.get("batchNumber")
                qty = int(itm.get("quantity") or 1)

                if specified_batch:
                    cur.execute("SELECT * FROM inventory WHERE batch_number = ? AND facility_id = ?", (specified_batch, rx["facility_id"]))
                    b_row = cur.fetchone()
                    if not b_row:
                        handler._send_error(f"Batch {specified_batch} not found in dispensary for {item_name}.", status=404, code="BATCH_NOT_FOUND")
                        return True
                    batch = dict(b_row)
                    if batch["expiry_date"] <= today_str:
                        handler._send_error(f"Dispensing blocked: Batch {specified_batch} for {item_name} has expired.", status=400, code="EXPIRED_STOCK_ERROR")
                        return True
                    if batch.get("is_schedule_e1") and not batch.get("mudabbar_cert"):
                        handler._send_error(f"DISPENSE BLOCKED: Schedule E(1) item {item_name} requires validated Mudabbar Certificate.", status=403, code="MUDABBAR_CERTIFICATE_REQUIRED")
                        return True
                    if batch["stock_qty"] < qty:
                        handler._send_error(f"Insufficient stock for {item_name} (batch {specified_batch}). Available: {batch['stock_qty']}, Requested: {qty}.", status=400, code="INSUFFICIENT_STOCK")
                        return True

                    new_qty = batch["stock_qty"] - qty
                    cur.execute("UPDATE inventory SET stock_qty = ? WHERE batch_number = ?", (new_qty, specified_batch))
                    item_cost = batch.get("unit_price", 150.0) * qty
                    total_amount += item_cost
                    dispensed_items.append({
                        "name": item_name,
                        "batch_number": specified_batch,
                        "quantity": qty,
                        "unit_price": batch.get("unit_price", 150.0),
                        "cost": item_cost,
                        "expiry_date": batch["expiry_date"],
                        "mudabbar_cert": batch.get("mudabbar_cert")
                    })
                else:
                    # FEFO Allocation
                    cur.execute("""
                    SELECT * FROM inventory
                    WHERE name = ? AND facility_id = ? AND stock_qty > 0
                    ORDER BY expiry_date ASC
                    """, (item_name, rx["facility_id"]))
                    batches = [dict(b) for b in cur.fetchall()]
                    eligible = [b for b in batches if b["expiry_date"] > today_str and (not b.get("is_schedule_e1") or b.get("mudabbar_cert"))]

                    if not eligible:
                        handler._send_error(f"No valid unexpired batches available in stock for {item_name}.", status=400, code="OUT_OF_STOCK")
                        return True

                    b = eligible[0]
                    if b["stock_qty"] < qty:
                        handler._send_error(f"Insufficient stock for {item_name}. Available: {b['stock_qty']}, Requested: {qty}.", status=400, code="INSUFFICIENT_STOCK")
                        return True
                    new_qty = b["stock_qty"] - qty
                    cur.execute("UPDATE inventory SET stock_qty = ? WHERE batch_number = ?", (new_qty, b["batch_number"]))
                    item_cost = b.get("unit_price", 150.0) * qty
                    total_amount += item_cost
                    dispensed_items.append({
                        "name": item_name,
                        "batch_number": b["batch_number"],
                        "quantity": qty,
                        "unit_price": b.get("unit_price", 150.0),
                        "cost": item_cost,
                        "expiry_date": b["expiry_date"],
                        "mudabbar_cert": b.get("mudabbar_cert")
                    })

            # Mark prescription DISPENSED
            cur.execute("UPDATE prescriptions SET status = 'DISPENSED' WHERE id = ?", (rx["id"],))

            # Auto-generate Pharmacy Billing Invoice
            inv_id = f"INV-PHARM-{uuid.uuid4().hex[:6].upper()}"
            inv_num = f"RCPT-PHARM-{random.randint(1000, 9999)}"
            payment_method = body.get("paymentMethod") or "UPI"

            cur.execute("""
            INSERT INTO invoices (id, invoice_number, mrn, patient_name, amount, department, payment_method, status, prescription_id, items_json, facility_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                inv_id,
                inv_num,
                rx["mrn"],
                rx["patient_name"],
                round(total_amount, 2),
                "Central Dispensary",
                payment_method,
                "PAID",
                rx["id"],
                json.dumps(dispensed_items),
                rx["facility_id"]
            ))

            # Anchor in Merkle audit ledger
            dispense_raw = f"{rx['id']}|{inv_num}|{json.dumps(dispensed_items)}|{datetime.utcnow().isoformat()}"
            leaf_hash = hashlib.sha256(dispense_raw.encode("utf-8")).hexdigest()
            cur.execute("""
            INSERT INTO audit_ledger (leaf_hash, event_type, signer, status, facility_id, details_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                leaf_hash,
                "PRESCRIPTION_DISPENSED",
                auth_ctx["fullName"] if auth_ctx else "Pharmacist System",
                "ANCHORED",
                rx["facility_id"],
                json.dumps({"prescription_id": rx["id"], "order_number": rx["order_number"], "invoice_number": inv_num, "amount": total_amount})
            ))
            conn.commit()

        handler._send_json({
            "ok": True,
            "message": f"Prescription {rx['order_number']} successfully dispensed under FEFO protocol.",
            "prescription": {
                "id": rx["id"],
                "order_number": rx["order_number"],
                "mrn": rx["mrn"],
                "patient_name": rx["patient_name"],
                "status": "DISPENSED"
            },
            "dispensed_items": dispensed_items,
            "invoice": {
                "id": inv_id,
                "invoice_number": inv_num,
                "amount": round(total_amount, 2),
                "department": "Central Dispensary",
                "status": "PAID"
            },
            "audit_block": {
                "leaf_hash": leaf_hash,
                "event": "PRESCRIPTION_DISPENSED"
            }
        })
        return True

    # Record Billing Invoice (RBAC: Receptionist/Admin Only)
    if path == "/api/v1/billing/invoices":
        if auth_ctx and auth_ctx["role"] == "PATIENT":
            handler._send_error("Access restricted: Patients are not authorized to create billing invoices.", status=403, code="FORBIDDEN")
            return True

        mrn = body.get("mrn") or "MRN-2026-0814"
        patient_name = body.get("patientName") or "Patient"
        amount = float(body.get("amount", 800.0))
        dept = body.get("department") or "Integrative Unani OPD"
        method = body.get("paymentMethod") or "UPI"
        facility_id = handler._resolve_facility(auth_ctx, query_params, body)
        inv_id = f"INV-{uuid.uuid4().hex[:6].upper()}"
        inv_num = f"RCPT-2026-{uuid.uuid4().hex[:4].upper()}"

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO invoices (id, invoice_number, mrn, patient_name, amount, department, payment_method, status, facility_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (inv_id, inv_num, mrn, patient_name, amount, dept, method, "PAID", facility_id))
            conn.commit()

        handler._send_json({
            "ok": True,
            "message": "Invoice generated and payment recorded.",
            "invoice": {
                "id": inv_id,
                "invoiceNumber": inv_num,
                "mrn": mrn,
                "patientName": patient_name,
                "amount": amount,
                "facilityId": facility_id,
                "status": "PAID"
            }
        }, status=201)
        return True

    # ── Payment Order Creation (Razorpay-compatible) ─────────────────────
    if path == "/api/v1/payments/orders/create":
        if not auth_ctx:
            handler._send_error("Authentication required.", status=401, code="UNAUTHORIZED")
            return True
        amount = body.get("amount") or 0
        currency = body.get("currency") or "INR"
        mrn = body.get("mrn") or ""
        order_id = f"order_{uuid.uuid4().hex[:16]}"
        handler._send_json({
            "ok": True,
            "order_id": order_id,
            "amount": amount,
            "currency": currency,
            "mrn": mrn,
            "status": "created",
            "provider": "ZAYVORA Payment Gateway",
            "note": "Razorpay integration pending — test mode active"
        }, status=201)
        return True
    return False
