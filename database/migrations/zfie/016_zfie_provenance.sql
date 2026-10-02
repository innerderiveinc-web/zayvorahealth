-- Migration: 016_zfie_provenance
CREATE TABLE IF NOT EXISTS zfie_provenance (provenance_id TEXT PRIMARY KEY, source_name TEXT, dataset_version TEXT, retrieval_date TEXT, license_type TEXT);
