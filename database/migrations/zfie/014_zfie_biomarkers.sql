-- Migration: 014_zfie_biomarkers
CREATE TABLE IF NOT EXISTS zfie_biomarkers (marker_id TEXT PRIMARY KEY, name TEXT, standard_range TEXT, unit TEXT);
