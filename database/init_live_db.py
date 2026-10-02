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
    cursor = conn.cursor()
    
    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read())
        
    # Seed Facilities
    facilities = [
        ("FAC-HQ-01", "zayvora clinic and hospital", "ZAYVORA-CLINIC-HOSP", "HOSPITAL", "Main Health Boulevard", "New Delhi", "Delhi", "+91 97738 82657", 1),
        ("FAC-BRANCH-02", "zayvora hospital", "ZAYVORA-HOSP", "HOSPITAL", "Charminar Road", "Hyderabad", "Telangana", "+91 40 2452 1102", 1),
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
    """, ("USR-ADMIN-REQ", "admin@zayvorahealth", pwd_hash, salt, "Super Admin", "+91 98110 00001", "SUPER_ADMIN", "FAC-HQ-01"))

    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-DOC-REQ1", "dr.irfan@zayvorahealth", doc_hash, doc_salt, "Dr. Irfan Ashraf", "+91 98110 44219", "DOCTOR", "FAC-HQ-01"))

    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-DOC-REQ2", "dr.malik@zayvorahealth", doc_hash, doc_salt, "Dr. Malik", "+91 98480 33110", "DOCTOR", "FAC-BRANCH-02"))

    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-REC-REQ", "reception@zayvorahealth", rec_hash, rec_salt, "Reception Desk", "+91 98110 55301", "RECEPTIONIST", "FAC-HQ-01"))

    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-PHARM-REQ", "pharmacy@zayvorahealth", pharm_hash, pharm_salt, "Chief Pharmacist", "+91 98110 88123", "PHARMACIST", "FAC-HQ-01"))

    # Test compatibility aliases
    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-ADMIN-01", "admin@zayvora.health", pwd_hash, salt, "Irfan Ashraf", "+91 98110 00001", "SUPER_ADMIN", "FAC-HQ-01"))
    
    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-DOC-01", "mansoor.alam@zayvora.health", doc_hash, doc_salt, "Prof. (Dr.) Mansoor Alam", "+91 98110 44219", "DOCTOR", "FAC-HQ-01"))
    
    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-DOC-02", "sirajuddin@zayvora.health", doc_hash, doc_salt, "Dr. Hakim Sirajuddin", "+91 98480 33110", "DOCTOR", "FAC-BRANCH-02"))

    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-REC-01", "reception.opd@zayvora.health", rec_hash, rec_salt, "Tariq Ansari", "+91 98110 55301", "RECEPTIONIST", "FAC-HQ-01"))

    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-PHARM-01", "zainab.pharm@zayvora.health", pharm_hash, pharm_salt, "Zainab Ali", "+91 98110 88123", "PHARMACIST", "FAC-HQ-01"))
    
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

    # Seed Appointments & OPD Queue
    appointments = [
        ("APT-104", "T-104", "MRN-2026-0814", "Hamza Farooqi", "Prof. (Dr.) Mansoor Alam", "CCIM-U-1988-0412", "Integrative Unani OPD", "Room 3", "2026-09-13", "10:15 AM", "STANDARD", "Bilateral knee stiffness & joint ache in damp weather", "IN_CONSULTATION", 800.0, "PAID", "FAC-HQ-01"),
        ("APT-105", "T-105", "MRN-2026-0815", "Ayesha Siddiqui", "Dr. Aisha Siddiqui", "CCIM-U-2004-1892", "Preventive Dietetics", "Room 2", "2026-09-13", "10:28 AM", "URGENT", "Acute Su-e-Hazm with post-prandial heartburn", "WAITING", 800.0, "PAID", "FAC-HQ-01"),
        ("APT-106", "T-106", "MRN-2026-0816", "Mohammed Zeeshan", "Dr. Tariq Zafar", "CCIM-U-2009-3341", "Musculoskeletal & Regimenal", "Room 1", "2026-09-13", "10:40 AM", "FOLLOWUP", "Post-Tadbeer evaluation for lumbar spasm", "WAITING", 500.0, "PAID", "FAC-HQ-01"),
        ("APT-107", "T-107", "MRN-2026-0817", "Fatima Bi", "Prof. (Dr.) Mansoor Alam", "CCIM-U-1988-0412", "Integrative Unani OPD", "Room 3", "2026-09-13", "10:55 AM", "STANDARD", "Metabolic follow-up (Ziabetus Shakari) & HbA1c review", "WAITING", 800.0, "PENDING", "FAC-HQ-01"),
        ("APT-201", "T-201", "MRN-2026-0901", "Bilqees Begum", "Dr. Hakim Sirajuddin", "CCIM-U-1996-0912", "ZAYVORA Regimenal OPD", "Room 101", "2026-09-13", "11:00 AM", "STANDARD", "Chronic Tahazzul and osteoarthritis evaluation", "WAITING", 600.0, "PAID", "FAC-BRANCH-02"),
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

    # Seed Invoices
    invoices = [
        ("INV-001", "RCPT-2026-1041", "MRN-2026-0814", "Hamza Farooqi", 800.0, "Integrative Unani OPD", "UPI", "PAID", None, json.dumps([{"item": "Consultation Fee", "qty": 1, "price": 800.0}]), "FAC-HQ-01"),
        ("INV-002", "RCPT-2026-1042", "MRN-2026-0815", "Ayesha Siddiqui", 800.0, "Preventive Dietetics", "CARD", "PAID", None, json.dumps([{"item": "Consultation Fee", "qty": 1, "price": 800.0}]), "FAC-HQ-01"),
        ("INV-003", "RCPT-2026-1043", "MRN-2026-0816", "Mohammed Zeeshan", 500.0, "Musculoskeletal & Regimenal", "CASH", "PAID", None, json.dumps([{"item": "Consultation Fee", "qty": 1, "price": 500.0}]), "FAC-HQ-01"),
        ("INV-004", "RCPT-2026-2011", "MRN-2026-0901", "Bilqees Begum", 600.0, "ZAYVORA Regimenal OPD", "UPI", "PAID", None, json.dumps([{"item": "Consultation Fee", "qty": 1, "price": 600.0}]), "FAC-BRANCH-02"),
    ]
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
            "DOC-01",
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

    # Seed Canonical Evidence Sources (Layer 14)
    sources = [
        ("SRC-UPI-VOL1", "The Unani Pharmacopoeia of India, Part I, Volume I", "Department of AYUSH, Ministry of Health and Family Welfare", "1st Edition", 2007, "ISBN 978-81-904000-0-8", "PHARMACOPOEIA", "INDIA", "a1b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef0"),
        ("SRC-UPI-VOL2", "The Unani Pharmacopoeia of India, Part I, Volume II", "Department of AYUSH, Ministry of Health and Family Welfare", "1st Edition", 2008, "ISBN 978-81-904000-1-5", "PHARMACOPOEIA", "INDIA", "b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef01a"),
        ("SRC-NFUM-PT1", "National Formulary of Unani Medicine, Part I", "Department of AYUSH, Ministry of Health and Family Welfare", "Reprint Edition", 2006, "ISBN 978-81-904000-2-2", "PHARMACOPOEIA", "INDIA", "c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef01ab2"),
        ("SRC-IBN-SINA-CANON", "Al-Qanun fi al-Tibb (The Canon of Medicine)", "Ibn Sina (Avicenna)", "Canonical Bulaq Edition", 1593, "CANON-AVICENNA-1025-CE", "CLASSICAL_CANON", "GLOBAL", "d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef01ab2c3")
    ]
    cursor.executemany("""
    INSERT OR REPLACE INTO evidence_sources (
        source_id, title, author, edition, publication_year, isbn_or_doi, source_type, jurisdiction, digital_sha256_checksum
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sources)

    conn.commit()
    conn.close()

    try:
        from database.migrations.zfie.runner import apply_migrations
        from database.seed_zfie_live import seed_zfie_database
        apply_migrations(DB_PATH)
        seed_zfie_database(DB_PATH)
    except Exception as e:
        print(f"Note on ZFIE migrations/seed: {e}")

    print(f"Successfully initialized live database at {DB_PATH}")

if __name__ == "__main__":
    init_db()
