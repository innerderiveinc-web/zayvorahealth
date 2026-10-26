# ZAYVORA Security & Permission Audit

## Authentication Security
| Check | Status | Evidence | Risk |
| --- | --- | --- | --- |
| JWT Implementation | SECURE | RS256/HS256 in `services/identity/app/core/security.py`, Token revocation implemented with blocklist | LOW |
| Hardcoded Secrets | SECURE | Secrets are sourced from OS env `os.environ.get("STRIPE_WEBHOOK_SECRET")` | LOW |
| Token Expiry | SECURE | Expiry enforced using `timedelta` in `services/identity/app/core/security.py:326` | LOW |

## RBAC/Authorization
| Check | Status | Evidence | Risk |
| --- | --- | --- | --- |
| Total API endpoints | 219 | Counted `@router` and `@app` | - |
| Endpoints with auth | 45 | Counted `Depends(get_current_user)` | - |
| Unprotected endpoints | ~174 | `auth.py` and `tenancy.py` have multiple unprotected routes like `list_users`, `list_organizations`, `create_role`. In `live_api_server.py`, `/api/v1/facilities` does not check `auth_ctx`. | HIGH |

## Patient Data Isolation
| Check | Status | Evidence | Risk |
| --- | --- | --- | --- |
| Filter by org/tenant | PARTIAL | Tenant filters exist `organization_id == organization_id` in `auth.py`, but leaks exist | MED |
| Data Leaks | NOT_ENFORCED | Direct `.all()` calls bypassing tenant filters found in `list_users` (auth.py:668), `list_organizations` (tenancy.py:85) | HIGH |

## Clinical Safety (AI)
| Check | Status | Evidence | Severity |
| --- | --- | --- | --- |
| Safety firewall exists | SAFE | `run_safety_firewall` intercepts draft in `nuskha.py` and `live_api_server.py:2214` | LOW |
| Autonomous prescribing prevented | SAFE | Check in `live_api_server.py:2498` requires manual review & digital signature | LOW |
| Clinician approval enforced | SAFE | Overriding safety hold requires `safety_firewall.override` permission | LOW |
| Schedule E1 controls | SAFE | `match_schedule_e1_substance` used to filter ingredients | LOW |
| Prescription tamper protection | SAFE | 21 CFR Part 11 Cryptographic seal for lock in `live_api_server.py:1604` | LOW |

## PHI / Data Protection
| Check | Status | Evidence |
| --- | --- | --- |
| Encryption | PARTIALLY_SECURE | GDPR data erasure/anonymization implemented via hashing (e.g., `uid_hash = hashlib.sha256(str(user.id).encode()).hexdigest()[:12]`), but PII like phone/name might be plain text in DB before erasure. |
| Data at Rest | PARTIALLY_SECURE | Uses bcrypt for passwords in `hash_password`. |

## Security Headers
| Header | Present | Status |
| --- | --- | --- |
| X-Content-Type-Options | Yes | Enforced in `security_headers.py:72` |
| X-Frame-Options | Yes | Enforced in `security_headers.py:75` as `DENY` |
| Content-Security-Policy | Yes | Enforced in `security_headers.py:86` |
| HSTS | Yes | Enforced if applicable |
| CORS | Yes | Checked `ZAYVORA_IDENTITY_CORS_ALLOWED_ORIGINS` in `config.py` |

## Rate Limiting
| Service | Rate Limited | Status |
| --- | --- | --- |
| Auth/Login | Yes | Applied to `auth.py:209` (6 attempts per 300s) using sliding window |

## Audit Logging
| Action Type | Logged | Status |
| --- | --- | --- |
| Auth events | Yes | `log_event` is called on login success/fail, MFA, GDPR export |
| GDPR Export | Yes | `action="gdpr.export.requested"` |
| Prescription Sign | Yes | 21 CFR Part 11 anchors are logged |

## UNSAFE Issues Found (P0)
- **Unprotected Routes exposing PII / Tenant Details**: `list_users` (auth.py:668), `list_organizations`, `create_organization` do not use `Depends(get_current_user)`. Anyone can call `/api/v1/auth/users` and pull all DB users!
- **Test suite failures**: `test_phase2_auth_rbac_tenancy.py` fails directly with a 401 error initially, preventing automated security validation.

## High Security Issues (P1)
- **Data Isolation Bypass**: `.all()` is used in `list_users` without considering tenant scoping, allowing a user (if auth was enforced) or an unauthenticated user to read data across all tenants.

## Test Results
- Phase 2 RBAC Test Suite: **FAILED** (`TypeError: 'NoneType' object is not subscriptable` after a 401 Unauthorized during setup).
- Phase 5 AI Safety Test Suite: **FAILED** (pytest not found, fallback script failure).

## Summary
- P0 UNSAFE issues: 1
- P1 High security issues: 1
- P2 Medium: 0
- Authentication: PARTIALLY_SECURE
- AI Safety: SAFE
- Data Isolation: NOT_ENFORCED
