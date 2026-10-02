-- Migration: 004_zfie_formula_ingredients
CREATE TABLE IF NOT EXISTS zfie_formula_ingredients (id TEXT PRIMARY KEY, version_id TEXT NOT NULL, mufrad_id TEXT NOT NULL, botanical_name TEXT, ratio REAL, part_used TEXT, processing_method TEXT);
