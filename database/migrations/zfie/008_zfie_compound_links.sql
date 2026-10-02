-- Migration: 008_zfie_compound_links
CREATE TABLE IF NOT EXISTS zfie_compound_links (id TEXT PRIMARY KEY, mufrad_id TEXT, compound_id TEXT, concentration_range TEXT);
