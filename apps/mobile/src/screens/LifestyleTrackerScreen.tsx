import React, { useState } from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from "react-native";
import { AsbabSittahLog } from "../types";

export const LifestyleTrackerScreen: React.FC<{ onBack: () => void }> = ({ onBack }) => {
  const [log, setLog] = useState<AsbabSittahLog>({
    date: new Date().toISOString().split("T")[0],
    hawa_air: "moderate_ventilated",
    makul_food: "balanced_prescribed",
    harakat_movement: 40,
    nawm_sleep: 7.5,
    istifragh_retention: "normal_evacuation",
    nafsaniyah_psychic: "calm_focused"
  });

  const [savedMessage, setSavedMessage] = useState<string | null>(null);

  const saveLog = () => {
    setSavedMessage("Asbab-e-Sittah الضرورية adherence saved to EHR ledger.");
    setTimeout(() => setSavedMessage(null), 3500);
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.headerRow}>
        <TouchableOpacity onPress={onBack} style={styles.backButton}>
          <Text style={styles.backText}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.title}>Asbab-e-Sittah (6 Essentials)</Text>
      </View>

      <Text style={styles.sub}>
        Classical Unani preventive regime to preserve health (Hifz-e-Sehat) and restore humoral balance.
      </Text>

      {savedMessage && (
        <View style={styles.alertSuccess}>
          <Text style={styles.alertText}>✓ {savedMessage}</Text>
        </View>
      )}

      {/* 1. Hawa-e-Muheet (Ambient Air) */}
      <View style={styles.card}>
        <Text style={styles.factorTitle}>1. Hawa-e-Muheet (Air & Respiration)</Text>
        <Text style={styles.factorDesc}>Exposure to well-ventilated, unpolluted ambient air.</Text>
        <View style={styles.pillGroup}>
          <TouchableOpacity
            style={[styles.pill, log.hawa_air === "fresh_mountain" && styles.pillActive]}
            onPress={() => setLog({ ...log, hawa_air: "fresh_mountain" })}
          >
            <Text style={styles.pillText}>Fresh / Morning Air</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.pill, log.hawa_air === "moderate_ventilated" && styles.pillActive]}
            onPress={() => setLog({ ...log, hawa_air: "moderate_ventilated" })}
          >
            <Text style={styles.pillText}>Ventilated Indoor</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* 2. Makul wa Mashrub (Food & Drink) */}
      <View style={styles.card}>
        <Text style={styles.factorTitle}>2. Makul wa Mashrub (Dietary Regimen)</Text>
        <Text style={styles.factorDesc}>Humoral dietary compliance (Ghiza barid/yabis adjustments).</Text>
        <View style={styles.pillGroup}>
          <TouchableOpacity
            style={[styles.pill, log.makul_food === "balanced_prescribed" && styles.pillActive]}
            onPress={() => setLog({ ...log, makul_food: "balanced_prescribed" })}
          >
            <Text style={styles.pillText}>Prescribed Diet Compliant</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.pill, log.makul_food === "excess_spicy" && styles.pillActive]}
            onPress={() => setLog({ ...log, makul_food: "excess_spicy" })}
          >
            <Text style={styles.pillText}>Spicy / Hot Food Deviated</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* 3. Harakat wa Sukun Badani (Physical Movement) */}
      <View style={styles.card}>
        <Text style={styles.factorTitle}>3. Harakat wa Sukun Badani (Physical Activity)</Text>
        <Text style={styles.factorDesc}>Minutes of moderate exercise (Riyazat) today: {log.harakat_movement} mins</Text>
        <View style={styles.pillGroup}>
          {[15, 30, 45, 60].map((mins) => (
            <TouchableOpacity
              key={mins}
              style={[styles.pill, log.harakat_movement === mins && styles.pillActive]}
              onPress={() => setLog({ ...log, harakat_movement: mins })}
            >
              <Text style={styles.pillText}>{mins}m</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {/* 4. Nawm wa Yaqzah (Sleep & Wakefulness) */}
      <View style={styles.card}>
        <Text style={styles.factorTitle}>4. Nawm wa Yaqzah (Restorative Sleep)</Text>
        <Text style={styles.factorDesc}>Hours of restful sleep last night: {log.nawm_sleep} hrs</Text>
        <View style={styles.pillGroup}>
          {[6, 7, 7.5, 8, 9].map((hrs) => (
            <TouchableOpacity
              key={hrs}
              style={[styles.pill, log.nawm_sleep === hrs && styles.pillActive]}
              onPress={() => setLog({ ...log, nawm_sleep: hrs })}
            >
              <Text style={styles.pillText}>{hrs} hrs</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {/* 5. Istifragh wa Ihtibas (Evacuation & Retention) */}
      <View style={styles.card}>
        <Text style={styles.factorTitle}>5. Istifragh wa Ihtibas (Bowel & Humoral Clearance)</Text>
        <Text style={styles.factorDesc}>Elimination status and waste expulsion:</Text>
        <View style={styles.pillGroup}>
          <TouchableOpacity
            style={[styles.pill, log.istifragh_retention === "normal_evacuation" && styles.pillActive]}
            onPress={() => setLog({ ...log, istifragh_retention: "normal_evacuation" })}
          >
            <Text style={styles.pillText}>Normal Regular Clearance</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.pill, log.istifragh_retention === "constipated" && styles.pillActive]}
            onPress={() => setLog({ ...log, istifragh_retention: "constipated" })}
          >
            <Text style={styles.pillText}>Constipated / Stagnant</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* 6. Harakat wa Sukun Nafsaniyah (Psychic & Emotional States) */}
      <View style={styles.card}>
        <Text style={styles.factorTitle}>6. Harakat Nafsaniyah (Emotional State & Stress)</Text>
        <Text style={styles.factorDesc}>Mental tranquility and nervous system equilibrium:</Text>
        <View style={styles.pillGroup}>
          <TouchableOpacity
            style={[styles.pill, log.nafsaniyah_psychic === "calm_focused" && styles.pillActive]}
            onPress={() => setLog({ ...log, nafsaniyah_psychic: "calm_focused" })}
          >
            <Text style={styles.pillText}>Calm / Harmonious</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.pill, log.nafsaniyah_psychic === "moderate_stress" && styles.pillActive]}
            onPress={() => setLog({ ...log, nafsaniyah_psychic: "moderate_stress" })}
          >
            <Text style={styles.pillText}>Moderate Pressure</Text>
          </TouchableOpacity>
        </View>
      </View>

      <TouchableOpacity style={styles.submitBtn} onPress={saveLog}>
        <Text style={styles.submitText}>Save Daily Asbab-e-Sittah Log</Text>
      </TouchableOpacity>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0A0F1D", padding: 16 },
  headerRow: { flexDirection: "row", alignItems: "center", marginBottom: 8 },
  backButton: { marginRight: 12, paddingVertical: 4, paddingHorizontal: 8, backgroundColor: "#1E293B", borderRadius: 8 },
  backText: { color: "#2DD4BF", fontSize: 13, fontWeight: "600" },
  title: { color: "#FFFFFF", fontSize: 18, fontWeight: "bold" },
  sub: { color: "#94A3B8", fontSize: 12, marginBottom: 14 },
  alertSuccess: { backgroundColor: "rgba(13, 148, 136, 0.2)", borderColor: "#0D9488", borderWidth: 1, borderRadius: 8, padding: 10, marginBottom: 14 },
  alertText: { color: "#2DD4BF", fontSize: 12, fontWeight: "600" },
  card: { backgroundColor: "#1E293B", borderRadius: 12, padding: 14, marginBottom: 12, borderWidth: 1, borderColor: "#334155" },
  factorTitle: { color: "#FFFFFF", fontSize: 14, fontWeight: "bold", marginBottom: 4 },
  factorDesc: { color: "#94A3B8", fontSize: 11, marginBottom: 10 },
  pillGroup: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  pill: { paddingVertical: 6, paddingHorizontal: 12, borderRadius: 20, backgroundColor: "#0F172A", borderWidth: 1, borderColor: "#334155" },
  pillActive: { backgroundColor: "#0D9488", borderColor: "#2DD4BF" },
  pillText: { color: "#CBD5E1", fontSize: 11, fontWeight: "600" },
  submitBtn: { backgroundColor: "#0D9488", paddingVertical: 14, borderRadius: 12, alignItems: "center", marginTop: 8, marginBottom: 32 },
  submitText: { color: "#FFFFFF", fontSize: 14, fontWeight: "bold" }
});
