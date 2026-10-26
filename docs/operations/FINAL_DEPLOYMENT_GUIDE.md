# ZAYVORA Health OS™ — Deployment Guide

**Version: 2.0.0 · Helm Chart · Kubernetes**
**Status: Pre-staging · For pilot deployment only**

## Prerequisites

- Kubernetes cluster (1.28+)
- Helm 3.12+
- PostgreSQL 15+ (`zayvora` database)
- Redis 7+
- Neo4j 5+ (for ZKB knowledge graph)
- HashiCorp Vault (for secrets — currently not live)
- Docker registry access

## Helm Deployment

```bash
# Add ZAYVORA Helm repo (placeholder — not yet published)
helm repo add zayvora https://helm.zayvora.com

# Install with values override
helm install zayvora zayvora/zayvora \
  --namespace zayvora-pilot \
  --create-namespace \
  --values infrastructure/helm/zayvora/values.yaml \
  --set gateway.image.tag=2.0.0 \
  --set identity.image.tag=2.0.0

# Verify deployment
helm status zayvora -n zayvora-pilot
```

## Environment Variables Required

```env
# Identity Service
DATABASE_URL=postgresql://user:pass@host:5432/zayvora
JWT_PRIVATE_KEY=<RS256 private key PEM>
JWT_PUBLIC_KEY=<RS256 public key PEM>
JWT_ALGORITHM=RS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
MFA_REQUIRED=true

# AI Service
GEMINI_API_KEY=<from Google AI Studio>
OPENAI_API_KEY=<optional fallback>

# Redis
REDIS_URL=redis://host:6379/0
```

## Security Pre-flight Checklist

- [ ] Independent security audit completed
- [ ] All secrets migrated to HashiCorp Vault
- [ ] TLS/SSL certificate provisioned
- [ ] CORS origins restricted to production domain
- [ ] Rate limiting configured at API gateway
- [ ] Container images scanned for CVEs
- [ ] Database connection pooling configured
- [ ] Backup schedule verified
- [ ] Incident response runbook prepared

## Health Checks

```bash
# Gateway health
curl http://localhost:8000/health

# Service-by-service
curl http://localhost:8001/health  # Identity
curl http://localhost:8002/health  # Clinical
curl http://localhost:8003/health  # Knowledge
curl http://localhost:8004/health  # Therapeutic
curl http://localhost:8005/health  # AI
```

> ⚠️ This is a pilot-candidate deployment guide. Do NOT use in production
> with real patient data until all security checklist items are verified.
