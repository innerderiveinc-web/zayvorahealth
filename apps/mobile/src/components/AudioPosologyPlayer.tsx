import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { Language } from "../types";

interface AudioPosologyPlayerProps {
  prescriptionTitle: string;
  transcripts: {
    en: string;
    ur: string;
    hi: string;
  };
  durationSeconds?: number;
}

export const AudioPosologyPlayer: React.FC<AudioPosologyPlayerProps> = ({
  prescriptionTitle,
  transcripts,
  durationSeconds = 18,
}) => {
  const [selectedLang, setSelectedLang] = useState<Language>("ur");
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [playbackSpeed, setPlaybackSpeed] = useState<number>(1.0);
  const [elapsed, setElapsed] = useState<number>(0);

  useEffect(() => {
    let interval: any = null;
    if (isPlaying) {
      interval = setInterval(() => {
        setElapsed((prev) => {
          if (prev >= durationSeconds) {
            setIsPlaying(false);
            return 0;
          }
          return prev + 1;
        });
      }, 1000 / playbackSpeed);
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isPlaying, playbackSpeed, durationSeconds]);

  const togglePlayback = () => {
    setIsPlaying(!isPlaying);
  };

  const cycleSpeed = () => {
    if (playbackSpeed === 1.0) setPlaybackSpeed(1.25);
    else if (playbackSpeed === 1.25) setPlaybackSpeed(0.75);
    else setPlaybackSpeed(1.0);
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>🔊 Vernacular Audio Posology</Text>
        <Text style={styles.targetMed}>{prescriptionTitle}</Text>
      </View>

      {/* Language Tabs */}
      <View style={styles.langRow}>
        <TouchableOpacity
          style={[styles.langBtn, selectedLang === "ur" && styles.langBtnActive]}
          onPress={() => setSelectedLang("ur")}
        >
          <Text style={[styles.langText, selectedLang === "ur" && styles.langTextActive]}>Urdu (Roman)</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.langBtn, selectedLang === "hi" && styles.langBtnActive]}
          onPress={() => setSelectedLang("hi")}
        >
          <Text style={[styles.langText, selectedLang === "hi" && styles.langTextActive]}>हिन्दी (Hindi)</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.langBtn, selectedLang === "en" && styles.langBtnActive]}
          onPress={() => setSelectedLang("en")}
        >
          <Text style={[styles.langText, selectedLang === "en" && styles.langTextActive]}>English</Text>
        </TouchableOpacity>
      </View>

      {/* Spoken Text Display */}
      <View style={styles.transcriptBox}>
        <Text style={[styles.spokenText, selectedLang === "ur" && styles.urduText]}>
          "{transcripts[selectedLang]}"
        </Text>
      </View>

      {/* Waveform Visualization Bars */}
      <View style={styles.waveRow}>
        {[14, 22, 38, 26, 45, 32, 20, 48, 30, 18, 36, 24, 40, 16, 28, 44].map((height, idx) => (
          <View
            key={idx}
            style={[
              styles.waveBar,
              {
                height: isPlaying ? Math.min(48, height * (0.6 + Math.sin(idx + elapsed) * 0.4)) : 10,
                backgroundColor: isPlaying ? "#2DD4BF" : "#334155",
              },
            ]}
          />
        ))}
      </View>

      {/* Audio Controls */}
      <View style={styles.controlsRow}>
        <Text style={styles.timerText}>
          00:{elapsed < 10 ? `0${elapsed}` : elapsed} / 00:{durationSeconds}
        </Text>

        <TouchableOpacity style={styles.playButton} onPress={togglePlayback}>
          <Text style={styles.playButtonText}>{isPlaying ? "⏸ Pause Voice" : "▶ Play Voice"}</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.speedButton} onPress={cycleSpeed}>
          <Text style={styles.speedText}>{playbackSpeed}x</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: "#0F172A",
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "#334155",
    padding: 16,
    marginVertical: 10,
  },
  header: { marginBottom: 12 },
  title: { color: "#2DD4BF", fontSize: 13, fontWeight: "bold", textTransform: "uppercase" },
  targetMed: { color: "#FFFFFF", fontSize: 15, fontWeight: "bold", marginTop: 2 },
  langRow: { flexDirection: "row", gap: 8, marginBottom: 12 },
  langBtn: {
    flex: 1,
    paddingVertical: 6,
    backgroundColor: "#1E293B",
    borderRadius: 8,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#334155",
  },
  langBtnActive: { backgroundColor: "#0D9488", borderColor: "#2DD4BF" },
  langText: { color: "#94A3B8", fontSize: 11, fontWeight: "600" },
  langTextActive: { color: "#FFFFFF", fontWeight: "bold" },
  transcriptBox: {
    backgroundColor: "#1E293B",
    padding: 12,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "#334155",
    marginBottom: 12,
  },
  spokenText: { color: "#F8FAFC", fontSize: 13, lineHeight: 20, fontStyle: "italic" },
  urduText: { textAlign: "right", fontSize: 15, lineHeight: 24, fontStyle: "normal" },
  waveRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    height: 52,
    gap: 5,
    marginVertical: 6,
  },
  waveBar: { width: 4, borderRadius: 2 },
  controlsRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginTop: 8,
    paddingTop: 8,
    borderTopWidth: 1,
    borderTopColor: "#1E293B",
  },
  timerText: { color: "#64748B", fontSize: 11, fontVariant: ["tabular-nums"] },
  playButton: {
    backgroundColor: "#0D9488",
    paddingVertical: 8,
    paddingHorizontal: 18,
    borderRadius: 10,
  },
  playButtonText: { color: "#FFFFFF", fontSize: 12, fontWeight: "bold" },
  speedButton: {
    backgroundColor: "#1E293B",
    paddingVertical: 6,
    paddingHorizontal: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#334155",
  },
  speedText: { color: "#2DD4BF", fontSize: 11, fontWeight: "bold" },
});
