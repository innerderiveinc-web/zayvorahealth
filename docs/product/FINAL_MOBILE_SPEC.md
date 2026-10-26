# ZAYVORA Health OS™ — Mobile App Specification

**Three Expo React Native apps · Status: Pre-staging**

## Apps

### 1. ZAYVORA Patient App (`apps/mobile`)

**Target:** Patients using ZAYVORA Matab™ services

Key screens:
- Home / Dashboard (vitals, upcoming appointments, Mizaj profile)
- Appointment Booking (doctor search, slot selection, mode)
- Teleconsultation (video/voice — mocked, integration pending)
- Prescription Viewer (active Nuskha, dosage reminders)
- Mizaj Assessment (10-question Ajnas-e-Ashrah)
- Lifestyle Tracker (diet, sleep, exercise)
- Notifications (push, dosage reminders)

### 2. ZAYVORA Doctor App (planned)

**Target:** Hakeem / physician using ZAYVORA Matab™ clinical tools

Key screens:
- Patient Queue
- Patient 360 View
- Encounter / eBMR entry
- Nuskha Composer
- Hakeem Sahab AI™ interface
- Follow-up management

### 3. ZAYVORA Receptionist App (planned)

**Target:** Clinic reception staff

Key screens:
- Queue Management
- Appointment Booking
- Patient Registration
- Token Display

## Technical Stack

- **Framework:** Expo SDK 51+ / React Native 0.74+
- **Navigation:** React Navigation v6
- **State:** React Context (upgrade to Zustand planned)
- **Notifications:** Expo Notifications
- **Auth:** JWT stored in SecureStore
- **API:** RESTful calls to ZAYVORA Health OS™ API Gateway

## Status

| Feature | Status |
|:---|:---|
| Navigation (AppNavigator) | Implemented |
| Mizaj Assessment Screen | Implemented |
| Notification Service | Implemented |
| Teleconsult Room | Mocked (UI only) |
| Lifestyle Tracker | Mocked (UI only) |
| Doctor App | Not started |
| Receptionist App | Not started |
