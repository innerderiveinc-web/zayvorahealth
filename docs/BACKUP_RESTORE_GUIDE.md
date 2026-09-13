# ZAYVORA Health OS — Backup & Disaster Recovery Guide
**Document ID**: `ZAY-OPS-003`  
**Classification**: Business Continuity & Data Governance Standard  
**Date**: September 2026  

---

## 1. Automated Disaster Recovery Architecture

ZAYVORA Health OS features an integrated backup and disaster recovery engine implemented in `database/dr_backup_restore.py`.

### 1.1 Backup Execution
To take an instantaneous, immutable cryptographic snapshot of the clinical database:
```bash
python3 database/dr_backup_restore.py --backup
```
The runner creates a compressed snapshot in `backups/zayvora_backup_<timestamp>.db.gz` and records its SHA-256 checksum.

### 1.2 Database Restoration Procedure
In the event of hardware failure, disk corruption, or accidental data loss:
```bash
python3 database/dr_backup_restore.py --restore backups/zayvora_backup_<timestamp>.db.gz
```
The restoration engine:
1. Verifies the cryptographic SHA-256 checksum of the backup archive.
2. Uncompresses and mounts the snapshot into `database/zayvora_live.db`.
3. Validates foreign key constraints and schema integrity.
4. Executes a post-restore smoke test asserting user, patient, and prescription counts.

