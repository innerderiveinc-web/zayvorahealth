import React, { useState } from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, TextInput } from "react-native";

export const ClinicianCompanionScreen: React.FC<{ onBack: () => void }> = ({ onBack }) => {
  const [lockedList, setLockedList] = useState<string[]>([]);
  const [signingId, setSigningId] = useState<string | null>(null);
  const [clinicianPin, setClinicianPin] = useState("");
  const [pinError, setPinError] = useState<string | null>(null);

  const pendingApprovals = [
    {
      id: "appr-01",
      patient: "Mohammad Tariq (MRN-8819)",
      mizaj: "Balghami (Cold & Moist)",
      regimen: "Tanqiya Protocol + ManiVital Pro + Arq-e-Badiyan",
      contraindicationsCheck: "PASSED (0 toxic elements, 0 Schedule E(1) unverified)",
      hakeemConfidence: "89% concordance",
    },
    {
      id: "appr-02",
      patient: "Zainab Fatima (MRN-9104)",
      mizaj: "Safrawi-Damawi (Biliary Heat)",
      regimen: "OvaSync + Sharbath-e-Buzoori Motadil",
      contraindicationsCheck: "PASSED (All botanicals UPI verified)",
      hakeemConfidence: "94% concordance",
    },
  ];

  const triggerSignModal = (id: string) => {
    setSigningId(id);
    setClinicianPin("");
    setPinError(null);
  };

  const verifyAndLock = () => {
    if (clinicianPin !== "2026") {
      setPinError("Invalid Clinician PIN. Please enter your 4-digit 21 CFR signature PIN (2026).");
      return;
    }
    if (signingId) {
      setLockedList([...lockedList, signingId]);
      setSigningId(null);
      setClinicianPin("");
    }
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
          Non-delegable clinician discretion barrier. Artificial intelligence cannot lock or dispatch prescriptions without your cryptographic signature.
        </Text>
      </View>

      {/* Signature Modal */}
      {signingId && (
        <View style={styles.modalOverlay}>
          <View style={styles.modalCard}>
            <Text style={styles.modalTitle}>🔒 21 CFR Part 11 Signature Confirmation</Text>
            <Text style={styles.modalSub}>
              By entering your cryptographic PIN, you certify that you have reviewed the clinical findings, verified contraindications, and take legal responsibility for this prescription.
            </Text>

            <View style={styles.pinBox}>
              <Text style={styles.pinLabel}>Enter Clinician Authorization PIN:</Text>
              <TextInput
                style={styles.pinInput}
                value={clinicianPin}
                onChangeText={setClinicianPin}
                placeholder="Enter 4-digit PIN (2026)"
                placeholderTextColor="#64748B"
                keyboardType="numeric"
                secureTextEntry
                maxLength={4}
              />
            </View>

            {pinError && <Text style={styles.errorText}>{pinError}</Text>}

            <View style={styles.modalButtons}>
              <TouchableOpacity style={styles.cancelBtn} onPress={() => setSigningId(null)}>
                <Text style={styles.cancelText}>Cancel</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.confirmBtn} onPress={verifyAndLock}>
                <Text style={styles.confirmText}>Sign & Lock Rx</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      )}

      <Text style={styles.sectionHeader}>Pending Clinical Approvals ({pendingApprovals.length - lockedList.length})</Text>

      {pendingApprovals.map((item) => {
        const isLocked = lockedList.includes(item.id);
        return (
          <View key={item.id} style={styles.card}>
            <View style={styles.cardHeader}>
              <Text style={styles.patientName}>{item.patient}</Text>
              <Text style={styles.badgeConfidence}>{item.hakeemConfidence}</Text>
            </View>
            <Text style={styles.metaRow}>Mizaj: {item.mizaj}</Text>
            <View style={styles.regimenBox}>
              <Text style={styles.regimenLabel}>Proposed Nuskha Regimen:</Text>
              <Text style={styles.regimenVal}>{item.regimen}</Text>
            </View>
            <Text style={styles.safetyText}>Safety Screening: {item.contraindicationsCheck}</Text>

            {isLocked ? (
              <View style={styles.lockedBanner}>
                <Text style={styles.lockedBannerText}>🔒 21 CFR Cryptographically Signed & Locked</Text>
                <Text style={styles.lockedSub}>Dispensary FEFO Allocation Queued • Merkle Leaf Generated</Text>
              </View>
            ) : (
              <TouchableOpacity style={styles.lockBtn} onPress={() => triggerSignModal(item.id)}>
                <Text style={styles.lockBtnText}>Review & Cryptographically Sign (PIN)</Text>
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
  cardHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  patientName: { color: "#FFFFFF", fontSize: 15, fontWeight: "bold", flex: 1 },
  badgeConfidence: { backgroundColor: "#0F172A", color: "#2DD4BF", fontSize: 10, fontWeight: "bold", paddingHorizontal: 6, paddingVertical: 2, borderRadius: 6 },
  metaRow: { color: "#2DD4BF", fontSize: 11, marginTop: 4 },
  regimenBox: { backgroundColor: "#0F172A", padding: 10, borderRadius: 8, marginTop: 8, marginBottom: 8 },
  regimenLabel: { color: "#64748B", fontSize: 10, fontWeight: "bold" },
  regimenVal: { color: "#F8FAFC", fontSize: 12, fontWeight: "600", marginTop: 2 },
  safetyText: { color: "#94A3B8", fontSize: 11, marginBottom: 12 },
  lockBtn: { backgroundColor: "#0D9488", paddingVertical: 12, borderRadius: 10, alignItems: "center" },
  lockBtnText: { color: "#FFFFFF", fontSize: 12, fontWeight: "bold" },
  lockedBanner: { backgroundColor: "rgba(13, 148, 136, 0.2)", borderWidth: 1, borderColor: "#0D9488", padding: 10, borderRadius: 10, alignItems: "center" },
  lockedBannerText: { color: "#2DD4BF", fontSize: 12, fontWeight: "bold" },
  lockedSub: { color: "#CBD5E1", fontSize: 10, marginTop: 2 },
  modalOverlay: { backgroundColor: "rgba(0,0,0,0.8)", borderRadius: 16, padding: 16, marginBottom: 16, borderWidth: 1, borderColor: "#0D9488" },
  modalCard: { spaceY: 10 },
  modalTitle: { color: "#2DD4BF", fontSize: 14, fontWeight: "bold", marginBottom: 6 },
  modalSub: { color: "#CBD5E1", fontSize: 11, lineHeight: 16, marginBottom: 12 },
  pinBox: { marginBottom: 10 },
  pinLabel: { color: "#94A3B8", fontSize: 11, marginBottom: 6 },
  pinInput: { backgroundColor: "#0F172A", color: "#FFFFFF", borderWidth: 1, borderColor: "#334155", borderRadius: 8, paddingHorizontal: 12, paddingVertical: 8, fontSize: 16, textAlign: "center", letterSpacing: 4 },
  errorText: { color: "#EF4444", fontSize: 11, marginBottom: 8 },
  modalButtons: { flexDirection: "row", gap: 10, marginTop: 6 },
  cancelBtn: { flex: 1, backgroundColor: "#334155", paddingVertical: 10, borderRadius: 8, alignItems: "center" },
  cancelText: { color: "#CBD5E1", fontSize: 12, fontWeight: "600" },
  confirmBtn: { flex: 2, backgroundColor: "#0D9488", paddingVertical: 10, borderRadius: 8, alignItems: "center" },
  confirmText: { color: "#FFFFFF", fontSize: 12, fontWeight: "bold" },
});
