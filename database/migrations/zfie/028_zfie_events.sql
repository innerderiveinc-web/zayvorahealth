-- Migration: 028_zfie_events
CREATE TABLE IF NOT EXISTS zfie_events (event_id TEXT PRIMARY KEY, event_type TEXT, payload_json TEXT, created_at REAL);
