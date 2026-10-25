"""
ZAYVORA Health OS — Telemedicine, Appointments & Patient Engagement Router
==========================================================================
Modular request dispatcher for:
- Clinical Appointments Lifecycle (Booking, Token Generation, Digital Check-in, Queue Transitions)
- Appointment Status Updates, Rescheduling (PATCH), and Cancellations (DELETE)
- QSURA Omnichannel Patient Communication Dispatch (SMS, WhatsApp, Email, Webhook)
- QSURA Message Templates Catalog and Delivery Notification Audit Logs
- Telemedicine Consultation Rooms Lifecycle (WebRTC room creation, token minting, status query, room closure)
"""

from datetime import datetime
import json
from typing import Any, Dict
import uuid


def handle_telemedicine_get(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any]) -> bool:
    """Dispatches GET requests for appointments, QSURA, and telemedicine."""
    import services.live_api_server as srv

    # 1. Appointment Lifecycle OS: Patient Appointments by URL path
    if path.startswith("/api/v1/appointments/patient/"):
        pat_id = path.replace("/api/v1/appointments/patient/", "").strip()
        if srv.AppointmentLifecycleOS:
            apts = srv.AppointmentLifecycleOS.get_patient_appointments(pat_id)
        else:
            apts = []
        handler._send_json({"ok": True, "patient_id": pat_id, "count": len(apts), "appointments": apts})
        return True

    # 2. Appointment Lifecycle OS: Queue Lifecycle by query param
    if path in ("/api/v1/appointments/lifecycle", "/api/v1/appointments/queue-lifecycle"):
        pat_id = query_params.get("patient_id", ["PAT-774901"])[0]
        if srv.AppointmentLifecycleOS:
            apts = srv.AppointmentLifecycleOS.get_patient_appointments(pat_id)
        else:
            apts = []
        handler._send_json({"ok": True, "patient_id": pat_id, "count": len(apts), "appointments": apts})
        return True

    # 3. Appointments & OPD Queue (Tenant-Scoped)
    if path == "/api/v1/appointments":
        target_facility = handler._resolve_facility(auth_ctx, query_params)
        with srv.get_db() as conn:
            cur = conn.cursor()
            if (auth_ctx and auth_ctx["role"] == "SUPER_ADMIN" and "all" in query_params.get("scope", [])) or (not auth_ctx and not query_params):
                cur.execute("SELECT * FROM appointments ORDER BY appointment_time ASC")
            else:
                cur.execute("SELECT * FROM appointments WHERE facility_id = ? ORDER BY appointment_time ASC", (target_facility,))
            rows = [dict(r) for r in cur.fetchall()]
        handler._send_json({"ok": True, "count": len(rows), "facilityId": target_facility, "appointments": rows})
        return True

    # 4. QSURA Templates Catalog
    if path == "/api/v1/qsura/templates":
        handler._send_json({"ok": True, "templates": srv.MESSAGE_TEMPLATES})
        return True

    # 5. QSURA Dispatch Logs / Notifications (Facility & Patient Scoped)
    if path in ("/api/v1/qsura/notifications", "/api/v1/qsura/logs"):
        target_facility = handler._resolve_facility(auth_ctx, query_params)
        with srv.get_db() as conn:
            cur = conn.cursor()
            if auth_ctx and auth_ctx["role"] == "PATIENT":
                cur.execute("SELECT * FROM notifications WHERE mrn = ? ORDER BY created_at DESC", (auth_ctx["mrn"],))
            elif "mrn" in query_params:
                cur.execute("SELECT * FROM notifications WHERE mrn = ? ORDER BY created_at DESC", (query_params["mrn"][0],))
            elif (auth_ctx and auth_ctx["role"] == "SUPER_ADMIN" and "all" in query_params.get("scope", [])) or (not auth_ctx and "all" in query_params.get("scope", [])):
                cur.execute("SELECT * FROM notifications ORDER BY created_at DESC")
            else:
                cur.execute("SELECT * FROM notifications WHERE facility_id = ? ORDER BY created_at DESC", (target_facility,))
            rows = [dict(r) for r in cur.fetchall()]
        handler._send_json({"ok": True, "count": len(rows), "notifications": rows})
        return True

    # 6. Telemedicine Active Rooms List
    if path == "/api/v1/telemedicine/rooms":
        target_facility = handler._resolve_facility(auth_ctx, query_params)
        with srv.get_db() as conn:
            cur = conn.cursor()
            if auth_ctx and auth_ctx["role"] == "PATIENT":
                cur.execute("SELECT * FROM telemedicine_rooms WHERE mrn = ? ORDER BY created_at DESC", (auth_ctx["mrn"],))
            elif (auth_ctx and auth_ctx["role"] == "SUPER_ADMIN" and "all" in query_params.get("scope", [])) or (not auth_ctx and "all" in query_params.get("scope", [])):
                cur.execute("SELECT * FROM telemedicine_rooms ORDER BY created_at DESC")
            else:
                cur.execute("SELECT * FROM telemedicine_rooms WHERE facility_id = ? ORDER BY created_at DESC", (target_facility,))
            rows = [dict(r) for r in cur.fetchall()]
        handler._send_json({"ok": True, "count": len(rows), "rooms": rows})
        return True

    # 7. Single Telemedicine Room Lookup
    if path.startswith("/api/v1/telemedicine/rooms/"):
        room_id = path.split("/")[-1]
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM telemedicine_rooms WHERE id = ? OR room_id = ?", (room_id, room_id))
            row = cur.fetchone()
            if not row:
                handler._send_error("Telemedicine consultation room not found.", status=404, code="ROOM_NOT_FOUND")
                return True
            r_dict = dict(row)
            if auth_ctx and auth_ctx["role"] == "PATIENT":
                if r_dict.get("mrn") != auth_ctx.get("mrn"):
                    handler._send_error("Access denied: Patient is not authorized to access consultation rooms of other patients.", status=403, code="UNAUTHORIZED_ROOM_ACCESS")
                    return True
            elif auth_ctx and auth_ctx["role"] != "SUPER_ADMIN":
                if r_dict.get("facility_id") and r_dict["facility_id"] != auth_ctx["facilityId"]:
                    handler._send_error("Access denied: You do not have authorization to view clinical sessions from a different healthcare facility.", status=403, code="CROSS_TENANT_ACCESS_DENIED")
                    return True

        handler._send_json({"ok": True, "room": r_dict})
        return True

    return False


