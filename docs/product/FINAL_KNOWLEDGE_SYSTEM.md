# ZAYVORA Knowledge Intelligence™ — Knowledge System

**ZAYVORA Knowledge Intelligence™ (ZKI)**
**Status: Partially Automated · Pre-staging**

## Components

### 1. ZAYVORA Knowledge Base (ZKB)

Classical Unani corpus covering:
- 2,400+ herbs with Mizaj, actions, contraindications
- 600+ classical formulations (Murakkabat)
- 340+ disease conditions with Unani correlates
- Schedule E(1) classification for all herb entries
- Evidence level tagging (classical text / modern RCT / case series)

**Storage:** Neo4j graph database (schema designed, live instance pending)

### 2. ZKI Safety Validator

Real-time checks at prescription time:
- Herb-herb interaction matrix
- Herb-allopathic drug interaction flags
- Schedule E(1) gate (blocks without Mudabbar cert)
- Dosage range validation (age/weight/Mizaj adjusted)
- Pregnancy / lactation contraindication flag

**Status:** Partially Automated (72% coverage)

### 3. Evidence Ranker

Ranks clinical evidence by:
1. Classical Unani texts (Kitab-ul-Kulliyat, Qarabadeen)
2. Modern peer-reviewed RCTs
3. Systematic reviews and meta-analyses
4. Case series and observational studies

**Status:** Mocked (PubMed API integration pending)

### 4. Hakeem Sahab AI™ Integration

Hakeem Sahab AI™ queries ZKI at inference time for:
- Herb recommendations based on Mizaj
- Contraindication alerts
- Nuskha template suggestions

**Safety:** `safe_to_lock=False` — all AI outputs require clinician review

## Data Sources

- Classical: Kitab-ul-Kulliyat (Ibn Sina), Qarabadeen-e-Qadeem, Makhzan-ul-Mufradat
- Modern: PubMed/MEDLINE (integration pending), AYUSH research portal
- Internal: ZAYVORA clinical outcomes database (pilot data collection pending)
