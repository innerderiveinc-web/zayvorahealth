# ZAYVORA HEALTH OS v5.0 — ENTERPRISE API CONTRACTS
**Document ID**: `ZAY-DOC-V5-API-01`  
**Version**: Enterprise Clinical OS v5.0  
**Classification**: Technical Interface Specification  

---

## 1. CORE SERVICE ENDPOINTS

### 1.1 Clinical Service (`services/clinical :8001`)
- `GET /api/v1/patients/{patient_id}`: Fetches complete longitudinal clinical profile.
- `POST /api/v1/encounters`: Initiates a new clinical encounter.
- `POST /api/v1/encounters/{id}/notes`: Saves structured SOAP note with cryptographic SHA-256 hash.
- `GET /api/v1/queue/today`: Returns the real-time OPD token queue with patient status.
- `POST /api/v1/queue/checkin`: Issues an OPD queue token and assigns a consultation room.

### 1.2 Therapeutic Service (`services/therapeutic :8002`)
- `POST /api/v1/prescriptions`: Creates a draft Nuskha prescription.
- `POST /api/v1/prescriptions/{id}/sign`: Signs and locks prescription using 21 CFR Part 11 digital signature.
- `GET /api/v1/dispensary/queue`: Returns pending prescription orders awaiting dispensing.
- `POST /api/v1/dispensary/dispense`: Atomically executes 12-step verification, decrements FEFO stock, and logs Merkle transaction.
- `POST /api/v1/safety/mudabbar-verify`: Validates Schedule E(1) batch detoxification certificate hash.

### 1.3 Knowledge Service (`services/knowledge :8003`)
- `GET /api/v1/knowledge/mufradat/search?q={query}`: Searches classical Unani single herbs.
- `GET /api/v1/knowledge/organ-axis/{axis_id}`: Evaluates organ cross-talk susceptibility vectors.
- `POST /api/v1/knowledge/mizaj/calculate`: Computes 10-Ajnas temperament equilibrium.

### 1.4 AI Service (`services/ai :8004`)
- `POST /api/v1/ai/hakeem/assist`: Advisory clinical assistant. Enforces `safe_to_lock = False`.
- `POST /api/v1/ai/scribe/transcribe`: Ambient speech-to-SOAP synthesis.

### 1.5 Identity & Governance Service (`services/identity :8005`)
- `POST /api/v1/auth/login`: Issues cryptographic JWT tokens with embedded role claims.
- `GET /api/v1/audit/merkle-root`: Returns current 21 CFR Part 11 cryptographic Merkle root hash.

---
**Approved By**: Principal Backend Engineer, ZAYVORA HEALTH OS™
