# ZAYVORA Health OS™ — User Guide

**Version: 2.0 · Pre-staging**

## Getting Started

### For Patients

1. **Register** at `/patient/register` — provide name, email, date of birth
2. **Login** at `/patient/login`
3. **Complete Mizaj Assessment** — 10-question temperament evaluation
4. **Book a Consultation** — Select doctor, date, time, and mode (in-person or teleconsult)
5. **View Prescriptions** — Access your Nuskha with dosage instructions

### For Doctors (Hakeem)

1. **Login** at `/` or `/doctor` — use your clinic credentials
2. **View Queue** — See all waiting patients at `/doctor/queue`
3. **Open Patient 360** — Click any patient to see full clinical history
4. **Create Encounter** — Document consultation at `/doctor/encounters`
5. **Write Nuskha** — Compose prescription at `/doctor/nuskha`
6. **Consult Hakeem Sahab AI™** — AI clinical reasoning at `/doctor/hakeem-sahab`
7. **Sign Prescription** — Review AI suggestions, sign manually (safe_to_lock=False)

### For Receptionists

1. **Login** at `/receptionist`
2. **Manage Queue** — Token assignment at `/receptionist/queue`
3. **Book Appointments** — Schedule consultations at `/receptionist/appointments`

### For Pharmacists

1. **Login** at `/pharmacy`
2. **Process Dispensing** — Review signed Nuskha at `/pharmacy/dispensing`
3. **Manage Inventory** — Stock tracking at `/pharmacy/inventory`

## Key Safety Notes

- Never act on a prescription marked **Draft** — only **Signed** prescriptions are valid
- Hakeem Sahab AI™ suggestions are for **clinical reasoning support only**
- All prescriptions with AI involvement have `safe_to_lock=False` — human review mandatory
- Report any adverse events to your clinic administrator immediately

## Support

- Help Center: `/website/faqs`
- Contact: `/website/contact`
- Emergency: Contact your nearest hospital; ZAYVORA is not an emergency service

## Default Seed Credentials

| Role | Email | Password | Facility / Notes |
|:---|:---|:---|:---|
| **Super Admin** | `admin@zayvorahealth` | `admin123` | zayvora clinic and hospital |
| **Doctor / Tabeeb** | `dr.irfan@zayvorahealth` | `doctor123` | Integrative Unani OPD (zayvora clinic and hospital) |
| **Doctor / Tabeeb** | `dr.malik@zayvorahealth` | `doctor123` | zayvora hospital |
| **Receptionist** | `reception@zayvorahealth` | `reception123` | Patient Queue & Token Management |
| **Pharmacist** | `pharmacy@zayvorahealth` | `pharmacy123` | Dispensary & 21 CFR Part 11 eBMR |
| **Patient** | `ahmad.khan@example.com` | `password123` | MRN: `MRN-2026-0001` (Mizaj: Damawi) |

