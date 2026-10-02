-- Migration: 013_zfie_biological_states
CREATE TABLE IF NOT EXISTS zfie_biological_states (state_id TEXT PRIMARY KEY, patient_id TEXT, profile_json TEXT, evaluated_at REAL);
