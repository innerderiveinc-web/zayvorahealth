-- Migration: 012_zfie_pathway_links
CREATE TABLE IF NOT EXISTS zfie_pathway_links (id TEXT PRIMARY KEY, target_id TEXT, pathway_id TEXT);
