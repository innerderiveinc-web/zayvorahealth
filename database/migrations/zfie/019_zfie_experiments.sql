-- Migration: 019_zfie_experiments
CREATE TABLE IF NOT EXISTS zfie_experiments (experiment_id TEXT PRIMARY KEY, hypothesis_id TEXT, title TEXT, protocol_reference TEXT, lead_investigator TEXT, status TEXT);
