# ZAYVORA Health OS™ Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [5.0.0] — 2026-09-14

### 🎉 Major Release — Full-Stack Production Readiness

#### Backend Services

**Identity Service**
- JWT access + refresh token pair with RS256/HS256 support
- JTI-based token revocation backed by Redis
- Refresh token rotation with reuse detection
- RBAC with permission-level granularity
- Password policy (12+ chars, complexity, 100 common-password blocklist)
- Security headers middleware (CSP, HSTS, X-Frame-Options, Referrer-Policy)
- TOTP MFA scaffolding
- Full audit logging on all write operations
- Stripe payments integration (subscriptions, PaymentIntents, webhooks)
- Twilio SMS + SendGrid email notification client
- Rate limiting with lockout (10 attempts → 15 min lockout)

**Clinical Service**
- Encounter lifecycle management (create, close, timeline)
- Mizaj (temperament) assessment with Afaal cascade analysis
- Organ Axis Engine with Unani diagnostic mapping
- Digital twin patient model
- Scribe (ambient clinical note AI)
- Lab results with FHIR R4 integration client
- FHIR client supporting SMART on FHIR OAuth2 flow
- Prescriptions, appointments, patient portal
- Research & RWE endpoints

**Knowledge Service**
- Neo4j knowledge graph for Materia Medica
- Hybrid RAG (vector + graph) search
- Mufradat (single herbs) and Murakkabat (compound formulations) catalogue
- Taxonomy and organ-axis classification
- Pharmacopoeia search with evidence grading
- OCR pipeline for ingesting Unani manuscripts

**Therapeutic Service**
- Nuskha (prescription) compiler with safety firewall
- Schedule E1 (banned substances) enforcement
- Drug interaction checking via OpenFDA
- FEFO dispensary management
- Courier logistics tracking
- Tadbeer (lifestyle prescriptions) and Ghiza (dietary advice) endpoints
- OpenFDA drug information client with Redis caching

**AI Service**
- Hakeem Sahab clinical copilot (Anthropic Claude integration)
- ZAPE personalization engine (Mizaj-aware responses)
- Response validator for clinical safety guardrails
- Multimodal document analysis
- Qdrant vector store integration for semantic search

**API Gateway**
- Path-based routing to all 5 services
- Token bucket rate limiter
- Hop-by-hop header stripping
- Transparent proxy with upstream health tracking

#### Web Application (Next.js 14)
- Admin Console: Dashboard, Users, Audit Logs, System Health
- Nuskha Builder, Hakeem Review Drawer, Mizaj Assessment Modal
- Patient Portal Cockpit, Multimodal Lab Cockpit
- Full RBAC-driven route protection

#### Mobile Application (React Native / Expo 51)
- Auth Screen (login + register)
- Profile Screen with Mizaj badge
- Lab Results Screen (expandable, flagged values)
- Notifications Screen (read/unread, delete)
- Bottom tab navigation with auth guard
- API service with JWT injection
- Auth service with AsyncStorage token persistence

#### Design System
- Brand tokens: Primary `#2D6A4F`, Secondary `#1B4332`, Accent `#F4A261`
- Components: Button, Card, Badge, Input, Modal, Spinner
- Tailwind config with custom tokens

#### Infrastructure
- Docker Compose (9 services: 6 app + postgres + redis + neo4j)
- docker-compose.override.yml with hot-reload + pgAdmin + Mailhog + Redis Commander
- Helm chart for Kubernetes production deployment
- GitHub Actions CI (lint, test matrix, Docker build, Trivy security scan)
- GitHub Actions Release (GHCR push, GitHub Release creation)
- Makefile with 20+ convenience targets
- Alembic migrations scaffolded for all 5 PostgreSQL services

#### Testing
- 70+ test files across all services
- Per-service conftest.py with SQLite in-memory test DB
- Jest + Testing Library for web app (admin console tests)
- Root-level pyproject.toml for unified test runs

#### Compliance
- HIPAA gap analysis with prioritised remediation plan
- GDPR gap analysis with Art. 15/17/20 implementation roadmap

---

## [4.0.0] — 2026-06-01

### Phase 0 Baseline
- Initial monorepo structure
- FastAPI service scaffolding
- SQLite-backed development databases
- Basic authentication

---

## Roadmap

### [5.1.0] — Planned
- [ ] GDPR data export endpoint
- [ ] GDPR erasure endpoint
- [ ] Enforced MFA for clinical staff
- [ ] mTLS inter-service communication
- [ ] Automated audit log archival

### [5.2.0] — Planned
- [ ] RabbitMQ/NATS event bus for async workflows
- [ ] Patient mobile offline sync
- [ ] WhatsApp integration for patient reminders
- [ ] Regulatory dossier generation
