"""
Zayvora Health OS — Demo Data Seeder
Adds 10 patients and 15 Unani prescriptions for demo/testing purposes.
"""

import sqlite3
import uuid
import json
import hashlib
import random
import datetime

DB_PATH = "database/zayvora_live.db"

# ── Patients to insert ────────────────────────────────────────────────────────
PATIENTS = [
    {
        "mrn": "PAT-0816",
        "first_name": "Fatima",
        "last_name": "Begum",
        "date_of_birth": "1975-03-15",
        "gender": "female",
        "contact_phone": "+91-9876543210",
        "contact_email": "fatima.begum@example.com",
        "blood_group": "B+",
        "mizaj_dominant": "Balghami",
    },
    {
        "mrn": "PAT-0817",
        "first_name": "Abdul",
        "last_name": "Rehman",
        "date_of_birth": "1960-07-22",
        "gender": "male",
        "contact_phone": "+91-9812345678",
        "contact_email": "abdul.rehman@example.com",
        "blood_group": "O+",
        "mizaj_dominant": "Safrawi",
    },
    {
        "mrn": "PAT-0818",
        "first_name": "Zainab",
        "last_name": "Khatoon",
        "date_of_birth": "1990-11-08",
        "gender": "female",
        "contact_phone": "+91-9988776655",
        "contact_email": "zainab.khatoon@example.com",
        "blood_group": "A+",
        "mizaj_dominant": "Damawi",
    },
    {
        "mrn": "PAT-0819",
        "first_name": "Mohammad",
        "last_name": "Yusuf",
        "date_of_birth": "1945-02-14",
        "gender": "male",
        "contact_phone": "+91-9001122334",
        "contact_email": "mohammad.yusuf@example.com",
        "blood_group": "AB+",
        "mizaj_dominant": "Sawdawi",
    },
    {
        "mrn": "PAT-0820",
        "first_name": "Rukhsar",
        "last_name": "Bano",
        "date_of_birth": "1985-09-30",
        "gender": "female",
        "contact_phone": "+91-9345678901",
        "contact_email": "rukhsar.bano@example.com",
        "blood_group": "B-",
        "mizaj_dominant": "Balghami",
    },
    {
        "mrn": "PAT-0821",
        "first_name": "Imran",
        "last_name": "Sheikh",
        "date_of_birth": "2000-05-12",
        "gender": "male",
        "contact_phone": "+91-9456789012",
        "contact_email": "imran.sheikh@example.com",
        "blood_group": "O-",
        "mizaj_dominant": "Damawi",
    },
    {
        "mrn": "PAT-0822",
        "first_name": "Nasreen",
        "last_name": "Parveen",
        "date_of_birth": "1955-12-03",
        "gender": "female",
        "contact_phone": "+91-9567890123",
        "contact_email": "nasreen.parveen@example.com",
        "blood_group": "A-",
        "mizaj_dominant": "Safrawi",
    },
    {
        "mrn": "PAT-0823",
        "first_name": "Tariq",
        "last_name": "Mehmood",
        "date_of_birth": "1978-08-19",
        "gender": "male",
        "contact_phone": "+91-9678901234",
        "contact_email": "tariq.mehmood@example.com",
        "blood_group": "B+",
        "mizaj_dominant": "Sawdawi",
    },
    {
        "mrn": "PAT-0824",
        "first_name": "Shagufta",
        "last_name": "Akhtar",
        "date_of_birth": "1995-04-25",
        "gender": "female",
        "contact_phone": "+91-9789012345",
        "contact_email": "shagufta.akhtar@example.com",
        "blood_group": "O+",
        "mizaj_dominant": "Damawi",
    },
    {
        "mrn": "PAT-0825",
        "first_name": "Khalid",
        "last_name": "Hussain",
        "date_of_birth": "1935-10-11",
        "gender": "male",
        "contact_phone": "+91-9890123456",
        "contact_email": "khalid.hussain@example.com",
        "blood_group": "A+",
        "mizaj_dominant": "Balghami",
    },
]

