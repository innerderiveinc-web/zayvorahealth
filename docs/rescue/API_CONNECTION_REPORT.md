# ZAYVORA Health OS™ — API Connection Report

| Frontend User Action | HTTP Method | Target REST Endpoint | Backend Handler |
|---|---|---|---|
| Register Patient | `POST` | `/api/v1/patients` | `_handle_create_patient` |
| Book Appointment | `POST` | `/api/v1/appointments/book` | `_handle_book_appointment` |
| Scribe Voice Notes | `POST` | `/api/v1/scribe/extract` | `_handle_scribe_extract` |
| Calculate 10-Ajnas Mizaj | `POST` | `/api/v1/clinical/mizaj/calculate` | `_handle_mizaj_calculate` |
| Evaluate Organ-Axis | `POST` | `/api/v1/clinical/organ-axis/analyze` | `_handle_organ_axis_analyze` |
| Query Hakeem Sahab | `POST` | `/api/v1/ai/hakeem/assist` | `_handle_hakeem_assist` |
| Compile Nuskha Formula | `POST` | `/api/v1/therapeutic/nuskha/compile` | `_handle_nuskha_compile` |
| Run Safety Audit | `POST` | `/api/v1/therapeutic/safety/audit` | `_handle_safety_audit` |
| Sign Prescription (21 CFR 11) | `POST` | `/api/v1/prescriptions/lock` | `_handle_prescription_lock` |
| Dispense FEFO Order | `POST` | `/api/v1/pharmacy/dispense` | `_handle_pharmacy_dispense` |
| Log Adverse Event (ICH E2B) | `POST` | `/api/v1/research/adverse-event/report` | `_handle_adverse_event_report` |
| Verify Merkle Ledger | `GET` | `/api/v1/governance/audit/merkle` | `_send_json(DB.get_merkle_root())` |
