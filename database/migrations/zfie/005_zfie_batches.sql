-- Migration: 005_zfie_batches
CREATE TABLE IF NOT EXISTS zfie_batches (batch_id TEXT PRIMARY KEY, formulation_id TEXT NOT NULL, formula_version TEXT, lot_number TEXT NOT NULL, manufacture_date TEXT, expiry_date TEXT, quality_status TEXT, hplc_fingerprint_id TEXT);
