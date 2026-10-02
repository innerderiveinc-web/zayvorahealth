-- Migration: 011_zfie_pathways
CREATE TABLE IF NOT EXISTS zfie_pathways (canonical_id TEXT PRIMARY KEY, pathway_name TEXT, kegg_id TEXT, organ_axis TEXT);