# ── Unani medicines palette ───────────────────────────────────────────────────
MEDICINES = [
    {"name": "Sharbat Banafsha",    "dose": "2 tsp",  "frequency": "BID",          "duration": "7 days"},
    {"name": "Majoon Ushba",        "dose": "5g",     "frequency": "OD morning",   "duration": "21 days"},
    {"name": "Roghan Baiza Murgh",  "dose": "5 ml",   "frequency": "local application BD", "duration": "14 days"},
    {"name": "Khamira Marwareed",   "dose": "3g",     "frequency": "OD at bedtime","duration": "30 days"},
    {"name": "Habbe Jadwar",        "dose": "2 pills","frequency": "TID",          "duration": "10 days"},
    {"name": "Itrifal Kishneezi",   "dose": "10g",    "frequency": "OD at bedtime","duration": "21 days"},
    {"name": "Sharbat Anar",        "dose": "3 tsp",  "frequency": "BID",          "duration": "7 days"},
    {"name": "Majoon Falasfa",      "dose": "5g",     "frequency": "OD morning",   "duration": "15 days"},
    {"name": "Habbe Mumsik Tilai",  "dose": "1 pill", "frequency": "OD",           "duration": "21 days"},
    {"name": "Sharbat Dinar",       "dose": "2 tsp",  "frequency": "TID",          "duration": "5 days"},
]

DIETARY_ADVICE = [
    "Avoid sour and cold foods. Prefer warm, light meals.",
    "Take meals at regular times. Avoid fried and spicy food.",
    "Increase intake of fresh fruits and vegetables. Drink warm water.",
    "Reduce sugar and refined carbohydrates. Prefer whole grains.",
    "Avoid exposure to cold wind. Keep warm. Drink herbal teas.",
]

REGIMENAL_ADVICE = [
    "Light morning walk for 20 minutes. Rest after Zuhr prayer.",
    "Avoid strenuous exercise. Ensure 7-8 hours of sleep.",
    "Practice deep breathing exercises twice daily.",
    "Fomentation on affected area twice daily with warm cloth.",
    "Mild steam inhalation twice daily. Gargle with warm salt water.",
]

# ── Prescriptions to insert (15 total, one per new patient + extras) ──────────
def make_rx_items(n=2):
    chosen = random.sample(MEDICINES, min(n, len(MEDICINES)))
    return json.dumps(chosen)

PRESCRIPTIONS_SPEC = [
    ("PAT-0816", "Fatima Begum",      3),
    ("PAT-0817", "Abdul Rehman",      2),
    ("PAT-0818", "Zainab Khatoon",    2),
    ("PAT-0819", "Mohammad Yusuf",    3),
    ("PAT-0820", "Rukhsar Bano",      2),
    ("PAT-0821", "Imran Sheikh",      2),
    ("PAT-0822", "Nasreen Parveen",   3),
    ("PAT-0823", "Tariq Mehmood",     2),
    ("PAT-0824", "Shagufta Akhtar",   2),
    ("PAT-0825", "Khalid Hussain",    2),
]


