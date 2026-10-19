# ZAYVORA Health OS™ — Backend Microservices Audit
**Document ID**: `AUDIT-BE-03`  
**Target**: `services/` (Python 3, FastAPI, SQLAlchemy, Pydantic v2)  
**Standard**: Statutory Compliant, Asynchronous Microservice Mesh  

---

## 1. Service Topology & Ports

| Microservice | Directory | Port | Key Responsibilities |
|---|---|---|---|
| **API Gateway** | `services/gateway` | 8000 | Reverse-proxy routing, rate limiting (Token Bucket), TLS termination, CORS. |
| **Clinical Core** | `services/clinical` | 8001 | Patient 360, Encounters, 10-Ajnas Mizaj, Organ-Axis, Timeline, Scribe, Digital Twin. |
| **Therapeutic Core** | `services/therapeutic` | 8002 | Nuskha Compiler, Safety Firewall, Tadbeer Guardrails, Ghiza Plans, Dispensary FEFO, Logistics. |
| **Knowledge Core** | `services/knowledge` | 8003 | ZKB Pharmacopoeia (UPI, NFUM), Taxonomy, Evidence Engine, Neo4j Graph, 3/3 Quorum. |
| **AI & Cognitive** | `services/ai` | 8004 | Hakeem Sahab Copilot, ZAPE Personalization, Multimodal Lab Extractor, Eval Engine. |
| **Identity Core** | `services/identity` | 8005 | Multi-tenancy, User Auth (JWT), RBAC Permissions Catalogue, Audit Logging. |

---

## 2. Microservice Health & Probes
All 6 services implement standardized health check probes:
- `GET /health/live`: Fast process liveness heartbeat returning `200 OK`.
- `GET /health/ready`: Deep dependency readiness check validating DB, Cache, and Worker queues.
- `GET /api/health`: Aggregate gateway health check querying all upstream services.

---

## 3. Resilience & Error Handling
- **Non-blocking Asynchronous I/O**: High-throughput async handlers for all read-heavy routes.
- **Circuit Breakers**: Upstream service calls wrapped in timeouts (3.0s gateway timeout) to avoid cascading thread starvation.
- **Standardized Exception Handlers**: Global HTTPException mapping with structured error codes (`UNAUTHORIZED`, `SAFETY_VIOLATION`, `POSOLOGY_EXCEEDED`, `MUDABBAR_REQUIRED`).
