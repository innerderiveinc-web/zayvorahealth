import React, { useState } from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from "react-native";

export const AppointmentsScreen: React.FC<{ onBack: () => void }> = ({ onBack }) => {
  const [selectedSlot, setSelectedSlot] = useState<string>("Tomorrow 10:30 AM");
  const [booked, setBooked] = useState(false);

  return (
    <ScrollView style={styles.container}>
      <View style={styles.headerRow}>
        <TouchableOpacity onPress={onBack} style={styles.backButton}>
          <Text style={styles.backText}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.title}>Integrative Consultation</Text>
      </View>

      <View style={styles.doctorCard}>
        <Text style={styles.doctorName}>Prof. Hakim Syed Mansoor Ahmad</Text>
        <Text style={styles.doctorRole}>Senior Tabeeb & Integrative Endocrinologist</Text>
        <Text style={styles.doctorAffil}>Jamia Hamdard • 26+ Yrs Clinical Experience</Text>
        <View style={styles.tagBadge}>
          <Text style={styles.tagText}>⭐ 4.9/5 (1,240 consultations)</Text>
        </View>
      </View>

      <Text style={styles.sectionTitle}>Select Consultation Format</Text>
      <View style={styles.formatRow}>
        <TouchableOpacity style={[styles.formatCard, styles.formatActive]}>
          <Text style={styles.formatEmoji}>📹</Text>
          <Text style={styles.formatTitle}>Tele-Video</Text>
          <Text style={styles.formatSub}>Encrypted WebRTC</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.formatCard}>
          <Text style={styles.formatEmoji}>🏥</Text>
          <Text style={styles.formatTitle}>In-Clinic Matab</Text>
          <Text style={styles.formatSub}>Pulse & Tongue Exam</Text>
        </TouchableOpacity>
      </View>

      <Text style={styles.sectionTitle}>Available Appointment Slots</Text>
      <View style={styles.slotsGrid}>
        {["Tomorrow 10:30 AM", "Tomorrow 02:00 PM", "Thursday 11:15 AM", "Thursday 04:30 PM"].map((slot) => (
          <TouchableOpacity
            key={slot}
            style={[styles.slotBtn, selectedSlot === slot && styles.slotBtnActive]}
            onPress={() => setSelectedSlot(slot)}
          >
            <Text style={[styles.slotText, selectedSlot === slot && styles.slotTextActive]}>{slot}</Text>
          </TouchableOpacity>
        ))}
      </View>

      {booked ? (
        <View style={styles.successBox}>
          <Text style={styles.successTitle}>Consultation Confirmed!</Text>
          <Text style={styles.successSub}>
            Appointment booked for {selectedSlot}. Telemedicine room link sent to your verified mobile number.
          </Text>
        </View>
      ) : (
        <TouchableOpacity style={styles.bookBtn} onPress={() => setBooked(true)}>
          <Text style={styles.bookBtnText}>Confirm Consultation ({selectedSlot})</Text>
        </TouchableOpacity>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0A0F1D", padding: 16 },
  headerRow: { flexDirection: "row", alignItems: "center", marginBottom: 16 },
  backButton: { marginRight: 12, paddingVertical: 4, paddingHorizontal: 8, backgroundColor: "#1E293B", borderRadius: 8 },
  backText: { color: "#2DD4BF", fontSize: 13, fontWeight: "600" },
  title: { color: "#FFFFFF", fontSize: 18, fontWeight: "bold" },
  doctorCard: { backgroundColor: "#1E293B", borderRadius: 14, padding: 16, marginBottom: 16, borderWidth: 1, borderColor: "#334155" },
  doctorName: { color: "#FFFFFF", fontSize: 16, fontWeight: "bold" },
  doctorRole: { color: "#2DD4BF", fontSize: 12, marginTop: 2 },
  doctorAffil: { color: "#94A3B8", fontSize: 11, marginTop: 2 },
  tagBadge: { marginTop: 10, alignSelf: "flex-start", backgroundColor: "#0F172A", paddingHorizontal: 8, paddingVertical: 4, borderRadius: 6 },
  tagText: { color: "#F8FAFC", fontSize: 11, fontWeight: "600" },
  sectionTitle: { color: "#FFFFFF", fontSize: 14, fontWeight: "bold", marginBottom: 10 },
  formatRow: { flexDirection: "row", gap: 10, marginBottom: 16 },
  formatCard: { flex: 1, backgroundColor: "#1E293B", borderRadius: 12, padding: 12, alignItems: "center", borderWidth: 1, borderColor: "#334155" },
  formatActive: { borderColor: "#2DD4BF", backgroundColor: "rgba(13, 148, 136, 0.1)" },
  formatEmoji: { fontSize: 24, marginBottom: 4 },
  formatTitle: { color: "#FFFFFF", fontSize: 13, fontWeight: "bold" },
  formatSub: { color: "#94A3B8", fontSize: 10 },
  slotsGrid: { flexDirection: "row", flexWrap: "wrap", gap: 8, marginBottom: 20 },
  slotBtn: { width: "48%", backgroundColor: "#1E293B", paddingVertical: 10, borderRadius: 8, alignItems: "center", borderWidth: 1, borderColor: "#334155" },
  slotBtnActive: { backgroundColor: "#0D9488", borderColor: "#2DD4BF" },
  slotText: { color: "#94A3B8", fontSize: 11, fontWeight: "600" },
  slotTextActive: { color: "#FFFFFF", fontWeight: "bold" },
  bookBtn: { backgroundColor: "#0D9488", paddingVertical: 14, borderRadius: 12, alignItems: "center", marginBottom: 24 },
  bookBtnText: { color: "#FFFFFF", fontSize: 14, fontWeight: "bold" },
  successBox: { backgroundColor: "rgba(13, 148, 136, 0.2)", borderWidth: 1, borderColor: "#0D9488", borderRadius: 12, padding: 16, alignItems: "center", marginBottom: 24 },
  successTitle: { color: "#2DD4BF", fontSize: 16, fontWeight: "bold" },
  successSub: { color: "#CBD5E1", fontSize: 12, textAlign: "center", marginTop: 6, lineHeight: 18 }
});
