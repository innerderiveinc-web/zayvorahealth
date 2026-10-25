"""
ZAYVORA Health OS — Authentication & Identity Core Engine
==========================================================
Core cryptographic identity, PBKDF2-HMAC-SHA256 password hashing,
session minting, refresh token rotation, and OTP verification engine.
"""

import base64
import datetime
from datetime import datetime, timezone, timedelta
import hashlib
import hmac
import json
import os
import re
import secrets
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

import services.live_api_server as srv

ACTIVE_OTP_RECORDS = {}  # identifier -> {hash, salt, expires_at, attempts}
OTP_RATE_LIMITS = {}     # identifier -> [timestamps]

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """Generates NIST SP 800-63B compliant PBKDF2-HMAC-SHA256 password hash (100,000 rounds)."""
    if not salt:
        salt = uuid.uuid4().hex
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000)
    hashed = f"pbkdf2:sha256:100000${key.hex()}"
    return hashed, salt

def verify_password(plain_password: str, stored_hash: str, salt: str) -> bool:
    """Verifies plain password against stored hash, supporting both PBKDF2 and legacy SHA256."""
    if not stored_hash or not salt:
        return False
    if stored_hash.startswith("pbkdf2:"):
        parts = stored_hash.split("$")
        if len(parts) == 2:
            expected_hex = parts[1]
            calc_key = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100000)
            return hmac.compare_digest(calc_key.hex(), expected_hex)
    legacy_hash = hashlib.sha256((plain_password + salt).encode("utf-8")).hexdigest()
    return hmac.compare_digest(legacy_hash, stored_hash)

def normalize_email_identifiers(identifier: str) -> list[str]:
    """Returns domain variants for seamless email authentication across zayvorahealth.com, zayvorahealth, and legacy test aliases."""
    ident = (identifier or "").strip().lower()
    variants = [ident]
    if "@zayvorahealth.com" in ident:
        variants.append(ident.replace("@zayvorahealth.com", "@zayvora.health"))
        variants.append(ident.replace("@zayvorahealth.com", "@zayvorahealth"))
    elif "@zayvora.health" in ident:
        variants.append(ident.replace("@zayvora.health", "@zayvorahealth.com"))
        variants.append(ident.replace("@zayvora.health", "@zayvorahealth"))
    elif "@zayvorahealth" in ident:
        variants.append(ident.replace("@zayvorahealth", "@zayvorahealth.com"))
        variants.append(ident.replace("@zayvorahealth", "@zayvora.health"))

    # Map role shortcuts & legacy test aliases to standard clean hospital emails
    alias_map = {
        "doctor@zayvorahealth.com": ["dr.irfan@zayvorahealth.com", "dr.irfan@zayvorahealth"],
        "doctor@zayvora.health": ["dr.irfan@zayvorahealth.com", "dr.irfan@zayvorahealth"],
        "doctor": ["dr.irfan@zayvorahealth.com", "dr.irfan@zayvorahealth"],
        "dr.irfan@zayvorahealth": ["dr.irfan@zayvorahealth.com"],
        "dr.irfanashraf@zayvorahealth.com": ["dr.irfan@zayvorahealth.com"],
        "hakeem@zayvorahealth.com": ["dr.irfan@zayvorahealth.com"],
        "hakeem.irfan@zayvorahealth.com": ["dr.irfan@zayvorahealth.com"],
        "admin@zayvorahealth": ["admin@zayvorahealth.com"],
        "admin@zayvorahealth.com": ["admin@zayvorahealth.com", "admin@zayvorahealth", "admin@zayvora.health"],
        "admin@zayvora.health": ["admin@zayvorahealth.com", "admin@zayvorahealth"],
        "admin": ["admin@zayvorahealth.com", "admin@zayvorahealth"],
        "pharmacy@zayvorahealth": ["pharmacy@zayvorahealth.com"],
        "pharmacy@zayvorahealth.com": ["pharmacy@zayvorahealth.com", "pharmacy@zayvorahealth"],
        "pharmacy": ["pharmacy@zayvorahealth.com"],
        "dispensary@zayvorahealth.com": ["pharmacy@zayvorahealth.com", "pharmacy@zayvorahealth"],
        "reception@zayvorahealth": ["reception@zayvorahealth.com"],
        "reception@zayvorahealth.com": ["reception@zayvorahealth.com", "reception@zayvorahealth"],
        "reception": ["reception@zayvorahealth.com"],
        "clinic@zayvorahealth.com": ["reception@zayvorahealth.com", "reception@zayvorahealth"],
        "clinic": ["reception@zayvorahealth.com"],
        "nurse@zayvorahealth": ["nurse@zayvorahealth.com"],
        "nurse@zayvorahealth.com": ["nurse@zayvorahealth.com", "nurse@zayvorahealth"],
        "nurse": ["nurse@zayvorahealth.com"],
        "manufacturing@zayvorahealth.com": ["manufacturing@zayvorahealth.com"],
        "manufacturing": ["manufacturing@zayvorahealth.com"],
        "research@zayvorahealth.com": ["research@zayvorahealth.com"],
        "research": ["research@zayvorahealth.com"],
        "mansoor.alam@zayvora.health": ["doctor2@zayvorahealth.com"],
        "mansoor.alam@zayvorahealth.com": ["doctor2@zayvorahealth.com"],
        "sirajuddin@zayvora.health": ["doctor3@zayvorahealth.com"],
        "sirajuddin@zayvorahealth.com": ["doctor3@zayvorahealth.com"],
        "reception.opd@zayvora.health": ["reception2@zayvorahealth.com"],
        "reception.opd@zayvorahealth.com": ["reception2@zayvorahealth.com"],
        "zainab.pharm@zayvora.health": ["dispensary2@zayvorahealth.com"],
        "zainab.pharm@zayvorahealth.com": ["dispensary2@zayvorahealth.com"],
        "patient@zayvorahealth.com": ["hamza.farooqi@gmail.com"],
        "patient": ["hamza.farooqi@gmail.com"],
    }
    if ident in alias_map:
        variants.extend(alias_map[ident])

    return list(dict.fromkeys(variants))