def seed():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # ── Fetch existing schema columns ─────────────────────────────────────────
    c.execute("PRAGMA table_info(patients)")
    patient_cols = {row[1] for row in c.fetchall()}

    c.execute("PRAGMA table_info(prescriptions)")
    rx_cols = {row[1] for row in c.fetchall()}

    skipped_patient_cols  = set()
    skipped_rx_cols       = set()

    # ── Insert patients ───────────────────────────────────────────────────────
    patients_added = 0
    for p in PATIENTS:
        # Skip if MRN already exists
        c.execute("SELECT 1 FROM patients WHERE mrn = ?", (p["mrn"],))
        if c.fetchone():
            print(f"  [SKIP] Patient {p['mrn']} already exists.")
            continue

        row = {"id": str(uuid.uuid4()), "facility_id": "FAC-HQ-01", "allergies_json": "[]"}
        for k, v in p.items():
            if k in patient_cols:
                row[k] = v
            else:
                skipped_patient_cols.add(k)

        cols   = ", ".join(row.keys())
        placeholders = ", ".join(["?"] * len(row))
        c.execute(f"INSERT INTO patients ({cols}) VALUES ({placeholders})", list(row.values()))
        patients_added += 1
        print(f"  [OK] Patient {p['mrn']} — {p['first_name']} {p['last_name']}")

    conn.commit()

    # ── Insert prescriptions ──────────────────────────────────────────────────
    rx_added = 0
    random.seed(42)

    # Distribute 15 prescriptions across the 10 patients
    rx_queue = []
    for mrn, name, count in PRESCRIPTIONS_SPEC:
        for _ in range(count):
            rx_queue.append((mrn, name))
            if len(rx_queue) == 15:
                break
        if len(rx_queue) == 15:
            break
    # Trim or pad to exactly 15
    rx_queue = rx_queue[:15]

    for mrn, patient_name in rx_queue:
        order_number = f"RX-2026-{random.randint(100000, 999999)}"
        sig = hashlib.sha256(f"{order_number}{mrn}".encode()).hexdigest()[:32]
        items = make_rx_items(n=random.choice([2, 3]))

        candidate = {
            "id":             str(uuid.uuid4()),
            "order_number":   order_number,
            "mrn":            mrn,
            "patient_name":   patient_name,
            "doctor_name":    "Dr. Irfan Ashraf",
            "doctor_reg":     "BUMS/AMU/2010/1234",
            "items_json":     items,
            "dietary_advice": random.choice(DIETARY_ADVICE),
            "regimenal_advice": random.choice(REGIMENAL_ADVICE),
            "signature_hash": sig,
            "status":         "ISSUED",
            "facility_id":    "FAC-HQ-01",
        }

        row = {}
        for k, v in candidate.items():
            if k in rx_cols:
                row[k] = v
            else:
                skipped_rx_cols.add(k)

        cols         = ", ".join(row.keys())
        placeholders = ", ".join(["?"] * len(row))
        c.execute(f"INSERT INTO prescriptions ({cols}) VALUES ({placeholders})", list(row.values()))
        rx_added += 1
        print(f"  [OK] Prescription {order_number} → {patient_name}")

    conn.commit()

    # ── Final counts ──────────────────────────────────────────────────────────
    c.execute("SELECT COUNT(*) FROM patients")
    total_patients = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM prescriptions")
    total_rx = c.fetchone()[0]

    # ── Sample records ────────────────────────────────────────────────────────
    print("\n── Sample Patients ──────────────────────────────────────")
    c.execute("SELECT mrn, first_name, last_name, gender, mizaj_dominant, blood_group FROM patients ORDER BY created_at DESC LIMIT 3")
    for r in c.fetchall():
        print(dict(zip(["mrn","first_name","last_name","gender","mizaj_dominant","blood_group"], r)))

    print("\n── Sample Prescriptions ─────────────────────────────────")
    c.execute("SELECT order_number, mrn, patient_name, doctor_name, status FROM prescriptions ORDER BY created_at DESC LIMIT 3")
    for r in c.fetchall():
        print(dict(zip(["order_number","mrn","patient_name","doctor_name","status"], r)))

    conn.close()

    print("\n════════════════════════════════════════════")
    print(f"  Patients  added    : {patients_added}")
    print(f"  Prescriptions added: {rx_added}")
    print(f"  Skipped patient cols : {skipped_patient_cols or 'none'}")
    print(f"  Skipped rx cols      : {skipped_rx_cols or 'none'}")
    print(f"  Total patients now   : {total_patients}")
    print(f"  Total prescriptions  : {total_rx}")
    print("════════════════════════════════════════════")


if __name__ == "__main__":
    seed()
