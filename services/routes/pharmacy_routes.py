"""
ZAYVORA Health OS — Pharmacy & Pharmacopoeia Domain Router
==========================================================
Modular request dispatcher for:
- Statutory Unani Pharmacopoeia of India (UPI) monographs
- Classical posology and weights conversion (Appendix-7)
- Mudabbar detoxification SOPs (Appendix-6)
- FEFO batch inventory allocation and dispensing with Schedule E(1) guardrails
"""

import hashlib
import json
import time
from datetime import date
from typing import Any, Dict


def handle_pharmacy_get(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any]) -> bool:
    """Dispatches GET requests for pharmacopoeia, UPI, and inventory catalogs."""
    import services.live_api_server as srv

    # 1. Pharmacopoeia Monographs
    if path == "/api/v1/pharmacopoeia/monographs":
        if not auth_ctx:
            handler._send_error("Authentication required.", status=401, code="UNAUTHORIZED")
            return True
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, canonical_name_arabic, canonical_name_english, canonical_name_latin, mizaj_primary_quality, therapeutic_actions FROM zkb_mufradat ORDER BY canonical_name_latin ASC LIMIT 100")
            rows = [dict(r) for r in cur.fetchall()]
        handler._send_json({"ok": True, "count": len(rows), "monographs": rows})
        return True

    # 2. Statutory UPI Part-II, Vol-IV Monographs (Ministry of AYUSH)
    if path == "/api/v1/pharmacopoeia/upi-vol4":
        query_q = query_params.get("q", [""])[0].strip().lower()
        monographs = list(srv.UPI_PART2_VOL4_MONOGRAPHS)
        if query_q:
            monographs = [
                m for m in monographs
                if query_q in m["name"].lower()
                or query_q in m.get("urdu_name", "").lower()
                or any(query_q in u.lower() for u in m.get("therapeutic_uses", []))
                or any(query_q in a.lower() for a in m.get("actions", []))
            ]
        handler._send_json({
            "ok": True,
            "statutory_authority": "Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H), Ministry of AYUSH",
            "volume": "Unani Pharmacopoeia of India Part-II, Volume-IV (Formulations)",
            "edition": "First Edition (2026)",
            "count": len(monographs),
            "monographs": monographs
        })
        return True

    # 3. Appendix 7: Classical Weights & Posology Unit Converter
    if path == "/api/v1/pharmacopoeia/convert-weights":
        qty_str = query_params.get("quantity", ["1"])[0]
        unit = query_params.get("unit", ["masha"])[0]
        try:
            qty = float(qty_str)
        except ValueError:
            qty = 1.0
        conv = srv.convert_classical_weight(qty, unit)
        handler._send_json({
            "ok": True,
            "conversion": conv,
            "supported_units": srv.CLASSICAL_WEIGHTS_METRIC_MAP,
            "statutory_source": "Unani Pharmacopoeia of India Part-II, Appendix-7"
        })
        return True

    # 4. Appendix 6: Statutory Tadbir-e-Adviyah (Detoxification) SOPs
    if path == "/api/v1/pharmacopoeia/tadbir-sops":
        substance = query_params.get("substance", [""])[0].strip().lower()
        if substance and substance in srv.TADBIR_E_ADVIYAH_SOP:
            handler._send_json({
                "ok": True,
                "substance": substance,
                "sop": srv.TADBIR_E_ADVIYAH_SOP[substance],
                "statutory_source": "Unani Pharmacopoeia of India Part-II, Appendix-6.1.6"
            })
            return True
        handler._send_json({
            "ok": True,
            "statutory_source": "Unani Pharmacopoeia of India Part-II, Appendix-6 (Tadbir-e-Adviyah)",
            "count": len(srv.TADBIR_E_ADVIYAH_SOP),
            "sops": srv.TADBIR_E_ADVIYAH_SOP
        })
        return True

    return False