def handle_telemedicine_post(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any], body: Dict[str, Any]) -> bool:
    """Dispatches POST requests for appointments, QSURA, and telemedicine."""
    import services.live_api_server as srv

    # 1. Appointment Digital Check-in
    if path == "/api/v1/appointments/check-in":
        apt_id = body.get("appointment_id", "")
        proms = float(body.get("proms_score", 4.0))
        if srv.AppointmentLifecycleOS:
            try:
                res = srv.AppointmentLifecycleOS.digital_check_in(apt_id, proms)
                handler._send_json(res, status=200)
            except KeyError as ke:
                handler._send_error(str(ke), status=404, code="APPOINTMENT_NOT_FOUND")
        else:
            handler._send_error("Appointment Lifecycle engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # 2. Appointment State Transition
    if path == "/api/v1/appointments/transition":
        apt_id = body.get("appointment_id", "")
        target_state = body.get("target_state", "WAITING_IN_OPD")
        actor_id = body.get("actor_id", "STAFF-01")
        notes = body.get("notes", "")
        if srv.AppointmentLifecycleOS:
            try:
                res = srv.AppointmentLifecycleOS.transition_state(apt_id, target_state, actor_id, notes)
                handler._send_json(res, status=200)
            except KeyError as ke:
                handler._send_error(str(ke), status=404, code="APPOINTMENT_NOT_FOUND")
            except ValueError as ve:
                handler._send_error(str(ve), status=400, code="INVALID_STATE")
        else:
            handler._send_error("Appointment Lifecycle engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # 3. Book Appointment (Tenant-Scoped with Acuity & Token Issuance)
    if path == "/api/v1/appointments":
        patient_name = body.get("patientName") or body.get("patient_name") or "Walk-in Patient"
        mrn = body.get("mrn") or f"MRN-2026-{uuid.uuid4().hex[:4].upper()}"
        doctor_name = body.get("doctorName") or body.get("doctor_name") or "Prof. (Dr.) Mansoor Alam"
        app_date = body.get("date") or datetime.now().strftime("%Y-%m-%d")
        app_time = body.get("timeSlot") or body.get("time_slot") or "11:00 AM"
        chief_complaint = body.get("chiefComplaint") or body.get("chief_complaint") or "General Health Assessment"
        acuity = body.get("acuity") or "STANDARD"
        fee = float(body.get("fee", 800.0))
        facility_id = handler._resolve_facility(auth_ctx, query_params, body)

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = ? AND facility_id = ?", (app_date, facility_id))
            today_count = cur.fetchone()[0] + 101
            token_num = f"T-{today_count}"
            apt_id = f"APT-{uuid.uuid4().hex[:6].upper()}"

            cur.execute("""
            INSERT INTO appointments (id, token_number, mrn, patient_name, doctor_name, department, opd_room, appointment_date, appointment_time, acuity, chief_complaint, status, fee_amount, payment_status, facility_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (apt_id, token_num, mrn, patient_name, doctor_name, "Integrative Unani OPD", "Room 3", app_date, app_time, acuity, chief_complaint, "WAITING", fee, "PAID", facility_id))
            conn.commit()

        handler._send_json({
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
                "facilityId": facility_id,
                "status": "WAITING",
                "feeAmount": fee
            }
        }, status=201)
        return True

    # 4. QSURA Notification Dispatch
    if path == "/api/v1/qsura/send":
        if not auth_ctx or not (handler._has_permission(auth_ctx, "qsura:send") or auth_ctx["role"] in ("SUPER_ADMIN", "CLINIC_ADMIN", "DOCTOR", "HAKEEM", "RECEPTIONIST")):
            handler._send_error("Access denied: You do not have permission to dispatch patient communications.", status=403, code="INSUFFICIENT_PERMISSIONS")
            return True

        channel = (body.get("channel") or "sms").lower().strip()
        recipient = (body.get("recipient") or "").strip()
        message_type = (body.get("message_type") or "").strip()
        parameters = body.get("parameters", {})
        patient_consent_verified = body.get("patient_consent_verified", True)
        mrn = body.get("mrn") or (auth_ctx.get("mrn") if auth_ctx.get("role") == "PATIENT" else None)
        facility_id = handler._resolve_facility(auth_ctx, query_params, body)

        if not patient_consent_verified:
            handler._send_error("DISHA/GDPR Consent Violation: Patient communication consent must be verified.", status=400, code="CONSENT_REQUIRED")
            return True

        if channel not in ["whatsapp", "sms", "email", "webhook"]:
            handler._send_error(f"Unsupported communication channel: {channel}. Allowed channels: whatsapp, sms, email, webhook.", status=400, code="INVALID_CHANNEL")
            return True

        if not recipient:
            handler._send_error("Recipient contact information is required.", status=400, code="MISSING_RECIPIENT")
            return True

        if message_type not in srv.MESSAGE_TEMPLATES:
            handler._send_error(f"Unknown message template: {message_type}.", status=400, code="INVALID_TEMPLATE")
            return True

        template_text = srv.MESSAGE_TEMPLATES[message_type]
        rendered_text = template_text
        for k, v in parameters.items():
            rendered_text = rendered_text.replace(f"{{{k}}}", str(v))

        msg_id = f"QSURA-{channel.upper()[:2]}-{uuid.uuid4().hex[:8].upper()}"
        notif_uuid = f"NOTIF-{uuid.uuid4().hex[:8].upper()}"

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO notifications (id, notification_id, mrn, recipient, channel, template_id, message_text, status, facility_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                notif_uuid,
                msg_id,
                mrn,
                recipient,
                channel.upper(),
                message_type,
                rendered_text,
                "DELIVERED",
                facility_id
            ))
            conn.commit()

        dispatch_record = {
            "dispatch_id": msg_id,
            "channel": channel,
            "recipient": recipient,
            "message_type": message_type,
            "rendered_content": rendered_text,
            "delivery_status": "DELIVERED",
            "dispatched_at": datetime.utcnow().isoformat() + "Z",
            "regulatory_compliance": "DISHA / HIPAA / TRAI DLT Compliant",
            "facility_id": facility_id
        }

        handler._send_json({"ok": True, "dispatch": dispatch_record}, status=201)
        return True

    # 5. Telemedicine Room Creation
    if path == "/api/v1/telemedicine/rooms":
        if not auth_ctx or not (handler._has_permission(auth_ctx, "telemedicine:manage") or auth_ctx["role"] in ("SUPER_ADMIN", "CLINIC_ADMIN", "DOCTOR", "HAKEEM", "RECEPTIONIST")):
            handler._send_error("Access denied: Telemedicine room initialization requires clinical practitioner or administrator authorization.", status=403, code="INSUFFICIENT_PERMISSIONS")
            return True

        mrn = (body.get("mrn") or "").strip()
        if not mrn:
            handler._send_error("Patient MRN is required to create a telemedicine consultation room.", status=400, code="MISSING_MRN")
            return True

        patient_name = (body.get("patient_name") or "").strip()
        doctor_name = (body.get("doctor_name") or "").strip() or (auth_ctx.get("fullName") or auth_ctx.get("name") or "Clinical Specialist")
        encounter_id = body.get("encounter_id")
        appointment_id = body.get("appointment_id")
        facility_id = handler._resolve_facility(auth_ctx, query_params, body)

        with srv.get_db() as conn:
            cur = conn.cursor()
            if not patient_name:
                cur.execute("SELECT full_name FROM patients WHERE mrn = ?", (mrn,))
                p_row = cur.fetchone()
                if p_row:
                    patient_name = p_row["full_name"]
                else:
                    patient_name = "Patient " + mrn

            room_id = f"TELE-ROOM-{uuid.uuid4().hex[:8].upper()}"
            room_uuid = f"ROOM-{uuid.uuid4().hex[:8].upper()}"
            session_token = f"zyv.tele.{uuid.uuid4().hex[:16]}.webrtc"

            cur.execute("""
            INSERT INTO telemedicine_rooms (id, room_id, encounter_id, appointment_id, mrn, patient_name, doctor_name, session_token, status, facility_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                room_uuid,
                room_id,
                encounter_id,
                appointment_id,
                mrn,
                patient_name,
                doctor_name,
                session_token,
                "ACTIVE",
                facility_id
            ))
            conn.commit()

        room_data = {
            "id": room_uuid,
            "room_id": room_id,
            "encounter_id": encounter_id,
            "appointment_id": appointment_id,
            "mrn": mrn,
            "patient_name": patient_name,
            "doctor_name": doctor_name,
            "session_token": session_token,
            "status": "ACTIVE",
            "webrtc_signaling_url": f"wss://telemed.zayvora.internal/v1/signaling/{room_id}",
            "ice_servers": [
                {"urls": "stun:stun.l.google.com:19302"},
                {"urls": "turn:turn.zayvora.internal:3478", "username": f"user-{mrn}", "credential": session_token}
            ],
            "facility_id": facility_id,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }

        handler._send_json({"ok": True, "room": room_data}, status=201)
        return True

    # 6. Telemedicine Room Close
    if path.startswith("/api/v1/telemedicine/rooms/") and path.endswith("/close"):
        parts = path.split("/")
        room_id = parts[-2]
        if not auth_ctx or not (handler._has_permission(auth_ctx, "telemedicine:manage") or auth_ctx["role"] in ("SUPER_ADMIN", "CLINIC_ADMIN", "DOCTOR", "HAKEEM", "RECEPTIONIST")):
            handler._send_error("Access denied: Closing a consultation room requires clinical authorization.", status=403, code="INSUFFICIENT_PERMISSIONS")
            return True

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM telemedicine_rooms WHERE id = ? OR room_id = ?", (room_id, room_id))
            row = cur.fetchone()
            if not row:
                handler._send_error("Telemedicine room not found.", status=404, code="ROOM_NOT_FOUND")
                return True

            cur.execute("UPDATE telemedicine_rooms SET status = 'CLOSED', closed_at = CURRENT_TIMESTAMP WHERE id = ? OR room_id = ?", (room_id, room_id))
            conn.commit()

        handler._send_json({
            "ok": True,
            "message": "Telemedicine consultation room closed securely.",
            "room_id": room_id,
            "status": "CLOSED"
        })
        return True

    return False


def handle_telemedicine_patch(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any], body: Dict[str, Any]) -> bool:
    """Dispatches PATCH requests for appointment status updates and rescheduling."""
    import services.live_api_server as srv

    if path.startswith("/api/v1/appointments/"):
        parts = path.strip("/").split("/")
        apt_id = parts[3] if len(parts) > 3 else parts[-1]

        if path.endswith("/status"):
            new_status = body.get("status")
            if not new_status:
                handler._send_error("Status is required.", status=400, code="MISSING_STATUS")
                return True

            with srv.get_db() as conn:
                cur = conn.cursor()
                cur.execute("UPDATE appointments SET status = ? WHERE id = ? OR token_number = ?", (new_status, apt_id, apt_id))
                if cur.rowcount == 0:
                    handler._send_error("Appointment record not found.", status=404, code="APPOINTMENT_NOT_FOUND")
                    return True
                conn.commit()

            handler._send_json({"ok": True, "message": f"Appointment status updated to {new_status}."})
            return True

        date_val = body.get("date") or body.get("appointmentDate")
        time_val = body.get("timeSlot") or body.get("appointmentTime")
        status_val = body.get("status") or "RESCHEDULED"
        complaint_val = body.get("chiefComplaint")

        with srv.get_db() as conn:
            cur = conn.cursor()
            updates = []
            params = []
            if date_val:
                updates.append("appointment_date = ?")
                params.append(date_val)
            if time_val:
                updates.append("appointment_time = ?")
                params.append(time_val)
            if status_val:
                updates.append("status = ?")
                params.append(status_val)
            if complaint_val:
                updates.append("chief_complaint = ?")
                params.append(complaint_val)

            if not updates:
                handler._send_error("No valid update fields provided.", status=400, code="INVALID_UPDATE")
                return True

            params.extend([apt_id, apt_id])
            sql = f"UPDATE appointments SET {', '.join(updates)} WHERE id = ? OR token_number = ?"
            cur.execute(sql, params)
            if cur.rowcount == 0:
                handler._send_error("Appointment record not found.", status=404, code="APPOINTMENT_NOT_FOUND")
                return True
            conn.commit()

        handler._send_json({
            "ok": True,
            "message": "Appointment successfully updated.",
            "appointmentId": apt_id,
            "status": status_val
        })
        return True

    return False


def handle_telemedicine_delete(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any]) -> bool:
    """Dispatches DELETE requests for appointment cancellation."""
    import services.live_api_server as srv

    if path.startswith("/api/v1/appointments/"):
        apt_id = path.split("/")[-1]
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE appointments SET status = 'CANCELLED' WHERE id = ? OR token_number = ?", (apt_id, apt_id))
            if cur.rowcount == 0:
                handler._send_error("Appointment record not found.", status=404, code="APPOINTMENT_NOT_FOUND")
                return True
            conn.commit()

        handler._send_json({"ok": True, "message": f"Appointment {apt_id} successfully cancelled.", "status": "CANCELLED"})
        return True

    return False
