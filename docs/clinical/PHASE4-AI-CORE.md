# ZAYVORA Platform — Phase 4: AI (Hakeem Sahab)

Builds on Phases 0-3. Delivers `services/ai/`: Hakeem Sahab (§30), the first real
orchestrator that ties `services/clinical`, `services/knowledge`, and a real LLM
together — and the resolution of the "deliberate simplification" flagged at the end
of [Phase 3](./PHASE3-THERAPEUTIC-CORE.md).

## Read this before trusting this service

**Same honesty pattern as Phase 2's Neo4j gap, for a different reason.** There is no
`ANTHROPIC_API_KEY` available in the sandbox this was built in, so
`app/providers/anthropic_provider.py` — the code that actually calls the real
Anthropic Messages API — has never been exercised against the live API in this
session. Everything around it (prompt assembly, cross-service context fetching,
response structural validation, Postgres storage of the audit record) is tested for
real; the LLM call itself is not.

**This is a much smaller gap to close than Phase 2's**, though — you very likely
already have an Anthropic API key, and there's no infrastructure to stand up:

```bash
cd services/ai
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
export ZAYVORA_AI_ANTHROPIC_API_KEY="sk-ant-..."
export ZAYVORA_AI_DATABASE_URL="postgresql+psycopg://zayvora:zayvora@localhost:5432/zayvora_ai_dev"
export ZAYVORA_AI_CLINICAL_SERVICE_URL="http://localhost:8002"
export ZAYVORA_AI_KNOWLEDGE_SERVICE_URL="http://localhost:8003"
.venv/bin/python -m uvicorn app.main:app --reload --port 8005
```

Then with `services/clinical` and `services/knowledge` also running (and a real
patient + Mufradat registered in them), call `POST /api/v1/hakeem/consult` for real
and check the response actually has all 13 required sections
(`app/engines/response_validator.py` — the same check the test suite runs against
the fake). If Anthropic's response doesn't match the format instructed in
`SYSTEM_PROMPT`, that's the first thing to tune — models don't always follow a
formatting instruction as literally as the fake provider does.

## What this phase delivers

- **Hakeem Sahab orchestration** (`app/engines/hakeem_sahab.py`): fetches patient
  safety context from `services/clinical` and candidate Mufradat from
  `services/knowledge` (forwarding the caller's own JWT to both, so RBAC is enforced
  by those services themselves — this service never has broader access than the
  requesting user), builds a structured prompt, calls a model-agnostic
  `AIProvider`, and validates the response's structure before storing or returning
  it.
- **Model-agnostic provider interface** (§52): `AIProvider` Protocol with a real
  `AnthropicProvider` and a `ScriptedFakeProvider` for tests — swapping to a
  different model provider later means writing one new class, not touching the
  orchestration logic.
- **Structural response validation**: every response is checked against the 13
  required §59 section headers (CLINICAL SUMMARY, WHAT IS KNOWN, ... CLINICIAN
  REVIEW REQUIRED). A response missing any section is marked `is_valid: false` and
  returned with `missingSections` listed — never silently accepted as if it were
  complete. This is a format-compliance check, not a hallucination detector; see the
  module docstring in `response_validator.py` for the distinction.
- **AI Governance audit trail** (§50): every consultation — valid or not — is stored
  in `ai_consultations` (real PostgreSQL, real tests) with the request, the raw
  response, parsed sections, and a `reviewed_by_clinician` flag that starts `false`
  and must be explicitly set via `POST /consultations/{id}/mark-reviewed`.

## The Clinical Authority Guardrail, extended to this phase

Same principle as Phase 3, enforced at a different point: **this service never
creates a Nuskha draft.** `run_hakeem_consultation()` returns advisory text and a
candidate ingredient list; nothing in this codebase converts that into a
`POST /nuskha-drafts` call automatically. A clinician who wants to act on a
consultation does so by manually calling `services/therapeutic`'s existing
`POST /nuskha-drafts` endpoint — which independently runs its own Safety Firewall
regardless of what Hakeem Sahab said. The `converted_to_nuskha_draft_id` field on
`AiConsultation` exists purely to record that link after the fact, for the audit
trail; it is never set automatically.

## A real gap this phase surfaced in Phase 1

Building `clinical_client.get_patient_safety_context()` required mapping
`services/clinical`'s `Patient` model onto the safety-context shape
`services/therapeutic`'s Safety Firewall expects — and two fields don't exist yet:

- **`pregnancy_status`** — Patient 360 (Phase 1) has no structured field for this.
  `clinical_client.py` currently hardcodes `"not_applicable"` for every patient,
  which is wrong and known to be wrong (see the inline comment where it does this).
- **`comorbidities`** — same problem; Phase 1's `Patient` model captures
  `medical_history` as free text but nothing structured a Safety Firewall rule can
  reliably match against.

**This means Hakeem Sahab's safety context is currently incomplete for pregnant
patients and patients with comorbidities** — the two categories the Safety Firewall
treats most seriously. This is not a Phase 4 bug; it's a Phase 1 schema gap that
Phase 4 was the first thing to actually need and therefore the first thing to
notice. The fix belongs in `services/clinical`: add `pregnancy_status` and
`comorbidities` (structured, not free text) to the `Patient` model, run a migration,
update `PatientCreate`/`PatientUpdate`/`PatientOut` schemas, add tests — then update
`clinical_client.py` here to read the real fields instead of hardcoding placeholders.
Tracked here explicitly rather than silently worked around.

## What was verified

**18 pytest tests**, split by what's actually being proven:

- `test_response_validator.py` (6 tests) — pure logic, no I/O: well-formed response
  passes, missing any section is caught, empty response fails everything.
- `test_hakeem_engine.py` (4 tests) — orchestration logic against fakes: confirms
  the prompt sent to the provider actually contains the fetched patient/knowledge
  context (not just that a canned response comes back), unknown patient raises
  cleanly, a malformed provider response is flagged invalid rather than silently
  accepted.
- `test_hakeem_api.py` (8 tests) — full HTTP request → orchestration → **real
  PostgreSQL storage** → response, including auth, RBAC, tenant isolation, and the
  mark-reviewed governance flow.

**NOT verified**: the real Anthropic API call (see above).

## Running it locally

See the verification section above for the real-LLM path. For local dev without a
real Anthropic key, inject `ScriptedFakeProvider` the same way the test suite does
(pass it to `create_app()`) rather than trying to run the default `AnthropicProvider`
path without a key — it will fail at the Anthropic client with an auth error, not
gracefully degrade.

## Next: Phase 5 and beyond

Per the build prompt's phasing: Phase 5 is Digital Care (patient app, telemedicine,
Health Coach, QSURA communications). Before that, though, two things from this
phase are higher priority to close:

1. Verify the real Anthropic integration (above) — small effort, meaningful
   confidence gain.
2. Fix the Phase 1 Patient 360 schema gap (pregnancy_status, comorbidities) — this
   is a patient-safety-relevant gap, not a nice-to-have, and it's now blocking
   Hakeem Sahab from being fully trustworthy for two specific patient populations.
