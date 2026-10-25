"""
ZAYVORA Health OS — Identity, Authentication & Governance Domain Router
========================================================================
Modular request dispatcher for 21 CFR Part 11 compliant authentication,
session management, OTP challenges, password reset, and role permissions.
"""

import base64
import hashlib
import hmac
import json
import secrets
import time
import uuid
from typing import Any, Dict


def handle_auth_get(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any]) -> bool:
    """Dispatches GET requests for authentication and identity verification."""
    import services.live_api_server as srv

    # Current User Identity / Session Verification
    if path in ("/api/v1/auth/me", "/api/v1/auth/session"):
        if not auth_ctx:
            handler._send_error(
                "Authentication required: Please sign in with your credentials to access this clinical session.",
                status=401,
                code="UNAUTHORIZED"
            )
            return True

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM facilities WHERE id = ?", (auth_ctx["facilityId"],))
            fac_row = cur.fetchone()
            fac_name = fac_row["name"] if fac_row else "ZAYVORA Matab™ — Central Care Centre"

        handler._send_json({
            "ok": True,
            "user": {
                "id": auth_ctx["userId"],
                "email": auth_ctx["email"],
                "fullName": auth_ctx["fullName"],
                "role": auth_ctx["role"],
                "mrn": auth_ctx["mrn"],
                "facilityId": auth_ctx["facilityId"],
                "facilityName": fac_name,
                "permissions": auth_ctx["permissions"]
            },
            "roles": [auth_ctx["role"]],
            "permissions": auth_ctx["permissions"],
            "facility": {
                "id": auth_ctx["facilityId"],
                "name": fac_name
            }
        })
        return True

    return False


