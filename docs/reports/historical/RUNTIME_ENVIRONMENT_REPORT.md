# ZAYVORA Health OS™ — Runtime Environment & Architecture Report

## Executive Summary
This report documents the independent inspection of the execution environment, runtime dependencies, framework versions, database storage, microservices, and orchestration topology of **ZAYVORA Health OS™**.

---

## 1. Environment & Framework Specifications

| Subsystem | Framework / Technology | Version Detected | Execution Mode | Runtime Status |
| :--- | :--- | :---: | :--- | :---: |
| **Core API Gateway / REST** | Python Native HTTP Server | Python 3.9.6 | Standard Library / In-Memory | **OPERATIONAL** |
| **Microservices Blueprint** | FastAPI / Starlette | FastAPI 0.109+ (Manifested) | Containerized (Docker/K8s) | **BLUEPRINT / K8S READY** |
| **Relational Database** | SQLite (Dev/Pilot) / PostgreSQL (Cloud) | SQLite 3.39+ / PG 16 | Local File / Helm StatefulSet | **OPERATIONAL** |
| **Web Frontend** | Next.js / React | Next.js 16.3.1 / React 19.2.8 | SSR / Client Dynamic | **CONFIGURED** |
| **Mobile Application** | React Native / Expo | Expo SDK 51 / RN 0.74 | React Navigation 6 | **CONFIGURED** |
| **Design System** | Tailwind CSS v4 / Custom Tokens | Tailwind 4.0 / TypeScript 5 | Monorepo Shared Package | **OPERATIONAL** |
| **Infrastructure** | Kubernetes / Helm / Docker Compose | Helm 3 / Docker Compose v2 | Local & Multi-Region Staging | **CONFIGURED** |

---

## 2. Database Topology & Storage Classification

| Database Path / Resource | Type | Size | Record Count | Data Classification | Security Status |
| :--- | :---: | :---: | :---: | :--- | :---: |
| `database/zayvora_live.db` | SQLite | 696 KB | 31 Tables | **Development / Seeded Pilot Data** | Protected via `.gitignore` |
| `zayvora_dev.db` | SQLite | 57 KB | 12 Tables | **Local Development Database** | Protected via `.gitignore` |
| PostgreSQL Schema | PostgreSQL | N/A | DDL Defined | **Production Migration Blueprint** | Vault Credential Injection |

---

## 3. Required Environment Variables Audit

All sensitive variables have been verified for safe handling:

| Environment Variable | Category | Status | Value Treatment |
| :--- | :--- | :---: | :--- |
| `DATABASE_URL` | Database Connection | CONFIGURED | `REDACTED` (Local SQLite URI) |
| `ZAYVORA_IDENTITY_JWT_SECRET` | Authentication Secret | CONFIGURED | `REDACTED` (HMAC Dev Secret) |
| `ZAYVORA_IDENTITY_JWT_ALGORITHM` | Crypto Algorithm | CONFIGURED | `HS256` |
| `ZAYVORA_IDENTITY_ACCESS_TOKEN_TTL_SECONDS` | Token Expiry | CONFIGURED | `7200` (2 hours) |
| `SCHEDULE_E1_GATE_ENABLED` | Clinical Safety Gate | CONFIGURED | `true` |
| `MUDABBAR_CERT_REQUIRED` | Herb Detoxification Gate | CONFIGURED | `true` |
| `HAKEEM_SAHAB_SAFE_TO_LOCK` | AI Safety Invariant | CONFIGURED | `false` (Non-Autonomous) |
| `GEMINI_API_KEY` | External LLM | EMPTY / OPTIONAL | `REDACTED` (Fallback Active) |
| `OPENAI_API_KEY` | External LLM | EMPTY / OPTIONAL | `REDACTED` (Fallback Active) |
| `QSURA_SMS_API_KEY` | Telemetry / SMS | EMPTY / DEV | `REDACTED` (Mock Simulated) |
| `STRIPE_SECRET_KEY` | Billing / Payments | EMPTY / DEV | `REDACTED` (Test Order Mode) |

---

## 4. Background Workers & Services
- **`dr_backup_restore.py`**: Automated SQLite disaster recovery snapshot and integrity validator.
- **`live_api_server.py`**: Zero-dependency monolithic API server handling all REST routes on port 8000.
- **Docker Compose (`docker-compose.yml` & `docker-compose.override.yml`)**: Microservice orchestration with pgAdmin, Redis Commander, and MailHog development services.
- **Helm Chart (`infrastructure/helm/zayvora`)**: Production Kubernetes packaging with readiness and liveness probes.
