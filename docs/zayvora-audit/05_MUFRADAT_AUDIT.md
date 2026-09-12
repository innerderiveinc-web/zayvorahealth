# ZAYVORA HEALTH™ — Production Readiness Audit
## 05. Mufradat Taxonomy & Single Herb Ontology Audit
*Tagline: “Ancient Wisdom. Modern Science. Intelligent Care.”*

---

### 1. Scope of Mufradat Registry
Single herbal, mineral, and animal drugs (*Mufradat*) represent the therapeutic building blocks of Unani medicine:
- **Canonical Naming**: Unani name, Arabic/Persian synonyms, botanical binomial, family.
- **Mizaj Degrees**: Scale of 1 to 4 in Heat, Cold, Dryness, Moisture.
- **Af'al**: Primary pharmacological actions (e.g. *Muhallil*, *Mufattih*, *Munajjij*, *Musakkin*).
- **Posology**: Safe single and daily dose ceilings in milligrams and grams.
- **Musleh & Badal**: Corrective agents and substitute botanicals.

---

### 2. Findings

#### Finding MF-01: Botanical Nomenclature & Posology Registry
1. **Feature/module name**: Mufradat Master Catalog & Dosage Rules
2. **Expected behavior**: Resolves any classical or common botanical name to verified binomial, posology limit, and corrective pairing.
3. **Actual implementation status**: Curated registry in `knowledge/data/mufradat_data.py` and service API in `services/knowledge/app/routers/mufradat.py`.
4. **Evidence**:
   - **file path**: `services/knowledge/app/taxonomy/mufradat_registry.py`
   - **function/class/component**: `MufradatRegistry.get_herb()`, `search_by_action()`
   - **API route**: `GET /api/v1/knowledge/mufradat/{id}`, `GET /api/v1/knowledge/mufradat`
   - **database table**: Neo4j node `(:Mufrad)` and indexed in-memory dictionary
   - **test result**: `test_taxonomy.py` — PASSED (5/5 tests passing)
5. **Status**: FULLY IMPLEMENTED
6. **Severity**: P2 Medium
7. **Recommended fix**: Link each herb entry to the AYUSH Pharmacopoeia of India (UPI) monograph volume and page numbers.
8. **Dependencies**: `services/knowledge`
9. **Acceptance criteria**: Single herb posology checks accurately flag dosages exceeding maximum daily limits.
