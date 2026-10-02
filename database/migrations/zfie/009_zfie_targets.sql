-- Migration: 009_zfie_targets
CREATE TABLE IF NOT EXISTS zfie_targets (canonical_id TEXT PRIMARY KEY, gene_symbol TEXT, target_name TEXT, uniprot_id TEXT, organ_axis TEXT, pdb_code TEXT);
