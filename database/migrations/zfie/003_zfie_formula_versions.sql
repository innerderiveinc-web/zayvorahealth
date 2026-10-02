-- Migration: 003_zfie_formula_versions
CREATE TABLE IF NOT EXISTS zfie_formula_versions (version_id TEXT PRIMARY KEY, formulation_id TEXT NOT NULL, version_tag TEXT NOT NULL, hash_signature TEXT, created_at REAL, parent_version TEXT, change_rationale TEXT);
