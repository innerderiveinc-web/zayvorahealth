import React, { useState } from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from "react-native";

export const ClinicianCompanionScreen: React.FC<{ onBack: () => void }> = ({ onBack }) => {
  const [lockedList, setLockedList] = useState<string[]>([]);

  const pendingApprovals = [
    {
      id: "appr-01",
      patient: "Mohammad Tariq (MRN-8819)",
      mizaj: "Balghami",
      regimen: "Tanqiya Protocol + ManiVital Pro",
      contraindicationsCheck: "PASSED (0 toxic elements, 0 Schedule E(1) unverified)",
      hakeemConfidence: "89% concordance"
    },
    {
      id: "appr-02",
      patient: "Zainab Fatima (MRN-9104)",
      mizaj: "Safrawi-Damawi",
      regimen: "OvaSync + Sharbath-e-Buzoori Motadil",
      contraindicationsCheck: "PASSED",
      hakeemConfidence: "94% concordance"
    }
  ];

  const handleLock = (id: string) => {
    setLockedList([...lockedList, id]);
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.headerRow}>
        <TouchableOpacity onPress={onBack} style={styles.backButton}>
          <Text style={styles.backText}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.title}>Clinician Mobile Companion</Text>
      </View>

      <View style={styles.alertNotice}>
        <Text style={styles.alertNoticeTitle}>21 CFR Part 11 Electronic Signature Gate</Text>
        <Text style={styles.alertNoticeText}>
          Non-delegable clinician discretion barrier. AI cannot finalize prescriptions without your cryptographic lock.
        </Text>
      </View>

      <Text style={styles.sectionHeader}>Pending Clinical Sign-offs</Text>

      {pendingApprovals.map((item) => {
        const isLocked = lockedList.includes(item.id);
        return (
          <View key={item.id} style={styles.card}>
            <Text style={styles.patientName}>{item.patient}</Text>
            <Text style={styles.metaRow}>Mizaj: {item.mizaj} • AI Confidence: {item.hakeemConfidence}</Text>
            <View style={styles.regimenBox}>
              <Text style={styles.regimenLabel}>Proposed Nuskha Regimen:</Text>
              <Text style={styles.regimenVal}>{item.regimen}</Text>
            </View>
            <Text style={styles.safetyText}>Safety Gate: {item.contraindicationsCheck}</Text>

            {isLocked ? (
              <View style={styles.lockedBanner}>
                <Text style={styles.lockedBannerText}>🔒 21 CFR Cryptographically Signed & Locked</Text>
              </View>
            ) : (
              <TouchableOpacity style={styles.lockBtn} onPress={() => handleLock(item.id)}>
                <Text style={styles.lockBtnText}>Review & Sign E-Prescription (Lock)</Text>
              </TouchableOpacity>
            )}
          </View>
        );
      })}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0A0F1D", padding: 16 },
  headerRow: { flexDirection: "row", alignItems: "center", marginBottom: 16 },
  backButton: { marginRight: 12, paddingVertical: 4, paddingHorizontal: 8, backgroundColor: "#1E293B", borderRadius: 8 },
  backText: { color: "#2DD4BF", fontSize: 13, fontWeight: "600" },
  title: { color: "#FFFFFF", fontSize: 18, fontWeight: "bold" },
  alertNotice: { backgroundColor: "rgba(234, 179, 8, 0.15)", borderWidth: 1, borderColor: "#EAB308", borderRadius: 10, padding: 12, marginBottom: 16 },
  alertNoticeTitle: { color: "#FACC15", fontSize: 12, fontWeight: "bold" },
  alertNoticeText: { color: "#FEF08A", fontSize: 11, marginTop: 2, lineHeight: 16 },
  sectionHeader: { color: "#FFFFFF", fontSize: 14, fontWeight: "bold", marginBottom: 12 },
  card: { backgroundColor: "#1E293B", borderRadius: 14, padding: 16, marginBottom: 14, borderWidth: 1, borderColor: "#334155" },
  patientName: { color: "#FFFFFF", fontSize: 15, fontWeight: "bold" },
  metaRow: { color: "#2DD4BF", fontSize: 11, marginTop: 2 },
  regimenBox: { backgroundColor: "#0F172A", padding: 10, borderRadius: 8, marginTop: 8, marginBottom: 8 },
  regimenLabel: { color: "#64748B", fontSize: 10, fontWeight: "bold" },
  regimenVal: { color: "#F8FAFC", fontSize: 12, fontWeight: "600", marginTop: 2 },
  safetyText: { color: "#94A3B8", fontSize: 11, marginBottom: 12 },
  lockBtn: { backgroundColor: "#0D9488", paddingVertical: 10, borderRadius: 8, alignItems: "center" },
  lockBtnText: { color: "#FFFFFF", fontSize: 12, fontWeight: "bold" },
  lockedBanner: { backgroundColor: "rgba(13, 148, 136, 0.2)", borderWidth: 1, borderColor: "#0D9488", paddingVertical: 8, borderRadius: 8, alignItems: "center" },
  lockedBannerText: { color: "#2DD4BF", fontSize: 12, fontWeight: "bold" }
});
