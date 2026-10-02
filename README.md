<div align="center">
  <h1>🌿 ZAYVORA Health OS™</h1>
  <p><strong>ذیورہ</strong> — AI-Native Unani Healthcare Platform</p>
  <p><em>Ancient Wisdom. Modern Science.</em></p>

  ![Version](https://img.shields.io/badge/version-5.0.0-2D6A4F)
  ![License](https://img.shields.io/badge/license-Proprietary-red)
  ![Python](https://img.shields.io/badge/Python-3.12-blue)
  ![Next.js](https://img.shields.io/badge/Next.js-14-black)
  ![React Native](https://img.shields.io/badge/Expo-51-purple)
</div>

---

## Overview

ZAYVORA is a full-stack health operating system that bridges traditional Unani medicine with modern clinical AI. It provides:

- 🏥 **Clinical workflows** — encounters, Nuskha Nawisi (prescription writing), patient 360
- 🧠 **AI Copilot** — Hakeem Sahab, powered by Claude, grounded in Unani knowledge graph
- 🌿 **Mizaj Intelligence** — temperament assessment, organ-axis analysis, differential diagnostics
- 💊 **Therapeutic Engine** — Mufradat/Murakkabat catalogue, FEFO dispensary, safety firewall
- 📱 **Mobile App** — patient-facing React Native app with lab results, prescriptions, teleconsult
- 🔒 **Enterprise Security** — RBAC, JWT rotation, audit logging, HIPAA/GDPR alignment

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│                   Web App (Next.js 14)            │
│              Mobile App (React Native Expo 51)   │
└────────────────────┬────────────────────────────┘
                     │
              ┌──────▼──────┐
              │ API Gateway  │  :8000
              │  (FastAPI)   │
              └──────┬───────┘
    ┌─────────┬──────┼───────┬──────────┐
    ▼         ▼      ▼       ▼          ▼
Identity  Clinical Knowledge Therapeutic AI
 :8001     :8002    :8003     :8004    :8005
    │         │         │        │       │
    └────┬────┘         │        └───────┘
         ▼              ▼
      PostgreSQL      Neo4j
      (shared DB)   (graph DB)
         +
       Redis
```

---

## Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) 24+
- [Node.js](https://nodejs.org/) 20+
- [Python](https://www.python.org/) 3.12+

### 1. Clone and configure

```bash
git clone https://github.com/your-org/zayvora-platform.git
cd zayvora-platform
cp .env.example .env
# Edit .env with your API keys (Stripe, Twilio, Anthropic, etc.)
```

### 2. Start the full stack

```bash
make up          # Start all Docker services
make migrate     # Apply database migrations
```

### 3. Access services

| Service | URL |
|---------|-----|
| Web App | http://localhost:3000 |
| API Gateway | http://localhost:8000 |
| API Docs (Identity) | http://localhost:8001/docs |
| API Docs (Clinical) | http://localhost:8002/docs |
| pgAdmin | http://localhost:5050 |
| Redis Commander | http://localhost:8081 |
| Mailhog | http://localhost:8025 |
| Neo4j Browser | http://localhost:7474 |

---

## Development

```bash
make logs              # Tail all service logs
make shell-identity    # Shell into identity container
make shell-postgres    # psql into the database
make test              # Run all service tests
make lint              # Lint web app and check types
```

### Making DB changes

```bash
make migrate-create    # Autogenerate a new migration
make migrate           # Apply all pending migrations
```

---

## Project Structure

```
zayvora-platform/
├── services/
│   ├── identity/          # Auth, RBAC, Users, Organizations
│   ├── clinical/          # Encounters, Patients, Mizaj, Lab Results
│   ├── knowledge/         # Neo4j graph, RAG, Mufradat, Pharmacopoeia
│   ├── therapeutic/       # Nuskha, Dispensary, Logistics, Safety
│   ├── ai/                # Hakeem Sahab, ZAPE, Multimodal
│   └── gateway/           # API proxy, rate limiting
├── apps/
│   ├── web/               # Next.js 14 web application
│   └── mobile/            # React Native (Expo 51) mobile app
├── design-system/         # Shared UI component library
├── infrastructure/
│   ├── helm/zayvora/      # Kubernetes Helm chart
│   └── monitoring/        # Prometheus + Grafana configs
├── docs/
│   └── compliance/        # HIPAA + GDPR gap analyses
├── tests/                 # End-to-end & integration test suites
├── Makefile               # Developer convenience targets
├── docker-compose.yml     # Production-ready compose
├── docker-compose.override.yml  # Local dev overrides
└── .env.example           # Environment variable reference
```

---

## Deployment

### Docker Compose (Local / Staging)
```bash
make up-build    # Build and start all services
```

### Kubernetes (Production)
```bash
make helm-install   # Install via Helm
make helm-upgrade   # Upgrade existing deployment
```

---

## Compliance

- [HIPAA Gap Analysis](docs/compliance/HIPAA_GAP_ANALYSIS.md)
- [GDPR Gap Analysis](docs/compliance/GDPR_GAP_ANALYSIS.md)

> **Important:** Review compliance docs and complete all P0 actions before processing live patient data.

---

## Contributing

1. Branch off `develop`
2. Write tests for new features
3. Run `make lint && make test`
4. Open a PR against `develop`

---

## License

Proprietary — © 2026 ZAYVORA Technologies. All rights reserved.

---

## Deployment

### Local Development
```bash
./start.sh
```
Opens at http://localhost:8000

### Deploy to Railway.app (Free Hosting)
1. Create account at https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect this repository
4. Railway auto-detects Python and deploys
5. Set environment variables in Railway dashboard:
   - GEMINI_API_KEY (from https://aistudio.google.com)
6. Your live URL: https://zayvora-[random].railway.app

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| PORT | Server port (auto-set by Railway) | Auto |
| GEMINI_API_KEY | Google Gemini AI key | For AI features |
| ANTHROPIC_API_KEY | Claude AI backup | Optional |
