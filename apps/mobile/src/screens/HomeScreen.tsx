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

  return (
    <ScrollView style={styles.container}>
      {/* Header Profile Card */}
      <View style={styles.profileCard}>
        <View style={styles.rowBetween}>
          <View>
            <Text style={styles.greeting}>Marhaban / Welcome</Text>
            <Text style={styles.patientName}>{profile.name}</Text>
            <Text style={styles.mrnText}>MRN: {profile.mrn} • Age: {profile.age}</Text>
          </View>
          <View style={styles.badgeMizaj}>
            <Text style={styles.mizajText}>{profile.mizaj}</Text>
          </View>
        </View>

        <View style={styles.organAxisBadge}>
          <Text style={styles.axisLabel}>PRIMARY CLINICAL AXIS:</Text>
          <Text style={styles.axisValue}>Kabid-Mida (Hepato-Gastric Cross-talk)</Text>
        </View>
      </View>

      {/* Quick Action Matrix */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Essential Clinical Services</Text>
        <View style={styles.grid}>
          <TouchableOpacity style={styles.gridItem} onPress={() => onNavigate("prescriptions")}>
            <Text style={styles.gridEmoji}>💊</Text>
            <Text style={styles.gridText}>E-Prescriptions</Text>
            <Text style={styles.gridSub}>Audio Posology</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.gridItem} onPress={() => onNavigate("lifestyle")}>
            <Text style={styles.gridEmoji}>🌿</Text>
            <Text style={styles.gridText}>Asbab-e-Sittah</Text>
            <Text style={styles.gridSub}>6 Life Essentials</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.gridItem} onPress={() => onNavigate("appointments")}>
            <Text style={styles.gridEmoji}>🩺</Text>
            <Text style={styles.gridText}>Book Consult</Text>
            <Text style={styles.gridSub}>Video / Matab OPD</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.gridItem} onPress={() => onNavigate("clinician")}>
            <Text style={styles.gridEmoji}>🛡️</Text>
            <Text style={styles.gridText}>Doctor Mode</Text>
            <Text style={styles.gridSub}>Clinician Triage</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Active Phase of Treatment */}
      <View style={styles.regimenCard}>
        <Text style={styles.cardHeader}>Active Afaal Treatment Phase</Text>
        <View style={styles.phaseIndicator}>
          <Text style={styles.phaseStepActive}>Stage 1: Tanqiya (Humoral Detox)</Text>
          <Text style={styles.phaseStatus}>In Progress (Day 9 of 14)</Text>
        </View>
        <Text style={styles.regimenDesc}>
          Munzij-e-Balgham administered with Arq-e-Badiyan. Follow strict nocturnal fasting and hot water infusion.
        </Text>
      </View>

      {/* Vernacular Voice Alert Banner */}
      <TouchableOpacity style={styles.voiceBanner} onPress={() => onNavigate("prescriptions")}>
        <Text style={styles.voiceIcon}>🔊</Text>
        <View style={styles.voiceContent}>
          <Text style={styles.voiceTitle}>Sunein Apni Dawa Ki Khorak</Text>
          <Text style={styles.voiceSub}>Audio instructions available in Urdu, Hindi, and English</Text>
        </View>
      </TouchableOpacity>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0A0F1D", padding: 16 },
  profileCard: { backgroundColor: "#1E293B", borderRadius: 16, padding: 18, borderWidth: 1, borderColor: "#334155", marginBottom: 16 },
  rowBetween: { flexDirection: "row", justifyContent: "space-between", alignItems: "flex-start" },
  greeting: { color: "#2DD4BF", fontSize: 12, fontWeight: "600", textTransform: "uppercase" },
  patientName: { color: "#FFFFFF", fontSize: 22, fontWeight: "bold", marginTop: 2 },
  mrnText: { color: "#94A3B8", fontSize: 12, marginTop: 2 },
  badgeMizaj: { backgroundColor: "rgba(13, 148, 136, 0.2)", paddingHorizontal: 10, paddingVertical: 5, borderRadius: 20, borderWidth: 1, borderColor: "#0D9488" },
  mizajText: { color: "#2DD4BF", fontSize: 11, fontWeight: "bold" },
  organAxisBadge: { marginTop: 14, backgroundColor: "#0F172A", padding: 10, borderRadius: 10, borderWidth: 1, borderColor: "#1E293B" },
  axisLabel: { color: "#64748B", fontSize: 9, fontWeight: "bold", letterSpacing: 0.5 },
  axisValue: { color: "#F8FAFC", fontSize: 13, fontWeight: "600", marginTop: 2 },
  section: { marginBottom: 16 },
  sectionTitle: { color: "#F1F5F9", fontSize: 16, fontWeight: "bold", marginBottom: 12 },
  grid: { flexDirection: "row", flexWrap: "wrap", justifyContent: "space-between", gap: 10 },
  gridItem: { backgroundColor: "#1E293B", width: "48%", padding: 14, borderRadius: 14, borderWidth: 1, borderColor: "#334155" },
  gridEmoji: { fontSize: 24, marginBottom: 6 },
  gridText: { color: "#FFFFFF", fontSize: 14, fontWeight: "bold" },
  gridSub: { color: "#94A3B8", fontSize: 11, marginTop: 2 },
  regimenCard: { backgroundColor: "#0F172A", borderRadius: 14, padding: 16, borderWidth: 1, borderColor: "#1E293B", marginBottom: 16 },
  cardHeader: { color: "#2DD4BF", fontSize: 12, fontWeight: "bold", textTransform: "uppercase", marginBottom: 8 },
  phaseIndicator: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 6 },
  phaseStepActive: { color: "#FFFFFF", fontSize: 14, fontWeight: "bold" },
  phaseStatus: { color: "#EAB308", fontSize: 11, fontWeight: "600" },
  regimenDesc: { color: "#94A3B8", fontSize: 12, lineHeight: 18 },
  voiceBanner: { backgroundColor: "rgba(13, 148, 136, 0.15)", borderWidth: 1, borderColor: "#0D9488", borderRadius: 14, padding: 14, flexDirection: "row", alignItems: "center", marginBottom: 24 },
  voiceIcon: { fontSize: 28, marginRight: 12 },
  voiceContent: { flex: 1 },
  voiceTitle: { color: "#2DD4BF", fontSize: 14, fontWeight: "bold" },
  voiceSub: { color: "#CBD5E1", fontSize: 11, marginTop: 2 }
});
