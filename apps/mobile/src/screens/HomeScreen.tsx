import React, { useState } from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, TextInput } from "react-native";
import { PatientProfile } from "../types";

export const HomeScreen: React.FC<{ onNavigate: (screen: string) => void }> = ({ onNavigate }) => {
  const [activePersona, setActivePersona] = useState<"doctor" | "patient">("doctor");
  const [aiQuery, setAiQuery] = useState("");
  const [aiResponse, setAiResponse] = useState<string | null>(null);
  const [adherence, setAdherence] = useState<{ [key: string]: "taken" | "not_yet" | "skipped" }>({
    morning: "taken",
    afternoon: "not_yet",
    evening: "not_yet",
  });
  const [audioLang, setAudioLang] = useState<"urdu" | "hindi" | "english">("urdu");
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  const kpis = [
    { label: "Total Patients", value: "1,248", change: "+12%", color: "#10B981" },
    { label: "Appointments", value: "28", change: "8 Done", color: "#3B82F6" },
    { label: "Follow-ups", value: "14", change: "6 Urgent", color: "#F59E0B" },
    { label: "Active Plans", value: "89", change: "+7 wk", color: "#8B5CF6" },
    { label: "Today Revenue", value: "₹54.2K", change: "+18%", color: "#2DD4BF" },
    { label: "Critical Alerts", value: "2", change: "Action Req", color: "#EF4444" },
  ];

  const todayAppointments = [
    { id: "APT-801", name: "Hamza Farooqi", time: "10:30 AM", type: "In-Person", status: "In Consultation" },
    { id: "APT-802", name: "Ayesha Siddiqui", time: "11:15 AM", type: "Online", status: "Waiting" },
    { id: "APT-803", name: "Bilal Ahmad", time: "12:00 PM", type: "In-Person", status: "Confirmed" },
  ];

  const asbabFactors = [
    { name: "Hawa (Air)", score: 88, color: "#2DD4BF" },
    { name: "Makul (Diet)", score: 82, color: "#10B981" },
    { name: "Harkat (Motion)", score: 76, color: "#3B82F6" },
    { name: "Naum (Sleep)", score: 85, color: "#8B5CF6" },
    { name: "Istifragh (Detox)", score: 90, color: "#F59E0B" },
    { name: "Nafsani (Mind)", score: 83, color: "#EC4899" }
  ];

  function handleAskAi() {
    if (!aiQuery.trim()) return;
    setAiResponse(
      `AI Copilot: "${aiQuery}"\n` +
      `• Humoral Evaluation: Su-e-Mizaj Barid Balghami.\n` +
      `• Recommended Regimen: Afaal Stage 1 (Tanqiya) + Arq-e-Badiyan.\n` +
      `• Safety: safe_to_lock = False. Clinician review required.`
    );
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.scrollContent}>
      
      {/* Persona Toggle Bar */}
      <View style={styles.personaBar}>
        <Text style={styles.personaLabel}>DASHBOARD MODE:</Text>
        <View style={styles.personaGroup}>
          <TouchableOpacity
            style={[styles.personaBtn, activePersona === "doctor" && styles.personaBtnActive]}
            onPress={() => setActivePersona("doctor")}
          >
            <Text style={[styles.personaText, activePersona === "doctor" && styles.personaTextActive]}>
              🩺 Doctor View
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.personaBtn, activePersona === "patient" && styles.personaBtnActive]}
            onPress={() => setActivePersona("patient")}
          >
            <Text style={[styles.personaText, activePersona === "patient" && styles.personaTextActive]}>
              👤 Patient View
            </Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Welcome Section */}
      <View style={styles.welcomeCard}>
        <View style={styles.rowBetween}>
          <View>
            <Text style={styles.greeting}>
              {activePersona === "doctor" ? "Good Morning, Hakeem Dr. Irfan" : "Marhaban, Mohammad Tariq"}
            </Text>
            <Text style={styles.subGreeting}>
              {activePersona === "doctor"
                ? "Here is your clinical & operational overview for today."
                : "MRN: ZAY-2026-8819 • Balghami (Cold & Moist)"}
            </Text>
          </View>
          <View style={styles.badgeOpen}>
            <Text style={styles.badgeOpenText}>Clinic Open</Text>
          </View>
        </View>

        <View style={styles.metaRow}>
          <Text style={styles.metaItem}>📅 Sunday, 13 Sep 2026</Text>
          <Text style={styles.metaItem}>🕒 09:00 AM - 06:00 PM</Text>
          <Text style={styles.metaItem}>🏥 ZAYVORA Matab™ Central Care Centre</Text>
        </View>

        {/* Quick Action Matrix */}
        <View style={styles.quickActionsGrid}>
          <TouchableOpacity style={styles.actionBtn} onPress={() => onNavigate("appointments")}>
            <Text style={styles.actionIcon}>📅</Text>
            <Text style={styles.actionText}>Book Consult</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.actionBtn} onPress={() => onNavigate("prescriptions")}>
            <Text style={styles.actionIcon}>📝</Text>
            <Text style={styles.actionText}>Create Rx</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.actionBtn} onPress={() => onNavigate("teleconsult")}>
            <Text style={styles.actionIcon}>🩺</Text>
            <Text style={styles.actionText}>Start Video</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.actionBtn} onPress={() => onNavigate("clinician")}>
            <Text style={styles.actionIcon}>🛡️</Text>
            <Text style={styles.actionText}>Triage Mode</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* ============================================================= */}
      {/* DOCTOR VIEW                                                   */}
      {/* ============================================================= */}
      {activePersona === "doctor" && (
        <>
          {/* 6 KPI Cards Grid */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Operational & Clinical KPIs</Text>
            <View style={styles.kpiGrid}>
              {kpis.map((kpi, idx) => (
                <View key={idx} style={styles.kpiBox}>
                  <View style={styles.rowBetween}>
                    <Text style={styles.kpiLabel}>{kpi.label}</Text>
                    <Text style={[styles.kpiChange, { color: kpi.color }]}>{kpi.change}</Text>
                  </View>
                  <Text style={styles.kpiValue}>{kpi.value}</Text>
                </View>
              ))}
            </View>
          </View>

          {/* Clinical Safety Alerts Banner */}
          <View style={styles.alertCard}>
            <View style={styles.rowBetween}>
              <Text style={styles.alertHeader}>⚠️ CLINICAL SAFETY ALERTS (2 ACTIVE)</Text>
              <Text style={styles.alertBadge}>Mandatory Review</Text>
            </View>
            <Text style={styles.alertTitle}>Azaraqi + Sedative Co-administration Warning</Text>
            <Text style={styles.alertDesc}>
              Patient Hamza Farooqi: Mudabbar Schedule E(1) check required. 6h spacing mandatory.
            </Text>
          </View>

          {/* Today's Appointments */}
          <View style={styles.card}>
            <View style={styles.rowBetween}>
              <Text style={styles.cardTitle}>Today's OPD Consultations</Text>
              <TouchableOpacity onPress={() => onNavigate("appointments")}>
                <Text style={styles.linkText}>View All →</Text>
              </TouchableOpacity>
            </View>

            <View style={styles.aptList}>
              {todayAppointments.map((apt) => (
                <View key={apt.id} style={styles.aptItem}>
                  <View>
                    <Text style={styles.aptName}>{apt.name}</Text>
                    <Text style={styles.aptSub}>{apt.time} • {apt.type}</Text>
                  </View>
                  <View style={styles.aptActionGroup}>
                    <Text style={[
                      styles.aptStatus,
                      apt.status === "In Consultation" ? styles.statusAmber :
                      apt.status === "Waiting" ? styles.statusBlue : styles.statusGreen
                    ]}>
                      {apt.status}
                    </Text>
                    <TouchableOpacity
                      style={styles.btnStart}
                      onPress={() => onNavigate(apt.type === "Online" ? "teleconsult" : "appointments")}
                    >
                      <Text style={styles.btnStartText}>Consult</Text>
                    </TouchableOpacity>
                  </View>
                </View>
              ))}
            </View>
          </View>

          {/* Hakeem Sahab AI Doctor Copilot */}
          <View style={styles.aiCard}>
            <View style={styles.rowBetween}>
              <View style={styles.rowCenter}>
                <Text style={styles.aiIcon}>🤖</Text>
                <Text style={styles.aiTitle}>Hakeem Sahab AI Copilot</Text>
              </View>
              <Text style={styles.aiActiveBadge}>Active</Text>
            </View>

            <View style={styles.aiInputRow}>
              <TextInput
                style={styles.aiInput}
                value={aiQuery}
                onChangeText={setAiQuery}
                placeholder="Ask symptoms, herbs, or interaction..."
                placeholderTextColor="#64748B"
              />
              <TouchableOpacity style={styles.aiBtn} onPress={handleAskAi}>
                <Text style={styles.aiBtnText}>Ask</Text>
              </TouchableOpacity>
            </View>

            {aiResponse && (
              <View style={styles.aiResult}>
                <Text style={styles.aiResultText}>{aiResponse}</Text>
              </View>
            )}

            <Text style={styles.aiDisclaimer}>
              Statutory: AI is for decision support only. Prescriptions require licensed clinician signature.
            </Text>
          </View>
        </>
      )}

      {/* ============================================================= */}
      {/* PATIENT VIEW                                                  */}
      {/* ============================================================= */}
      {activePersona === "patient" && (
        <>
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
                      adherence[task.id] === "taken" ? styles.adherenceBadgeTaken :
                      adherence[task.id] === "skipped" ? styles.adherenceBadgeSkipped : styles.adherenceBadgePending
                    ]}>
                      {adherence[task.id] === "taken" ? "✓ Taken" :
                       adherence[task.id] === "skipped" ? "✕ Skipped" : "⏳ Pending"}
                    </Text>
                  </View>
                  <Text style={styles.adherenceTaskDetail}>{task.item}</Text>
                  <View style={styles.adherenceBtnRow}>
                    <TouchableOpacity
                      style={[styles.adherenceBtn, adherence[task.id] === "taken" && styles.adherenceBtnActive]}
                      onPress={() => setAdherence(prev => ({ ...prev, [task.id]: "taken" }))}
                    >
                      <Text style={[styles.adherenceBtnText, adherence[task.id] === "taken" && styles.adherenceBtnTextActive]}>✓ Taken</Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                      style={[styles.adherenceBtn, adherence[task.id] === "not_yet" && styles.adherenceBtnActive]}
                      onPress={() => setAdherence(prev => ({ ...prev, [task.id]: "not_yet" }))}
                    >
                      <Text style={[styles.adherenceBtnText, adherence[task.id] === "not_yet" && styles.adherenceBtnTextActive]}>⏳ Not Yet</Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                      style={[styles.adherenceBtn, adherence[task.id] === "skipped" && styles.adherenceBtnActive]}
                      onPress={() => setAdherence(prev => ({ ...prev, [task.id]: "skipped" }))}
                    >
                      <Text style={[styles.adherenceBtnText, adherence[task.id] === "skipped" && styles.adherenceBtnTextActive]}>✕ Skipped</Text>
                    </TouchableOpacity>
                  </View>
                </View>
              ))}
            </View>
          </View>

          {/* Next Dose & Vernacular Voice */}
          <View style={styles.rxCard}>
            <View style={styles.rowBetween}>
              <Text style={styles.rxHeader}>Next Scheduled Dose</Text>
              <Text style={styles.rxCountdown}>Due in 38 mins</Text>
            </View>
            <Text style={styles.rxDrugName}>Qurs-e-Mafasil (2 tab) + Arq-e-Badiyan</Text>
            <TouchableOpacity style={styles.audioBtn} onPress={() => onNavigate("prescriptions")}>
              <Text style={styles.audioBtnIcon}>🔊</Text>
              <Text style={styles.audioBtnText}>Sunein Apni Dawa Ki Khorak (Audio Posology)</Text>
            </TouchableOpacity>
          </View>

          {/* Asbab-e-Sittah & Meezan-e-Sehat Health Radar */}
          <View style={styles.card}>
            <View style={styles.rowBetween}>
              <View>
                <Text style={styles.cardEyebrow}>Asbab-e-Sittah Zarooriyyah</Text>
                <Text style={styles.cardTitle}>Meezan-e-Sehat Equilibrium</Text>
              </View>
              <View style={styles.scoreCircle}>
                <Text style={styles.scoreNumber}>84</Text>
                <Text style={styles.scoreSub}>/ 100</Text>
              </View>
            </View>

            <View style={styles.asbabGrid}>
              {asbabFactors.map((f) => (
                <View key={f.name} style={styles.asbabItem}>
                  <View style={styles.rowBetween}>
                    <Text style={styles.asbabName}>{f.name}</Text>
                    <Text style={[styles.asbabScore, { color: f.color }]}>{f.score}%</Text>
                  </View>
                  <View style={styles.progressBarBg}>
                    <View style={[styles.progressBarFill, { width: `${f.score}%`, backgroundColor: f.color }]} />
                  </View>
                </View>
              ))}
            </View>
          </View>
        </>
      )}

      {/* Professional Mobile Footer */}
      <View style={styles.footerContainer}>
        <Text style={styles.footerTitle}>ZAYVORA Health OS™ v1.0.0</Text>
        <Text style={styles.footerSub}>© 2026 ZAYVORA Health. Modern Unani Care System.</Text>
        <View style={styles.footerLinksRow}>
          <Text style={styles.footerLink}>Privacy Policy</Text>
          <Text style={styles.footerBullet}>•</Text>
          <Text style={styles.footerLink}>Terms</Text>
          <Text style={styles.footerBullet}>•</Text>
          <Text style={styles.footerLink}>Help Center</Text>
          <Text style={styles.footerBullet}>•</Text>
          <Text style={styles.footerLink}>Support</Text>
        </View>
        <View style={styles.footerStatusRow}>
          <View style={styles.pulseDot} />
          <Text style={styles.footerStatus}>System Status: Operational • 21 CFR Part 11</Text>
        </View>
      </View>

    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0A0F1D" },
  scrollContent: { padding: 14, paddingBottom: 40 },
  personaBar: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 12, backgroundColor: "#0F172A", padding: 8, borderRadius: 12, borderWidth: 1, borderColor: "#1E293B" },
  personaLabel: { color: "#64748B", fontSize: 9, fontWeight: "bold" },
  personaGroup: { flexDirection: "row", gap: 6 },
  personaBtn: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 8, backgroundColor: "#1E293B" },
  personaBtnActive: { backgroundColor: "#0D9488" },
  personaText: { color: "#94A3B8", fontSize: 10, fontWeight: "bold" },
  personaTextActive: { color: "#FFFFFF" },

  welcomeCard: { backgroundColor: "#1E293B", borderRadius: 18, padding: 16, borderWidth: 1, borderColor: "#334155", marginBottom: 14 },
  rowBetween: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  rowCenter: { flexDirection: "row", alignItems: "center" },
  greeting: { color: "#FFFFFF", fontSize: 18, fontWeight: "bold" },
  subGreeting: { color: "#94A3B8", fontSize: 11, marginTop: 2 },
  badgeOpen: { backgroundColor: "rgba(16, 185, 129, 0.2)", paddingHorizontal: 8, paddingVertical: 4, borderRadius: 12, borderWidth: 1, borderColor: "#10B981" },
  badgeOpenText: { color: "#10B981", fontSize: 9, fontWeight: "bold" },
  metaRow: { flexDirection: "row", flexWrap: "wrap", gap: 8, marginTop: 10, paddingTop: 10, borderTopWidth: 1, borderTopColor: "#334155" },
  metaItem: { color: "#2DD4BF", fontSize: 10, fontWeight: "600" },

  quickActionsGrid: { flexDirection: "row", flexWrap: "wrap", justifyContent: "space-between", gap: 8, marginTop: 12 },
  actionBtn: { width: "23%", backgroundColor: "#0F172A", padding: 8, borderRadius: 10, alignItems: "center", borderWidth: 1, borderColor: "#334155" },
  actionIcon: { fontSize: 16 },
  actionText: { color: "#FFFFFF", fontSize: 9, fontWeight: "bold", marginTop: 2, textAlign: "center" },

  section: { marginBottom: 14 },
  sectionTitle: { color: "#F1F5F9", fontSize: 14, fontWeight: "bold", marginBottom: 8 },
  kpiGrid: { flexDirection: "row", flexWrap: "wrap", justifyContent: "space-between", gap: 8 },
  kpiBox: { width: "31%", backgroundColor: "#1E293B", padding: 10, borderRadius: 12, borderWidth: 1, borderColor: "#334155" },
  kpiLabel: { color: "#94A3B8", fontSize: 9 },
  kpiChange: { fontSize: 8, fontWeight: "bold" },
  kpiValue: { color: "#FFFFFF", fontSize: 14, fontWeight: "bold", marginTop: 4 },

  alertCard: { backgroundColor: "rgba(239, 68, 68, 0.1)", borderRadius: 14, padding: 12, borderWidth: 1, borderColor: "#EF4444", marginBottom: 14 },
  alertHeader: { color: "#F87171", fontSize: 10, fontWeight: "bold" },
  alertBadge: { backgroundColor: "rgba(239, 68, 68, 0.2)", color: "#FCA5A5", fontSize: 8, fontWeight: "bold", paddingHorizontal: 6, paddingVertical: 2, borderRadius: 6 },
  alertTitle: { color: "#FFFFFF", fontSize: 12, fontWeight: "bold", marginTop: 4 },
  alertDesc: { color: "#FCA5A5", fontSize: 10, marginTop: 2, lineHeight: 14 },

  card: { backgroundColor: "#1E293B", borderRadius: 16, padding: 14, borderWidth: 1, borderColor: "#334155", marginBottom: 14 },
  cardTitle: { color: "#FFFFFF", fontSize: 14, fontWeight: "bold" },
  cardEyebrow: { color: "#2DD4BF", fontSize: 9, fontWeight: "bold", textTransform: "uppercase" },
  linkText: { color: "#2DD4BF", fontSize: 11, fontWeight: "bold" },
  aptList: { marginTop: 8, gap: 8 },
  aptItem: { backgroundColor: "#0F172A", padding: 10, borderRadius: 10, flexDirection: "row", justifyContent: "space-between", alignItems: "center", borderWidth: 1, borderColor: "#1E293B" },
  aptName: { color: "#FFFFFF", fontSize: 12, fontWeight: "bold" },
  aptSub: { color: "#94A3B8", fontSize: 10, marginTop: 1 },
  aptActionGroup: { alignItems: "flex-end", gap: 4 },
  aptStatus: { fontSize: 9, fontWeight: "bold", paddingHorizontal: 6, paddingVertical: 1, borderRadius: 4 },
  statusAmber: { backgroundColor: "rgba(245, 158, 11, 0.2)", color: "#F59E0B" },
  statusBlue: { backgroundColor: "rgba(59, 130, 246, 0.2)", color: "#60A5FA" },
  statusGreen: { backgroundColor: "rgba(16, 185, 129, 0.2)", color: "#34D399" },
  btnStart: { backgroundColor: "#0D9488", paddingHorizontal: 8, paddingVertical: 3, borderRadius: 6 },
  btnStartText: { color: "#FFFFFF", fontSize: 9, fontWeight: "bold" },

  aiCard: { backgroundColor: "#0F172A", borderRadius: 16, padding: 14, borderWidth: 1, borderColor: "#0D9488", marginBottom: 14 },
  aiIcon: { fontSize: 18, marginRight: 6 },
  aiTitle: { color: "#FFFFFF", fontSize: 13, fontWeight: "bold" },
  aiActiveBadge: { backgroundColor: "rgba(13, 148, 136, 0.2)", color: "#2DD4BF", fontSize: 9, fontWeight: "bold", paddingHorizontal: 6, paddingVertical: 2, borderRadius: 6 },
  aiInputRow: { flexDirection: "row", gap: 6, marginTop: 8 },
  aiInput: { flex: 1, backgroundColor: "#1E293B", borderRadius: 8, paddingHorizontal: 10, paddingVertical: 6, color: "#FFFFFF", fontSize: 11, borderWidth: 1, borderColor: "#334155" },
  aiBtn: { backgroundColor: "#0D9488", paddingHorizontal: 12, borderRadius: 8, justifyContent: "center" },
  aiBtnText: { color: "#FFFFFF", fontSize: 11, fontWeight: "bold" },
  aiResult: { marginTop: 8, backgroundColor: "#1E293B", padding: 8, borderRadius: 8, borderWidth: 1, borderColor: "#334155" },
  aiResultText: { color: "#E2E8F0", fontSize: 10, fontFamily: "monospace", lineHeight: 14 },
  aiDisclaimer: { color: "#94A3B8", fontSize: 8, marginTop: 6 },

  scoreCircle: { width: 44, height: 44, borderRadius: 22, backgroundColor: "rgba(13, 148, 136, 0.2)", borderWidth: 2, borderColor: "#2DD4BF", alignItems: "center", justifyContent: "center" },
  scoreNumber: { color: "#FFFFFF", fontSize: 14, fontWeight: "bold" },
  scoreSub: { color: "#2DD4BF", fontSize: 7, fontWeight: "bold", marginTop: -2 },
  asbabGrid: { flexDirection: "row", flexWrap: "wrap", justifyContent: "space-between", gap: 6, marginTop: 8 },
  asbabItem: { width: "48%", backgroundColor: "#0F172A", padding: 8, borderRadius: 8 },
  asbabName: { color: "#FFFFFF", fontSize: 10, fontWeight: "bold" },
  asbabScore: { fontSize: 10, fontWeight: "bold" },
  progressBarBg: { height: 3, backgroundColor: "#1E293B", borderRadius: 2, marginTop: 4, overflow: "hidden" },
  progressBarFill: { height: "100%", borderRadius: 2 },

  rxCard: { backgroundColor: "#0F172A", borderRadius: 14, padding: 12, borderWidth: 1, borderColor: "#0D9488", marginBottom: 14 },
  rxHeader: { color: "#2DD4BF", fontSize: 10, fontWeight: "bold", textTransform: "uppercase" },
  rxCountdown: { color: "#F59E0B", fontSize: 10, fontWeight: "bold" },
  rxDrugName: { color: "#FFFFFF", fontSize: 12, fontWeight: "bold", marginTop: 4 },
  audioBtn: { marginTop: 8, backgroundColor: "rgba(13, 148, 136, 0.15)", padding: 8, borderRadius: 8, flexDirection: "row", alignItems: "center", gap: 6, borderWidth: 1, borderColor: "#0D9488" },
  audioBtnIcon: { fontSize: 16 },
  audioBtnText: { color: "#2DD4BF", fontSize: 10, fontWeight: "bold" },

  footerContainer: { marginTop: 10, paddingTop: 16, borderTopWidth: 1, borderTopColor: "#1E293B", alignItems: "center" },
  footerTitle: { color: "#FFFFFF", fontSize: 11, fontWeight: "bold" },
  footerSub: { color: "#64748B", fontSize: 9, marginTop: 2 },
  footerLinksRow: { flexDirection: "row", gap: 6, alignItems: "center", marginTop: 8 },
  footerLink: { color: "#94A3B8", fontSize: 9 },
  footerBullet: { color: "#334155", fontSize: 9 },
  footerStatusRow: { flexDirection: "row", alignItems: "center", gap: 6, marginTop: 8 },
  pulseDot: { width: 6, height: 6, borderRadius: 3, backgroundColor: "#10B981" },
  footerStatus: { color: "#10B981", fontSize: 9, fontWeight: "600" },

  // Action Regimen Styles
  actionRegimenCard: { backgroundColor: "#0C1B2A", padding: 14, borderRadius: 16, borderWidth: 1, borderColor: "#0284C7", marginBottom: 14, gap: 6 },
  badgeActionHeader: { color: "#38BDF8", fontSize: 9, fontWeight: "700", backgroundColor: "rgba(56, 189, 248, 0.15)", paddingHorizontal: 8, paddingVertical: 2, borderRadius: 6 },
  regimenMainTask: { color: "#F0F9FF", fontSize: 14, fontWeight: "800", marginTop: 2 },
  regimenSub: { color: "#7DD3FC", fontSize: 10, marginBottom: 4 },
  adherenceList: { gap: 6 },
  adherenceItem: { backgroundColor: "#0F172A", padding: 8, borderRadius: 8, borderWidth: 1, borderColor: "#1E293B", gap: 3 },
  adherenceTaskName: { color: "#FFFFFF", fontSize: 11, fontWeight: "700" },
  adherenceBadge: { fontSize: 8, fontWeight: "700", paddingHorizontal: 5, paddingVertical: 1, borderRadius: 4 },
  adherenceBadgeTaken: { color: "#10B981", backgroundColor: "rgba(16, 185, 129, 0.15)" },
  adherenceBadgeSkipped: { color: "#EF4444", backgroundColor: "rgba(239, 68, 68, 0.15)" },
  adherenceBadgePending: { color: "#F59E0B", backgroundColor: "rgba(245, 158, 11, 0.15)" },
  adherenceTaskDetail: { color: "#94A3B8", fontSize: 10 },
  adherenceBtnRow: { flexDirection: "row", gap: 4, marginTop: 3 },
  adherenceBtn: { flex: 1, paddingVertical: 5, borderRadius: 5, backgroundColor: "#1E293B", alignItems: "center" },
  adherenceBtnActive: { backgroundColor: "#0D9488" },
  adherenceBtnText: { color: "#94A3B8", fontSize: 9, fontWeight: "700" },
  adherenceBtnTextActive: { color: "#FFFFFF" },
});
