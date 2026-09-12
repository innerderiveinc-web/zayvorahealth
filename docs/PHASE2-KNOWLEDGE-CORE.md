# ZAYVORA Platform — Phase 2: Knowledge Core

Builds on [Phase 0](./PHASE0-FOUNDATION.md) and [Phase 1](./PHASE1-CLINICAL-CORE.md).
Delivers `services/knowledge/`: Mufradat (Pharmacopoeia), Mizaj taxonomy, Organ-Axis
taxonomy, and provenance-tracked Evidence — the first real use of the Neo4j Knowledge
Graph described in the build prompt's §27 and §52.

## Read this before trusting this service

**Unlike `services/identity` and `services/clinical`, this service's core data layer
(`app/graph/neo4j_repository.py`) has not been run against a real Neo4j server.**

Both prior phases were verified by actually booting the service against a real
database in this session — Postgres was installable from Ubuntu's own package
repository, so I could install it, run it, and prove signup/login/CRUD/tenant
isolation all genuinely worked end-to-end, not just "the code looks right."

Neo4j has no equivalent path here: its install source (`dist.neo4j.org`) and the
Docker registry needed to pull its container image are both outside this sandbox's
network allowlist. There was no way to stand up a real Neo4j instance to test against.

**What this means concretely:**

- The Cypher queries in `neo4j_repository.py` were written carefully, reviewed for
  correctness against the schema in Master Build Prompt v4.0 §27, and structurally
  mirror the exact same operations that ARE tested (see below) — but a Cypher typo,
  a wrong relationship direction, or a subtle `MERGE` vs `CREATE` bug would not be
  caught by anything in this repository as it stands.
- What IS tested (27 passing pytest tests) is everything *around* the Cypher: FastAPI
  routing, request/response validation, RBAC permission enforcement, tenant
  isolation logic, and the business rules (e.g. evidence review_status always
  defaults to "pending", never auto-escalated). These tests run against
  `InMemoryGraphRepository` (`app/graph/fake_repository.py`), a hand-written fake
  that implements the identical `GraphRepository` interface.
- **Before you rely on this in anything real**: this repo now has a one-flag way to
  run the identical test suite against a real Neo4j instead of the fake — see
  "Verifying against real Neo4j" below. Do that first, on a machine with Docker
  (this was built in a sandbox that had neither Docker nor a network path to
  Neo4j's distribution servers — confirmed by trying apt, a direct download, and
  GitHub releases, none of which had it). If those tests don't pass, trust that
  over anything claimed here.

This is a different, more serious kind of gap than anything flagged in Phase 0 or
Phase 1 — those were real gaps in *logic* (a missing bootstrap role, an
unauthenticated endpoint) that were found precisely because everything was tested
live. This is a gap in *verification itself*. Naming that difference explicitly
matters more than the code looking finished.

## What Phase 2 delivers (architecture, pending the verification above)

- **Mufradat (Pharmacopoeia)** — `Mufrad` nodes: identity, botanical name, part used,
  synonyms, Af'al (classical actions), traditional uses, contraindications, Musleh
  (corrective), Badal (substitute), dose, modern pharmacology notes.
- **Mizaj taxonomy** — the four classical temperaments (Damwi/Safrawi/Saudawi/
  Balghami) as `Mizaj` nodes, linked to a Mufrad via `HAS_MIZAJ` with a
  hot-cold/wet-dry degree (1st-4th) on the relationship itself, per classical
  convention.
- **Organ-Axis taxonomy** — all 12 axes from §9, seeded verbatim, linked to a Mufrad
  via `ACTS_ON`.
- **Evidence Engine** — `Evidence` nodes with E0-E6 levels (§23) and Four Knowledge
  Worlds tagging A/B/C/D (§42), linked via `HAS_EVIDENCE`. `review_status` always
  defaults to `pending`, regardless of the evidence level supplied — enforced in
  both the fake and real repository, so a claim's evidence level can never silently
  self-upgrade to "reviewed" or "approved" (§23: "Never transform E0 into E3/E4
  automatically").
- **The multi-hop query this whole graph model exists for**:
  `GET /api/v1/mufradat?organ_axis=meda-amaa&mizaj_temperament=Safrawi` — find every
  ingredient acting on a given organ axis AND matching a given temperament, in one
  query. This is the concrete case for Neo4j over a relational join chain, and it's
  the one explicitly tested (`test_list_mufradat_combined_axis_and_mizaj_filter`).

## What was verified vs. what wasn't

**Verified (27 tests, real execution, just against the fake):**
- Tenant isolation (Mufradat from one org never visible to another)
- RBAC (`pharmacopoeia.read`/`write`, `evidence.read`/`write` all gate correctly)
- Mizaj temperament validation (only the 4 classical values accepted)
- Evidence level validation (E0-E6 only) and Knowledge World validation (A-D only)
- The combined organ-axis + mizaj-temperament filter query
- 404 handling for unknown Mufrad, unknown axis code

**NOT verified (needs a real Neo4j instance — see above):**
- That the actual Cypher in `neo4j_repository.py` runs without error
- That `MERGE` on `(:Mizaj {temperament, organizationId})` correctly avoids creating
  duplicate Mizaj nodes across multiple Mufradat in the same org (this is the kind
  of subtle correctness property that's easy to get wrong and easy to not notice
  until the graph has enough data for duplicates to matter)
- Actual query performance on a graph of realistic size

## Running it locally

```bash
cd services/knowledge
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
export ZAYVORA_KNOWLEDGE_NEO4J_URI="bolt://localhost:7687"
export ZAYVORA_KNOWLEDGE_NEO4J_PASSWORD="zayvora_dev_password"
.venv/bin/python -m uvicorn app.main:app --reload --port 8003
```

This requires a real Neo4j running locally (`docker compose up neo4j` from
`infrastructure/`, or your own install) — unlike identity/clinical, there's no
SQLite-style zero-setup path for local dev here. Organ-Axis taxonomy is seeded
automatically (idempotently) on startup.

## Verifying against real Neo4j (do this — it's the actual point of this document)

The test suite has a one-flag switch to run against a real Neo4j instance instead of
the in-memory fake, on any machine with Docker (this was built in a sandbox without
Docker — see above):

```bash
cd infrastructure
docker compose up -d neo4j
cd ../services/knowledge
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
export ZAYVORA_KNOWLEDGE_TEST_USE_REAL_NEO4J=1
export ZAYVORA_KNOWLEDGE_NEO4J_URI=bolt://localhost:7687
export ZAYVORA_KNOWLEDGE_NEO4J_PASSWORD=zayvora_dev_password
.venv/bin/pytest -q
```

Same 27 tests, same assertions — the only thing that changes is which
`GraphRepository` implementation answers them. Each test wipes the graph and
re-seeds the Organ-Axis taxonomy first (`wipe_all_data()` / `seed_organ_axes()` in
`app/graph/neo4j_repository.py`), so it's safe to run repeatedly against the same
Neo4j instance.

**If any test fails here that passed against the fake, trust this result.** That
would mean the Cypher has a real bug the fake's Python logic didn't have — likely
candidates to check first: the `MERGE` in `set_mufrad_mizaj` (does it actually avoid
creating duplicate `Mizaj` nodes per organization?), and the multi-`MATCH` chaining
in `list_mufradat` when both `organ_axis` and `mizaj_temperament` filters are given.

This is the single highest-priority thing to do before Phase 3 builds anything on
top of this knowledge graph.
