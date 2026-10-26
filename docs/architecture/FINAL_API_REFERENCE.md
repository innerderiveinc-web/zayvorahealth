# ZAYVORA Health OS™ — API Reference

**Version: v1**
**Base URL: http://localhost:8000/api/v1**
**Status: Pre-staging · Mock/Development responses**

## Authentication

All endpoints except `/auth/login` and `/auth/signup` require:
```
Authorization: Bearer <JWT>
```

JWT is RS256-signed. Public key available at `/api/v1/auth/jwks.json`.

## Identity Service (`/api/v1/auth`)

| Method | Path | Description |
|:---|:---|:---|
| POST | /auth/signup | Register a new user |
| POST | /auth/login | Login, returns access + refresh tokens |
| POST | /auth/refresh | Refresh access token |
| GET | /auth/session | Validate current session |
| POST | /auth/logout | Invalidate session |
| GET | /auth/jwks.json | JWKS public key endpoint |
| POST | /auth/mfa/setup | Initiate TOTP MFA setup |
| POST | /auth/mfa/verify-setup | Confirm MFA setup |
| POST | /auth/mfa/disable | Disable MFA (admin only) |
| GET | /auth/gdpr-export | Export user data (GDPR Art. 20) |
| DELETE | /auth/gdpr-erase | Erase user data (GDPR Art. 17) |
| GET | /auth/users | List all users (admin only) |

## Tenancy (`/api/v1`)

| Method | Path | Description |
|:---|:---|:---|
| POST | /organizations | Create organisation |
| GET | /organizations | List organisations |
| GET | /organizations/{slug} | Get organisation by slug |
| POST | /roles | Create role |

## Clinical (`/api/v1/clinical`)

| Method | Path | Description |
|:---|:---|:---|
| GET | /clinical/patients | List patients |
| POST | /clinical/patients | Register patient |
| GET | /clinical/patients/{id} | Patient 360 view |
| POST | /clinical/encounters | Create encounter |
| GET | /clinical/encounters/{id} | Get encounter |
| POST | /clinical/prescriptions | Create Nuskha draft |
| POST | /clinical/prescriptions/{id}/sign | Sign Nuskha (HMAC) |
| GET | /clinical/queue | Active queue |

## Safety Notes

- All prescription endpoints enforce `safe_to_lock=False` for AI-generated content
- Schedule E(1) herbs are blocked at the therapeutic service layer
- SHA-256 HMAC signature generated on every `/sign` call