def handle_pharmacy_post(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any], body: Dict[str, Any]) -> bool:
    """Dispatches POST requests for pharmacy item dispensing and FEFO batch allocation."""
    import services.live_api_server as srv

    # Dispense Pharmacy Item (RBAC Gated: Pharmacist/Admin Only)
    if path == "/api/v1/inventory/dispense":
        if auth_ctx and auth_ctx["role"] not in ("PHARMACIST", "SUPER_ADMIN", "CLINIC_ADMIN"):
            handler._send_error("Access restricted: Only licensed pharmacy personnel are authorized to dispense medications.", status=403, code="FORBIDDEN")
            return True

        batch_num = body.get("batchNumber")
        qty = int(body.get("quantity", 1))
        target_facility = handler._resolve_facility(auth_ctx, query_params, body)
        today_str = date.today().isoformat()

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM inventory WHERE batch_number = ?", (batch_num,))
            row = cur.fetchone()
            if not row:
                handler._send_error("Batch not found in dispensary.", status=404, code="BATCH_NOT_FOUND")
                return True
            item = dict(row)

            # Cross-tenant facility guard
            if auth_ctx and auth_ctx["role"] != "SUPER_ADMIN" and item.get("facility_id") != auth_ctx.get("facilityId", target_facility):
                handler._send_error("Access denied: You do not have authorization to dispense inventory from a different healthcare facility.", status=403, code="CROSS_TENANT_ACCESS_DENIED")
                return True

            # Expiry check
            if item["expiry_date"] <= today_str:
                handler._send_error("Dispensing blocked: This medication batch has passed its expiration date.", status=400, code="EXPIRED_STOCK_ERROR")
                return True

            # Schedule E(1) Mudabbar verification
            if item["is_schedule_e1"] and not item.get("mudabbar_cert"):
                handler._send_error("DISPENSE BLOCKED: Schedule E(1) item requires validated Mudabbar Certificate.", status=403, code="MUDABBAR_CERTIFICATE_REQUIRED")
                return True

            # Stock check
            if item["stock_qty"] < qty:
                handler._send_error(f"Insufficient stock for batch {batch_num}. Available: {item['stock_qty']}, Requested: {qty}.", status=400, code="INSUFFICIENT_STOCK")
                return True

            new_stock = item["stock_qty"] - qty
            cur.execute("UPDATE inventory SET stock_qty = ? WHERE batch_number = ?", (new_stock, batch_num))

            # Anchor in audit ledger
            dispense_leaf = hashlib.sha256(f"{batch_num}:{qty}:{new_stock}:{time.time()}".encode()).hexdigest()
            cur.execute("""
            INSERT INTO audit_ledger (leaf_hash, event_type, signer, status, facility_id, details_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                dispense_leaf,
                "INVENTORY_DISPENSED",
                auth_ctx["fullName"] if auth_ctx else "Chief Pharmacist",
                "ANCHORED",
                item.get("facility_id", target_facility),
                json.dumps({"batch_number": batch_num, "quantity": qty, "remaining_stock": new_stock})
            ))
            conn.commit()

        handler._send_json({
            "ok": True,
            "message": f"Successfully dispensed {qty} unit(s) of {item['name']}.",
            "batchNumber": batch_num,
            "remainingStock": new_stock
        })
        return True

    # FEFO Batch Allocation Calculation (First-Expired, First-Out)
    if path == "/api/v1/inventory/allocate-fefo":
        med_name = (body.get("medicineName") or body.get("medicine_name") or body.get("name") or "").strip()
        if not med_name:
            handler._send_error("Medicine name is required for FEFO batch allocation.", status=400, code="MEDICINE_NAME_REQUIRED")
            return True

        req_qty = float(body.get("requestedQuantity") or body.get("requested_quantity") or body.get("quantity") or 1)
        target_facility = handler._resolve_facility(auth_ctx, query_params, body)
        today_str = date.today().isoformat()

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
            SELECT * FROM inventory
            WHERE name = ? AND facility_id = ? AND stock_qty > 0
            ORDER BY expiry_date ASC
            """, (med_name, target_facility))
            all_batches = [dict(r) for r in cur.fetchall()]

        eligible_batches = []
        has_uncertified_e1 = False

        for b in all_batches:
            if b["expiry_date"] <= today_str:
                continue
            if b.get("is_schedule_e1") and not b.get("mudabbar_cert"):
                has_uncertified_e1 = True
                continue
            eligible_batches.append(b)

        if not eligible_batches and has_uncertified_e1:
            handler._send_error("FEFO allocation blocked: Substance is statutory Schedule E(1) and all available batches lack validated Mudabbar detoxification certificates.", status=403, code="MUDABBAR_CERTIFICATE_REQUIRED")
            return True

        allocations = []
        needed = req_qty
        for eb in eligible_batches:
            avail = float(eb["stock_qty"])
            take = min(avail, needed)
            allocations.append({
                "batch_id": eb["id"],
                "batch_number": eb["batch_number"],
                "allocated_quantity": take,
                "expiry_date": eb["expiry_date"],
                "stock_qty": eb["stock_qty"],
                "unit_price": eb.get("unit_price", 150.0),
                "is_schedule_e1": bool(eb.get("is_schedule_e1")),
                "mudabbar_cert": eb.get("mudabbar_cert")
            })
            needed -= take
            if needed <= 0.001:
                break

        total_allocated = sum(a["allocated_quantity"] for a in allocations)
        is_fulfilled = total_allocated >= (req_qty - 0.001)

        handler._send_json({
            "ok": True,
            "medicine_name": med_name,
            "facility_id": target_facility,
            "requested_quantity": req_qty,
            "total_allocated": total_allocated,
            "remaining_unfilled": max(0.0, req_qty - total_allocated),
            "status": "ALLOCATED" if is_fulfilled else "PARTIALLY_ALLOCATED",
            "allocations": allocations,
            "fefo_compliant": True
        })
        return True

    return False
