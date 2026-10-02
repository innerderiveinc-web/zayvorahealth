-- Migration: 007_zfie_compounds
CREATE TABLE IF NOT EXISTS zfie_compounds (canonical_id TEXT PRIMARY KEY, common_name TEXT, molecular_formula TEXT, molecular_weight REAL, smiles TEXT, pubchem_cid INTEGER);
