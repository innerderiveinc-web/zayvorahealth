# ZAYVORA Health OS™ — Disaster Recovery & Backup Runbook

## 1. Backup Architecture & SLA
- **Recovery Time Objective (RTO):** < 1 hour (Target: < 5 minutes).
- **Recovery Point Objective (RPO):** < 5 minutes (Target: < 1 minute via streaming WAL).
- **Snapshot Integrity:** Cryptographically verified SHA-256 checksums on all tarball archives.

## 2. Automated Daily Snapshot Drill
- Executed automatically by cron worker (`services/clinical/app/dr/backup_engine.py`).
- Simulates complete restore into isolated sandbox container, executes table count parity check, and verifies checksum.

## 3. Emergency Restoration Procedure
1. Halt public traffic at API Gateway (maintenance mode banner).
2. Retrieve latest verified snapshot:
   ```bash
   python3 database/dr_backup_restore.py --restore-latest --target-db zayvora_production
   ```
3. Replay WAL logs up to target point-in-time.
4. Execute audit ledger integrity check:
   ```bash
   python3 -c "from services.clinical.app.governance.audit_trail_engine import CryptographicAuditLedger; l = CryptographicAuditLedger(); assert l.verify_chain_integrity().is_valid"
   ```
5. Resume gateway traffic and notify Clinical Operations.
