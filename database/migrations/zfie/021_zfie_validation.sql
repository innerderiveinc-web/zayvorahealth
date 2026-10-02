-- Migration: 021_zfie_validation
CREATE TABLE IF NOT EXISTS zfie_validation (validation_id TEXT PRIMARY KEY, entity_id TEXT, status TEXT, approved_by TEXT, verified_at REAL);
