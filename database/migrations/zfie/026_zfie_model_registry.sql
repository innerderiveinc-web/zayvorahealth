-- Migration: 026_zfie_model_registry
CREATE TABLE IF NOT EXISTS zfie_model_registry (model_id TEXT PRIMARY KEY, name TEXT, version TEXT, algorithm TEXT, trained_at REAL);