def handle_auth_post(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any], body: Dict[str, Any]) -> bool:
    """Dispatches POST requests for authentication, signup, login, OTP, and session rotation."""
    import services.live_api_server as srv

    # Registration / Signup
    if path in ("/api/v1/auth/register", "/api/v1/auth/signup"):
        email = (body.get("email") or "").strip().lower()
        password = body.get("password") or ""
        full_name = (body.get("fullName") or body.get("full_name") or "").strip()
        phone = (body.get("phone") or "").strip()

        req_role = (body.get("role") or body.get("role_name") or "PATIENT").upper()
        if req_role != "PATIENT":
            auth_ctx_local = handler._get_auth_context()
            if not auth_ctx_local or auth_ctx_local.get("role") not in ("SUPER_ADMIN", "ADMIN"):
                handler._send_error(
                    "Public self-registration only permits the PATIENT role. Privileged accounts must be provisioned by an administrator.",
                    status=403,
                    code="PRIVILEGE_ESCALATION_BLOCKED"
                )
                return True
            role = req_role
        else:
            role = "PATIENT"

        facility_id = "FAC-HQ-01"

        if not email or "@" not in email:
            handler._send_error("A valid email address is required.", status=400, code="INVALID_EMAIL")
            return True
        if not password or len(password) < 4:
            handler._send_error("Password must be at least 4 characters.", status=400, code="WEAK_PASSWORD")
            return True
        if not full_name:
            handler._send_error("Full name is required.", status=400, code="MISSING_NAME")
            return True

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE email = ?", (email,))
            if cur.fetchone():
                handler._send_error("An account with this email address already exists.", status=409, code="ACCOUNT_EXISTS")
                return True

            pwd_hash, salt = srv.hash_password(password)
            user_id = f"USR-{uuid.uuid4().hex[:8].upper()}"

            mrn = None
            if role == "PATIENT":
                cur.execute("SELECT COUNT(*) FROM patients")
                p_count = cur.fetchone()[0] + 1
                mrn = f"MRN-2026-{p_count:04d}"

            cur.execute("""
            INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, mrn, facility_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, email, pwd_hash, salt, full_name, phone, role, mrn, facility_id))

            if role == "PATIENT":
                name_parts = full_name.split(" ", 1)
                first_name = name_parts[0]
                last_name = name_parts[1] if len(name_parts) > 1 else ""
                pat_id = f"PAT-{uuid.uuid4().hex[:6].upper()}"

                cur.execute("""
                INSERT INTO patients (id, mrn, user_id, first_name, last_name, date_of_birth, gender, contact_phone, contact_email, blood_group, mizaj_dominant, allergies_json, facility_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (pat_id, mrn, user_id, first_name, last_name, body.get("dob", "1995-01-01"), body.get("gender", "Unspecified"), srv._encrypt_phi(phone), srv._encrypt_phi(email), "B+", "Motadil (Balanced)", json.dumps([]), facility_id))

            conn.commit()

        token = srv.generate_session_token(user_id, role, facility_id, email, full_name, mrn)

        handler._send_json({
            "ok": True,
            "message": "User registered successfully.",
            "token": token,
            "access_token": token,
            "token_type": "bearer",
            "expires_in_seconds": 86400,
            "user": {
                "id": user_id,
                "email": email,
                "fullName": full_name,
                "phone": phone,
                "role": role,
                "mrn": mrn,
                "facilityId": facility_id,
                "facilityName": "ZAYVORA Matab™ — Central Care Centre",
                "permissions": srv.ROLE_PERMISSIONS.get(role, [])
            },
            "roles": [role],
            "permissions": srv.ROLE_PERMISSIONS.get(role, [])
        }, status=201)
        return True

    # Master OS System Settings Persistence
    if path == "/api/v1/system/settings":
        auth_ctx_local = handler._get_auth_context()
        if not auth_ctx_local:
            handler._send_error("Authentication required to update system settings.", status=401, code="UNAUTHENTICATED")
            return True
        if auth_ctx_local.get("role") not in ("SUPER_ADMIN", "ADMIN") and not handler._has_permission(auth_ctx_local, "system.settings.write"):
            handler._send_error("Forbidden: Administrative privilege required to modify system settings.", status=403, code="FORBIDDEN")
            return True

        ALLOWED_SETTING_KEYS = {
            "platform_edition", "dark_mode", "maintenance_mode", "telemetry_enabled",
            "session_timeout_minutes", "default_facility_id", "clinical_version",
            "mizaj_assessment_version", "prescriptions_auto_issue", "theme", "logo_url",
            "support_email", "support_phone", "audit_retention_days", "fhir_export_enabled"
        }
        try:
            with srv.get_db() as conn:
                cur = conn.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS system_settings (key TEXT PRIMARY KEY, value TEXT NOT NULL, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
                for k, v in body.items():
                    if k not in ALLOWED_SETTING_KEYS:
                        continue
                    val_str = json.dumps(v) if isinstance(v, (dict, list)) else str(v)
                    cur.execute("INSERT OR REPLACE INTO system_settings (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)", (k, val_str))
                conn.commit()
            handler._send_json({"ok": True, "message": "System settings persisted successfully."})
            return True
        except Exception as e:
            handler._send_json({"ok": False, "error": str(e)}, status=500)
            return True

    # OTP Request Challenge
    if path == "/api/v1/auth/otp/request":
        identifier = (body.get("identifier") or body.get("mobile") or body.get("email") or "").strip().lower()
        channel = (body.get("channel") or "sms").lower()
        if not identifier:
            handler._send_error("Mobile number or email is required to request OTP.", status=400, code="IDENTIFIER_REQUIRED")
            return True
        res = srv.request_otp_challenge(identifier, channel)
        if not res["ok"]:
            handler._send_error(res["error"], status=res.get("status", 400), code="OTP_REQUEST_FAILED")
            return True
        handler._send_json(res, status=200)
        return True

    # OTP Verification & Session Minting
    if path == "/api/v1/auth/otp/verify":
        identifier = (body.get("identifier") or body.get("mobile") or body.get("email") or "").strip().lower()
        otp_code = (body.get("otp") or body.get("code") or "").strip()
        if not identifier or not otp_code:
            handler._send_error("Identifier and OTP code are required.", status=400, code="OTP_PARAMS_REQUIRED")
            return True
        ver_res = srv.verify_otp_challenge(identifier, otp_code)
        if not ver_res["ok"]:
            handler._send_error(ver_res["error"], status=ver_res.get("status", 401), code="OTP_VERIFICATION_FAILED")
            return True

        with srv.get_db() as conn:
            cur = conn.cursor()
            idents = srv.normalize_email_identifiers(identifier)
            q_marks = ",".join("?" for _ in idents)
            cur.execute(f"SELECT * FROM users WHERE LOWER(email) IN ({q_marks}) OR phone = ?", (*idents, identifier))
            row = cur.fetchone()
            if row:
                user = dict(row)
                role = user["role"].upper()
                facility_id = user["facility_id"]
                token = srv.generate_session_token(user["id"], role, facility_id, user["email"], user["full_name"], user["mrn"])
                refresh_token = srv.generate_refresh_token(user["id"], role, facility_id)
                cur.execute("SELECT name FROM facilities WHERE id = ?", (user["facility_id"],))
                fac_row = cur.fetchone()
                fac_name = fac_row["name"] if fac_row else "ZAYVORA Matab™ — Central Care Centre"
                handler._send_json({
                    "ok": True,
                    "verified": True,
                    "token": token,
                    "access_token": token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer",
                    "expires_in_seconds": 3600,
                    "user": {
                        "id": user["id"],
                        "email": user["email"],
                        "fullName": user["full_name"],
                        "phone": user["phone"],
                        "role": role,
                        "mrn": user["mrn"],
                        "facilityId": facility_id,
                        "facilityName": fac_name,
                        "permissions": srv.ROLE_PERMISSIONS.get(role, [])
                    },
                    "roles": [role]
                }, status=200)
                return True
            else:
                verification_token = f"challenge.{uuid.uuid4().hex}"
                handler._send_json({
                    "ok": True,
                    "verified": True,
                    "is_registered": False,
                    "verification_token": verification_token,
                    "identifier": identifier,
                    "message": "Identity verified. Proceed with patient account registration."
                }, status=200)
                return True

    # Login / Authentication
    if path == "/api/v1/auth/login":
        identifier = (body.get("identifier") or body.get("email") or body.get("username") or "").strip().lower()
        password = body.get("password") or ""

        if not identifier or not password:
            handler._send_error("Email and password are required.", status=400, code="CREDENTIALS_REQUIRED")
            return True

        with srv.get_db() as conn:
            cur = conn.cursor()
            idents = srv.normalize_email_identifiers(identifier)
            q_marks = ",".join("?" for _ in idents)
            cur.execute(f"SELECT * FROM users WHERE LOWER(email) IN ({q_marks}) OR phone = ?", (*idents, identifier))
            row = cur.fetchone()
            if not row:
                handler._send_error("Invalid email or password. Please verify your credentials.", status=401, code="INVALID_CREDENTIALS")
                return True
            user = dict(row)

            cur.execute("SELECT name FROM facilities WHERE id = ?", (user["facility_id"],))
            fac_row = cur.fetchone()
            fac_name = fac_row["name"] if fac_row else "ZAYVORA Health — Virtual Matab & Tele-Care HQ"

        pwd_matches = srv.verify_password(password, user["password_hash"], user["salt"])
        if not pwd_matches:
            handler._send_error("Invalid password.", status=401, code="INVALID_CREDENTIALS")
            return True

        # Upgrade legacy hash to PBKDF2 if needed
        if not user["password_hash"].startswith("pbkdf2:"):
            new_hash, new_salt = srv.hash_password(password)
            with srv.get_db() as conn:
                conn.cursor().execute("UPDATE users SET password_hash = ?, salt = ? WHERE id = ?", (new_hash, new_salt, user["id"]))
                conn.commit()

        role = user["role"].upper()
        facility_id = user["facility_id"]
        token = srv.generate_session_token(user["id"], role, facility_id, user["email"], user["full_name"], user["mrn"])
        refresh_token = srv.generate_refresh_token(user["id"], role, facility_id)

        handler._send_json({
            "ok": True,
            "message": "Authentication successful.",
            "token": token,
            "access_token": token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in_seconds": 3600,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "fullName": user["full_name"],
                "phone": user["phone"],
                "role": role,
                "mrn": user["mrn"],
                "facilityId": facility_id,
                "facilityName": fac_name,
                "permissions": srv.ROLE_PERMISSIONS.get(role, [])
            },
            "roles": [role],
            "permissions": srv.ROLE_PERMISSIONS.get(role, []),
            "facility": {
                "id": facility_id,
                "name": fac_name
            }
        })
        return True

    # Refresh Token Rotation
    if path == "/api/v1/auth/refresh":
        refresh_token = body.get("refresh_token") or body.get("refreshToken") or ""
        if not refresh_token or not refresh_token.startswith("zyv.rf."):
            handler._send_error("Valid refresh token required.", status=400, code="INVALID_REFRESH_TOKEN")
            return True

        parts = refresh_token.split(".")
        if len(parts) != 4:
            handler._send_error("Malformed refresh token.", status=400, code="MALFORMED_REFRESH_TOKEN")
            return True

        _, _, b64_payload, signature = parts
        expected_sig = hmac.new(srv.JWT_SECRET.encode(), b64_payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected_sig):
            handler._send_error("Invalid refresh token signature.", status=401, code="INVALID_SIGNATURE")
            return True

        pad_len = 4 - (len(b64_payload) % 4)
        padded = b64_payload + ("=" * (pad_len % 4))
        try:
            payload = json.loads(base64.urlsafe_b64decode(padded.encode()).decode())
        except Exception:
            handler._send_error("Invalid refresh token payload.", status=400, code="INVALID_PAYLOAD")
            return True

        if int(time.time()) > payload.get("exp", 0):
            handler._send_error("Refresh token expired. Please log in again.", status=401, code="REFRESH_TOKEN_EXPIRED")
            return True

        user_id = payload.get("uid")
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE id = ? AND is_active = 1", (user_id,))
            user_row = cur.fetchone()
            if not user_row:
                handler._send_error("User not found or account deactivated.", status=401, code="USER_INACTIVE")
                return True
            user = dict(user_row)

            cur.execute("SELECT name FROM facilities WHERE id = ?", (user["facility_id"],))
            fac_row = cur.fetchone()
            fac_name = fac_row["name"] if fac_row else "ZAYVORA Matab™ — Central Care Centre"

        new_access_token = srv.generate_session_token(user["id"], user["role"], user["facility_id"], user["email"], user["full_name"], user["mrn"])
        new_refresh_token = srv.generate_refresh_token(user["id"], user["role"], user["facility_id"])

        handler._send_json({
            "ok": True,
            "token": new_access_token,
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in_seconds": 3600
        })
        return True

    # Password Reset — Request OTP
    if path == "/api/v1/auth/forgot-password":
        identifier = (body.get("identifier") or body.get("email") or body.get("phone") or "").strip().lower()
        if not identifier:
            handler._send_error("Registered email or mobile number is required.", status=400, code="IDENTIFIER_REQUIRED")
            return True

        with srv.get_db() as conn:
            cur = conn.cursor()
            idents = srv.normalize_email_identifiers(identifier)
            q_marks = ",".join("?" for _ in idents)
            cur.execute(f"SELECT id, email, phone, full_name FROM users WHERE LOWER(email) IN ({q_marks}) OR phone = ?", (*idents, identifier))
            user_row = cur.fetchone()

        if user_row:
            user = dict(user_row)
            raw_otp = f"{secrets.randbelow(900000) + 100000:06d}"
            salt = uuid.uuid4().hex
            otp_hash = hashlib.pbkdf2_hmac("sha256", raw_otp.encode("utf-8"), salt.encode("utf-8"), 10000).hex()
            exp_ts = int(time.time()) + 600

            with srv.get_db() as conn:
                cur = conn.cursor()
                cur.execute("""
                INSERT INTO password_reset_otps (id, identifier, otp_hash, salt, expires_at, attempts, used)
                VALUES (?, ?, ?, ?, datetime(?, 'unixepoch'), 0, 0)
                """, (f"OTP-{uuid.uuid4().hex[:8].upper()}", identifier, otp_hash, salt, exp_ts))
                conn.commit()

            try:
                with srv.get_db() as conn:
                    cur = conn.cursor()
                    notif_id = f"NOTIF-{uuid.uuid4().hex[:8].upper()}"
                    cur.execute("""
                    INSERT INTO notifications (id, notification_id, recipient, channel, template_id, message_text, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        notif_id,
                        notif_id,
                        user.get("phone") or user.get("email"),
                        "SMS" if user.get("phone") else "EMAIL",
                        "TPL_SECURITY_OTP",
                        f"Your ZAYVORA verification code is {raw_otp}. Valid for 10 minutes. Do not share.",
                        "DELIVERED"
                    ))
                    conn.commit()
            except Exception:
                pass

        handler._send_json({
            "ok": True,
            "message": "If an account exists for this identifier, a secure verification code has been dispatched."
        })
        return True

    # Password Reset — Verify OTP & Set New Password
    if path == "/api/v1/auth/reset-password":
        identifier = (body.get("identifier") or body.get("email") or body.get("phone") or "").strip().lower()
        otp = str(body.get("otp") or "").strip()
        new_password = body.get("newPassword") or body.get("new_password") or body.get("password") or ""

        if not identifier or not otp or not new_password:
            handler._send_error("Identifier, verification OTP, and new password are required.", status=400, code="MISSING_FIELDS")
            return True

        if len(new_password) < 8:
            handler._send_error("New password must be at least 8 characters in length.", status=400, code="WEAK_PASSWORD")
            return True

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
            SELECT id, otp_hash, salt, attempts, used, strftime('%s', expires_at) as exp_epoch
            FROM password_reset_otps
            WHERE identifier = ? AND used = 0
            ORDER BY created_at DESC LIMIT 1
            """, (identifier,))
            otp_row = cur.fetchone()

        if not otp_row:
            handler._send_error("Invalid or expired verification code.", status=400, code="INVALID_OTP")
            return True

        otp_data = dict(otp_row)
        if otp_data["attempts"] >= 3:
            handler._send_error("Too many failed attempts for this code. Please request a new OTP.", status=429, code="RATE_LIMITED")
            return True

        now_epoch = int(time.time())
        if otp_data["exp_epoch"] and now_epoch > int(otp_data["exp_epoch"]):
            handler._send_error("Verification code has expired. Please request a new OTP.", status=400, code="EXPIRED_OTP")
            return True

        calc_hash = hashlib.pbkdf2_hmac("sha256", otp.encode("utf-8"), otp_data["salt"].encode("utf-8"), 10000).hex()
        if not hmac.compare_digest(calc_hash, otp_data["otp_hash"]):
            with srv.get_db() as conn:
                conn.cursor().execute("UPDATE password_reset_otps SET attempts = attempts + 1 WHERE id = ?", (otp_data["id"],))
                conn.commit()
            handler._send_error("Invalid verification code. Please check and try again.", status=400, code="INVALID_OTP")
            return True

        with srv.get_db() as conn:
            cur = conn.cursor()
            idents = srv.normalize_email_identifiers(identifier)
            q_marks = ",".join("?" for _ in idents)
            cur.execute(f"SELECT id FROM users WHERE LOWER(email) IN ({q_marks}) OR phone = ?", (*idents, identifier))
            user_row = cur.fetchone()
            if not user_row:
                handler._send_error("User account not found.", status=404, code="USER_NOT_FOUND")
                return True
            user_id = user_row["id"]

            pwd_hash, salt = srv.hash_password(new_password)
            cur.execute("UPDATE users SET password_hash = ?, salt = ? WHERE id = ?", (pwd_hash, salt, user_id))
            cur.execute("UPDATE password_reset_otps SET used = 1 WHERE id = ?", (otp_data["id"],))
            cur.execute("UPDATE sessions SET revoked = 1 WHERE user_id = ?", (user_id,))

            # Merkle audit record
            cur.execute("""
            INSERT INTO audit_ledger (leaf_hash, event_type, signer, status, facility_id, details_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                hashlib.sha256(f"PWD_RESET:{user_id}:{time.time()}".encode()).hexdigest(),
                "AUTH_PASSWORD_RESET",
                user_id,
                "SUCCESS",
                "FAC-HQ-01",
                json.dumps({"identifier": identifier, "sessions_revoked": True})
            ))
            conn.commit()

        handler._send_json({
            "ok": True,
            "message": "Password updated successfully. All prior active sessions have been revoked."
        })
        return True

    # Logout / Invalidate Session
    if path == "/api/v1/auth/logout":
        if auth_ctx and auth_ctx.get("_raw_token"):
            srv.revoke_session_token(auth_ctx["_raw_token"])
        handler._send_json({"ok": True, "message": "Session invalidated successfully."})
        return True

    # Switch Facility Context
    if path == "/api/v1/auth/switch-facility":
        if not auth_ctx:
            handler._send_error("Authentication required.", status=401, code="UNAUTHORIZED")
            return True

        new_fac_id = body.get("facilityId") or body.get("facility_id")
        if not new_fac_id:
            handler._send_error("Target facility identifier is required.", status=400, code="FACILITY_REQUIRED")
            return True

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM facilities WHERE id = ? AND is_active = 1", (new_fac_id,))
            fac_row = cur.fetchone()
            if not fac_row:
                handler._send_error("Target facility does not exist or is inactive.", status=404, code="FACILITY_NOT_FOUND")
                return True

        new_token = srv.generate_session_token(
            auth_ctx["userId"],
            auth_ctx["role"],
            new_fac_id,
            auth_ctx["email"],
            auth_ctx["fullName"],
            auth_ctx.get("mrn")
        )

        handler._send_json({
            "ok": True,
            "message": f"Switched facility context to {fac_row['name']}.",
            "token": new_token,
            "facility": {
                "id": fac_row["id"],
                "name": fac_row["name"],
                "code": fac_row["code"]
            }
        })
        return True

    return False
