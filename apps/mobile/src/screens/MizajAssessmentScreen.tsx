import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  SafeAreaView,
  StatusBar,
  ActivityIndicator,
} from "react-native";

interface Question {
  id: number;
  criterion: string;
  question: string;
  options: {
    label: string;
    sublabel: string;
    humor: "damawi" | "safrawi" | "balghami" | "sawdawi";
  }[];
}

const QUESTIONS: Question[] = [
  {
    id: 1,
    criterion: "Skin Temperature & Texture (Lams)",
    question: "How does your skin generally feel to the touch?",
    options: [
      { label: "Warm and supple", sublabel: "Good blood circulation, smooth", humor: "damawi" },
      { label: "Hot and dry", sublabel: "Roughness, prone to flushing", humor: "safrawi" },
      { label: "Cool and moist / soft", sublabel: "Puffy, smooth, retains moisture", humor: "balghami" },
      { label: "Cold and rough / dry", sublabel: "Cracked, taut, dry", humor: "sawdawi" },
    ],
  },
  {
    id: 2,
    criterion: "Body Frame & Physique (Laham & Shaham)",
    question: "What best describes your natural physique?",
    options: [
      { label: "Muscular, robust & broad", sublabel: "Prominent veins, athletic", humor: "damawi" },
      { label: "Lean, toned & sharp", sublabel: "Medium build, defined features", humor: "safrawi" },
      { label: "Heavy, soft or stout", sublabel: "Tends to retain fluid / weight", humor: "balghami" },
      { label: "Slim, bony, slender", sublabel: "Narrow chest, low body fat", humor: "sawdawi" },
    ],
  },
  {
    id: 3,
    criterion: "Complexion (Lawn)",
    question: "What is your natural facial complexion hue?",
    options: [
      { label: "Rosy / Ruddy reddish", sublabel: "Flushed cheeks, radiant", humor: "damawi" },
      { label: "Sallow / Yellowish / Amber", sublabel: "Golden undertones", humor: "safrawi" },
      { label: "Chalky / Pale whitish", sublabel: "Fair, lacking rosiness", humor: "balghami" },
      { label: "Dusky / Earthy / Darkened", sublabel: "Dark circles under eyes", humor: "sawdawi" },
    ],
  },
  {
    id: 4,
    criterion: "Appetite & Digestion (Hazm)",
    question: "How would you describe your appetite and gut?",
    options: [
      { label: "Consistent & strong", sublabel: "Can eat anytime, digests well", humor: "damawi" },
      { label: "Intense, craves cold drinks", sublabel: "Acid reflux or burning if delayed", humor: "safrawi" },
      { label: "Slow, heavy digestion", sublabel: "Feels full for many hours, sluggish", humor: "balghami" },
      { label: "Variable & erratic", sublabel: "Gas, bloating, dry constipation", humor: "sawdawi" },
    ],
  },
  {
    id: 5,
    criterion: "Weather Sensitivity (Hawa)",
    question: "Which weather do you feel least comfortable in?",
    options: [
      { label: "Hot and humid weather", sublabel: "Feels congested, sweats easily", humor: "damawi" },
      { label: "Intense dry heat / summer", sublabel: "Irritable, headaches, dehydration", humor: "safrawi" },
      { label: "Cold and damp / winter rains", sublabel: "Joint stiffness, excess mucus", humor: "balghami" },
      { label: "Dry cold / windy autumn", sublabel: "Dry skin, insomnia, anxiety", humor: "sawdawi" },
    ],
  },
  {
    id: 6,
    criterion: "Sleep Patterns (Nawm)",
    question: "How do you typically sleep at night?",
    options: [
      { label: "Sound and restful", sublabel: "Falls asleep easily, 7-8 hours", humor: "damawi" },
      { label: "Light, short, restless", sublabel: "Wakes up quickly, active mind", humor: "safrawi" },
      { label: "Deep, long and heavy", sublabel: "Hard to wake up, groggy in morning", humor: "balghami" },
      { label: "Disturbed with vivid dreams", sublabel: "Prone to insomnia or waking early", humor: "sawdawi" },
    ],
  },
  {
    id: 7,
    criterion: "Emotional Nature & Temper (Nafs)",
    question: "How do you respond to stress or conflict?",
    options: [
      { label: "Optimistic, expressive, sociable", sublabel: "Cheerfully passionate, forgiving", humor: "damawi" },
      { label: "Passionate, quick-tempered, bold", sublabel: "Decisive, prone to impatience", humor: "safrawi" },
      { label: "Calm, tranquil, patient", sublabel: "Easy-going, avoids confrontation", humor: "balghami" },
      { label: "Analytical, reflective, cautious", sublabel: "Perfectionist, overthinks issues", humor: "sawdawi" },
    ],
  },
  {
    id: 8,
    criterion: "Physical Stamina (Harakah)",
    question: "How is your physical endurance?",
    options: [
      { label: "High stamina, energetic", sublabel: "Good muscle endurance", humor: "damawi" },
      { label: "Explosive energy bursts", sublabel: "Tires if overheated", humor: "safrawi" },
      { label: "Slow starter, steady pace", sublabel: "Dislikes intense cardio", humor: "balghami" },
      { label: "Low endurance, fatigues easily", sublabel: "Needs frequent rest and recovery", humor: "sawdawi" },
    ],
  },
];

