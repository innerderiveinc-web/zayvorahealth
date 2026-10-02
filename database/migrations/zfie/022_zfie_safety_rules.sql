-- Migration: 022_zfie_safety_rules
CREATE TABLE IF NOT EXISTS zfie_safety_rules (rule_id TEXT PRIMARY KEY, substance_id TEXT, rule_type TEXT, trigger_condition TEXT, action TEXT);
