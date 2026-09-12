# ZAYVORA Health OS™ — Production Deployment Runbook

## 1. Pre-Deployment Health Verification
1. Verify clean Git working tree on release tag.
2. Execute master automated verification suite:
   ```bash
   python3 tests/run_all_tests.py
   python3 tests/test_45_engines_connected.py
   python3 tests/test_30_critical_workflows.py
   python3 tests/test_definition_of_done.py
   ```
3. Verify zero open P0/P1 issues.

## 2. Database Migration Deployment
1. Take pre-migration WAL snapshot:
   ```bash
   python3 database/dr_backup_restore.py --snapshot-only
   ```
2. Apply reversible Alembic migrations across services:
   ```bash
   alembic -c services/clinical/alembic.ini upgrade head
   alembic -c services/therapeutic/alembic.ini upgrade head
   alembic -c services/identity/alembic.ini upgrade head
   alembic -c services/ai/alembic.ini upgrade head
   ```

## 3. Zero-Downtime Rolling Release
1. Deploy Helm release with Canary progression (10% -> 50% -> 100%):
   ```bash
   helm upgrade --install zayvora infrastructure/helm/zayvora --namespace production --values infrastructure/helm/zayvora/values-production.yaml
   ```
2. Monitor `/health/live` and `/health/ready` probes across all 6 microservice deployments.
3. Validate telemetry latency histograms and zero safety block spikes in Prometheus.
