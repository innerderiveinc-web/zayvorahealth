# ZAYVORA Platform — Phase 3: Therapeutic Core

Builds on [Phase 0](./PHASE0-FOUNDATION.md), [Phase 1](./PHASE1-CLINICAL-CORE.md),
and [Phase 2](./PHASE2-KNOWLEDGE-CORE.md). Delivers `services/therapeutic/`: Nuskha
Nawisi (with an integrated Safety Firewall and Clinical Authority Guardrail), Ilaj
bil-Tadbeer, and Ilaj bil-Ghiza — per the build prompt's §13-19.

**Scope decision**: `services/nuskha`, `services/tadbeer`, `services/ghiza`, and
`services/safety` from the target repo layout (§53) are consolidated into one
`services/therapeutic/` service here, for the same reason Phase 2 consolidated
Mufradat/Evidence into `services/knowledge/`: they're tightly coupled (a Nuskha
draft cannot be approved without the Safety Firewall verdict computed alongside it)
and none of them differ in scaling profile. This is a deliberate divergence from a
literal folder-per-line reading of §53, not an oversight.

## The core safety property this phase implements

ZAYVORA Clinical Architecture Specification v4.0 §19: *"Never automatically convert an AI-generated
candidate into a final prescription."* And §2: *"AI must NOT autonomously... bypass
red flags... override clinician judgment."*

Concretely, in this codebase:

1. `POST /nuskha-drafts` **always** creates a row with `status='draft'`. There is no
   code path — not a request parameter, not an admin flag — that creates one
   pre-approved. Grep `NuskhaDraft(` in `app/routers/nuskha.py` if you want to verify
   this yourself; `status` is hardcoded to `"draft"` in the one place a draft is ever
   constructed.
2. The Safety Firewall (`app/engines/safety_firewall.py`) runs automatically at
   draft-creation time, and its verdict/reasons are stored immutably on the draft.
   It is never recomputed or overwritten afterward — if the ingredients need to
   change, that's a new draft, preserving the record of what was actually checked
   against what.
3. `POST /nuskha-drafts/{id}/approve` is a **separate, permission-gated** action
   (`nuskha.approve`). If the stored verdict is `DO_NOT_RECOMMEND` or `REFER`,
   approval is blocked entirely UNLESS the approver *also* holds
   `safety_firewall.override` AND supplies a non-empty justification — which gets
   stored permanently on the draft (`safety_override_justification`), not just
   accepted and discarded. This is the one place in the service where a human can
   override a safety hold, and every time it happens, it's logged on the record
   itself, not just in an ephemeral audit log.

This was tested directly (`test_nuskha.py`, the guardrail-specific tests at the
bottom): approving a pregnancy-flagged draft fails with 403 for a user without
override permission, fails with 422 for a user who has override permission but no
justification, and succeeds only with both — and a non-blocking verdict (e.g.
elderly-patient `CAUTION`) approves normally without needing override at all, so the
guardrail doesn't over-fire on routine cases.

## A deliberate simplification, and what it means

This service does **not** call `services/clinical` or `services/knowledge` over
HTTP to fetch patient allergies/medications or ingredient Mizaj/evidence data
itself. Instead, the caller supplies `patient_safety_context` (allergies,
medications, pregnancy status, etc.) and ingredient names directly in the
`POST /nuskha-drafts` request body.

This was a deliberate choice, not a missed integration: it keeps this phase
testable in isolation, and mirrors how the existing v8.0 codebase's safety engine
also takes a flat patient dict rather than fetching cross-service. The real
integration point is Phase 4 (AI / Hakeem Sahab) — an orchestrator there will
assemble this payload from `services/clinical` (patient safety facts) and
`services/knowledge` (ingredient data) before calling this service. Until Phase 4
exists, anything calling this API directly (a frontend, a script, a human via
Swagger UI) is responsible for supplying accurate `patient_safety_context` itself —
there is no safety net catching a caller who passes stale or wrong data in.

## What was verified

**34 pytest tests, all against real PostgreSQL** (this service has no Neo4j
dependency, so it doesn't carry Phase 2's verification caveat):

- **Safety Firewall** (`test_safety_firewall.py`, 13 tests): every verdict path —
  red-flag complaint → `REFER`, pregnancy → `DO_NOT_RECOMMEND`, allergy conflict →
  `DO_NOT_RECOMMEND`, warfarin+garlic → `MODIFY`, warfarin alone → `CAUTION`,
  immunosuppressant → `DO_NOT_RECOMMEND`, pediatric/elderly/renal → `CAUTION`, and
  verdict escalation (multiple issues → the single most severe verdict wins, never
  averaged or overwritten by a later, milder check).
- **Nuskha workflow** (`test_nuskha.py`, 16 tests): draft creation always starts as
  `draft`, Safety Firewall result is stored, can't double-approve/reject, and the
  full Clinical Authority Guardrail override logic described above.
- **Tadbeer/Ghiza** (`test_tadbeer_and_ghiza.py`, 5 tests): creation, validation
  (category enum), auth, tenant scoping.

## Running it locally

```bash
cd services/therapeutic
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
export ZAYVORA_THERAPEUTIC_DATABASE_URL="postgresql+psycopg://zayvora:zayvora@localhost:5432/zayvora_therapeutic_dev"
.venv/bin/python -m uvicorn app.main:app --reload --port 8004
```

Tests:

```bash
export ZAYVORA_THERAPEUTIC_DATABASE_URL="postgresql+psycopg://zayvora:zayvora@localhost:5432/zayvora_therapeutic_test"
.venv/bin/pytest -q
```

## What's not in this phase

- **Nuskha Compiler automation** (§19's "candidate ingredients → classical
  compatibility → evidence → dose → formula logic" pipeline) — this phase covers
  the *workflow and safety gate* around a Nuskha, not an engine that proposes
  ingredients automatically. That's Phase 4 (AI) territory: Hakeem Sahab would
  produce ingredient candidates by querying `services/knowledge`, then hand them to
  this service's existing draft/approve/reject flow.
- **Formula Digital Twin / standardized product formulas** (§21) — Nuskha here is
  per-patient prescribing, not commercial product formulation. Separate concern,
  not yet built.
- **Cross-service integration** with clinical/knowledge, as discussed above.

## Next: Phase 4 (AI)

Per the build prompt's own phasing, Phase 4 is where ZAPE, Hakeem Sahab, and real
RAG over the Knowledge Graph get built — and where the "deliberate simplification"
above gets resolved by an actual orchestrator assembling cross-service context
instead of trusting the caller to supply it correctly.
