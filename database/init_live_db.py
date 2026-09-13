import sqlite3
import os
import hashlib
import json
import uuid

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
        ("FAC-HQ-01", "Jamia Hamdard AUTC - Main Hospital", "JH-AUTC-DELHI", "HOSPITAL", "Hamdard Nagar", "New Delhi", "Delhi", "+91 11 2605 9688", 1),
        ("FAC-BRANCH-02", "Nizamia General Hospital & Research Wing", "NGH-HYD-01", "RESEARCH_INSTITUTE", "Charminar Road", "Hyderabad", "Telangana", "+91 40 2452 1102", 1),
    ]
    cursor.executemany("""
    INSERT INTO facilities (id, name, code, facility_type, address, city, state, contact_phone, is_active)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, facilities)

    # Seed Users
    pwd_hash, salt = hash_password("admin123")
    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-ADMIN-01", "admin@zayvora.health", pwd_hash, salt, "Irfan Ashraf", "+91 98110 00001", "SUPER_ADMIN", "FAC-HQ-01"))
    
    doc_hash, doc_salt = hash_password("doctor123")
    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-DOC-01", "mansoor.alam@zayvora.health", doc_hash, doc_salt, "Prof. (Dr.) Mansoor Alam", "+91 98110 44219", "DOCTOR", "FAC-HQ-01"))
    
    doc2_hash, doc2_salt = hash_password("doctor123")
    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-DOC-02", "sirajuddin@zayvora.health", doc2_hash, doc2_salt, "Dr. Hakim Sirajuddin", "+91 98480 33110", "DOCTOR", "FAC-BRANCH-02"))

    rec_hash, rec_salt = hash_password("reception123")
    cursor.execute("""
    INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("USR-REC-01", "reception.opd@zayvora.health", rec_hash, rec_salt, "Tariq Ansari", "+91 98110 55301", "RECEPTIONIST", "FAC-HQ-01"))

    pharm_hash, pharm_salt = hash_password("pharmacy123")
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
        ("APT-201", "T-201", "MRN-2026-0901", "Bilqees Begum", "Dr. Hakim Sirajuddin", "CCIM-U-1996-0912", "Nizamia Regimenal OPD", "Room 101", "2026-09-13", "11:00 AM", "STANDARD", "Chronic Tahazzul and osteoarthritis evaluation", "WAITING", 600.0, "PAID", "FAC-BRANCH-02"),
    ]
    cursor.executemany("""
    INSERT INTO appointments (id, token_number, mrn, patient_name, doctor_name, doctor_reg, department, opd_room, appointment_date, appointment_time, acuity, chief_complaint, status, fee_amount, payment_status, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, appointments)

    # Seed Inventory
    inventory = [
        ("INV-001", "Majun Suranjan (Mudabbar)", "MS-2026-LOT4", "2027-08-30", 142, 25, "CLINIC_UNANI", 1, 1, "SHA256:7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b", "FAC-HQ-01"),
        ("INV-002", "Roghan-e-Balsan", "RB-2026-LOT1", "2028-01-15", 88, 15, "RETAIL_UNANI", 0, 0, None, "FAC-HQ-01"),
        ("INV-003", "Habb-e-Suranjan Forte", "HS-2026-LOT3", "2027-08-31", 210, 30, "CLINIC_UNANI", 1, 1, "SHA256:f1e2d3c4b5a6978800112233445566778899aabbccddeeff0011223344556677", "FAC-HQ-01"),
        ("INV-004", "MetaboCore Elite Powder", "MCE-2026-LOT2", "2028-06-20", 320, 50, "AYUSH_PROPRIETARY", 0, 0, None, "FAC-HQ-01"),
        ("INV-005", "RestoreVital Herbal Infusion", "RVH-2026-LOT5", "2028-11-15", 450, 60, "FSSAI_SUPPLEMENT", 0, 0, None, "FAC-HQ-01"),
        ("INV-006", "Khamira Gaozaban Ambari", "KGA-2026-B1", "2027-12-31", 95, 20, "CLINIC_UNANI", 0, 0, None, "FAC-BRANCH-02"),
    ]
    cursor.executemany("""
    INSERT INTO inventory (id, name, batch_number, expiry_date, stock_qty, min_threshold, category, is_schedule_e1, mudabbar_required, mudabbar_cert, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

    # Seed Audit Block
    cursor.execute("""
    INSERT INTO audit_ledger (leaf_hash, event_type, signer, status, facility_id, details_json)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "731f5cf53472e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495",
        "PRESCRIPTION_LOCKED",
        "Prof. (Dr.) Mansoor Alam (CCIM-U-1988-0412)",
        "ANCHORED",
        "FAC-HQ-01",
        json.dumps({"order_number": "RX-2026-0441", "mrn": "MRN-2026-0814"})
    ))

    # Seed Invoices
    invoices = [
        ("INV-001", "RCPT-2026-1041", "MRN-2026-0814", "Hamza Farooqi", 800.0, "Integrative Unani OPD", "UPI", "PAID", "FAC-HQ-01"),
        ("INV-002", "RCPT-2026-1042", "MRN-2026-0815", "Ayesha Siddiqui", 800.0, "Preventive Dietetics", "CARD", "PAID", "FAC-HQ-01"),
        ("INV-003", "RCPT-2026-1043", "MRN-2026-0816", "Mohammed Zeeshan", 500.0, "Musculoskeletal & Regimenal", "CASH", "PAID", "FAC-HQ-01"),
        ("INV-004", "RCPT-2026-2011", "MRN-2026-0901", "Bilqees Begum", 600.0, "Nizamia Regimenal OPD", "UPI", "PAID", "FAC-BRANCH-02"),
    ]
    cursor.executemany("""
    INSERT INTO invoices (id, invoice_number, mrn, patient_name, amount, department, payment_method, status, facility_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, invoices)

    conn.commit()
    conn.close()
    print(f"Successfully initialized live database at {DB_PATH}")

if __name__ == "__main__":
    init_db()
