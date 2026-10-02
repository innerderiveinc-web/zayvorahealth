import React, { useState } from "react";
import { SafeAreaView, View, Text, StyleSheet, TouchableOpacity, StatusBar, ScrollView, TextInput } from "react-native";

type MobileRole = "doctor" | "patient" | "receptionist";

export default function App() {
  const [activeRole, setActiveRole] = useState<MobileRole>("doctor");
  const [currentTab, setCurrentTab] = useState<string>("home");

  // Interactive mobile states
  const [audioLang, setAudioLang] = useState<"urdu" | "hindi" | "english">("urdu");
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [reportUploaded, setReportUploaded] = useState(false);
  const [patientAdherence, setPatientAdherence] = useState<{ [key: string]: "taken" | "not_yet" | "skipped" }>({
    morning: "taken",
    afternoon: "not_yet",
    evening: "not_yet",
  });
  const [aiQuery, setAiQuery] = useState("");
  const [aiResponse, setAiResponse] = useState<string | null>(null);
  const [activeQueue, setActiveQueue] = useState([
    { token: "T-104", name: "Hamza Farooqi", doctor: "Dr. Mansoor Alam", room: "OPD 3", status: "In Consultation", time: "10:15 AM" },
    { token: "T-105", name: "Ayesha Siddiqui", doctor: "Dr. Aisha Siddiqui", room: "OPD 2", status: "Waiting", time: "10:28 AM" },
    { token: "T-106", name: "Mohammed Zeeshan", doctor: "Dr. Tariq Zafar", room: "OPD 1", status: "Waiting", time: "10:40 AM" },
  ]);

  const handlePlayVoice = () => {
    setIsPlayingAudio(true);
    setTimeout(() => setIsPlayingAudio(false), 3000);
  };

  const handleAskAi = () => {
    if (!aiQuery.trim()) return;
    setAiResponse(
      `Hakeem Sahab AI Analysis for "${aiQuery}":\n` +
      `• Humoral Deviation: Su-e-Mizaj Barid Balghami.\n` +
      `• Prescribed Herb: Suranjan Talkh (Schedule E-1 Mudabbar mandatory).\n` +
      `• Advisory Only: Doctor review required before lock.`
    );
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="light-content" backgroundColor="#0A0F1D" />

      {/* Unified Top Mobile Header */}
      <View style={styles.topBar}>
        <View style={styles.brandRow}>
          <View style={styles.logoBox}>
            <Text style={styles.logoLetter}>Z</Text>
          </View>
          <View>
            <View style={styles.titleRow}>
              <Text style={styles.brandTitle}>ZAYVORA</Text>
              <Text style={styles.brandTag}>OS</Text>
            </View>
            <Text style={styles.brandSub}>ZAYVORA Matab™</Text>
          </View>
        </View>

        {/* Role Switcher Chips */}
        <View style={styles.roleSwitcher}>
          <TouchableOpacity
            style={[styles.roleChip, activeRole === "doctor" && styles.roleChipActive]}
            onPress={() => { setActiveRole("doctor"); setCurrentTab("home"); }}
          >
            <Text style={[styles.roleChipText, activeRole === "doctor" && styles.roleChipTextActive]}>Doctor</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.roleChip, activeRole === "patient" && styles.roleChipActive]}
            onPress={() => { setActiveRole("patient"); setCurrentTab("home"); }}
          >
            <Text style={[styles.roleChipText, activeRole === "patient" && styles.roleChipTextActive]}>Patient</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.roleChip, activeRole === "receptionist" && styles.roleChipActive]}
            onPress={() => { setActiveRole("receptionist"); setCurrentTab("queue"); }}
          >
            <Text style={[styles.roleChipText, activeRole === "receptionist" && styles.roleChipTextActive]}>OPD</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* ============================================================= */}
      {/* 1. DOCTOR MOBILE WORKSPACE                                   */}
      {/* ============================================================= */}
      {activeRole === "doctor" && (
        <ScrollView style={styles.scrollArea} contentContainerStyle={styles.scrollContent}>
          {currentTab === "home" && (
            <View style={styles.moduleSpace}>
              {/* Doctor Status Banner */}
              <View style={styles.doctorBanner}>
                <View>
                  <Text style={styles.bannerBadge}>OPD CONSULTATION ACTIVE</Text>
                  <Text style={styles.bannerTitle}>Prof. (Dr.) Mansoor Alam</Text>
                  <Text style={styles.bannerSub}>OPD Room 3 • 4 In Consult / Waiting</Text>
                </View>
                <View style={styles.pulseIndicator}>
                  <View style={styles.pulseDot} />
                  <Text style={styles.pulseText}>Live</Text>
                </View>
              </View>

              {/* Next Patient Card */}
              <View style={styles.cardHighlight}>
                <View style={styles.rowBetween}>
                  <Text style={styles.cardHeader}>NEXT PATIENT IN QUEUE</Text>
                  <Text style={styles.tokenTag}>Token: T-104</Text>
                </View>
                <Text style={styles.patientName}>Hamza Farooqi (44 M)</Text>
                <Text style={styles.patientDetails}>MRN-2026-0814 • Mizaj: Balghami (Cold & Moist)</Text>
                <Text style={styles.complaintText}>"Bilateral knee stiffness, joint ache in damp weather"</Text>
                
                <View style={styles.cardBtnRow}>
                  <TouchableOpacity style={styles.primaryBtn} onPress={() => alert("Launching Clinical Encounter ENC-2026-0814")}>
                    <Text style={styles.primaryBtnText}>Start Consultation 🩺</Text>
                  </TouchableOpacity>
                  <TouchableOpacity style={styles.secondaryBtn} onPress={() => setCurrentTab("ai")}>
                    <Text style={styles.secondaryBtnText}>AI Copilot 🤖</Text>
                  </TouchableOpacity>
                </View>
              </View>

              {/* Doctor Mobile KPIs */}
              <View style={styles.kpiGrid}>
                <View style={styles.kpiBox}>
                  <Text style={styles.kpiVal}>28</Text>
                  <Text style={styles.kpiLabel}>Today Appts</Text>
                </View>
                <View style={styles.kpiBox}>
                  <Text style={styles.kpiVal}>14</Text>
                  <Text style={styles.kpiLabel}>Follow-ups</Text>
                </View>
                <View style={styles.kpiBox}>
                  <Text style={styles.kpiVal}>3</Text>
                  <Text style={styles.kpiLabel}>Lab Reviews</Text>
                </View>
                <View style={styles.kpiBox}>
                  <Text style={styles.kpiVal}>₹38.4K</Text>
                  <Text style={styles.kpiLabel}>OPD Revenue</Text>
                </View>
              </View>

              {/* Clinical Safety Alerts */}
              <View style={styles.alertCard}>
                <Text style={styles.alertTitle}>⚠️ Active Clinical Safety Alert</Text>
                <Text style={styles.alertText}>
                  Schedule E(1) Mudabbar Gate: Patient T-104 prescribed Suranjan Talkh. Ensure Mudabbar lot MS-2026-LOT4 is verified before lock.
                </Text>
              </View>
            </View>
          )}

          {currentTab === "patients" && (
            <View style={styles.moduleSpace}>
              <Text style={styles.sectionHeading}>Patient Directory (Active Consultations)</Text>
              {[
                { name: "Hamza Farooqi", mrn: "MRN-2026-0814", cond: "Knee Osteoarthritis", mizaj: "Balghami" },
                { name: "Ayesha Siddiqui", mrn: "MRN-2026-0815", cond: "Su-e-Hazm & Gastritis", mizaj: "Safrawi" },
                { name: "Mohammed Zeeshan", mrn: "MRN-2026-0816", cond: "Lumbar Muscle Spasm", mizaj: "Saudawi" },
              ].map((p, i) => (
                <View key={i} style={styles.patientCard}>
                  <View style={styles.rowBetween}>
                    <Text style={styles.patientName}>{p.name}</Text>
                    <Text style={styles.mizajBadge}>{p.mizaj}</Text>
                  </View>
                  <Text style={styles.patientDetails}>{p.mrn} • {p.cond}</Text>
                  <TouchableOpacity style={styles.miniBtn} onPress={() => alert(`Opening ${p.name}'s dossier`)}>
                    <Text style={styles.miniBtnText}>View Clinical History →</Text>
                  </TouchableOpacity>
                </View>
              ))}
            </View>
          )}

          {currentTab === "ai" && (
            <View style={styles.moduleSpace}>
              <View style={styles.aiBanner}>
                <Text style={styles.aiTitle}>🤖 Hakeem Sahab™ Mobile Copilot</Text>
                <Text style={styles.aiSub}>Advisory Clinical Intelligence • 94.2% Concordance</Text>
              </View>

              <View style={styles.aiInputBox}>
                <TextInput
                  style={styles.aiTextInput}
                  placeholder="Ask about dosage, Asbab Sittah, herb interactions..."
                  placeholderTextColor="#64748B"
                  value={aiQuery}
                  onChangeText={setAiQuery}
                />
                <TouchableOpacity style={styles.aiSendBtn} onPress={handleAskAi}>
                  <Text style={styles.primaryBtnText}>Ask AI</Text>
                </TouchableOpacity>
              </View>

              {aiResponse && (
                <View style={styles.aiResultCard}>
                  <Text style={styles.aiResultText}>{aiResponse}</Text>
                </View>
              )}
            </View>
          )}
        </ScrollView>
      )}

      {/* ============================================================= */}
      {/* 2. PATIENT MOBILE WORKSPACE                                   */}
      {/* ============================================================= */}
      {activeRole === "patient" && (
        <ScrollView style={styles.scrollArea} contentContainerStyle={styles.scrollContent}>
          {currentTab === "home" && (
            <View style={styles.moduleSpace}>
              {/* Patient Profile Header */}
              <View style={styles.patientHeader}>
                <View>
                  <Text style={styles.bannerBadge}>PERSONAL HEALTH RECORD</Text>
                  <Text style={styles.bannerTitle}>Hamza Farooqi</Text>
                  <Text style={styles.bannerSub}>MRN-2026-0814 • Balghami (Cold & Moist)</Text>
                </View>
                <View style={styles.badgeActiveCare}>
                  <Text style={styles.badgeActiveCareText}>Stage 2: Tanqiya</Text>
                </View>
              </View>

              {/* Action-First Regimen: What do I do today? */}
              <View style={styles.actionRegimenCard}>
                <View style={styles.rowBetween}>
                  <Text style={styles.cardHeader}>TODAY'S CARE • NEXT ACTION</Text>
                  <Text style={styles.badgeActionHeader}>What do I do today?</Text>
                </View>
                <Text style={styles.regimenMainTask}>Hab-e-Suranjan (2 pills) + Roghan Massage</Text>
                <Text style={styles.regimenSub}>Scheduled for: After Lunch &amp; Bedtime</Text>

                <View style={styles.adherenceList}>
                  {[
                    { id: "morning", label: "Morning Dose", item: "Majun Suranjan 5g with lukewarm water", time: "8:00 AM" },
                    { id: "afternoon", label: "Afternoon Regimen", item: "Arq-e-Badiyan 25ml post-lunch", time: "1:30 PM" },
                    { id: "evening", label: "Bedtime Regimen", item: "Roghan-e-Balsan local joint massage", time: "9:00 PM" }
                  ].map((task) => (
                    <View key={task.id} style={styles.adherenceItem}>
                      <View style={styles.rowBetween}>
                        <Text style={styles.adherenceTaskName}>{task.label} ({task.time})</Text>
                        <Text style={[
                          styles.adherenceBadge,
                          patientAdherence[task.id] === "taken" ? styles.adherenceBadgeTaken :
                          patientAdherence[task.id] === "skipped" ? styles.adherenceBadgeSkipped : styles.adherenceBadgePending
                        ]}>
                          {patientAdherence[task.id] === "taken" ? "✓ Taken" :
                           patientAdherence[task.id] === "skipped" ? "✕ Skipped" : "⏳ Pending"}
                        </Text>
                      </View>
                      <Text style={styles.adherenceTaskDetail}>{task.item}</Text>
                      <View style={styles.adherenceBtnRow}>
                        <TouchableOpacity
                          style={[styles.adherenceBtn, patientAdherence[task.id] === "taken" && styles.adherenceBtnActive]}
                          onPress={() => setPatientAdherence(prev => ({ ...prev, [task.id]: "taken" }))}
                        >
                          <Text style={[styles.adherenceBtnText, patientAdherence[task.id] === "taken" && styles.adherenceBtnTextActive]}>✓ Taken</Text>
                        </TouchableOpacity>
                        <TouchableOpacity
                          style={[styles.adherenceBtn, patientAdherence[task.id] === "not_yet" && styles.adherenceBtnActive]}
                          onPress={() => setPatientAdherence(prev => ({ ...prev, [task.id]: "not_yet" }))}
                        >
                          <Text style={[styles.adherenceBtnText, patientAdherence[task.id] === "not_yet" && styles.adherenceBtnTextActive]}>⏳ Not Yet</Text>
                        </TouchableOpacity>
                        <TouchableOpacity
                          style={[styles.adherenceBtn, patientAdherence[task.id] === "skipped" && styles.adherenceBtnActive]}
                          onPress={() => setPatientAdherence(prev => ({ ...prev, [task.id]: "skipped" }))}
                        >
                          <Text style={[styles.adherenceBtnText, patientAdherence[task.id] === "skipped" && styles.adherenceBtnTextActive]}>✕ Skipped</Text>
                        </TouchableOpacity>
                      </View>
                    </View>
                  ))}
                </View>
              </View>

              {/* Next Scheduled Appointment */}
              <View style={styles.cardHighlight}>
                <Text style={styles.cardHeader}>NEXT CLINICAL VISIT</Text>
                <Text style={styles.patientName}>Sep 15, 2026 at 10:30 AM</Text>
                <Text style={styles.patientDetails}>ZAYVORA Matab™ • OPD Room 3</Text>
                <Text style={styles.doctorName}>Prof. (Dr.) Mansoor Alam</Text>
                <View style={styles.cardBtnRow}>
                  <TouchableOpacity style={styles.primaryBtn} onPress={() => alert("Connecting to HD Encrypted Teleconsultation...")}>
                    <Text style={styles.primaryBtnText}>Join Video Call 📹</Text>
                  </TouchableOpacity>
                  <TouchableOpacity style={styles.secondaryBtn} onPress={() => alert("Reschedule requested")}>
                    <Text style={styles.secondaryBtnText}>Reschedule 📅</Text>
                  </TouchableOpacity>
                </View>
              </View>

              {/* Vernacular Audio Medication Guide */}
              <View style={styles.audioCard}>
                <View style={styles.rowBetween}>
                  <Text style={styles.cardHeader}>🔊 VOICE MEDICATION GUIDE</Text>
                  <View style={styles.langRow}>
                    {(["urdu", "hindi", "english"] as const).map(l => (
                      <TouchableOpacity
                        key={l}
                        style={[styles.langBtn, audioLang === l && styles.langBtnActive]}
                        onPress={() => setAudioLang(l)}
                      >
                        <Text style={[styles.langBtnText, audioLang === l && styles.langBtnTextActive]}>
                          {l.toUpperCase()}
                        </Text>
                      </TouchableOpacity>
                    ))}
                  </View>
                </View>

                <Text style={styles.audioScript}>
                  {audioLang === "urdu" && "Majun Suranjan subah aur sham 5 gram neem garam pani ke sath lein."}
                  {audioLang === "hindi" && "Majun Suranjan subah aur shaam 5 gram gungune paani ke saath lein."}
                  {audioLang === "english" && "Take Majun Suranjan 5 grams twice daily with lukewarm water."}
                </Text>

                <TouchableOpacity style={styles.voicePlayBtn} onPress={handlePlayVoice}>
                  <Text style={styles.voicePlayText}>
                    {isPlayingAudio ? "▶ Playing Voice Instructions..." : "🔊 Listen to Voice Posology"}
                  </Text>
                </TouchableOpacity>
              </View>

              {/* Upload Report Quick Action */}
              <View style={styles.uploadCard}>
                <Text style={styles.cardHeader}>DIAGNOSTIC LAB REPORTS</Text>
                <Text style={styles.uploadSub}>Drop or capture your blood panel / knee X-ray</Text>
                <TouchableOpacity
                  style={styles.uploadActionBtn}
                  onPress={() => {
                    setReportUploaded(true);
                    alert("Report uploaded: ESR_CRP_Panel_Sep2026.pdf (Verified ABDM Encrypted)");
                  }}
                >
                  <Text style={styles.uploadActionText}>
                    {reportUploaded ? "✓ Report Uploaded (Pending Review)" : "📷 Take Photo / Upload Lab PDF"}
                  </Text>
                </TouchableOpacity>
              </View>
            </View>
          )}

          {currentTab === "careplan" && (
            <View style={styles.moduleSpace}>
              <Text style={styles.sectionHeading}>4-Stage Afaal Treatment Cascade</Text>
              {[
                { stage: "Stage 01: Taskeen-e-Alam", desc: "Pain mitigation with warm Roghan-e-Balsan.", status: "Done" },
                { stage: "Stage 02: Tanqiya-e-Mawad", desc: "Humor evacuation with Munzij herbs.", status: "Active" },
                { stage: "Stage 03: Ta'dil-e-Mizaj", desc: "Temperamental normalization via diet.", status: "Upcoming" },
                { stage: "Stage 04: Taqwiyat-e-Mafasil", desc: "Joint fortification and cartilage care.", status: "Upcoming" },
              ].map((c, i) => (
                <View key={i} style={[styles.patientCard, c.status === "Active" && styles.cardActiveBorder]}>
                  <View style={styles.rowBetween}>
                    <Text style={styles.patientName}>{c.stage}</Text>
                    <Text style={styles.mizajBadge}>{c.status}</Text>
                  </View>
                  <Text style={styles.patientDetails}>{c.desc}</Text>
                </View>
              ))}
            </View>
          )}
        </ScrollView>
      )}

      {/* ============================================================= */}
      {/* 3. RECEPTIONIST MOBILE WORKSPACE                              */}
      {/* ============================================================= */}
      {activeRole === "receptionist" && (
        <ScrollView style={styles.scrollArea} contentContainerStyle={styles.scrollContent}>
          <View style={styles.moduleSpace}>
            <View style={styles.receptionHeader}>
              <Text style={styles.bannerBadge}>OPD RECEPTION & TRIAGE</Text>
              <Text style={styles.bannerTitle}>Live OPD Queue (Queue Tokens)</Text>
              <Text style={styles.bannerSub}>Check-in patients, call tokens to room, collect fees.</Text>
            </View>

            {/* Quick Register Token Button */}
            <TouchableOpacity style={styles.fullPrimaryBtn} onPress={() => alert("Issued Token T-107 for Walk-In Patient")}>
              <Text style={styles.primaryBtnText}>+ Issue Walk-In OPD Token</Text>
            </TouchableOpacity>

            {/* Live Queue Cards */}
            {activeQueue.map((item, idx) => (
              <View key={idx} style={styles.queueCard}>
                <View style={styles.rowBetween}>
                  <Text style={styles.queueToken}>{item.token}</Text>
                  <Text style={styles.queueStatus}>{item.status}</Text>
                </View>
                <Text style={styles.patientName}>{item.name}</Text>
                <Text style={styles.patientDetails}>{item.doctor} • {item.room} • {item.time}</Text>

                <View style={styles.cardBtnRow}>
                  <TouchableOpacity style={styles.miniCallBtn} onPress={() => alert(`Calling Token ${item.token} to ${item.room}`)}>
                    <Text style={styles.miniCallBtnText}>🔊 Call Token</Text>
                  </TouchableOpacity>
                  <TouchableOpacity style={styles.miniDoneBtn} onPress={() => alert(`Marked ${item.token} Completed`)}>
                    <Text style={styles.miniDoneBtnText}>✓ Check-Out</Text>
                  </TouchableOpacity>
                </View>
              </View>
            ))}
          </View>
        </ScrollView>
      )}

      {/* Unified Bottom Navigation Tabs */}
      <View style={styles.bottomNav}>
        {activeRole === "doctor" && (
          <>
            <TouchableOpacity style={styles.navItem} onPress={() => setCurrentTab("home")}>
              <Text style={styles.navIcon}>📊</Text>
              <Text style={[styles.navLabel, currentTab === "home" && styles.navLabelActive]}>Home</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.navItem} onPress={() => setCurrentTab("patients")}>
              <Text style={styles.navIcon}>👥</Text>
              <Text style={[styles.navLabel, currentTab === "patients" && styles.navLabelActive]}>Patients</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.navItem} onPress={() => setCurrentTab("ai")}>
              <Text style={styles.navIcon}>🤖</Text>
              <Text style={[styles.navLabel, currentTab === "ai" && styles.navLabelActive]}>AI Doctor</Text>
            </TouchableOpacity>
          </>
        )}

        {activeRole === "patient" && (
          <>
            <TouchableOpacity style={styles.navItem} onPress={() => setCurrentTab("home")}>
              <Text style={styles.navIcon}>👤</Text>
              <Text style={[styles.navLabel, currentTab === "home" && styles.navLabelActive]}>Health 360</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.navItem} onPress={() => setCurrentTab("careplan")}>
              <Text style={styles.navIcon}>🌿</Text>
              <Text style={[styles.navLabel, currentTab === "careplan" && styles.navLabelActive]}>Care Plan</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.navItem} onPress={() => alert("Opening Doctor Chat Thread...")}>
              <Text style={styles.navIcon}>💬</Text>
              <Text style={styles.navLabel}>Messages</Text>
            </TouchableOpacity>
          </>
        )}

        {activeRole === "receptionist" && (
          <>
            <TouchableOpacity style={styles.navItem} onPress={() => setCurrentTab("queue")}>
              <Text style={styles.navIcon}>🏥</Text>
              <Text style={[styles.navLabel, currentTab === "queue" && styles.navLabelActive]}>OPD Queue</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.navItem} onPress={() => alert("Doctor Roster: Room 1 Active, Room 2 Active, Room 3 Busy, Room 4 Active")}>
              <Text style={styles.navIcon}>🩺</Text>
              <Text style={styles.navLabel}>Roster</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.navItem} onPress={() => alert("Today Fees: ₹38,450 (100% Reconciled)")}>
              <Text style={styles.navIcon}>💳</Text>
              <Text style={styles.navLabel}>Billing</Text>
            </TouchableOpacity>
          </>
        )}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: "#0A0F1D" },
  topBar: {
    paddingHorizontal: 16,
    paddingVertical: 10,
    backgroundColor: "#0F172A",
    borderBottomWidth: 1,
    borderBottomColor: "#1E293B",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  brandRow: { flexDirection: "row", alignItems: "center", gap: 10 },
  logoBox: {
    width: 32,
    height: 32,
    borderRadius: 8,
    backgroundColor: "#0D9488",
    alignItems: "center",
    justifyContent: "center",
  },
  logoLetter: { color: "#FFFFFF", fontWeight: "900", fontSize: 18 },
  titleRow: { flexDirection: "row", alignItems: "center", gap: 4 },
  brandTitle: { color: "#FFFFFF", fontWeight: "800", fontSize: 15, letterSpacing: 0.5 },
  brandTag: { color: "#2DD4BF", fontWeight: "700", fontSize: 10, backgroundColor: "rgba(45,212,191,0.15)", paddingHorizontal: 4, borderRadius: 4 },
  brandSub: { color: "#94A3B8", fontSize: 10 },
  roleSwitcher: { flexDirection: "row", gap: 4, backgroundColor: "#0A0F1D", padding: 3, borderRadius: 10 },
  roleChip: { paddingHorizontal: 8, paddingVertical: 4, borderRadius: 6 },
  roleChipActive: { backgroundColor: "#0D9488" },
  roleChipText: { color: "#94A3B8", fontSize: 11, fontWeight: "600" },
  roleChipTextActive: { color: "#FFFFFF" },
  scrollArea: { flex: 1 },
  scrollContent: { padding: 16, paddingBottom: 80 },
  moduleSpace: { gap: 16 },
  doctorBanner: {
    backgroundColor: "#132338",
    padding: 16,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "#1E3A5F",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  patientHeader: {
    backgroundColor: "#0E2428",
    padding: 16,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "#134E4A",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  receptionHeader: {
    backgroundColor: "#172554",
    padding: 16,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "#1E3A8A",
  },
  bannerBadge: { color: "#2DD4BF", fontSize: 10, fontWeight: "800", letterSpacing: 1 },
  bannerTitle: { color: "#FFFFFF", fontSize: 18, fontWeight: "800", marginTop: 2 },
  bannerSub: { color: "#94A3B8", fontSize: 11, marginTop: 2 },
  pulseIndicator: { flexDirection: "row", alignItems: "center", gap: 6, backgroundColor: "rgba(16,185,129,0.2)", paddingHorizontal: 8, paddingVertical: 4, borderRadius: 8 },
  pulseDot: { width: 8, height: 8, borderRadius: 4, backgroundColor: "#10B981" },
  pulseText: { color: "#10B981", fontSize: 10, fontWeight: "700" },
  badgeActiveCare: { backgroundColor: "#064E3B", paddingHorizontal: 10, paddingVertical: 5, borderRadius: 8, borderWidth: 1, borderColor: "#059669" },
  badgeActiveCareText: { color: "#6EE7B7", fontSize: 11, fontWeight: "700" },
  cardHighlight: {
    backgroundColor: "#1E293B",
    padding: 16,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "#334155",
    gap: 8,
  },
  rowBetween: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  cardHeader: { color: "#2DD4BF", fontSize: 10, fontWeight: "800", letterSpacing: 1 },
  tokenTag: { color: "#FDE68A", fontSize: 12, fontWeight: "800", backgroundColor: "#78350F", paddingHorizontal: 8, paddingVertical: 2, borderRadius: 6 },
  patientName: { color: "#FFFFFF", fontSize: 16, fontWeight: "700" },
  patientDetails: { color: "#94A3B8", fontSize: 12 },
  doctorName: { color: "#2DD4BF", fontSize: 12, fontWeight: "600" },
  complaintText: { color: "#E2E8F0", fontSize: 12, fontStyle: "italic", marginTop: 2 },
  cardBtnRow: { flexDirection: "row", gap: 8, marginTop: 8 },
  primaryBtn: { flex: 1, backgroundColor: "#0D9488", paddingVertical: 10, borderRadius: 10, alignItems: "center" },
  primaryBtnText: { color: "#FFFFFF", fontWeight: "700", fontSize: 12 },
  secondaryBtn: { flex: 1, backgroundColor: "#334155", paddingVertical: 10, borderRadius: 10, alignItems: "center" },
  secondaryBtnText: { color: "#E2E8F0", fontWeight: "600", fontSize: 12 },
  fullPrimaryBtn: { backgroundColor: "#0D9488", paddingVertical: 12, borderRadius: 12, alignItems: "center" },
  kpiGrid: { flexDirection: "row", gap: 8 },
  kpiBox: { flex: 1, backgroundColor: "#0F172A", padding: 12, borderRadius: 12, borderWidth: 1, borderColor: "#1E293B", alignItems: "center" },
  kpiVal: { color: "#FFFFFF", fontSize: 16, fontWeight: "800" },
  kpiLabel: { color: "#94A3B8", fontSize: 10, marginTop: 2 },
  alertCard: { backgroundColor: "#450A0A", padding: 12, borderRadius: 12, borderWidth: 1, borderColor: "#7F1D1D", gap: 4 },
  alertTitle: { color: "#FCA5A5", fontWeight: "700", fontSize: 12 },
  alertText: { color: "#FECACA", fontSize: 11, lineHeight: 16 },
  sectionHeading: { color: "#FFFFFF", fontSize: 15, fontWeight: "700" },
  patientCard: { backgroundColor: "#0F172A", padding: 14, borderRadius: 14, borderWidth: 1, borderColor: "#1E293B", gap: 6 },
  cardActiveBorder: { borderColor: "#0D9488", backgroundColor: "#0B1D22" },
  mizajBadge: { color: "#2DD4BF", fontSize: 10, fontWeight: "700", backgroundColor: "#134E4A", paddingHorizontal: 6, paddingVertical: 2, borderRadius: 4 },
  miniBtn: { marginTop: 4 },
  miniBtnText: { color: "#2DD4BF", fontSize: 11, fontWeight: "600" },
  aiBanner: { backgroundColor: "#083344", padding: 14, borderRadius: 14, borderWidth: 1, borderColor: "#155E75" },
  aiTitle: { color: "#67E8F9", fontSize: 14, fontWeight: "700" },
  aiSub: { color: "#A5F3FC", fontSize: 10, marginTop: 2 },
  aiInputBox: { flexDirection: "row", gap: 8 },
  aiTextInput: { flex: 1, backgroundColor: "#0F172A", borderWidth: 1, borderColor: "#334155", borderRadius: 10, paddingHorizontal: 12, color: "#FFFFFF", fontSize: 12 },
  aiSendBtn: { backgroundColor: "#0D9488", paddingHorizontal: 16, borderRadius: 10, justifyContent: "center" },
  aiResultCard: { backgroundColor: "#0F172A", padding: 14, borderRadius: 14, borderWidth: 1, borderColor: "#1E293B" },
  aiResultText: { color: "#E2E8F0", fontSize: 12, lineHeight: 18 },
  audioCard: { backgroundColor: "#0F172A", padding: 14, borderRadius: 14, borderWidth: 1, borderColor: "#1E293B", gap: 10 },
  langRow: { flexDirection: "row", gap: 4 },
  langBtn: { paddingHorizontal: 6, paddingVertical: 2, borderRadius: 4, backgroundColor: "#1E293B" },
  langBtnActive: { backgroundColor: "#0D9488" },
  langBtnText: { color: "#94A3B8", fontSize: 9, fontWeight: "700" },
  langBtnTextActive: { color: "#FFFFFF" },
  audioScript: { color: "#CBD5E1", fontSize: 12, fontStyle: "italic", lineHeight: 18 },
  voicePlayBtn: { backgroundColor: "#134E4A", paddingVertical: 10, borderRadius: 10, alignItems: "center" },
  voicePlayText: { color: "#5EEAD4", fontSize: 12, fontWeight: "700" },
  uploadCard: { backgroundColor: "#0F172A", padding: 14, borderRadius: 14, borderWidth: 1, borderColor: "#1E293B", gap: 6 },
  uploadSub: { color: "#94A3B8", fontSize: 11 },
  uploadActionBtn: { borderWidth: 1, borderStyle: "dashed", borderColor: "#0D9488", paddingVertical: 14, borderRadius: 10, alignItems: "center", backgroundColor: "rgba(13,148,136,0.05)" },
  uploadActionText: { color: "#2DD4BF", fontSize: 12, fontWeight: "600" },
  queueCard: { backgroundColor: "#0F172A", padding: 14, borderRadius: 14, borderWidth: 1, borderColor: "#1E293B", gap: 6 },
  queueToken: { color: "#2DD4BF", fontSize: 15, fontWeight: "900", fontVariant: ["tabular-nums"] },
  queueStatus: { color: "#FDE68A", fontSize: 10, fontWeight: "700", backgroundColor: "#78350F", paddingHorizontal: 6, paddingVertical: 2, borderRadius: 4 },
  miniCallBtn: { flex: 1, backgroundColor: "#0D9488", paddingVertical: 6, borderRadius: 8, alignItems: "center" },
  miniCallBtnText: { color: "#FFFFFF", fontSize: 11, fontWeight: "700" },
  miniDoneBtn: { flex: 1, backgroundColor: "#059669", paddingVertical: 6, borderRadius: 8, alignItems: "center" },
  miniDoneBtnText: { color: "#FFFFFF", fontSize: 11, fontWeight: "700" },
  bottomNav: {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    height: 60,
    backgroundColor: "#0F172A",
    borderTopWidth: 1,
    borderTopColor: "#1E293B",
    flexDirection: "row",
    justifyContent: "space-around",
    alignItems: "center",
  },
  navItem: { alignItems: "center", gap: 2 },
  navIcon: { fontSize: 18 },
  navLabel: { color: "#94A3B8", fontSize: 10, fontWeight: "600" },
  navLabelActive: { color: "#2DD4BF" },

  // Action Regimen Styles
  actionRegimenCard: { backgroundColor: "#0C1B2A", padding: 14, borderRadius: 16, borderWidth: 1, borderColor: "#0284C7", gap: 8 },
  badgeActionHeader: { color: "#38BDF8", fontSize: 10, fontWeight: "700", backgroundColor: "rgba(56, 189, 248, 0.15)", paddingHorizontal: 8, paddingVertical: 2, borderRadius: 6 },
  regimenMainTask: { color: "#F0F9FF", fontSize: 15, fontWeight: "800", marginTop: 2 },
  regimenSub: { color: "#7DD3FC", fontSize: 11, marginBottom: 4 },
  adherenceList: { gap: 8 },
  adherenceItem: { backgroundColor: "#0F172A", padding: 10, borderRadius: 10, borderWidth: 1, borderColor: "#1E293B", gap: 4 },
  adherenceTaskName: { color: "#FFFFFF", fontSize: 12, fontWeight: "700" },
  adherenceBadge: { fontSize: 9, fontWeight: "700", paddingHorizontal: 6, paddingVertical: 2, borderRadius: 4 },
  adherenceBadgeTaken: { color: "#10B981", backgroundColor: "rgba(16, 185, 129, 0.15)" },
  adherenceBadgeSkipped: { color: "#EF4444", backgroundColor: "rgba(239, 68, 68, 0.15)" },
  adherenceBadgePending: { color: "#F59E0B", backgroundColor: "rgba(245, 158, 11, 0.15)" },
  adherenceTaskDetail: { color: "#94A3B8", fontSize: 11 },
  adherenceBtnRow: { flexDirection: "row", gap: 6, marginTop: 4 },
  adherenceBtn: { flex: 1, paddingVertical: 6, borderRadius: 6, backgroundColor: "#1E293B", alignItems: "center" },
  adherenceBtnActive: { backgroundColor: "#0D9488" },
  adherenceBtnText: { color: "#94A3B8", fontSize: 10, fontWeight: "700" },
  adherenceBtnTextActive: { color: "#FFFFFF" },
});
