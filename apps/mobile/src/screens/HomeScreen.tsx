import React, { useState } from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from "react-native";
import { PatientProfile } from "../types";

export const HomeScreen: React.FC<{ onNavigate: (screen: string) => void }> = ({ onNavigate }) => {
  const [profile] = useState<PatientProfile>({
    mrn: "ZAY-2026-8819",
    name: "Mohammad Tariq",
    age: 44,
    gender: "Male",
    mizaj: "Balghami (Phlegmatic)",
    dominantOrganAxis: "Kabid-Mida",
    activeConditions: ["Su-e-Mizaj Barid Balghami", "Metabolic Dysregulation", "Dyspeptic Stasis"]
  });

  const [vitals] = useState({
    bp: "124/82",
    pulse: "72 bpm",
    spo2: "98%",
    glucose: "98 mg/dL"
  });

  const asbabFactors = [
    { name: "Hawa", label: "Air & Breath", score: 88, color: "#2DD4BF" },
    { name: "Makul", label: "Diet & Anupan", score: 82, color: "#10B981" },
    { name: "Harkat", label: "Physical Activity", score: 76, color: "#3B82F6" },
    { name: "Naum", label: "Sleep Architecture", score: 85, color: "#8B5CF6" },
    { name: "Istifragh", label: "Detox & Evacuation", score: 90, color: "#F59E0B" },
    { name: "Nafsani", label: "Mental Equilibrium", score: 83, color: "#EC4899" }
  ];

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.scrollContent}>
      {/* Header Profile Card */}
      <View style={styles.profileCard}>
        <View style={styles.rowBetween}>
          <View>
            <Text style={styles.greeting}>Marhaban / Welcome</Text>
            <Text style={styles.patientName}>{profile.name}</Text>
            <Text style={styles.mrnText}>MRN: {profile.mrn} • Age: {profile.age} • Blood Group: B+</Text>
          </View>
          <View style={styles.badgeMizaj}>
            <Text style={styles.mizajText}>{profile.mizaj}</Text>
          </View>
        </View>

        <View style={styles.organAxisBadge}>
          <Text style={styles.axisLabel}>PRIMARY CLINICAL AXIS & TARGET AFFINITY:</Text>
          <Text style={styles.axisValue}>Kabid-Mida (Hepato-Gastric Cross-talk Axis)</Text>
        </View>
      </View>

      {/* Bluetooth Hardware Sensor Sync HUD */}
      <View style={styles.hwSyncCard}>
        <View style={styles.rowBetween}>
          <View style={styles.rowCenter}>
            <View style={styles.pulseDot} />
            <Text style={styles.hwSyncTitle}>Diagnostic Sensor Mesh Live</Text>
          </View>
          <Text style={styles.hwSyncStatus}>3 NODES CONNECTED</Text>
        </View>
        
        <View style={styles.hwGrid}>
          <View style={styles.hwItem}>
            <Text style={styles.hwIcon}>💍</Text>
            <Text style={styles.hwName}>Nabz Ring</Text>
            <Text style={styles.hwMetric}>100Hz • 72 BPM</Text>
          </View>
          <View style={styles.hwItem}>
            <Text style={styles.hwIcon}>📡</Text>
            <Text style={styles.hwName}>BLE Hub</Text>
            <Text style={styles.hwMetric}>SpO2 98% • Active</Text>
          </View>
          <View style={styles.hwItem}>
            <Text style={styles.hwIcon}>💊</Text>
            <Text style={styles.hwName}>Smart Box</Text>
            <Text style={styles.hwMetric}>Synced • Dosed</Text>
          </View>
        </View>
      </View>

      {/* Asbab-e-Sittah (6 Life Essentials) & Meezan-e-Sehat 0-100 Score */}
      <View style={styles.card}>
        <View style={styles.rowBetween}>
          <div>
            <Text style={styles.cardEyebrow}>Asbab-e-Sittah الضرورية</Text>
            <Text style={styles.cardTitle}>Meezan-e-Sehat Equilibrium</Text>
          </div>
          <View style={styles.scoreCircle}>
            <Text style={styles.scoreNumber}>84</Text>
            <Text style={styles.scoreSub}>/ 100</Text>
          </View>
        </View>

        <Text style={styles.scoreNote}>
          Optimal Humoral Balance: Balghami-Damawi harmony maintained. Sleep and diet rhythm currently optimal.
        </Text>

        <View style={styles.asbabGrid}>
          {asbabFactors.map((f) => (
            <View key={f.name} style={styles.asbabItem}>
              <View style={styles.rowBetween}>
                <Text style={styles.asbabName}>{f.name}</Text>
                <Text style={[styles.asbabScore, { color: f.color }]}>{f.score}%</Text>
              </View>
              <Text style={styles.asbabLabel}>{f.label}</Text>
              <View style={styles.progressBarBg}>
                <View style={[styles.progressBarFill, { width: `${f.score}%`, backgroundColor: f.color }]} />
              </View>
            </View>
          ))}
        </View>
      </View>

      {/* Next Prescription Dose Countdown & Vernacular Audio Player */}
      <View style={styles.rxCard}>
        <View style={styles.rowBetween}>
          <Text style={styles.rxHeader}>Next Scheduled Regimen</Text>
          <Text style={styles.rxCountdown}>Due in 38 mins</Text>
        </View>
        
        <View style={styles.rxDetails}>
          <Text style={styles.rxDrugName}>Qurs-e-Mafasil (2 tablets) + Arq-e-Badiyan</Text>
          <Text style={styles.rxDirection}>Post-prandial intake with warm fennel distillate vehicle (Anupan).</Text>
        </View>

        <TouchableOpacity style={styles.audioActionBtn} onPress={() => onNavigate("prescriptions")}>
          <Text style={styles.audioActionIcon}>🔊</Text>
          <View style={styles.audioActionTextGroup}>
            <Text style={styles.audioActionTitle}>Sunein Apni Dawa Ki Khorak (Audio Posology)</Text>
            <Text style={styles.audioActionSub}>Tap to play instructions in Urdu, Hindi, or English</Text>
          </View>
          <Text style={styles.audioActionArrow}>→</Text>
        </TouchableOpacity>
      </View>

      {/* Upcoming Teleconsultation Banner */}
      <View style={styles.teleCard}>
        <View style={styles.rowBetween}>
          <View>
            <Text style={styles.teleBadge}>UPCOMING VIDEO CLINICAL ENCOUNTER</Text>
            <Text style={styles.teleDoctor}>Dr. Mohammad Tariq, MD (Unani)</Text>
            <Text style={styles.teleSpecialty}>Senior Tabeeb • Jamia Hamdard AUTC</Text>
            <Text style={styles.teleTime}>Today, 5:00 PM IST (Encounter ENC-2026-0814)</Text>
          </View>
          <TouchableOpacity style={styles.teleJoinBtn} onPress={() => onNavigate("teleconsult")}>
            <Text style={styles.teleJoinText}>Join Call</Text>
            <Text style={styles.teleJoinSub}>WebRTC 4K</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Active Phase of Treatment */}
      <View style={styles.regimenCard}>
        <View style={styles.rowBetween}>
          <Text style={styles.cardHeader}>Active Afaal Treatment Phase</Text>
          <Text style={styles.phaseStatus}>Stage 1 of 4: In Progress</Text>
        </View>
        <View style={styles.phaseIndicator}>
          <Text style={styles.phaseStepActive}>Tanqiya (Humoral Detoxification)</Text>
          <Text style={styles.phaseDays}>Day 9 of 14</Text>
        </View>
        <Text style={styles.regimenDesc}>
          Munzij-e-Balgham administered with warm Arq-e-Badiyan. Follow strict nocturnal fasting and avoid heavy cold dairy products (*Mukhrij-e-Rutubat* protocol).
        </Text>
      </View>

      {/* Real-Time Vitals Snapshot */}
      <View style={styles.vitalsSection}>
        <Text style={styles.sectionTitle}>Current Clinical Vitals</Text>
        <View style={styles.vitalsGrid}>
          <View style={styles.vitalBox}>
            <Text style={styles.vitalLabel}>Blood Pressure</Text>
            <Text style={styles.vitalValue}>{vitals.bp}</Text>
            <Text style={styles.vitalUnit}>mmHg</Text>
          </View>
          <View style={styles.vitalBox}>
            <Text style={styles.vitalLabel}>Pulse Rate</Text>
            <Text style={styles.vitalValue}>{vitals.pulse}</Text>
            <Text style={styles.vitalUnit}>Bat'ee (Slow)</Text>
          </View>
          <View style={styles.vitalBox}>
            <Text style={styles.vitalLabel}>SpO2</Text>
            <Text style={styles.vitalValue}>{vitals.spo2}</Text>
            <Text style={styles.vitalUnit}>Pulse Oximetry</Text>
          </View>
          <View style={styles.vitalBox}>
            <Text style={styles.vitalLabel}>Blood Glucose</Text>
            <Text style={styles.vitalValue}>{vitals.glucose}</Text>
            <Text style={styles.vitalUnit}>Fasting</Text>
          </View>
        </View>
      </View>

      {/* Quick Action Matrix */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Essential Clinical Services</Text>
        <View style={styles.grid}>
          <TouchableOpacity style={styles.gridItem} onPress={() => onNavigate("prescriptions")}>
            <Text style={styles.gridEmoji}>💊</Text>
            <Text style={styles.gridText}>E-Prescriptions</Text>
            <Text style={styles.gridSub}>Posology & Refills</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.gridItem} onPress={() => onNavigate("lifestyle")}>
            <Text style={styles.gridEmoji}>🌿</Text>
            <Text style={styles.gridText}>Asbab Tracker</Text>
            <Text style={styles.gridSub}>6 Life Precepts</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.gridItem} onPress={() => onNavigate("appointments")}>
            <Text style={styles.gridEmoji}>🩺</Text>
            <Text style={styles.gridText}>Appointments</Text>
            <Text style={styles.gridSub}>Queue & OPD Slots</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.gridItem} onPress={() => onNavigate("clinician")}>
            <Text style={styles.gridEmoji}>🛡️</Text>
            <Text style={styles.gridText}>Doctor Mode</Text>
            <Text style={styles.gridSub}>Clinician Triage</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0A0F1D" },
  scrollContent: { padding: 16, paddingBottom: 40 },
  profileCard: { backgroundColor: "#1E293B", borderRadius: 18, padding: 18, borderWidth: 1, borderColor: "#334155", marginBottom: 14 },
  rowBetween: { flexDirection: "row", justifyContent: "space-between", alignItems: "flex-start" },
  rowCenter: { flexDirection: "row", alignItems: "center" },
  greeting: { color: "#2DD4BF", fontSize: 11, fontWeight: "700", textTransform: "uppercase", letterSpacing: 0.5 },
  patientName: { color: "#FFFFFF", fontSize: 22, fontWeight: "bold", marginTop: 2 },
  mrnText: { color: "#94A3B8", fontSize: 11, marginTop: 3 },
  badgeMizaj: { backgroundColor: "rgba(13, 148, 136, 0.2)", paddingHorizontal: 10, paddingVertical: 5, borderRadius: 20, borderWidth: 1, borderColor: "#0D9488" },
  mizajText: { color: "#2DD4BF", fontSize: 11, fontWeight: "bold" },
  organAxisBadge: { marginTop: 14, backgroundColor: "#0F172A", padding: 10, borderRadius: 10, borderWidth: 1, borderColor: "#1E293B" },
  axisLabel: { color: "#64748B", fontSize: 9, fontWeight: "bold", letterSpacing: 0.5 },
  axisValue: { color: "#F8FAFC", fontSize: 13, fontWeight: "600", marginTop: 2 },
  
  hwSyncCard: { backgroundColor: "#0F172A", borderRadius: 14, padding: 12, borderWidth: 1, borderColor: "#1E293B", marginBottom: 14 },
  pulseDot: { width: 8, height: 8, borderRadius: 4, backgroundColor: "#10B981", marginRight: 6 },
  hwSyncTitle: { color: "#2DD4BF", fontSize: 11, fontWeight: "bold" },
  hwSyncStatus: { color: "#10B981", fontSize: 9, fontWeight: "bold", fontFamily: "monospace" },
  hwGrid: { flexDirection: "row", justifyContent: "space-between", gap: 8, marginTop: 10 },
  hwItem: { backgroundColor: "#1E293B", flex: 1, padding: 8, borderRadius: 8, alignItems: "center", borderWidth: 1, borderColor: "#334155" },
  hwIcon: { fontSize: 16 },
  hwName: { color: "#FFFFFF", fontSize: 10, fontWeight: "bold", marginTop: 2 },
  hwMetric: { color: "#94A3B8", fontSize: 8, marginTop: 1 },

  card: { backgroundColor: "#1E293B", borderRadius: 16, padding: 16, borderWidth: 1, borderColor: "#334155", marginBottom: 14 },
  cardEyebrow: { color: "#2DD4BF", fontSize: 10, fontWeight: "bold", textTransform: "uppercase" },
  cardTitle: { color: "#FFFFFF", fontSize: 16, fontWeight: "bold", marginTop: 2 },
  scoreCircle: { width: 52, height: 52, borderRadius: 26, backgroundColor: "rgba(13, 148, 136, 0.2)", borderWidth: 2, borderColor: "#2DD4BF", alignItems: "center", justifyContent: "center" },
  scoreNumber: { color: "#FFFFFF", fontSize: 18, fontWeight: "bold" },
  scoreSub: { color: "#2DD4BF", fontSize: 8, fontWeight: "bold", marginTop: -2 },
  scoreNote: { color: "#94A3B8", fontSize: 11, lineHeight: 16, marginTop: 8, marginBottom: 12 },
  asbabGrid: { flexDirection: "row", flexWrap: "wrap", justifyContent: "space-between", gap: 8 },
  asbabItem: { width: "48%", backgroundColor: "#0F172A", padding: 10, borderRadius: 10, borderWidth: 1, borderColor: "#1E293B" },
  asbabName: { color: "#FFFFFF", fontSize: 11, fontWeight: "bold" },
  asbabScore: { fontSize: 11, fontWeight: "bold" },
  asbabLabel: { color: "#64748B", fontSize: 9, marginTop: 1 },
  progressBarBg: { height: 4, backgroundColor: "#1E293B", borderRadius: 2, marginTop: 6, overflow: "hidden" },
  progressBarFill: { height: "100%", borderRadius: 2 },

  rxCard: { backgroundColor: "#0F172A", borderRadius: 16, padding: 16, borderWidth: 1, borderColor: "#0D9488", marginBottom: 14 },
  rxHeader: { color: "#2DD4BF", fontSize: 11, fontWeight: "bold", textTransform: "uppercase" },
  rxCountdown: { color: "#F59E0B", fontSize: 11, fontWeight: "bold" },
  rxDetails: { marginTop: 8, marginBottom: 12 },
  rxDrugName: { color: "#FFFFFF", fontSize: 14, fontWeight: "bold" },
  rxDirection: { color: "#94A3B8", fontSize: 11, marginTop: 2, lineHeight: 16 },
  audioActionBtn: { backgroundColor: "rgba(13, 148, 136, 0.15)", borderWidth: 1, borderColor: "#0D9488", borderRadius: 12, padding: 12, flexDirection: "row", alignItems: "center" },
  audioActionIcon: { fontSize: 24, marginRight: 10 },
  audioActionTextGroup: { flex: 1 },
  audioActionTitle: { color: "#2DD4BF", fontSize: 12, fontWeight: "bold" },
  audioActionSub: { color: "#94A3B8", fontSize: 10, marginTop: 2 },
  audioActionArrow: { color: "#2DD4BF", fontSize: 16, fontWeight: "bold" },

  teleCard: { backgroundColor: "#1E293B", borderRadius: 16, padding: 16, borderWidth: 1, borderColor: "#3B82F6", marginBottom: 14 },
  teleBadge: { color: "#3B82F6", fontSize: 9, fontWeight: "bold", letterSpacing: 0.5 },
  teleDoctor: { color: "#FFFFFF", fontSize: 14, fontWeight: "bold", marginTop: 2 },
  teleSpecialty: { color: "#94A3B8", fontSize: 11 },
  teleTime: { color: "#E2E8F0", fontSize: 11, fontWeight: "600", marginTop: 4 },
  teleJoinBtn: { backgroundColor: "#2563EB", paddingHorizontal: 16, paddingVertical: 10, borderRadius: 12, alignItems: "center", justifyContent: "center" },
  teleJoinText: { color: "#FFFFFF", fontSize: 12, fontWeight: "bold" },
  teleJoinSub: { color: "#93C5FD", fontSize: 8, fontWeight: "bold" },

  regimenCard: { backgroundColor: "#0F172A", borderRadius: 14, padding: 16, borderWidth: 1, borderColor: "#1E293B", marginBottom: 14 },
  cardHeader: { color: "#2DD4BF", fontSize: 11, fontWeight: "bold", textTransform: "uppercase" },
  phaseStatus: { color: "#F59E0B", fontSize: 10, fontWeight: "600" },
  phaseIndicator: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginTop: 6, marginBottom: 6 },
  phaseStepActive: { color: "#FFFFFF", fontSize: 14, fontWeight: "bold" },
  phaseDays: { color: "#10B981", fontSize: 11, fontWeight: "bold" },
  regimenDesc: { color: "#94A3B8", fontSize: 11, lineHeight: 16 },

  vitalsSection: { marginBottom: 14 },
  sectionTitle: { color: "#F1F5F9", fontSize: 15, fontWeight: "bold", marginBottom: 10 },
  vitalsGrid: { flexDirection: "row", flexWrap: "wrap", justifyContent: "space-between", gap: 8 },
  vitalBox: { width: "48%", backgroundColor: "#1E293B", padding: 12, borderRadius: 12, borderWidth: 1, borderColor: "#334155" },
  vitalLabel: { color: "#64748B", fontSize: 10, fontWeight: "bold", textTransform: "uppercase" },
  vitalValue: { color: "#FFFFFF", fontSize: 16, fontWeight: "bold", marginTop: 2 },
  vitalUnit: { color: "#2DD4BF", fontSize: 9, marginTop: 1 },

  section: { marginBottom: 14 },
  grid: { flexDirection: "row", flexWrap: "wrap", justifyContent: "space-between", gap: 10 },
  gridItem: { backgroundColor: "#1E293B", width: "48%", padding: 14, borderRadius: 14, borderWidth: 1, borderColor: "#334155" },
  gridEmoji: { fontSize: 24, marginBottom: 6 },
  gridText: { color: "#FFFFFF", fontSize: 13, fontWeight: "bold" },
  gridSub: { color: "#94A3B8", fontSize: 10, marginTop: 2 }
});
