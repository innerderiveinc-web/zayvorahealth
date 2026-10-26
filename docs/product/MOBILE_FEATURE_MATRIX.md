# ZAYVORA Health OS™ — MOBILE FEATURE MATRIX
**Audit Date:** September 15, 2026  
**Platform:** Expo ~51.0.0, React Native 0.74.5, React Navigation 6

---

## Screens Inventory

| Screen | File | Lines | Status | Backend Connection |
|---|---|---|---|---|
| **AuthScreen** | `AuthScreen.tsx` | 112 | ✅ FULLY IMPLEMENTED | `identity:8001/auth/login` + `/register` |
| **HomeScreen** | `HomeScreen.tsx` | 372 | 🟡 PARTIAL | Fetches health metrics — needs live API wiring |
| **AppointmentsScreen** | `AppointmentsScreen.tsx` | 105 | 🟡 PARTIAL | `appointments` API call pattern present |
| **LabResultsScreen** | `LabResultsScreen.tsx` | 105 | ✅ FULLY IMPLEMENTED | Lab results with expand/flag UI |
| **PrescriptionsScreen** | `PrescriptionsScreen.tsx` | 132 | 🟡 PARTIAL | Prescription list UI — API partially connected |
| **NotificationsScreen** | `NotificationsScreen.tsx` | 103 | ✅ FULLY IMPLEMENTED | Categorized, mark-as-read, real-time ready |
| **ProfileScreen** | `ProfileScreen.tsx` | 90 | ✅ FULLY IMPLEMENTED | Auth logout, settings display |
| **ClinicianCompanionScreen** | `ClinicianCompanionScreen.tsx` | 171 | 🔵 FRONTEND ONLY | No backend connection |
| **TeleConsultRoom** | `TeleConsultRoom.tsx` | 194 | 🔵 FRONTEND ONLY | No WebRTC/video integration |
| **LifestyleTrackerScreen** | `LifestyleTrackerScreen.tsx` | 236 | 🔵 FRONTEND ONLY | No wearable/health API |

---

## Services Inventory

| Service | File | Status | Purpose |
|---|---|---|---|
| `auth.service.ts` | `services/auth.service.ts` | ✅ | Login, refresh, logout, token storage |
| `api.service.ts` | `services/api.service.ts` | ✅ | Base GET/POST with JWT headers |
| `OfflineStorageService.ts` | `services/OfflineStorageService.ts` | ✅ | AsyncStorage-backed offline sync |

---

## Navigation

| Component | File | Status |
|---|---|---|
| `AppNavigator.tsx` | `navigation/AppNavigator.tsx` | ✅ — Auth-guarded bottom tabs, role-based routing |

---

## Feature Gap Analysis

| Feature | Status | Priority | Implementation Path |
|---|---|---|---|
| **Authentication** | ✅ | — | Done |
| **Biometric login** (FaceID/TouchID) | ❌ | P1 | Expo Local Authentication |
| **Push notifications** | ❌ | P1 | Expo Push + FCM/APNs |
| **Deep linking** | ❌ | P1 | Expo Linking + React Navigation deeplink config |
| **Offline patient data** | ✅ | — | `OfflineStorageService.ts` |
| **Offline prescription viewing** | 🟡 | P1 | Extend offline service with prescription cache |
| **Teleconsult (video)** | 🔵 | P1 | WebRTC via Jitsi/Daily.co SDK |
| **Wearable/health sync** | 🔵 | P2 | Apple HealthKit + Google Fit via Expo |
| **Lifestyle tracking** | 🔵 | P2 | Connect `LifestyleTrackerScreen` to clinical API |
| **AI Chat (Hakeem Sahab AI™)** | ❌ | P1 | New screen — wire to `ai:8005/hakeem` |
| **QR code prescription** | ❌ | P2 | Generate QR for pharmacy scanning |
| **Nabz pulse capture** | ❌ | P3 | Hardware driver abstraction in therapeutic service |
| **Multilingual (Urdu/Arabic)** | ❌ | P1 | i18n setup with RTL support |
| **Dark mode** | ❌ | P2 | Theme context + StyleSheet variants |
| **Accessibility (a11y)** | ❌ | P1 | `accessibilityLabel` on all interactive elements |

---

## Missing Screens (Required by Master Directive)

| Screen | Purpose | Priority |
|---|---|---|
| `AIChatScreen` | Hakeem Sahab AI™ mobile chat | P1 |
| `MizajAssessmentScreen` | Mobile Mizaj self-assessment | P1 |
| `BookAppointmentScreen` | Full appointment booking flow | P1 |
| `VitalEntryScreen` | Manual vital entry (BP, weight, pulse) | P1 |
| `ConsultSummaryScreen` | Post-consultation summary & prescription | P1 |
| `PharmacyLocatorScreen` | Find ZAYVORA Matab™ near user | P2 |
| `ProgramEnrollmentScreen` | Enroll in ZAYVORA Health Programs | P2 |
| `EmergencyScreen` | Red flag — emergency protocols | P0 |

---

## Mobile Build Configuration

| Config | Current Status | Notes |
|---|---|---|
| `app.json` / `app.config.js` | ✅ Exists | Expo config |
| Bundle ID (iOS) | 🔴 Likely placeholder | Needs production bundle ID |
| Package name (Android) | 🔴 Likely placeholder | Needs production package name |
| App signing | ❌ | EAS Build configuration needed |
| OTA updates | ❌ | EAS Update not configured |
| Privacy manifest (iOS) | ❌ | Required for App Store since 2024 |
