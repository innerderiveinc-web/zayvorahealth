# ZAYVORA Platform — Phase 1: Clinical Core

Builds on [Phase 0](./PHASE0-FOUNDATION.md). Delivers `services/clinical/` per the
build prompt's own Phase 1 scope (§61): "patient, EMR, appointments, clinical notes,
prescriptions, timeline, investigations." Investigations (labs/imaging) are deferred —
see "What's not in this phase" below.

## What Phase 1 delivers

- **Patient 360 core** — registration, demographics, contact, emergency contact,
  allergies, current medications/supplements, medical/surgical/family history,
  patient goals/preferences, consent. Tenant-isolated: every row carries
  `organization_id` and every query filters on it explicitly.
- **Encounters** — a consultation/visit record that notes, prescriptions, and (later)
  diagnoses attach to. Open → closed lifecycle.
- **Versioned clinical notes** — SOAP notes that are **never edited or deleted**.
  Amending a note creates a new row pointing back at the original via
  `amends_note_id`; the original flips to `is_current = false` but stays in the
  database forever, queryable via `/clinical-notes/{id}/history`. This is a direct,
  tested implementation of the build prompt's §5 requirement: "Never overwrite
  historical clinical information. Use versioned records."
- **Prescriptions** — issuing and discontinuing. Discontinuing sets a status flag,
  never deletes the row, for the same reason as note versioning.
- **Appointments** — scheduling and status updates (scheduled/completed/
  cancelled/no_show).
- **Clinical Timeline** (§6) — `GET /api/v1/patients/{id}/timeline` aggregates
  encounters, current note versions, prescriptions (including discontinuation
  events), and appointments into one chronologically sorted, machine-readable feed.

## Cross-service auth — verified, not assumed

The clinical service does not issue its own tokens; it verifies JWTs issued by the
identity service, using the same secret (`ZAYVORA_IDENTITY_JWT_SECRET` /
`ZAYVORA_CLINICAL_JWT_SECRET` — **must be set to the same value in any environment
where either is actually configured**, i.e. production).

This was verified with a real two-process integration test, not just unit tests
against a locally-minted token: the identity service was booted on port 8100, a
clinic was registered and a user signed up through its real HTTP API, and the
resulting `access_token` was sent to the clinical service (booted separately on port
8200), which accepted it and correctly scoped the created patient to the right
organization. See the session history for the exact commands — this is the kind of
integration risk that's easy to get wrong (secret mismatch, claim-shape mismatch,
clock skew) and worth re-verifying if either service's token handling changes.

**Known tech debt, tracked explicitly**: sharing one secret across services via
matching env vars doesn't scale past a handful of services. Once Phase 2/3 add more
services that need to verify identity's tokens, replace this with a JWKS endpoint on
the identity service (`GET /.well-known/jwks.json`) so services verify against a
public key instead of a shared secret.

## What was verified

- `services/clinical`: **30 pytest tests**, all against real PostgreSQL:
  - Patient CRUD + tenant isolation (cross-org 404s, MRN uniqueness scoped per-org,
    same MRN allowed across different orgs)
  - Encounter lifecycle (open → closed, can't double-close)
  - **Clinical note versioning**: create, amend (new row + original preserved and
    marked non-current), can't amend an already-superseded note, list hides
    superseded versions by default, `/history` walks the full amendment chain
  - Prescription create/discontinue, can't double-discontinue, discontinued rows
    kept not deleted
  - Appointment create/update, status enum validation
  - Timeline: correct event types, chronological ordering, only current note
    versions shown, 404s and org-scoping on unknown/foreign patients
- Cross-service integration (identity → clinical) verified live, as described above.

## What's not in this phase

- **Investigations** (lab orders/results, imaging) — deferred to keep this phase
  focused; add as a new router + model in `services/clinical` when needed, following
  the same tenant-scoping and versioning patterns established here.
- **Diagnoses / differential diagnosis** — this is Phase 4 (AI/Diagnostic
  Intelligence) territory per the build prompt's own phasing, not Clinical Core.
- **Frontend UI for any of this** — `apps/web` still only has the Phase 0
  login/signup/dashboard shell. Patient list, encounter view, note editor, etc. are
  not yet built. The API is real and tested; nothing in `apps/web` calls it yet.
- **The bootstrap-endpoint auth gap noted in Phase 0** (`POST /api/v1/organizations`
  is unauthenticated) is still open — still fine for private beta, still needs
  fixing before public launch.

## Running it locally

```bash
cd services/clinical
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
export ZAYVORA_CLINICAL_DATABASE_URL="postgresql+psycopg://zayvora:zayvora@localhost:5432/zayvora_clinical_dev"
.venv/bin/python -m uvicorn app.main:app --reload --port 8002
```

Tests (requires a running Postgres with a `zayvora_clinical_test` database owned by
user `zayvora`, same as Phase 0's setup):

```bash
export ZAYVORA_CLINICAL_DATABASE_URL="postgresql+psycopg://zayvora:zayvora@localhost:5432/zayvora_clinical_test"
.venv/bin/pytest -q
```

Or via the full stack: `cd infrastructure && docker compose up --build` — the
clinical service is now included, on port 8002.
