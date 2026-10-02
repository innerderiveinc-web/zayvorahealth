# ZAYVORA Platform — Phase 0: Foundation

This is a **new, parallel build** started from the "ZAYVORA ZAYVORA Clinical Architecture Specification v4.0"
architecture (Next.js + FastAPI microservices + PostgreSQL + Neo4j + Redis), separate
from the existing v8.0 monolithic FastAPI codebase.

**Why this exists alongside v8.0:** v8.0 is real, tested, and working (58 passing
tests, verified frontend build, verified full-stack boot) — see that codebase's own
README. This rewrite was a deliberate choice made after weighing that against a
target microservices/graph-DB architecture. If you're unsure which one to build on,
re-read that trade-off before adding to either codebase, so effort doesn't split
silently between two systems.

## What Phase 0 delivers

Per the build prompt's own methodology (§61 — "DO NOT attempt to build all modules
simultaneously"), Phase 0 is **only** the foundation every later phase depends on:

- **`services/identity/`** — FastAPI microservice: authentication (JWT), multi-tenancy
  (organizations), RBAC (roles + fine-grained permissions), and an append-only audit
  log. Real PostgreSQL, not SQLite-with-a-plan-to-migrate.
- **`apps/web/`** — Next.js (App Router, TypeScript, Tailwind) clinic sign-in, clinic
  registration, and a dashboard shell showing the logged-in user's roles/permissions
  and the phase roadmap.
- **`infrastructure/docker-compose.yml`** — Postgres, Redis, and Neo4j wired up for
  local dev. Redis and Neo4j are provisioned but **not yet used by any service** —
  they come online in later phases (communications/rate-limiting and the Knowledge
  Graph respectively). Included now so the infra shape matches the target
  architecture from day one, per §52.

## What was verified, not just written

- `services/identity`: 22 pytest tests passing against a **real PostgreSQL instance**
  (not SQLite/mocks) — signup, login, wrong-password/unknown-user indistinguishable
  401s, rate limiting, RBAC permission gating, and the organization bootstrap flow.
- `apps/web`: TypeScript typecheck clean, production `next build` succeeds (4 static
  routes generated).
- Full integration: booted the identity service against Postgres and ran the exact
  flow the web signup form performs (create organization → auto-provision Owner role
  → signup → receive a working JWT with all 8 baseline permissions attached).

## A gap this phase surfaced and fixed

The build prompt doesn't specify how a brand-new organization gets its *first* role,
and role creation is (correctly) permission-gated behind `role.manage` — which nobody
has yet for a new org. This is a real chicken-and-egg bootstrap problem. Fixed by
auto-provisioning an `Owner` role with the full baseline permission set at the moment
an organization is created (`app/core/permissions_catalogue.py`). Covered by
`test_new_organization_auto_provisions_owner_role_for_first_signup`.

**This bootstrap endpoint (`POST /api/v1/organizations`) is currently unauthenticated
by design** (see the docstring on it) — anyone can create an organization and become
its Owner. That's fine for a private beta; before any public launch this needs either
an invite-code gate or a platform-operator token. Tracked here explicitly rather than
left implicit, so it isn't missed later.

## Running it locally

### Identity service
```bash
cd services/identity
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
export ZAYVORA_IDENTITY_DATABASE_URL="postgresql+psycopg://zayvora:zayvora@localhost:5432/zayvora_identity_dev"
.venv/bin/python -m uvicorn app.main:app --reload --port 8001
```

### Web app
```bash
cd apps/web
npm install
NEXT_PUBLIC_IDENTITY_API_URL=http://localhost:8001 npm run dev
```

### Tests
```bash
cd services/identity
# requires a running Postgres with a zayvora_identity_test database owned by user `zayvora`
export ZAYVORA_IDENTITY_DATABASE_URL="postgresql+psycopg://zayvora:zayvora@localhost:5432/zayvora_identity_test"
.venv/bin/pytest -q
```

### Full stack via Docker Compose
```bash
cd infrastructure
docker compose up --build
```

## Next phases (per the build prompt's own §61 methodology)

- **Phase 1 — Clinical Core**: `services/clinical/` — Patient 360, EMR, appointments,
  clinical notes, prescriptions, timeline. This is the next thing to build, and should
  reuse the identity service's JWT/RBAC pattern established here rather than
  reinventing auth per-service.
- **Phase 2 — Knowledge Core**: Mufradat, Pharmacopoeia, Mizaj, Organ-Axis — first
  real use of the Neo4j instance already running in the compose stack.
- **Phase 3 onward**: see the root build prompt document for the full phase list.

Each phase should ship with the same rigor as this one: real tests against a real
database, a verified build/boot, and gaps documented rather than glossed over.
