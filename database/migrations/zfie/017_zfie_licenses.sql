-- Migration: 017_zfie_licenses
CREATE TABLE IF NOT EXISTS zfie_licenses (license_id TEXT PRIMARY KEY, name TEXT, commercial_use INTEGER, derivative_rights INTEGER);
