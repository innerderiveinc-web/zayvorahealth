import React, { useState } from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from "react-native";
import { PrescriptionItem, Language } from "../types";
import { AudioPosologyPlayer } from "../components/AudioPosologyPlayer";

export const PrescriptionsScreen: React.FC<{ onBack: () => void }> = ({ onBack }) => {
  const [selectedLang, setSelectedLang] = useState<Language>("ur");
  const [playingId, setPlayingId] = useState<string | null>(null);

  const prescriptions: PrescriptionItem[] = [
    {
      id: "rx-01",
      formulation: "ManiVital Pro Formula",
      dosage: "5g (1 metric tsp)",
      frequency: "Twice daily after meals",
      duration: "30 Days",
      anupan: "With lukewarm cow milk or sweetened almond emulsion",
      audioGuideAvailable: true,
      audioPosologyText: {
        en: "Take one teaspoon twice daily after breakfast and dinner with lukewarm milk. Avoid cold drinks.",
        ur: "Ek chamach subah aur sham khane ke baad neem garam doodh ke sath lein. Thande mashroobat aur khatti cheezon se parhez karein.",
        hi: "एक चम्मच सुबह और शाम खाना खाने के बाद गुनगुने दूध के साथ लें। ठंडी चीजों और खट्टी चीजों से परहेज करें।"
      }
    },
    {
      id: "rx-02",
      formulation: "Safoof-e-Muzil-e-Balgham (Afaal Tanqiya)",
      dosage: "3g",
      frequency: "Every morning fasting",
      duration: "14 Days",
      anupan: "With Arq-e-Badiyan (Fennel distillate) 60ml",
      audioGuideAvailable: true,
      audioPosologyText: {
        en: "Take 3 grams early morning on an empty stomach with 60ml Arq-e-Badiyan.",
        ur: "Subah nahar munh teen gram safoof 60 ml araq-e-badiyan ke sath piyein.",
        hi: "सुबह खाली पेट तीन ग्राम चूर्ण साठ मिलीलीटर सौंफ के अर्क के साथ लें。"
      }
    }
  ];

  return (
    <ScrollView style={styles.container} contentContainerStyle={{ paddingBottom: 40 }}>
      <View style={styles.headerRow}>
        <TouchableOpacity onPress={onBack} style={styles.backButton}>
          <Text style={styles.backText}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.title}>Active Prescriptions</Text>
      </View>

      {/* Language Selector for Audio Guidance */}
      <View style={styles.langContainer}>
        <Text style={styles.langLabel}>Vernacular Audio Language:</Text>
        <View style={styles.langButtons}>
          <TouchableOpacity
            style={[styles.langBtn, selectedLang === "ur" && styles.langBtnActive]}
            onPress={() => setSelectedLang("ur")}
          >
            <Text style={[styles.langBtnText, selectedLang === "ur" && styles.langBtnTextActive]}>Urdu (Roman)</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.langBtn, selectedLang === "hi" && styles.langBtnActive]}
            onPress={() => setSelectedLang("hi")}
          >
            <Text style={[styles.langBtnText, selectedLang === "hi" && styles.langBtnTextActive]}>हिन्दी (Hindi)</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.langBtn, selectedLang === "en" && styles.langBtnActive]}
            onPress={() => setSelectedLang("en")}
          >
            <Text style={[styles.langBtnText, selectedLang === "en" && styles.langBtnTextActive]}>English</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Prescriptions List */}
      {prescriptions.map((rx) => (
        <View key={rx.id} style={styles.card}>
          <View style={styles.cardHeader}>
            <Text style={styles.formulationName}>{rx.formulation}</Text>
            <Text style={styles.statusVerified}>21 CFR Verified</Text>
          </View>
          <Text style={styles.dosageText}><strong>Posology:</strong> {rx.dosage} • {rx.frequency}</Text>
          <Text style={styles.anupanText}><strong>Vehicle (Anupan):</strong> {rx.anupan}</Text>
          <Text style={styles.durationText}><strong>Duration:</strong> {rx.duration}</Text>

          {/* Audio Player Widget */}
          <AudioPosologyPlayer
            prescriptionTitle={rx.formulation}
            transcripts={rx.audioPosologyText}
            durationSeconds={18}
          />

          {/* Order Refill Button */}
          <TouchableOpacity style={styles.refillBtn}>
            <Text style={styles.refillText}>Request Dispensary FEFO Refill</Text>
          </TouchableOpacity>
        </View>
      ))}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0A0F1D", padding: 16 },
  headerRow: { flexDirection: "row", alignItems: "center", marginBottom: 16 },
  backButton: { marginRight: 12, paddingVertical: 4, paddingHorizontal: 8, backgroundColor: "#1E293B", borderRadius: 8 },
  backText: { color: "#2DD4BF", fontSize: 13, fontWeight: "600" },
  title: { color: "#FFFFFF", fontSize: 20, fontWeight: "bold" },
  langContainer: { backgroundColor: "#1E293B", padding: 12, borderRadius: 12, marginBottom: 16 },
  langLabel: { color: "#94A3B8", fontSize: 11, marginBottom: 8 },
  langButtons: { flexDirection: "row", gap: 8 },
  langBtn: { flex: 1, paddingVertical: 8, alignItems: "center", borderRadius: 8, backgroundColor: "#0F172A", borderWidth: 1, borderColor: "#334155" },
  langBtnActive: { backgroundColor: "#0D9488", borderColor: "#2DD4BF" },
  langBtnText: { color: "#94A3B8", fontSize: 12, fontWeight: "600" },
  langBtnTextActive: { color: "#FFFFFF", fontWeight: "bold" },
  card: { backgroundColor: "#1E293B", borderRadius: 14, padding: 16, marginBottom: 14, borderWidth: 1, borderColor: "#334155" },
  cardHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 8 },
  formulationName: { color: "#FFFFFF", fontSize: 16, fontWeight: "bold", flex: 1 },
  statusVerified: { color: "#2DD4BF", fontSize: 10, backgroundColor: "rgba(13, 148, 136, 0.2)", paddingHorizontal: 6, paddingVertical: 2, borderRadius: 6, borderWidth: 1, borderColor: "#0D9488" },
  dosageText: { color: "#E2E8F0", fontSize: 13, marginBottom: 4 },
  anupanText: { color: "#CBD5E1", fontSize: 12, marginBottom: 4 },
  durationText: { color: "#94A3B8", fontSize: 12, marginBottom: 10 },
  audioBox: { backgroundColor: "#0F172A", padding: 12, borderRadius: 10, borderWidth: 1, borderColor: "#334155", marginBottom: 10 },
  audioMeta: { marginBottom: 8 },
  audioLangTitle: { color: "#2DD4BF", fontSize: 11, fontWeight: "bold" },
  audioTranscript: { color: "#F1F5F9", fontSize: 13, marginTop: 4, fontStyle: "italic", lineHeight: 18 },
  playBtn: { backgroundColor: "#0D9488", paddingVertical: 8, paddingHorizontal: 12, borderRadius: 8, alignItems: "center" },
  playBtnActive: { backgroundColor: "#EAB308" },
  playBtnText: { color: "#FFFFFF", fontSize: 12, fontWeight: "bold" },
  refillBtn: { backgroundColor: "transparent", borderWidth: 1, borderColor: "#0D9488", paddingVertical: 8, borderRadius: 8, alignItems: "center" },
  refillText: { color: "#2DD4BF", fontSize: 12, fontWeight: "600" }
});
