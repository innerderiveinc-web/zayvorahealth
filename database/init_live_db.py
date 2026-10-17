import sqlite3
import os
import hashlib
import json
import uuid
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

DB_PATH = os.path.join(os.path.dirname(__file__), "zayvora_live.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    if not salt:
        salt = uuid.uuid4().hex[:16]
    hashed = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
    return hashed, salt

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA busy_timeout=10000")
    cursor = conn.cursor()
    
    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read())
        
    # Seed Facilities
    facilities = [
        ("FAC-HQ-01", "ZAYVORA Health — Virtual Matab & Tele-Care HQ", "ZAYVORA-TELE-HQ", "VIRTUAL_CLINIC", "Digital Consultations & Tele-Care Headquarters", "New Delhi", "Delhi", "+91 97738 82657", 1),
        ("FAC-BRANCH-02", "ZAYVORA Partner Node (Testing)", "ZAYVORA-TEST-02", "CLINIC", "Clinical Testing Node", "Hyderabad", "Telangana", "+91 40 2452 1102", 1),
    ]
    cursor.executemany("""
    INSERT INTO facilities (id, name, code, facility_type, address, city, state, contact_phone, is_active)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, facilities)

    # Seed Users
    pwd_hash, salt = hash_password("admin123")
    doc_hash, doc_salt = hash_password("doctor123")
    rec_hash, rec_salt = hash_password("reception123")
    pharm_hash, pharm_salt = hash_password("pharmacy123")

    # Primary requested credentials
    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-ADMIN-REQ", "admin@zayvorahealth.com", pwd_hash, salt, "Enterprise Super Administrator", "+91 98110 00001", "SUPER_ADMIN", "FAC-HQ-01"))

    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-DOC-REQ1", "dr.irfan@zayvorahealth.com", doc_hash, doc_salt, "Hakeem Dr. Irfan Ashraf", "+91 98110 44219", "DOCTOR", "FAC-HQ-01"))

    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-DOC-REQ2", "doctor2@zayvorahealth.com", doc_hash, doc_salt, "Consulting Physician (Room 2)", "+91 98480 33110", "DOCTOR", "FAC-HQ-01"))

    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-REC-REQ", "reception@zayvorahealth.com", rec_hash, rec_salt, "OPD Reception Desk", "+91 98110 55301", "RECEPTIONIST", "FAC-HQ-01"))

    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-PHARM-REQ", "pharmacy@zayvorahealth.com", pharm_hash, pharm_salt, "Matab Pharmacy Counter", "+91 98110 88123", "PHARMACIST", "FAC-HQ-01"))

    nurse_hash, nurse_salt = hash_password("nurse123")
    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-NURSE-REQ", "nurse@zayvorahealth.com", nurse_hash, nurse_salt, "Inpatient Nursing Station", "+91 98110 77201", "NURSE", "FAC-HQ-01"))

    mfg_hash, mfg_salt = hash_password("admin123")
    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-MFG-REQ", "manufacturing@zayvorahealth.com", mfg_hash, mfg_salt, "Botanical QA/QC Lab", "+91 98110 88201", "MANUFACTURING", "FAC-HQ-01"))

    res_hash, res_salt = hash_password("doctor123")
    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-RES-REQ", "research@zayvorahealth.com", res_hash, res_salt, "Clinical Research Department", "+91 98110 99201", "RESEARCH", "FAC-HQ-01"))

    # Secondary clinical desks
    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-DOC-02", "doctor3@zayvorahealth.com", doc_hash, doc_salt, "Consulting Physician (Branch)", "+91 98480 33110", "DOCTOR", "FAC-BRANCH-02"))

    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-REC-01", "reception2@zayvorahealth.com", rec_hash, rec_salt, "OPD Registration Counter 2", "+91 98110 55301", "RECEPTIONIST", "FAC-HQ-01"))

    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-PHARM-01", "dispensary2@zayvorahealth.com", pharm_hash, pharm_salt, "Dispensary Counter 2", "+91 98110 88123", "PHARMACIST", "FAC-HQ-01"))
    
    pat_hash, pat_salt = hash_password("password123")
    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, mrn, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-PAT-01", "hamza.farooqi@gmail.com", pat_hash, pat_salt, "Hamza Farooqi", "+91 98110 44219", "PATIENT", "MRN-2026-0814", "FAC-HQ-01"))

    pat2_hash, pat2_salt = hash_password("password123")
    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, mrn, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-PAT-02", "bilqees.begum@gmail.com", pat2_hash, pat2_salt, "Bilqees Begum", "+91 98480 99221", "PATIENT", "MRN-2026-0901", "FAC-BRANCH-02"))

    ahmad_hash, ahmad_salt = hash_password("password123")
    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, mrn, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-PAT-AHMAD", "ahmad.khan@example.com", ahmad_hash, ahmad_salt, "Ahmad Khan", "+91 98110 12345", "PATIENT", "MRN-2026-0001", "FAC-HQ-01"))

    cursor.execute("""
    INSERT INTO patients (id, mrn, user_id, first_name, last_name, date_of_birth, gender, contact_phone, contact_email, blood_group, mizaj_dominant, allergies_json, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("PAT-0001", "MRN-2026-0001", "USR-PAT-AHMAD", "Ahmad", "Khan", "1990-03-15", "Male", "+91 98110 12345", "ahmad.khan@example.com", "B+", "Damawi (Sanguine)", json.dumps([]), "FAC-HQ-01"))

    # Seed Patients (HQ & Branch)
    cursor.execute("""
    INSERT INTO patients (id, mrn, user_id, first_name, last_name, date_of_birth, gender, contact_phone, contact_email, blood_group, mizaj_dominant, allergies_json, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("PAT-0814", "MRN-2026-0814", "USR-PAT-01", "Hamza", "Farooqi", "1982-04-12", "Male", "+91 98110 44219", "hamza.farooqi@gmail.com", "B+", "Balghami (Cold & Moist)", json.dumps(["Sonf (Foeniculum vulgare)"]), "FAC-HQ-01"))

    cursor.execute("""
    INSERT INTO patients (id, mrn, user_id, first_name, last_name, date_of_birth, gender, contact_phone, contact_email, blood_group, mizaj_dominant, allergies_json, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("PAT-0815", "MRN-2026-0815", None, "Ayesha", "Siddiqui", "1990-08-23", "Female", "+91 98221 55301", "ayesha.siddiqui@gmail.com", "O+", "Safrawi (Hot & Dry)", json.dumps([]), "FAC-HQ-01"))

    cursor.execute("""
    INSERT INTO patients (id, mrn, user_id, first_name, last_name, date_of_birth, gender, contact_phone, contact_email, blood_group, mizaj_dominant, allergies_json, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("PAT-0816", "MRN-2026-0816", None, "Mohammed", "Zeeshan", "1988-11-05", "Male", "+91 98334 77190", "m.zeeshan@gmail.com", "A+", "Damawi (Sanguine)", json.dumps([]), "FAC-HQ-01"))

    cursor.execute("""
    INSERT INTO patients (id, mrn, user_id, first_name, last_name, date_of_birth, gender, contact_phone, contact_email, blood_group, mizaj_dominant, allergies_json, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("PAT-0901", "MRN-2026-0901", "USR-PAT-02", "Bilqees", "Begum", "1975-02-18", "Female", "+91 98480 99221", "bilqees.begum@gmail.com", "AB+", "Sawdawi (Cold & Dry)", json.dumps([]), "FAC-BRANCH-02"))

    # Seed Appointments & OPD Queue (1 Completed Test Appointment for Foreign Key Compliance, Active Queue: 0)
    appointments = [
        ("APT-104", "T-TEST", "MRN-2026-0814", "Hamza Farooqi [TEST]", "Hakeem Dr. Irfan Ashraf", "CCIM-U-1988-0412", "Integrative Unani OPD", "Room 3", "2026-09-13", "10:15 AM", "STANDARD", "Sandbox Verification Record", "COMPLETED", 0.0, "PAID", "FAC-HQ-01"),
    ]
    cursor.executemany("""
    INSERT INTO appointments (id, token_number, mrn, patient_name, doctor_name, doctor_reg, department, opd_room, appointment_date, appointment_time, acuity, chief_complaint, status, fee_amount, payment_status, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, appointments)

    # Seed Inventory (Phase 4 FEFO, Batch Allocation & Mudabbar Gates)
    inventory = [
        ("INV-001", "Majun Suranjan (Mudabbar)", "MS-2026-LOT4", "2027-08-30", 500, 25, "CLINIC_UNANI", 240.0, 1, 1, "SHA256:7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b", "FAC-HQ-01"),
        ("INV-002", "Roghan-e-Balsan", "RB-2026-LOT1", "2028-01-15", 350, 15, "RETAIL_UNANI", 180.0, 0, 0, None, "FAC-HQ-01"),
        ("INV-003", "Habb-e-Suranjan Forte", "HS-2026-LOT3", "2027-08-31", 400, 30, "CLINIC_UNANI", 310.0, 1, 1, "SHA256:f1e2d3c4b5a6978800112233445566778899aabbccddeeff0011223344556677", "FAC-HQ-01"),
        ("INV-004", "MetaboCore Elite Powder", "MCE-2026-LOT2", "2028-06-20", 500, 50, "AYUSH_PROPRIETARY", 450.0, 0, 0, None, "FAC-HQ-01"),
        ("INV-005", "RestoreVital Herbal Infusion", "RVH-2026-LOT5", "2028-11-15", 600, 60, "FSSAI_SUPPLEMENT", 280.0, 0, 0, None, "FAC-HQ-01"),
        ("INV-006", "Khamira Gaozaban Ambari", "KGA-2026-B1", "2027-12-31", 300, 20, "CLINIC_UNANI", 190.0, 0, 0, None, "FAC-BRANCH-02"),
        ("INV-007", "Majun Suranjan (Mudabbar)", "MS-2026-LOT5", "2027-05-15", 45, 20, "CLINIC_UNANI", 240.0, 1, 1, "SHA256:7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b", "FAC-HQ-01"),
        ("INV-008", "Majun Suranjan (Unpurified Raw)", "MS-2026-RAW", "2028-01-01", 100, 10, "CLINIC_UNANI", 180.0, 1, 1, None, "FAC-HQ-01"),
        ("INV-009", "Roghan-e-Balsan (Expired)", "RB-2024-EXP", "2024-12-31", 20, 10, "RETAIL_UNANI", 150.0, 0, 0, None, "FAC-HQ-01"),
    ]
    cursor.executemany("""
    INSERT INTO inventory (id, name, batch_number, expiry_date, stock_qty, min_threshold, category, unit_price, is_schedule_e1, mudabbar_required, mudabbar_cert, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, inventory)

    # Seed Prescription
    rx_items = [
        {"name": "Majun Suranjan (Mudabbar)", "dose": "5g twice daily with lukewarm water", "duration": "14 days", "isScheduleE1": True, "batchNumber": "MS-2026-LOT4"},
        {"name": "Roghan-e-Balsan", "dose": "Local gentle application nocte", "duration": "14 days", "isScheduleE1": False, "batchNumber": "RB-2026-LOT1"}
    ]
    cursor.execute("""
    INSERT INTO prescriptions (id, order_number, mrn, patient_name, doctor_name, doctor_reg, items_json, dietary_advice, regimenal_advice, signature_hash, status, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "RX-001",
        "RX-2026-0441",
        "MRN-2026-0814",
        "Hamza Farooqi",
        "Prof. (Dr.) Mansoor Alam",
        "CCIM-U-1988-0412",
        json.dumps(rx_items),
        "Avoid sour, cold, and flatulent foods. Prefer warm ginger decoction.",
        "Nutool Haar with warm water daily for 10 minutes.",
        "731f5cf53472e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495",
        "PENDING_VERIFICATION",
        "FAC-HQ-01"
    ))

    # Seed 25 Contiguous Audit Blocks for 21 CFR Part 11 Sequential Chain Integrity
    initial_audit_blocks = []
    prev_h = "0000000000000000000000000000000000000000000000000000000000000000"
    for blk_idx in range(1, 26):
        data_str = f"BLOCK-{blk_idx}|ZAYVORA-INIT-AUDIT|{prev_h}"
        curr_h = hashlib.sha256(data_str.encode("utf-8")).hexdigest()
        initial_audit_blocks.append((
            curr_h,
            "PRESCRIPTION_LOCKED_21CFR11" if blk_idx % 2 == 0 else "CONSULTATION_NOTE_SIGNED",
            "Prof. (Dr.) Mansoor Alam (CCIM-U-1988-0412)",
            "ANCHORED",
            "FAC-HQ-01",
            json.dumps({"block_index": blk_idx, "system": "ZAYVORA Health OS Genesis"})
        ))
        prev_h = curr_h

    cursor.executemany("""
    INSERT INTO audit_ledger (leaf_hash, event_type, signer, status, facility_id, details_json)
    VALUES (?, ?, ?, ?, ?, ?)
    """, initial_audit_blocks)

    # Seed Invoices (Clean Production Launch: Zero revenue by default)
    invoices = []
    if invoices:
        cursor.executemany("""
        INSERT INTO invoices (id, invoice_number, mrn, patient_name, amount, department, payment_method, status, prescription_id, items_json, facility_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, invoices)

    # Seed Encounters (Phase 3 Core Clinical Continuum)
    vitals_data = {"bp": "124/82", "pulse": "72", "temp": "98.4", "weight": "78", "spo2": "98", "hrv": "46.2"}
    soap_data = {
        "subjective": "Bilateral knee pain and morning stiffness (>45 min) aggravated by damp cold weather.",
        "objective": "Nabz: Bat'ee, Layyin. Lisan: Rutubat-e-Ghaliba, whitish fur. Patellofemoral crepitus present.",
        "assessment": "Waja-ul-Mafasil Barid Balghami (Osteoarthritis / Phlegmatic Arthropathy - ICD-11: FA00).",
        "plan": "Stage 2 Tahleel: Majun Suranjan 5g bd + Roghan Balsan local application + Nutool Haar."
    }
    mizaj_data = {
        "dominant": "Balghami (Cold & Moist)",
        "secondary": "Damawi",
        "su_e_mizaj": "Su-e-Mizaj Barid Balghami",
        "dyscrasia_degree": 2
    }
    axis_data = {
        "primary_axis": "Brain-Liver-Joint Triadic Axis",
        "status": "IMPAIRED_DRAINAGE",
        "rationale": "Phlegmatic humor congestion in synovial joints with sluggish systemic clearance."
    }
    afaal_data = {
        "current_stage": "TAHLEEL",
        "goals": ["Resolve morning knee stiffness to <15 min", "Reduce synovial fullness", "Achieve >40% VAS pain relief"],
        "regimen": "Nutool Haar with warm decoction for 10 minutes daily"
    }

    cursor.execute("""
    INSERT INTO encounters (id, encounter_number, mrn, patient_name, appointment_id, doctor_name, doctor_reg, facility_id, chief_complaint, examination_notes, vitals_json, soap_json, mizaj_json, organ_axis_json, afaal_cascade_json, prescription_id, status, signature_hash)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "ENC-001",
        "ENC-2026-0814",
        "MRN-2026-0814",
        "Hamza Farooqi",
        "APT-104",
        "Prof. (Dr.) Mansoor Alam",
        "CCIM-U-1988-0412",
        "FAC-HQ-01",
        "Bilateral knee stiffness & joint ache in damp weather",
        "Nabz: Bat'ee, Layyin. Lisan: Rutubat-e-Ghaliba. Joints: Mild crepitus, no acute erythema.",
        json.dumps(vitals_data),
        json.dumps(soap_data),
        json.dumps(mizaj_data),
        json.dumps(axis_data),
        json.dumps(afaal_data),
        "RX-001",
        "LOCKED_AND_SIGNED",
        "731f5cf53472e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495"
    ))

    # Seed Baseline AI Consultation
    ai_advisory = {
        "CLINICAL SUMMARY": "62-year-old male with chronic knee joint stiffness (Waja-ul-Mafasil Barid Balghami).",
        "WHAT IS KNOWN": "Known case of osteoarthritis with cold-moist humoral dyscrasia.",
        "UNANI PERSPECTIVE": "Sluggish phlegmatic drainage along Mafasil-Asab triadic axis.",
        "BIOMEDICAL PERSPECTIVE": "Bilateral knee osteoarthrosis, radiological Kellgren-Lawrence Grade II.",
        "DIFFERENTIAL CONSIDERATIONS": "Waja-ul-Mafasil, Niqris (Gout), Osteoarthritis, Pseudogout.",
        "RED FLAGS": "None reported in current presentation. No acute septic arthritis.",
        "MISSING INFORMATION": "Recent serum uric acid and inflammatory markers (ESR/CRP).",
        "EVIDENCE": "UPI Monograph Vol I: Majun Suranjan & Suranjan Talkh Mudabbar indicated for joint arthralgia.",
        "SAFETY": "Schedule E(1) alkaloid (Colchicine). Mandatory Mudabbar certification required. Renal clearance monitoring advised.",
        "POSSIBLE CARE OPTIONS": "Majun Suranjan 5g nocte, Roghan Suranjan local application, Dalak Layyin regimen.",
        "MONITORING": "Follow-up at 14 days to assess VAS pain reduction and joint mobility.",
        "UNCERTAINTY": "Low uncertainty. Presentation concordant with classical descriptions.",
        "CLINICIAN REVIEW REQUIRED": "Yes — this AI advisory requires non-delegable clinician review before clinical action."
    }
    ai_citations = [
        {"title": "Suranjan Talkh Monograph", "source": "Unani Pharmacopoeia of India (UPI) Vol 1", "part": "Dried corm", "schedule": "Schedule E(1)", "mudabbar": "Boiled in cow's milk (Sheer-e-Gao)"},
        {"title": "Majun Suranjan Classical Formulation", "source": "National Formulary of Unani Medicine (NFUM) Part I", "dosage": "5g post-prandial"}
    ]
    cursor.execute("""
    INSERT INTO ai_consultations (id, consultation_id, mrn, patient_name, doctor_name, chief_complaint, organ_axis, mizaj, advisory_sections_json, citations_json, safety_verdict, provider_used, safe_to_lock, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "AIC-001",
        "AI-CONSULT-001",
        "MRN-2026-0814",
        "Hamza Farooqi",
        "Prof. (Dr.) Mansoor Alam",
        "Bilateral knee stiffness & joint ache in damp weather",
        "mafasil-asab",
        "Balghami (Cold & Moist)",
        json.dumps(ai_advisory),
        json.dumps(ai_citations),
        "CAUTION",
        "Primary (Anthropic Claude 3.5 Sonnet)",
        0,
        "FAC-HQ-01"
    ))

    # Seed QSURA Baseline Notifications
    cursor.execute("""
    INSERT INTO notifications (id, notification_id, mrn, recipient, channel, template_id, message_text, status, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "NOTIF-001",
        "MSG-2026-9011",
        "MRN-2026-0814",
        "+91 98110 44219",
        "SMS",
        "DISPENSE_READY_NOTIFICATION",
        "Dear Hamza Farooqi, your customized Unani prescription from ZAYVORA Pharmacy is prepared and verified. Batch: MS-2026-LOT4. Dosage: Majun Suranjan 5g nocte with warm milk.",
        "DELIVERED",
        "FAC-HQ-01"
    ))

    # Seed Active Telemedicine Room
    cursor.execute("""
    INSERT INTO telemedicine_rooms (id, room_id, encounter_id, appointment_id, mrn, patient_name, doctor_name, session_token, status, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "ROOM-001",
        "TELE-ROOM-2026-HF",
        "ENC-001",
        "APT-104",
        "MRN-2026-0814",
        "Hamza Farooqi",
        "Prof. (Dr.) Mansoor Alam",
        "zyv.tele.d9f8e7a6b5c4.webrtc",
        "ACTIVE",
        "FAC-HQ-01"
    ))

    # Seed System Provenance Metadata
    prov_data = [
        ("environment", "DEVELOPMENT_DEMO_FIXTURES"),
        ("data_custodian", "ZAYVORA Health OS Clinical Information Unit"),
        ("regulatory_compliance", "Digital Personal Data Protection Act, 2023 (read with DPDP Rules, 2025), IT Act 2000, & US-Export 21 CFR Part 11 / HIPAA Safe Harbor"),
        ("merkle_audit_root", "0x89aef23b0907d891bcae89012356789abcdef0123456789abcdef0123456789a"),
        ("clinical_intent", "Algorithm training, test suite execution & UI workflow demonstration.")
    ]
    cursor.executemany("INSERT OR REPLACE INTO system_provenance (key, value) VALUES (?, ?)", prov_data)

    # Seed Master Organ Axes (12 Canonical Axes)
    try:
        from services.knowledge.app.data.organ_axes_master import ORGAN_AXES_CATALOG
        axes_rows = [
            (
                ax["id"],
                ax.get("arabic_name", ""),
                ax.get("body_system", ""),
                ax.get("governing_power", ""),
                json.dumps(ax.get("key_diseases", [])),
                json.dumps(ax.get("primary_products", [])),
                ax.get("regulatory_track", ""),
                ax.get("description", "")
            )
            for ax in ORGAN_AXES_CATALOG.values()
        ]
        cursor.executemany("INSERT OR REPLACE INTO master_organ_axes VALUES (?, ?, ?, ?, ?, ?, ?, ?)", axes_rows)
    except Exception as e:
        print(f"Warning: could not seed master_organ_axes: {e}")

    # Seed Master Protocols (21 Clinical Protocols)
    try:
        from services.knowledge.app.data.protocols_master import MASTER_PROTOCOLS
        proto_rows = [
            (
                p["id"],
                p.get("name", ""),
                p.get("category", ""),
                p.get("organ_axis", ""),
                p.get("icd11_code", ""),
                p.get("primary_humor", ""),
                json.dumps(p.get("phase1", {})),
                json.dumps(p.get("phase2", {})),
                json.dumps(p.get("phase3", {})),
                json.dumps(p.get("product_stack", {})),
                json.dumps(p.get("lab_monitoring", [])),
                json.dumps(p.get("clinical_warnings", []))
            )
            for p in MASTER_PROTOCOLS.values()
        ]
        cursor.executemany("INSERT OR REPLACE INTO master_protocols VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", proto_rows)
    except Exception as e:
        print(f"Warning: could not seed master_protocols: {e}")

    # Seed Master Protocol Kits (21 Protocol Kits)
    try:
        from services.knowledge.app.data.kits_master import MASTER_KITS
        kit_rows = [
            (
                k["kit_id"],
                k.get("name", ""),
                k.get("protocol_id", ""),
                k.get("category", ""),
                json.dumps(k.get("products", [])),
                float(k.get("monthly_price", 0.0))
            )
            for k in MASTER_KITS.values()
        ]
        cursor.executemany("INSERT OR REPLACE INTO master_protocol_kits VALUES (?, ?, ?, ?, ?, ?)", kit_rows)
    except Exception as e:
        print(f"Warning: could not seed master_protocol_kits: {e}")

    # Seed Master Products (32 Products)
    try:
        from services.knowledge.app.data.products_master import MASTER_PRODUCTS
        prod_rows = [
            (
                p["sku"],
                p.get("name", ""),
                p.get("category", ""),
                p.get("section", ""),
                p.get("organ_axis", ""),
                1 if p.get("is_prescription_required") else 0,
                p.get("dosage_form") or p.get("formulation_type", ""),
                p.get("daily_dose") or p.get("dosage", ""),
                json.dumps(p.get("composition", [])),
                json.dumps(p.get("contraindications", [])),
                json.dumps(p.get("monitoring", [])),
                json.dumps(p.get("citations", [])),
                float(p.get("mrp") or p.get("mrp_inr", 0.0)),
                float(p.get("b2b_price") or (float(p.get("mrp_inr", 0.0)) * 0.5)),
                p.get("regulatory_track", ""),
                p.get("unani_name", ""),
                1 if p.get("is_hero_launch") else 0
            )
            for p in MASTER_PRODUCTS.values()
        ]
        cursor.executemany("INSERT OR REPLACE INTO master_products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", prod_rows)
    except Exception as e:
        print(f"Warning: could not seed master_products: {e}")

    # Seed Master Parhez (8 Protocols)
    try:
        from services.knowledge.app.data.parhez_master import MASTER_PARHEZ
        parhez_rows = [
            (
                pz["code"],
                pz.get("name", ""),
                pz.get("classical_principle", ""),
                json.dumps(pz.get("target_axes", [])),
                int(pz.get("duration_days", 30)),
                json.dumps(pz.get("rules", []))
            )
            for pz in MASTER_PARHEZ.values()
        ]
        cursor.executemany("INSERT OR REPLACE INTO master_parhez VALUES (?, ?, ?, ?, ?, ?)", parhez_rows)
    except Exception as e:
        print(f"Warning: could not seed master_parhez: {e}")

    # Seed Authoritative Clinician Credential Registry (Layers 2 & 3)
    clinicians = [
        (
            "CLN-IRFAN-01",
            "USR-DOC-REQ1",
            "Reg. No: (Updating / Verification in Progress)",
            "Board of Ayurvedic and Unani Systems of Medicine / NCISM",
            "Delhi",
            "PERMANENT",
            "UNANI_MEDICINE",
            "BUMS (AKTC Aligarh Muslim University, Batch 2002, Passed 2007)",
            "ALL",
            "CONSULTANT_TABEEB",
            "2007-06-15",
            "2030-06-14",
            "UPDATING_VERIFICATION",
            "REGISTRAR_NCISM",
            "2026-01-10 10:00:00"
        ),
        (
            "CLN-MANSOOR-02",
            "USR-DOC-02",
            "UP-UNANI-2012-08819",
            "Uttar Pradesh Board of Indian Medicine / NCISM",
            "Uttar Pradesh",
            "PERMANENT",
            "MOALAJAT",
            "BUMS",
            "FAC-HQ-01",
            "CONSULTANT_TABEEB",
            "2012-04-20",
            "2028-04-19",
            "VERIFIED_ACTIVE",
            "REGISTRAR_NCISM",
            "2026-01-10 10:00:00"
        ),
        (
            "CLN-MALIK-03",
            "USR-DOC-REQ2",
            "TEL-UNANI-2020-03310",
            "Telangana Board of Indian Medicine / NCISM",
            "Telangana",
            "PERMANENT",
            "UNANI_MEDICINE",
            "BUMS",
            "FAC-BRANCH-02",
            "GENERAL_PRACTICE",
            "2020-08-11",
            "2027-08-10",
            "VERIFIED_ACTIVE",
            "REGISTRAR_NCISM",
            "2026-01-10 10:00:00"
        )
    ]
    cursor.executemany("""
    INSERT OR REPLACE INTO clinician_registry (
        clinician_id, user_id, registration_number, registration_body, registration_state,
        registration_type, specialty, qualification, facility_scope, clinical_scope,
        issued_at, expires_at, verification_status, verified_by, verified_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, clinicians)

    # Seed Canonical Evidence Sources (Layer 14 — Classical Canon, Pharmacopoeias & Modern Textbooks)
    sources = [
        ("SRC-UPI-VOL1", "The Unani Pharmacopoeia of India, Part I, Volume I", "Department of AYUSH, Ministry of Health and Family Welfare", "1st Edition", 2007, "ISBN 978-81-904000-0-8", "PHARMACOPOEIA", "INDIA", "a1b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef0"),
        ("SRC-UPI-VOL2", "The Unani Pharmacopoeia of India, Part I, Volume II", "Department of AYUSH, Ministry of Health and Family Welfare", "1st Edition", 2008, "ISBN 978-81-904000-1-5", "PHARMACOPOEIA", "INDIA", "b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef01a"),
        ("SRC-NFUM-PT1", "National Formulary of Unani Medicine, Part I", "Department of AYUSH, Ministry of Health and Family Welfare", "Reprint Edition", 2006, "ISBN 978-81-904000-2-2", "PHARMACOPOEIA", "INDIA", "c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef01ab2"),
        ("SRC-IBN-SINA-CANON", "Al-Qanun fi al-Tibb (The Canon of Medicine)", "Ibn Sina (Avicenna, 980–1037 CE)", "Canonical Bulaq Edition / Rome 1593", 1593, "CANON-AVICENNA-1025-CE", "CLASSICAL_CANON", "GLOBAL", "d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef01ab2c3"),
        ("SRC-IBN-BAITAR-JAMI", "Kitab al-Jami' li-Mufradat al-Adwiya wa-al-Aghdhiya (Grand Botanical Compendium)", "Ibn al-Baitar (Diya al-Din al-Malaqi, 1197–1248 CE)", "Dar al-Kutub al-Ilmiyyah / Bulaq Edition", 1874, "IBN-BAITAR-JAMI-1248-CE", "CLASSICAL_CANON", "GLOBAL", "b78a6846ec361d9a27eb2a1d3545df44e21df903901b0f19a0a4c0eb3f8a481e"),
        ("SRC-AL-RAZI-HAWI", "Kitab al-Hawi fi al-Tibb (Continens Liber, 23 Volumes)", "Abu Bakr Muhammad ibn Zakariyya al-Razi (Rhazes, 865–925 CE)", "Dairat-ul-Ma'arif al-Osmania, Hyderabad Edition", 1955, "AL-RAZI-HAWI-925-CE", "CLASSICAL_CANON", "GLOBAL", "db6bd1b8c2f216503c73bb1b59074092b7617ea2d46e2794323c21a4d0ec353e"),
        ("SRC-AL-MAJUSI-KAMIL", "Kamil al-Sina'a al-Tibbiyya (Al-Kitab al-Maliki / Liber Regius)", "Ali ibn al-Abbas al-Majusi (Haly Abbas, c. 930–994 CE)", "Bulaq Classical Cairo Edition", 1877, "AL-MAJUSI-KAMIL-994-CE", "CLASSICAL_CANON", "GLOBAL", "1ae7e9b9519f85c3db6eec6a9e144a1ebfe407ae0e7e1fec3b51909a8037fe6a"),
        ("SRC-AL-ZAHRAWI-TASREEF", "Kitab al-Tasreef liman 'Ajiza 'an al-Ta'leef (On Regimenal Surgery & Instruments)", "Abul Qasim Khalaf ibn al-Abbas al-Zahrawi (Albucasis, 936–1013 CE)", "Dar al-Kitab al-Lubnani / Oxford Edition", 1908, "AL-ZAHRAWI-TASREEF-1013-CE", "CLASSICAL_CANON", "GLOBAL", "ed66e89c45b2b2b1cf59f9c73bfa99b4aa238ff7594ec1d4cb8008003f56d97c"),
        ("SRC-AZAM-KHAN-AKSEER", "Akseer-e-Azam (Encyclopedia of Clinical Internal Medicine & Therapeutics, 4 Volumes)", "Hakim Muhammad Azam Khan (Nazim-e-Jahan, 1814–1902 CE)", "Munshi Nawal Kishore Press / CCRUM Edition", 1888, "ISBN 978-81-87748-02-1", "CLASSICAL_CANON", "INDIA", "d8f62840077c5ba84a51e60cb6c5ffaebe1e39a3f2c58908f972b9389cfbb78d"),
        ("SRC-AZAM-KHAN-MUHEET", "Muheet-e-Azam (Grand Compendium of Materia Medica, 4 Volumes)", "Hakim Muhammad Azam Khan (Nazim-e-Jahan, 1814–1902 CE)", "Central Council for Research in Unani Medicine (CCRUM)", 1896, "ISBN 978-93-83864-12-6", "CLASSICAL_CANON", "INDIA", "a5a7c3205ef29ea3be01901c80f6f4c1732a3fcbb0a40d5178fc66a26d7ca194"),
        ("SRC-AL-ALAWI-MAKHZAN", "Makhzan-ul-Advia (Compendium of Materia Medica & Pharmacology)", "Mir Muhammad Husain Al-Alawi Shirazi (1771 CE)", "Munshi Nawal Kishore Press, Lucknow Edition", 1874, "AL-ALAWI-MAKHZAN-1771-CE", "CLASSICAL_CANON", "INDIA", "d26ae7a30f5ee7aa6fcbe01524e931fa3c11f7c7ec518cf41f879bf73a4b9868"),
        ("SRC-ARZANI-TIBB-AKBAR", "Tibb-e-Akbar (Comprehensive Clinical Internal Medicine)", "Hakim Muhammad Akbar Arzani (d. 1722 CE)", "Munshi Nawal Kishore Press, Lucknow Edition", 1878, "ARZANI-TIBB-AKBAR-1700-CE", "CLASSICAL_CANON", "INDIA", "469a14d0a24b1a43a05b38d35e16ecf6e80b435ae53d10526e0be5a60395cb21"),
        ("SRC-KABIRUDDIN-BAYAZ", "Bayaz-e-Kabir (Vol I & II — Standard Unani Compounding & Formulary)", "Hakim Mohammad Kabiruddin", "Idara Kitab-us-Shifa, New Delhi Edition", 1938, "ISBN 978-81-89841-45-4", "PHARMACOPOEIA", "INDIA", "8e2b8362d10fbb101e1491cf0fc53cb1cbf8922e4ff9ca68e61234f9a0d81e01"),
        ("SRC-NAJMUL-GHANI-KHAZAIN", "Khazain-ul-Advia (3 Volumes — Comprehensive Materia Medica & Action of Drugs)", "Hakim Najmul Ghani Rampuri (1859–1932 CE)", "Munshi Nawal Kishore Press / Idara Kitab-us-Shifa", 1926, "ISBN 978-81-89841-33-1", "PHARMACOPOEIA", "INDIA", "23fec9f2f1d93ebff12ebbf8ccb416e7aa7b031c3c9caae812c33ba20d2cb29a"),
        ("SRC-WHO-MED-PLANTS", "WHO Monographs on Selected Medicinal Plants (Volumes 1, 2, 3 & 4)", "World Health Organization (WHO), Geneva", "WHO Official Geneva Publications", 2009, "ISBN 978-92-4-154702-4", "MODERN_EVIDENCE", "GLOBAL", "0b236472fedbc5ce9ef23961da8187803e04746f3a3a78f6974e6f4a86b168ff"),
        ("SRC-ZAYVORA-CP-AFUM", "ZAYVORA Compendium of Axis-Based Functional Unani Medicine (CP-AFUM)", "Hakeem Dr. Irfan Ashraf, BUMS (AKTC AMU Aligarh, Batch 2002, Passed 2007)", "ZAYVORA Medical Publishing, 1st Edition", 2026, "ZYV-CP-AFUM-2026-REG", "CLINICAL_DOCTRINE", "INDIA", "7a2ed5499a2cbeec0fc1f71df42f77894a80698064d4b17f54c9cb2405073e6b")
    ]
    cursor.executemany("""
    INSERT OR REPLACE INTO evidence_sources (
        source_id, title, author, edition, publication_year, isbn_or_doi, source_type, jurisdiction, digital_sha256_checksum
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sources)

    # Seed Standard Unani Medical Terminology (CCRUM / AYUSH UMA)
    uma_json = os.path.join(BASE_DIR, "services", "knowledge", "app", "data", "standard_unani_terminology_uma.json")
    if os.path.exists(uma_json):
        try:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS unani_standard_terms (
                uma_code TEXT PRIMARY KEY,
                unani_term TEXT NOT NULL,
                english_equivalent TEXT,
                definition TEXT,
                source TEXT
            )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_unani_terms_term ON unani_standard_terms(unani_term)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_unani_terms_eng ON unani_standard_terms(english_equivalent)")
            with open(uma_json, "r", encoding="utf-8") as uf:
                uma_records = json.load(uf)
            cursor.executemany("""
            INSERT OR REPLACE INTO unani_standard_terms (uma_code, unani_term, english_equivalent, definition, source)
            VALUES (?, ?, ?, ?, ?)
            """, [(r["uma_code"], r["unani_term"], r.get("english_equivalent", ""), r.get("definition", ""), r.get("source", "")) for r in uma_records])
        except Exception as e:
            print(f"Note on UMA seeding: {e}")

    # Seed ZKB 250 Canonical Mufradat
    try:
        from services.knowledge.app.data.mufradat_250_registry import RAW_MUFRADAT_LIST, HIGH_RISK_28_REGISTRY
        mufradat_rows = []
        for item in RAW_MUFRADAT_LIST:
            zmf_id = item[0]
            urdu_name = item[1]
            botanical = item[2]
            family = item[3]
            part = item[4]
            mizaj = item[5]
            actions_raw = item[6] or ""
            actions_list = [a.strip() for a in actions_raw.split(";") if a.strip()]
            actions_json = json.dumps(actions_list)
            risk_level = item[9]
            is_high_risk = (zmf_id in HIGH_RISK_28_REGISTRY) or (risk_level == "CRITICAL")
            degree = 1
            if "3" in mizaj: degree = 3
            elif "4" in mizaj: degree = 4
            elif "2" in mizaj: degree = 2
            mufradat_rows.append((
                zmf_id,
                botanical.split("(")[0].strip() if "(" in botanical else botanical,
                urdu_name,
                urdu_name,
                urdu_name.title(),
                botanical,
                f"UPI-{zmf_id}",
                "VEGETABLE",
                part,
                mizaj,
                degree,
                1 if is_high_risk else 0,
                1 if is_high_risk else 0,
                "Classical Mudabbar Purification Protocol" if is_high_risk else None,
                "3g - 5g" if not is_high_risk else "250mg - 500mg (Mudabbar)",
                5.0 if not is_high_risk else 0.5,
                10.0 if not is_high_risk else 1.0,
                actions_json,
                json.dumps([]),
                json.dumps([]),
                "CONTRAINDICATED" if is_high_risk else "SAFE",
                "CONTRAINDICATED" if is_high_risk else "SAFE",
                "CONTRAINDICATED" if is_high_risk else "SAFE",
                "SAFE",
                "E1" if is_high_risk else "E2",
                "VERIFIED" if not is_high_risk else "RESTRICTED",
                0 if is_high_risk else 1
            ))
        cursor.executemany("""
        INSERT OR REPLACE INTO zkb_mufradat (
            id, canonical_name_latin, canonical_name_urdu, canonical_name_arabic,
            canonical_name_english, botanical_name, upi_code, origin_category,
            plant_part_used, mizaj_primary_quality, mizaj_degree, is_schedule_e1_poison,
            mandatory_mudabbar, mudabbar_protocol, historical_dose, approved_single_dose_max_grams,
            approved_daily_dose_max_grams, therapeutic_actions, badal_substitutes, musleh_correctives,
            pregnancy_status, lactation_status, pediatric_status, geriatric_status,
            evidence_level, current_lifecycle_state, safe_for_ai
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, mufradat_rows)
    except Exception as e:
        print(f"Note on zkb_mufradat seeding: {e}")

    # Seed Source Authors and Books
    try:
        from services.knowledge.app.core.source_registry import SourceRegistry
        s_reg = SourceRegistry()
        s_auth_rows = [(a["id"], a.get("canonical_name", ""), a.get("arabic_name", ""), a.get("persian_name", ""), a.get("urdu_name", ""), a.get("era_hijri", ""), a.get("era_ce", ""), a.get("biography_summary", ""), 1 if a.get("is_classical", True) else 0) for a in s_reg.authors.values()]
        cursor.executemany("""
        INSERT OR REPLACE INTO source_authors (
            id, canonical_name, arabic_name, persian_name, urdu_name,
            era_hijri, era_ce, biography_summary, is_classical
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, s_auth_rows)
        s_book_rows = [(b["id"], b.get("primary_author_id", ""), b.get("canonical_title", ""), b.get("original_title", ""), b.get("transliterated_title", ""), b.get("language_code", "ar"), b.get("discipline", ""), b.get("historical_era", ""), b.get("source_type", "CLASSICAL_TREATISE"), b.get("description", "")) for b in s_reg.books.values()]
        cursor.executemany("""
        INSERT OR REPLACE INTO source_books (
            id, primary_author_id, canonical_title, original_title, transliterated_title,
            language_code, discipline, historical_era, source_type, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, s_book_rows)
    except Exception as e:
        print(f"Note on source tables seeding: {e}")

    # Seed ZKB Drug Interactions (Herb-Drug Allopathic Safety Matrix)
    try:
        interactions = [
            ("INT-001", "ZMF-001", "Benzodiazepines / Sedatives (Diazepam, Alprazolam, Clonazepam)", "Additive central GABA-A receptor modulation and sedative synergism.", "Excessive daytime somnolence, psychomotor impairment, severe CNS depression.", "HIGH", "Monitor mental status closely; reduce benzodiazepine dosage by 25-50% if co-administered."),
            ("INT-002", "ZMF-001", "Thyroid Hormone Replacements (Levothyroxine)", "Withanolides stimulate endogenous T3 and T4 synthesis.", "Risk of additive thyrotoxicosis or elevated free T4 levels.", "MODERATE", "Monitor thyroid function tests (FT3, FT4, TSH) after 4 weeks of initiation."),
            ("INT-003", "ZMF-002", "CYP3A4 & P-gp Inhibitors (Clarithromycin, Ketoconazole, Erythromycin)", "Inhibition of intestinal P-glycoprotein and hepatic CYP3A4-mediated clearance of colchicine.", "Life-threatening acute colchicine toxicity: pancytopenia, severe neuromyopathy, rhabdomyolysis, shock.", "CRITICAL", "STRICTLY CONTRAINDICATED. Do not co-prescribe. Use non-colchicine alternatives."),
            ("INT-004", "ZMF-002", "HMG-CoA Reductase Inhibitors / Statins (Atorvastatin, Rosuvastatin)", "Synergistic skeletal muscle toxicity and inhibition of glucuronidation.", "Acute rhabdomyolysis, myoglobinuria, acute kidney injury.", "HIGH", "Temporarily withhold statin therapy during acute Suranjan treatment course; monitor serum CPK."),
            ("INT-005", "ZMF-003", "Class I & Class III Antiarrhythmics (Amiodarone, Flecainide, Sotalol)", "Aconitine binds voltage-gated sodium channels in open state, inducing prolonged action potential.", "Lethal polymorphic ventricular tachycardia, torsades de pointes, cardiac arrest.", "CRITICAL", "ABSOLUTELY CONTRAINDICATED. Co-prescription triggers fail-closed safety block."),
            ("INT-006", "ZMF-004", "Central Nervous System Stimulants (Caffeine, Theophylline, Modafinil)", "Strychnine antagonism of inhibitory postsynaptic glycine receptors synergizes with CNS stimulation.", "Hyperreflexia, muscle spasticity, generalized tetanic convulsions, respiratory arrest.", "CRITICAL", "ABSOLUTELY CONTRAINDICATED. Emergency clinical hold."),
            ("INT-007", "ZMF-005", "Opioid Analgesics (Tramadol, Morphine, Codeine, Fentanyl)", "Direct additive mu- and kappa-opioid receptor stimulation.", "Profound CNS depression, respiratory rate <8/min, fatal respiratory failure.", "CRITICAL", "ABSOLUTE CONTRAINDICATION. Fail-closed block enforced."),
            ("INT-008", "ZMF-005", "Monoamine Oxidase Inhibitors (MAOIs - Selegiline, Moclobemide)", "Inhibition of monoamine catabolism combined with natural opium alkaloids.", "Severe hyperpyrexic serotonin syndrome, hypertensive crisis, coma.", "CRITICAL", "STRICTLY CONTRAINDICATED. Washout period of 14 days required."),
            ("INT-009", "ZMF-006", "Anticoagulants & Antiplatelets (Warfarin, Dabigatran, Clopidogrel, Aspirin)", "Guggulsterones exhibit intrinsic anti-platelet and fibrinolytic properties.", "Prolonged prothrombin time (PT/INR), spontaneous mucosal hemorrhage, gastrointestinal bleeding.", "HIGH", "Monitor PT/INR every 7 days; discontinue 7 days prior to elective surgical procedures."),
            ("INT-010", "ZMF-010", "Loop and Thiazide Diuretics (Furosemide, Hydrochlorothiazide)", "Glycyrrhizin inhibits 11-beta-hydroxysteroid dehydrogenase type 2 (11b-HSD2), causing mineralocorticoid excess.", "Severe hypokalemia (<3.0 mEq/L), metabolic alkalosis, cardiac dysrhythmias.", "HIGH", "Advise dietary potassium supplementation; monitor serum electrolytes monthly; limit Mulethi <3g/day."),
            ("INT-011", "ZMF-010", "Cardiac Glycosides (Digoxin)", "Mulethi-induced hypokalemia sensitizes myocardial Na+/K+ ATPase to cardiac glycosides.", "Fatal digoxin toxicity: nausea, yellow-green vision (xanthopsia), ventricular arrhythmias.", "HIGH", "Monitor serum digoxin levels; keep potassium >4.0 mEq/L; reduce licorice dose."),
            ("INT-012", "ZMF-010", "Antihypertensives (Amlodipine, Telmisartan, Enalapril)", "Pseudo-hyperaldosteronism induces sodium and water retention.", "Rebound elevation in systolic and diastolic blood pressure, blunted antihypertensive response.", "MODERATE", "Monitor home BP weekly; avoid high-dose Glycyrrhiza in stage 2 hypertension."),
            ("INT-013", "ZMF-015", "Oral Hypoglycemics & Insulins (Metformin, Glimepiride, Insulin Glargine)", "Charantin, polypeptide-p, and vicine promote glucose uptake and insulin secretion.", "Symptomatic acute hypoglycemia (shivering, diaphoresis, cognitive impairment, syncope).", "HIGH", "Instruct patient on hypoglycemia signs; consider prophylactic 25% reduction of oral agent."),
            ("INT-014", "ZMF-020", "Stimulant Cathartics & Narrow Therapeutic Index Drugs (Lithium, Phenytoin)", "Accelerated intestinal transit time markedly reduces gastrointestinal drug absorption window.", "Sub-therapeutic blood levels of critical maintenance medications, loss of therapeutic seizure/mood control.", "MODERATE", "Separate administration of Senna/Sana by at least 4 hours from oral maintenance drugs.")
        ]
        cursor.executemany("""
        INSERT OR REPLACE INTO zkb_drug_interactions (
            id, mufradat_id, modern_drug_class, interaction_mechanism,
            clinical_effect, risk_severity, recommended_action
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, interactions)
    except Exception as e:
        print(f"Note on zkb_drug_interactions seeding: {e}")

    conn.commit()
    conn.close()

    try:
        from database.migrations.zfie.runner import apply_migrations
        from database.seed_zfie_live import seed_zfie_database
        from scripts.seed_v2_clinical_governance import seed_v2_records
        apply_migrations(DB_PATH)
        seed_zfie_database(DB_PATH)
        seed_v2_records()
    except Exception as e:
        print(f"Note on ZFIE migrations/seed or V2 seed: {e}")

    print(f"Successfully initialized live database at {DB_PATH}")

if __name__ == "__main__":
    init_db()
