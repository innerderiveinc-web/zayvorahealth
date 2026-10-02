-- Migration: 020_zfie_experiment_results
CREATE TABLE IF NOT EXISTS zfie_experiment_results (id TEXT PRIMARY KEY, experiment_id TEXT, raw_data_uri TEXT, effect_size REAL, p_value REAL, replicates INTEGER, validation_status TEXT);
