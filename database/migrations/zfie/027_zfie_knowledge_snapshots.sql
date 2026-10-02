-- Migration: 027_zfie_knowledge_snapshots
CREATE TABLE IF NOT EXISTS zfie_knowledge_snapshots (snapshot_id TEXT PRIMARY KEY, created_at REAL, zkb_version TEXT, external_data_version TEXT, models_version TEXT);
