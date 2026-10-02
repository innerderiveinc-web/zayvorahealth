-- Migration: 006_zfie_chemical_fingerprints
CREATE TABLE IF NOT EXISTS zfie_chemical_fingerprints (fingerprint_id TEXT PRIMARY KEY, batch_id TEXT, peaks_json TEXT, similarity_score REAL);
