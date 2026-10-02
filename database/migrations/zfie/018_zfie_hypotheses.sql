-- Migration: 018_zfie_hypotheses
CREATE TABLE IF NOT EXISTS zfie_hypotheses (hypothesis_id TEXT PRIMARY KEY, formulation_id TEXT, statement TEXT, falsification_criteria TEXT, target_protein TEXT, status TEXT);
