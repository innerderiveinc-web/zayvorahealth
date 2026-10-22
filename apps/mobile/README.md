# ZAYVORA Health OS™ Mobile Application (v5.0 Enterprise)

Cross-platform React Native / Expo application for integrative patient self-management, OPD token tracking, vernacular voice posology, and clinician point-of-care decision support.

---

## 📱 Architecture & Production Capabilities

1. **Patient 360 & Personal Health Record (PHR):**
   - Longitudinal Mizaj monitoring with 10-Ajnas humoral balance calculation.
   - Interactive organ-axis health trajectory and biomarker visualization.
2. **Vernacular Audio Posology (صوتی خوراک و ہدایات):**
   - High-fidelity spoken medication instructions in **Urdu (اردو)**, **Hindi (हिंदी)**, and **English**.
   - Custom Anupan (adjuvant) guidance (e.g. warm milk, arq-e-gulab).
3. **Asbab-e-Sittah Zarooriyyah (6 Essentials Lifestyle Tracker):**
   - Daily logging of Hawa (Air), Makool wa Mashroob (Diet), Harkat wa Sukoon Badani & Nafsani (Physical & Psychic movement), Naum wa Yaqzah (Sleep), and Ihtibas wa Istifragh (Evacuation).
4. **OPD Queue & Telemedicine Suite:**
   - Real-time token number, estimated wait countdown, and WebRTC encrypted video consult chamber.
5. **Doctor Mobile Companion:**
   - Rapid bedside triage queue, Hakeem Sahab AI copilot, and 21 CFR Part 11 electronic prescription sign-off.

---

## 🚀 How to Run & Build the Mobile App

### Option 1: Instant Live Preview on Any Phone (Android & iOS via Expo Go)
No compiler or Android Studio required:
```bash
# 1. Install dependencies
cd apps/mobile
npm install

# 2. Start the development server
npx expo start
```
- Open **Expo Go** app on your phone (available free on Google Play Store & Apple App Store).
- Scan the terminal QR code to run ZAYVORA Mobile instantly on your device.

---

### Option 2: 1-Click Free Cloud APK Build (Installable Android APK)
Using Expo Application Services (EAS):
```bash
# 1. Install EAS CLI globally
npm install -g eas-cli

# 2. Login to free Expo account
eas login

# 3. Trigger 1-click cloud build for standalone APK
eas build -p android --profile preview
```
Expo will compile the app in the cloud and give you a direct download link for the `.apk` file to install on any Android phone.

---

### Option 3: Progressive Web App (PWA) Mode
ZAYVORA is also optimized for all mobile browsers (Chrome / Safari):
- Open `https://zayvorahealth.com` on your smartphone.
- Tap **Share / Options** → **"Add to Home Screen"**.
- The app will run in standalone full-screen mode without browser chrome.
