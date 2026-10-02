-- Migration: 015_zfie_evidence
CREATE TABLE IF NOT EXISTS zfie_evidence (evidence_id TEXT PRIMARY KEY, level TEXT, title TEXT, doi TEXT, sample_size INTEGER, study_design TEXT, reviewer TEXT);