def generate_session_token(user_id: str, role: str, facility_id: str, email: str, full_name: str, mrn: str = None) -> str:
    """Issues a cryptographically signed HMAC-SHA256 session token and registers session."""
    now_ts = int(time.time())
    exp_ts = now_ts + 3600  # 1 hour standard production session
    payload = {
        "uid": user_id,
        "email": email,
        "name": full_name,
        "role": role.upper(),
        "fac": facility_id,
        "mrn": mrn,
        "iat": now_ts,
        "exp": exp_ts,
        "jti": uuid.uuid4().hex
    }
    raw_payload = json.dumps(payload, sort_keys=True)
    b64_payload = base64.urlsafe_b64encode(raw_payload.encode()).decode().rstrip("=")
    sig = hmac.new(srv.JWT_SECRET.encode(), b64_payload.encode(), hashlib.sha256).hexdigest()
    token = f"zyv.{b64_payload}.{sig}"

    try:
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
            INSERT OR REPLACE INTO sessions (token, user_id, role, facility_id, expires_at, revoked)
            VALUES (?, ?, ?, ?, datetime(?, 'unixepoch'), 0)
            """, (token, user_id, role.upper(), facility_id, exp_ts))
            conn.commit()
    except Exception:
        pass

    return token

def generate_refresh_token(user_id: str, role: str, facility_id: str) -> str:
    """Issues a cryptographically signed HMAC-SHA256 refresh token valid for 7 days."""
    now_ts = int(time.time())
    exp_ts = now_ts + (7 * 86400)
    payload = {
        "uid": user_id,
        "role": role.upper(),
        "fac": facility_id,
        "type": "refresh",
        "iat": now_ts,
        "exp": exp_ts,
        "jti": uuid.uuid4().hex
    }
    raw_payload = json.dumps(payload, sort_keys=True)
    b64_payload = base64.urlsafe_b64encode(raw_payload.encode()).decode().rstrip("=")
    sig = hmac.new(srv.JWT_SECRET.encode(), b64_payload.encode(), hashlib.sha256).hexdigest()
    return f"zyv.rf.{b64_payload}.{sig}"

# -----------------------------------------------------------------------------
# CRYPTOGRAPHIC OTP VAULT (Server-Side Verification Barrier)
# -----------------------------------------------------------------------------
ACTIVE_OTP_RECORDS = {}  # identifier -> {hash, salt, expires_at, attempts}
OTP_RATE_LIMITS = {}     # identifier -> [timestamps]

def request_otp_challenge(identifier: str, channel: str = "sms") -> dict:
    """Generates a cryptographic 6-digit OTP, applies rate-limits, and stores with 5m TTL."""
    import secrets
    clean_id = identifier.strip().lower()
    now = time.time()
    
    # Rate limit: max 3 requests per 10 minutes
    history = [t for t in OTP_RATE_LIMITS.get(clean_id, []) if now - t < 600]
    if len(history) >= 3:
        return {"ok": False, "error": "Too many OTP requests. Please wait 10 minutes.", "status": 429}
    history.append(now)
    OTP_RATE_LIMITS[clean_id] = history
    
    otp = f"{secrets.randbelow(900000) + 100000:06d}"
    salt = uuid.uuid4().hex[:16]
    hashed_otp = hashlib.sha256((otp + salt).encode()).hexdigest()
    
    ACTIVE_OTP_RECORDS[clean_id] = {
        "hash": hashed_otp,
        "salt": salt,
        "expires_at": now + 300,
        "attempts": 0
    }
    
    # Redact sensitive identifier and secret token in system logs for ISO 27001 / HIPAA compliance
    if "@" in clean_id:
        user_part, domain = clean_id.split("@", 1)
        masked_id = f"{user_part[:2]}***@{domain}"
    else:
        masked_id = f"{clean_id[:3]}***{clean_id[-2:]}" if len(clean_id) >= 5 else "***"
    
    debug_otp = os.environ.get("DEBUG_OTP", "0") == "1"
    logged_code = otp if debug_otp else "[REDACTED]"
    print(f"[AUTH OTP DISPATCH] Identifier: {masked_id} | Channel: {channel} | Code: {logged_code} | TTL: 300s")
    
    return {
        "ok": True,
        "message": f"Verification code dispatched via {channel.upper()}.",
        "identifier": clean_id,
        "channel": channel,
        "expires_in_seconds": 300
    }

def verify_otp_challenge(identifier: str, otp_code: str) -> dict:
    """Verifies submitted OTP against active cryptographic challenge."""
    clean_id = identifier.strip().lower()
    clean_otp = (otp_code or "").strip()
    
    if clean_otp == "otp-verified" or len(clean_otp) != 6 or not clean_otp.isdigit():
        return {"ok": False, "error": "Invalid OTP code format. Enter the 6-digit verification code.", "status": 400}
        
    record = ACTIVE_OTP_RECORDS.get(clean_id)
    if not record:
        return {"ok": False, "error": "No active OTP request found. Please request a new code.", "status": 404}
        
    now = time.time()
    if now > record["expires_at"]:
        ACTIVE_OTP_RECORDS.pop(clean_id, None)
        return {"ok": False, "error": "Verification code expired. Please request a fresh OTP.", "status": 401}
        
    record["attempts"] += 1
    if record["attempts"] > 3:
        ACTIVE_OTP_RECORDS.pop(clean_id, None)
        return {"ok": False, "error": "Too many failed attempts. Code invalidated.", "status": 429}
        
    calc_hash = hashlib.sha256((clean_otp + record["salt"]).encode()).hexdigest()
    if not hmac.compare_digest(calc_hash, record["hash"]):
        return {"ok": False, "error": "Incorrect verification code. Please check and retry.", "status": 401}
        
    ACTIVE_OTP_RECORDS.pop(clean_id, None)
    return {"ok": True, "identifier": clean_id}

def validate_session_token(token: str) -> dict:
    """Validates token authenticity, expiration, revocation status, and returns session context."""
    if not token or not isinstance(token, str):
        return None

    try:
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT revoked, expires_at FROM sessions WHERE token = ?", (token,))
            row = cur.fetchone()
            if row and row["revoked"] == 1:
                return None
    except Exception:
        pass

    if token.startswith("zyv."):
        parts = token.split(".")
        if len(parts) != 3:
            return None
        _, b64_payload, signature = parts
        expected_sig = hmac.new(srv.JWT_SECRET.encode(), b64_payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected_sig):
            return None

        pad_len = 4 - (len(b64_payload) % 4)
        padded = b64_payload + ("=" * (pad_len % 4))
        try:
            payload = json.loads(base64.urlsafe_b64decode(padded.encode()).decode())
        except Exception:
            return None

        if int(time.time()) > payload.get("exp", 0):
            return None

        role = payload.get("role", "PATIENT").upper()
        return {
            "userId": payload.get("uid"),
            "email": payload.get("email"),
            "fullName": payload.get("name"),
            "role": role,
            "facilityId": payload.get("fac", "FAC-HQ-01"),
            "mrn": payload.get("mrn"),
            "permissions": srv.ROLE_PERMISSIONS.get(role, [])
        }

    try:
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
            SELECT s.user_id, s.role, s.facility_id, s.revoked, u.email, u.full_name, u.mrn
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.token = ? AND s.revoked = 0
            """, (token,))
            row = cur.fetchone()
            if row:
                role = row["role"].upper()
                return {
                    "userId": row["user_id"],
                    "email": row["email"],
                    "fullName": row["full_name"],
                    "role": role,
                    "facilityId": row["facility_id"],
                    "mrn": row["mrn"],
                    "permissions": srv.ROLE_PERMISSIONS.get(role, [])
                }
    except Exception:
        pass

    # Legacy prefix tokens without cryptographic signature validation are strictly rejected
    return None

def revoke_session_token(token: str) -> bool:
    """Revokes active session."""
    try:
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE sessions SET revoked = 1 WHERE token = ?", (token,))
            conn.commit()
            return True
    except Exception:
        return False

