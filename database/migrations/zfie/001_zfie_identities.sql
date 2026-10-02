-- Migration: 001_zfie_identities
CREATE TABLE IF NOT EXISTS zfie_identities (canonical_id TEXT PRIMARY KEY, entity_type TEXT NOT NULL, created_at REAL, metadata_json TEXT);
