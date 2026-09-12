import React, { useState } from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from "react-native";
import { AsbabSittahLog } from "../types";
import { OfflineStorageService } from "../services/OfflineStorageService";

export const LifestyleTrackerScreen: React.FC<{ onBack: () => void }> = ({ onBack }) => {
  const [log, setLog] = useState<AsbabSittahLog>({
    date: new Date().toISOString().split("T")[0],
    hawa_air: "moderate_ventilated",
    makul_food: "balanced_prescribed",
    harakat_movement: 40,
    nawm_sleep: 7.5,
    istifragh_retention: "normal_evacuation",
    nafsaniyah_psychic: "calm_focused",
  });

  const [savedMessage, setSavedMessage] = useState<string | null>(null);

  // Dynamic Meezan-e-Sehat (Health Equilibrium Index 0 - 100)
  const calculateMeezanScore = () => {
    let score = 0;
    // 1. Hawa (Max 16)
    score += log.hawa_air === "fresh_mountain" ? 16 : 12;
    // 2. Makul (Max 18)
    score += log.makul_food === "balanced_prescribed" ? 18 : 8;
    // 3. Harakat (Max 16)
    if (log.harakat_movement >= 45) score += 16;
    else if (log.harakat_movement >= 30) score += 13;
    else score += 9;
    // 4. Nawm (Max 18)
    if (log.nawm_sleep >= 7 && log.nawm_sleep <= 8.5) score += 18;
    else if (log.nawm_sleep >= 6) score += 12;
    else score += 8;
    // 5. Istifragh (Max 16)
    score += log.istifragh_retention === "normal_evacuation" ? 16 : 6;
    // 6. Nafsaniyah (Max 16)
    score += log.nafsaniyah_psychic === "calm_focused" ? 16 : 9;

    return score;
  };

  const meezanScore = calculateMeezanScore();

  const saveLog = async () => {
    await OfflineStorageService.enqueueMutation("asbab_sittah", "PAT-774901", {
      ...log,
      meezan_score: meezanScore,
    });
    setSavedMessage(`Meezan-e-Sehat Score: ${meezanScore}/100. Saved to local queue & synchronized with EHR ledger.`);
    setTimeout(() => setSavedMessage(null), 4000);
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
        Classical Unani preventive regime to preserve health (Hifz-e-Sehat) and maintain humoral equilibrium.
      </Text>

      {/* Meezan-e-Sehat Live Score Gauge */}
      <View style={styles.scoreCard}>
        <View style={styles.scoreRow}>
          <div>
            <Text style={styles.scoreLabel}>Meezan-e-Sehat (Equilibrium Index):</Text>
            <Text style={styles.scoreDesc}>
              {meezanScore >= 85 ? "Optimal Humoral Equilibrium (Motadil)" : "Moderate Dyscrasia Risk (Deviation)"}
            </Text>
          </div>
          <View style={[styles.scoreBadge, meezanScore >= 85 ? styles.badgeGreen : styles.badgeYellow]}>
            <Text style={styles.scoreVal}>{meezanScore}</Text>
            <Text style={styles.scoreOutOf}>/100</Text>
          </View>
        </View>
      </View>

      {savedMessage && (
        <View style={styles.alertSuccess}>
          <Text style={styles.alertText}>✓ {savedMessage}</Text>
        </View>
      )}

      {/* 1. Hawa-e-Muheet */}
      <View style={styles.card}>
        <Text style={styles.factorTitle}>1. Hawa-e-Muheet (Ambient Air & Respiration)</Text>
        <Text style={styles.factorDesc}>Ventilation and exposure to unpolluted morning air:</Text>
        <View style={styles.pillGroup}>
          <TouchableOpacity
            style={[styles.pill, log.hawa_air === "fresh_mountain" && styles.pillActive]}
            onPress={() => setLog({ ...log, hawa_air: "fresh_mountain" })}
          >
            <Text style={styles.pillText}>Fresh / Morning Air (16 pts)</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.pill, log.hawa_air === "moderate_ventilated" && styles.pillActive]}
            onPress={() => setLog({ ...log, hawa_air: "moderate_ventilated" })}
          >
            <Text style={styles.pillText}>Ventilated Indoor (12 pts)</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* 2. Makul wa Mashrub */}
      <View style={styles.card}>
        <Text style={styles.factorTitle}>2. Makul wa Mashrub (Dietary Regimen)</Text>
        <Text style={styles.factorDesc}>Compliance with prescribed humoral diet (Parhez):</Text>
        <View style={styles.pillGroup}>
          <TouchableOpacity
            style={[styles.pill, log.makul_food === "balanced_prescribed" && styles.pillActive]}
            onPress={() => setLog({ ...log, makul_food: "balanced_prescribed" })}
          >
            <Text style={styles.pillText}>Compliant with Prescribed Diet (18 pts)</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.pill, log.makul_food === "excess_spicy" && styles.pillActive]}
            onPress={() => setLog({ ...log, makul_food: "excess_spicy" })}
          >
            <Text style={styles.pillText}>Spicy / Cold Deviated (8 pts)</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* 3. Harakat wa Sukun Badani */}
      <View style={styles.card}>
        <Text style={styles.factorTitle}>3. Harakat wa Sukun Badani (Physical Movement)</Text>
        <Text style={styles.factorDesc}>Minutes of moderate exercise (Riyazat) today: {log.harakat_movement}m</Text>
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

      {/* 4. Nawm wa Yaqzah */}
      <View style={styles.card}>
        <Text style={styles.factorTitle}>4. Nawm wa Yaqzah (Restorative Sleep)</Text>
        <Text style={styles.factorDesc}>Hours of continuous restful sleep: {log.nawm_sleep} hrs</Text>
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

      {/* 5. Istifragh wa Ihtibas */}
      <View style={styles.card}>
        <Text style={styles.factorTitle}>5. Istifragh wa Ihtibas (Evacuation & Retention)</Text>
        <Text style={styles.factorDesc}>Elimination status and waste expulsion:</Text>
        <View style={styles.pillGroup}>
          <TouchableOpacity
            style={[styles.pill, log.istifragh_retention === "normal_evacuation" && styles.pillActive]}
            onPress={() => setLog({ ...log, istifragh_retention: "normal_evacuation" })}
          >
            <Text style={styles.pillText}>Normal Clearance (16 pts)</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.pill, log.istifragh_retention === "constipated" && styles.pillActive]}
            onPress={() => setLog({ ...log, istifragh_retention: "constipated" })}
          >
            <Text style={styles.pillText}>Constipated / Stagnant (6 pts)</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* 6. Harakat Nafsaniyah */}
      <View style={styles.card}>
        <Text style={styles.factorTitle}>6. Harakat Nafsaniyah (Emotional & Psychic State)</Text>
        <Text style={styles.factorDesc}>Mental tranquility and stress adaptation:</Text>
        <View style={styles.pillGroup}>
          <TouchableOpacity
            style={[styles.pill, log.nafsaniyah_psychic === "calm_focused" && styles.pillActive]}
            onPress={() => setLog({ ...log, nafsaniyah_psychic: "calm_focused" })}
          >
            <Text style={styles.pillText}>Calm / Tranquil (16 pts)</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.pill, log.nafsaniyah_psychic === "moderate_stress" && styles.pillActive]}
            onPress={() => setLog({ ...log, nafsaniyah_psychic: "moderate_stress" })}
          >
            <Text style={styles.pillText}>Moderate Stress (9 pts)</Text>
          </TouchableOpacity>
        </View>
      </View>

      <TouchableOpacity style={styles.submitBtn} onPress={saveLog}>
        <Text style={styles.submitText}>Save & Sync Asbab-e-Sittah Log</Text>
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
  scoreCard: { backgroundColor: "#1E293B", borderRadius: 14, padding: 14, borderWidth: 1, borderColor: "#334155", marginBottom: 14 },
  scoreRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  scoreLabel: { color: "#2DD4BF", fontSize: 11, fontWeight: "bold", textTransform: "uppercase" },
  scoreDesc: { color: "#F8FAFC", fontSize: 12, marginTop: 2 },
  scoreBadge: { flexDirection: "row", alignItems: "baseline", paddingHorizontal: 12, paddingVertical: 6, borderRadius: 12 },
  badgeGreen: { backgroundColor: "rgba(16, 185, 129, 0.2)", borderWidth: 1, borderColor: "#10B981" },
  badgeYellow: { backgroundColor: "rgba(245, 158, 11, 0.2)", borderWidth: 1, borderColor: "#F59E0B" },
  scoreVal: { color: "#FFFFFF", fontSize: 20, fontWeight: "extrabold" },
  scoreOutOf: { color: "#94A3B8", fontSize: 11, marginLeft: 2 },
  alertSuccess: { backgroundColor: "rgba(13, 148, 136, 0.2)", borderColor: "#0D9488", borderWidth: 1, borderRadius: 8, padding: 10, marginBottom: 14 },
  alertText: { color: "#2DD4BF", fontSize: 12, fontWeight: "600" },
  card: { backgroundColor: "#1E293B", borderRadius: 12, padding: 14, marginBottom: 12, borderWidth: 1, borderColor: "#334155" },
  factorTitle: { color: "#FFFFFF", fontSize: 13, fontWeight: "bold", marginBottom: 2 },
  factorDesc: { color: "#94A3B8", fontSize: 11, marginBottom: 10 },
  pillGroup: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  pill: { paddingVertical: 6, paddingHorizontal: 12, borderRadius: 20, backgroundColor: "#0F172A", borderWidth: 1, borderColor: "#334155" },
  pillActive: { backgroundColor: "#0D9488", borderColor: "#2DD4BF" },
  pillText: { color: "#CBD5E1", fontSize: 11, fontWeight: "600" },
  submitBtn: { backgroundColor: "#0D9488", paddingVertical: 14, borderRadius: 12, alignItems: "center", marginTop: 8, marginBottom: 32 },
  submitText: { color: "#FFFFFF", fontSize: 14, fontWeight: "bold" },
});