export const MizajAssessmentScreen: React.FC<{
  onComplete?: (result: any) => void;
  onBack?: () => void;
}> = ({ onComplete, onBack }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState<Record<number, "damawi" | "safrawi" | "balghami" | "sawdawi">>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState<any>(null);

  const question = QUESTIONS[currentStep];

  const handleSelect = (humor: "damawi" | "safrawi" | "balghami" | "sawdawi") => {
    const updated = { ...answers, [question.id]: humor };
    setAnswers(updated);

    if (currentStep < QUESTIONS.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      calculateResult(updated);
    }
  };

  const calculateResult = (allAnswers: Record<number, string>) => {
    setIsSubmitting(true);
    setTimeout(() => {
      const counts: Record<string, number> = { damawi: 0, safrawi: 0, balghami: 0, sawdawi: 0 };
      Object.values(allAnswers).forEach((h) => {
        counts[h] = (counts[h] || 0) + 1;
      });

      const total = Object.values(allAnswers).length;
      const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);
      const primary = sorted[0][0];
      const secondary = sorted[1][0];

      const res = {
        primary: primary.toUpperCase(),
        secondary: secondary.toUpperCase(),
        percentages: {
          damawi: Math.round((counts.damawi / total) * 100),
          safrawi: Math.round((counts.safrawi / total) * 100),
          balghami: Math.round((counts.balghami / total) * 100),
          sawdawi: Math.round((counts.sawdawi / total) * 100),
        },
        recommendation:
          primary === "damawi"
            ? "Mufarreh & Cool Regimen: Include pomegranate, barley sattu, coriander, and light aerobic exercise."
            : primary === "safrawi"
            ? "Mubarrid (Cooling) Diet: Cucumber, rose water, mint infusion, avoid pungent chili and excessive sun."
            : primary === "balghami"
            ? "Musakhin (Warming) Regimen: Ginger tea, black pepper, warm dry saunas, honey, avoid cold curd."
            : "Murattib (Moistening) Regimen: Almond milk with saffron, hydration, calming meditation, warm baths.",
      };

      setResult(res);
      setIsSubmitting(false);
      if (onComplete) onComplete(res);
    }, 800);
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#0F172A" />

      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={onBack} style={styles.backBtn}>
          <Text style={styles.backBtnText}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Mizaj (Temperament) Assessment</Text>
        <View style={{ width: 50 }} />
      </View>

      {/* Progress Bar */}
      {!result && (
        <View style={styles.progressBarContainer}>
          <View
            style={[
              styles.progressBarFill,
              { width: `${((currentStep + 1) / QUESTIONS.length) * 100}%` },
            ]}
          />
        </View>
      )}

      {isSubmitting ? (
        <View style={styles.centerContainer}>
          <ActivityIndicator size="large" color="#2DD4BF" />
          <Text style={styles.loadingText}>Computing Unani Humoral Deviation (Su-e-Mizaj)...</Text>
        </View>
      ) : result ? (
        /* Results View */
        <ScrollView contentContainerStyle={styles.resultScroll}>
          <View style={styles.resultCard}>
            <Text style={styles.resultBadge}>VALIDATED UNANI PROFILE</Text>
            <Text style={styles.resultTitle}>
              {result.primary} {result.secondary !== result.primary ? `with ${result.secondary} Tendency` : ""}
            </Text>
            <Text style={styles.resultSub}>
              {result.primary === "DAMAWI"
                ? "Hot & Moist (Sanguine) — Dominated by Dam (Blood)"
                : result.primary === "SAFRAWI"
                ? "Hot & Dry (Choleric) — Dominated by Safra (Yellow Bile)"
                : result.primary === "BALGHAMI"
                ? "Cold & Moist (Phlegmatic) — Dominated by Balgham (Phlegm)"
                : "Cold & Dry (Melancholic) — Dominated by Sawda (Black Bile)"}
            </Text>

            {/* Humor Breakdown */}
            <View style={styles.breakdownGrid}>
              <View style={styles.breakdownItem}>
                <Text style={styles.humorLabel}>Damawi (Sanguine)</Text>
                <Text style={styles.humorVal}>{result.percentages.damawi}%</Text>
              </View>
              <View style={styles.breakdownItem}>
                <Text style={styles.humorLabel}>Safrawi (Choleric)</Text>
                <Text style={styles.humorVal}>{result.percentages.safrawi}%</Text>
              </View>
              <View style={styles.breakdownItem}>
                <Text style={styles.humorLabel}>Balghami (Phlegmatic)</Text>
                <Text style={styles.humorVal}>{result.percentages.balghami}%</Text>
              </View>
              <View style={styles.breakdownItem}>
                <Text style={styles.humorLabel}>Sawdawi (Melancholic)</Text>
                <Text style={styles.humorVal}>{result.percentages.sawdawi}%</Text>
              </View>
            </View>

            {/* Clinical Regimen Recommendation */}
            <View style={styles.recommendationBox}>
              <Text style={styles.recTitle}>🌿 Asbab-e-Sittah Zarooriyyah (Lifestyle Regimen)</Text>
              <Text style={styles.recBody}>{result.recommendation}</Text>
            </View>

            <TouchableOpacity
              onPress={() => {
                setResult(null);
                setCurrentStep(0);
                setAnswers({});
              }}
              style={styles.retakeBtn}
            >
              <Text style={styles.retakeBtnText}>Retake Assessment</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      ) : (
        /* Questions View */
        <ScrollView contentContainerStyle={styles.questionScroll}>
          <View style={styles.metaRow}>
            <Text style={styles.stepCount}>
              Criterion {currentStep + 1} of {QUESTIONS.length}
            </Text>
            <Text style={styles.criterionTag}>{question.criterion}</Text>
          </View>

          <Text style={styles.questionText}>{question.question}</Text>

          <View style={styles.optionsList}>
            {question.options.map((opt, idx) => (
              <TouchableOpacity
                key={idx}
                onPress={() => handleSelect(opt.humor)}
                style={styles.optionCard}
                activeOpacity={0.7}
              >
                <View style={styles.optionHeader}>
                  <Text style={styles.optionLabel}>{opt.label}</Text>
                  <Text style={styles.humorIndicator}>{opt.humor.toUpperCase()}</Text>
                </View>
                <Text style={styles.optionSub}>{opt.sublabel}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </ScrollView>
      )}
    </SafeAreaView>
  );
};

export default MizajAssessmentScreen;

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0A0F1D" },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 16,
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: "#1E293B",
  },
  backBtn: { padding: 4 },
  backBtnText: { color: "#2DD4BF", fontSize: 13, fontWeight: "600" },
  headerTitle: { color: "#FFFFFF", fontSize: 15, fontWeight: "700" },
  progressBarContainer: { height: 4, backgroundColor: "#1E293B", width: "100%" },
  progressBarFill: { height: 4, backgroundColor: "#2DD4BF" },
  questionScroll: { padding: 20, gap: 16 },
  metaRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  stepCount: { color: "#94A3B8", fontSize: 12, fontWeight: "600" },
  criterionTag: { color: "#2DD4BF", fontSize: 11, fontWeight: "700", backgroundColor: "#134E4A", paddingHorizontal: 8, paddingVertical: 2, borderRadius: 6 },
  questionText: { color: "#FFFFFF", fontSize: 18, fontWeight: "700", lineHeight: 26 },
  optionsList: { gap: 12, marginTop: 8 },
  optionCard: {
    backgroundColor: "#0F172A",
    borderWidth: 1,
    borderColor: "#1E293B",
    borderRadius: 14,
    padding: 16,
    gap: 4,
  },
  optionHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  optionLabel: { color: "#FFFFFF", fontSize: 15, fontWeight: "600" },
  humorIndicator: { color: "#94A3B8", fontSize: 10, fontWeight: "800" },
  optionSub: { color: "#94A3B8", fontSize: 12 },
  centerContainer: { flex: 1, justifyContent: "center", alignItems: "center", gap: 16, padding: 24 },
  loadingText: { color: "#94A3B8", fontSize: 13, textAlign: "center" },
  resultScroll: { padding: 20 },
  resultCard: { backgroundColor: "#0F172A", borderWidth: 1, borderColor: "#1E293B", borderRadius: 16, padding: 20, gap: 16 },
  resultBadge: { color: "#2DD4BF", fontSize: 11, fontWeight: "800", letterSpacing: 1 },
  resultTitle: { color: "#FFFFFF", fontSize: 22, fontWeight: "800" },
  resultSub: { color: "#94A3B8", fontSize: 13, lineHeight: 18 },
  breakdownGrid: { flexDirection: "row", flexWrap: "wrap", gap: 8, marginTop: 4 },
  breakdownItem: { flex: 1, minWidth: "45%", backgroundColor: "#1E293B", padding: 12, borderRadius: 10 },
  humorLabel: { color: "#94A3B8", fontSize: 11 },
  humorVal: { color: "#2DD4BF", fontSize: 18, fontWeight: "800", marginTop: 2 },
  recommendationBox: { backgroundColor: "#083344", borderWidth: 1, borderColor: "#155E75", padding: 16, borderRadius: 12, gap: 6 },
  recTitle: { color: "#67E8F9", fontSize: 13, fontWeight: "700" },
  recBody: { color: "#E2E8F0", fontSize: 12, lineHeight: 18 },
  retakeBtn: { backgroundColor: "#134E4A", paddingVertical: 12, borderRadius: 12, alignItems: "center", marginTop: 8 },
  retakeBtnText: { color: "#2DD4BF", fontWeight: "700", fontSize: 13 },
});
