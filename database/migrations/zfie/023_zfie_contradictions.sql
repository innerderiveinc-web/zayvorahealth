-- Migration: 023_zfie_contradictions
CREATE TABLE IF NOT EXISTS zfie_contradictions (contradiction_id TEXT PRIMARY KEY, formulation_id TEXT, claim_a TEXT, source_a TEXT, claim_b TEXT, source_b TEXT, status TEXT);
