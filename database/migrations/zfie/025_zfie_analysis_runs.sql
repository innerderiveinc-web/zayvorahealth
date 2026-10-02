-- Migration: 025_zfie_analysis_runs
CREATE TABLE IF NOT EXISTS zfie_analysis_runs (run_id TEXT PRIMARY KEY, formulation_id TEXT, version_id TEXT, batch_id TEXT, mode TEXT, status TEXT, executed_at REAL, result_json TEXT);
