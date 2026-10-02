-- Migration: 010_zfie_target_links
CREATE TABLE IF NOT EXISTS zfie_target_links (id TEXT PRIMARY KEY, compound_id TEXT, target_id TEXT, binding_energy_kcal_mol REAL, evidence_level TEXT);
