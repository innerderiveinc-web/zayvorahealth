# ZAYVORA Health OS™ — Mobile Application Smoke Test Report

## Executive Summary
This report documents the architectural, navigation, and functional verification of the **ZAYVORA Mobile Application** (`apps/mobile/`), built with React Native and Expo. The mobile app provides specialized role-adaptive interfaces for patients and clinicians.

---

## 1. Mobile Screen Inventory & Audit Status

| Screen Name | File Path | Primary Audience | API Integration | Mock / Live Status |
| :--- | :--- | :--- | :--- | :---: |
| **AuthScreen** | `src/screens/AuthScreen.tsx` | All Users | `/api/v1/auth/login`, `/register` | **LIVE API** |
| **HomeScreen** | `src/screens/HomeScreen.tsx` | Patient / Clinician | `/api/v1/patient/my-records` | **LIVE API** |
| **AppointmentsScreen** | `src/screens/AppointmentsScreen.tsx` | Patient | `/api/v1/appointments` | **LIVE API** |
| **PrescriptionsScreen** | `src/screens/PrescriptionsScreen.tsx` | Patient | `/api/v1/prescriptions` | **LIVE API** |
| **LabResultsScreen** | `src/screens/LabResultsScreen.tsx` | Patient | `/api/v1/labs` | **HYBRID / LIVE** |
| **NotificationsScreen** | `src/screens/NotificationsScreen.tsx` | All Users | `/api/v1/notifications` | **LIVE API** |
| **ProfileScreen** | `src/screens/ProfileScreen.tsx` | All Users | `/api/v1/user/profile` | **LIVE API** |
| **TeleConsultRoom** | `src/screens/TeleConsultRoom.tsx` | Patient / Clinician | WebRTC Signaling Gateway | **LIVE WEBRTC** |
| **LifestyleTrackerScreen** | `src/screens/LifestyleTrackerScreen.tsx` | Patient | `/api/v1/lifestyle` | **LIVE API** |
| **MizajAssessmentScreen** | `src/screens/MizajAssessmentScreen.tsx` | Patient | `/api/v1/mizaj/assessment` | **LIVE API** |
| **ClinicianCompanionScreen** | `src/screens/ClinicianCompanionScreen.tsx` | Doctor | `/api/v1/doctor/companion` | **LIVE API** |

---

## 2. Navigation Architecture

- **Root Navigator**: Evaluates auth state stored in `SecureStore`.
  - Unauthenticated State -> Renders `AuthScreen` (Login / Registration tabs).
  - Authenticated State -> Conditionally loads either:
    - **Patient Tab Navigator**: Home, Appointments, Prescriptions, Care Plan, Profile.
    - **Clinician Navigator**: OPD Cockpit, Tele-consult Room, Patient Chart, Scribe.
- **Deep Linking**: Configured for tele-consult invitations (`zayvora://consult/{roomId}`) and appointment reminders.

---

## 3. Automated Smoke Test Verification

Executed via `tests/test_mobile_application.py`:

```
test_01_mobile_screen_inventory (__main__.TestMobileApplication) ... ok
test_02_mobile_navigation_hierarchy (__main__.TestMobileApplication) ... ok
test_03_mobile_api_service_layer (__main__.TestMobileApplication) ... ok
test_04_mobile_role_based_routing (__main__.TestMobileApplication) ... ok
test_05_mobile_offline_storage_layer (__main__.TestMobileApplication) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.082s

OK
```

### Test Highlights:
1. **Screen Inventory Completeness**: Confirms all 11 core screens exist, export valid React components, and implement brand color tokens (`#2D6A4F`).
2. **Navigation Hierarchy**: Confirms stack navigators and bottom tab bars are correctly defined.
3. **API Client**: Verifies axios/fetch client injects `Authorization: Bearer <token>` and handles 401 token refresh automatically.
4. **Offline Storage**: Confirms `AsyncStorage` and `SecureStore` abstractions protect user session tokens and cache offline regimens.
