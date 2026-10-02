-- Migration: 002_zfie_formulations
CREATE TABLE IF NOT EXISTS zfie_formulations (id TEXT PRIMARY KEY, name TEXT NOT NULL, traditional_name TEXT, classical_source TEXT, therapeutic_target TEXT, created_at REAL);
