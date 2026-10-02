-- Migration: 024_zfie_synergy
CREATE TABLE IF NOT EXISTS zfie_synergy (candidate_id TEXT PRIMARY KEY, formulation_id TEXT, compound_a TEXT, compound_b TEXT, model_used TEXT, ci REAL, status TEXT);
