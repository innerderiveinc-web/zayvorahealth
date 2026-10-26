# ZAYVORA Health OS — System Runtime Topology Specification
## Formalizing the Dual-Profile Architecture (Modular Monolith vs Distributed Cloud)

**Author:** ZAYVORA Systems Architecture Group  
**Classification:** Enterprise Technical Specification  
**Status:** Canonical & Active

---

## 1. Architectural Motivation

In modern digital healthcare, systems often suffer from one of two extremes:
1. **The Brittle Monolith:** Unseparated spaghetti code where UI, business logic, and database queries are intertwined in a single codebase.
2. **Microservices Overhead (Premature Distribution):** Splitting a system into 10+ networked microservices too early, introducing network latency, serialization costs, complex RPC failures, and massive operational overhead for local hospital deployments.

**ZAYVORA Health OS solves this through the "Dual-Profile Architecture":**
- **Domain logic is modularly decoupled** into pure Python packages and specialized engines (`services/clinical/app/engines`, `services/knowledge/app/core`, etc.).
- **At runtime**, the system can execute either as a **Modular Monolith** (Profile A) or as **Distributed Microservices** (Profile B) using the same underlying algorithmic code.

```mermaid
flowchart LR
    subgraph Client["Client Tier"]
        C1["PWA / Web App"]
        C2["Mobile App (Expo)"]
        C3["FHIR R4 Consumers"]
    end

    subgraph ProfileA["Profile A: Modular Monolith (Edge/Clinic)"]
        M1["live_api_server.py<br>(Zero-Dep HTTP Dispatcher)"]
        M2["12 Micro-Routers<br>(services/routes/)"]
        M3["engine_registry.py<br>(In-Memory Facade)"]
        M4["SQLite (WAL Mode)<br>Local Storage"]
        M1 --> M2 --> M3 --> M4
    end

    subgraph ProfileB["Profile B: Distributed Cloud (Kubernetes)"]
        K1["API Gateway Reverse Proxy"]
        K2["Clinical Microservice Pod"]
        K3["Therapeutic Microservice Pod"]
        K4["AI / Deep RAG Pod"]
        K5["PostgreSQL / Cloud SQL Cluster"]
        K1 --> K2 & K3 & K4
        K2 & K3 & K4 --> K5
    end

    Client -->|Local Node| ProfileA
    Client -->|Cloud Edge| ProfileB
```

---

## 2. Runtime Profile Comparison

| Capability | Profile A: Modular Monolith | Profile B: Distributed Cloud |
| :--- | :--- | :--- |
| **Primary Target** | Single clinic, rural hospital, laptop deployment | Regional health network, cloud SaaS, multi-tenant |
| **Process Model** | 1 single OS process | 6+ container pods + Gateway |
| **Startup Time** | < 45 milliseconds | 30 - 60 seconds (cold start) |
| **Memory Footprint** | ~ 45 MB RAM | ~ 1.2 GB RAM (aggregate) |
| **Dependencies** | Python Standard Library + SQLite | Docker, Kubernetes, PostgreSQL, Redis |
| **Inter-Service Calls**| In-memory direct Python function invocations | HTTP/REST or gRPC with JSON serialization |
| **Failure Domain** | Single process (managed by systemd/launchd) | Isolated container pods (managed by Kubelet) |
| **Disaster Recovery** | Point-in-time SQLite atomic backup (`.db`) | Distributed WAL replication + cloud snapshots |

---

## 3. How the Engine Registry Enables Zero-Overhead In-Process Execution

The heart of the dual architecture is [`services/engine_registry.py`](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/engine_registry.py).

When running in **Modular Monolith Profile**, `engine_registry.py` loads the algorithmic engines directly into process memory using Python's `importlib`:
- Classical Unani pharmacopoeia & monographs
- 12-Organ Axis, Qaroorah, and Mizaj scoring
- Nuskha formulation safety firewall & Schedule E1 screening
- Merkle seal generation and patient cryptographic primitives

This guarantees that:
1. Business logic is written **once** in the domain service directories.
2. The standalone server runs with **zero network latency** and **zero RPC overhead**.
3. In distributed deployments, the exact same domain engines are wrapped by FastAPI routes inside Docker containers.

---

## 4. Verification & Certification

This topology is validated by automated CI/CD gates:
- Standalone Monolith runtime verified by: `tests/test_hardware_and_complete_ecosystem.py` and `tests/test_live_api_integration.py`.
- Microservices schema and Alembic migrations verified by: `tests/test_dr_backup_restore_and_staging.py`.
