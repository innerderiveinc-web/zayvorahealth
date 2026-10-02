import React, { useState } from "react";
import { View, Text, StyleSheet, TouchableOpacity, TextInput, ScrollView } from "react-native";

export const TeleConsultRoom: React.FC<{ onEndCall: () => void }> = ({ onEndCall }) => {
  const [micMuted, setMicMuted] = useState(false);
  const [cameraOff, setCameraOff] = useState(false);
  const [activeTab, setActiveTab] = useState<"video" | "hud" | "chat">("video");
  const [chatInput, setChatInput] = useState("");
  const [messages, setMessages] = useState<Array<{ sender: string; text: string; time: string }>>([
    { sender: "Clinician", text: "Assalamu Alaikum. Can you describe your morning knee stiffness?", time: "10:31" },
    { sender: "Patient", text: "Yes doctor, it feels heavy and cold for about 45 minutes after waking up.", time: "10:32" },
  ]);

  const sendMessage = () => {
    if (!chatInput.trim()) return;
    setMessages([...messages, { sender: "Patient", text: chatInput.trim(), time: "10:33" }]);
    setChatInput("");
  };

  return (
    <View style={styles.container}>
      {/* Top Telehealth Status Bar */}
      <View style={styles.topBar}>
        <View style={styles.doctorInfo}>
          <Text style={styles.doctorName}>Hakeem Dr. Irfan Ashraf</Text>
          <Text style={styles.callMeta}>Encrypted WebRTC • Room: ENC-2026-0814</Text>
        </View>
        <View style={styles.liveBadge}>
          <Text style={styles.liveText}>● LIVE 12:44</Text>
        </View>
      </View>

      {/* Main Encounter Window */}
      {activeTab === "video" && (
        <View style={styles.videoArea}>
          {/* Main Remote Video Stream (Doctor) */}
          <View style={styles.remoteVideo}>
            <Text style={styles.videoPlaceholder}>🩺 Hakeem Dr. Irfan Ashraf (Video Active)</Text>
            <View style={styles.webrtcQuality}>
              <Text style={styles.qualityText}>HD 1080p • 24ms • TLS 1.3</Text>
            </View>
          </View>

          {/* Picture-in-Picture Self View (Patient) */}
          <View style={styles.selfVideo}>
            <Text style={styles.selfText}>👤 You</Text>
          </View>
        </View>
      )}

      {activeTab === "hud" && (
        <ScrollView style={styles.hudArea}>
          <Text style={styles.hudTitle}>Live In-Call Clinical HUD</Text>
          <View style={styles.hudCard}>
            <Text style={styles.hudLabel}>ACTIVE MIZAJ EVALUATION:</Text>
            <Text style={styles.hudVal}>Balghami (Cold & Moist) — Degree 2</Text>
          </View>
          <View style={styles.hudCard}>
            <Text style={styles.hudLabel}>LIVE IN-CALL PRESCRIPTION DRAFT:</Text>
            <Text style={styles.hudVal}>1. Majun Suranjan (5g twice daily)</Text>
            <Text style={styles.hudVal}>2. Arq-e-Badiyan (60ml morning fasting)</Text>
            <Text style={styles.hudVal}>3. Natool of Gul-e-Surkh (Warm fomentation)</Text>
          </View>
          <View style={styles.hudCard}>
            <Text style={styles.hudLabel}>STATUTORY CLINICAL SAFETY:</Text>
            <Text style={styles.safetyOk}>✓ 0 Drug Interactions Detected</Text>
            <Text style={styles.safetyOk}>✓ Schedule E(1) Mudabbar Certified</Text>
          </View>
        </ScrollView>
      )}

      {activeTab === "chat" && (
        <View style={styles.chatArea}>
          <ScrollView style={styles.chatScroll}>
            {messages.map((m, idx) => (
              <View key={idx} style={[styles.msgRow, m.sender === "Patient" ? styles.msgRight : styles.msgLeft]}>
                <Text style={styles.msgSender}>{m.sender} ({m.time})</Text>
                <Text style={styles.msgText}>{m.text}</Text>
              </View>
            ))}
          </ScrollView>
          <View style={styles.chatInputRow}>
            <TextInput
              style={styles.inputField}
              value={chatInput}
              onChangeText={setChatInput}
              placeholder="Send in-call message..."
              placeholderTextColor="#64748B"
            />
            <TouchableOpacity style={styles.sendBtn} onPress={sendMessage}>
              <Text style={styles.sendBtnText}>Send</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}

      {/* Mode Switcher */}
      <View style={styles.modeRow}>
        <TouchableOpacity
          style={[styles.modeBtn, activeTab === "video" && styles.modeBtnActive]}
          onPress={() => setActiveTab("video")}
        >
          <Text style={styles.modeText}>📹 Video</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.modeBtn, activeTab === "hud" && styles.modeBtnActive]}
          onPress={() => setActiveTab("hud")}
        >
          <Text style={styles.modeText}>📋 Clinical HUD</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.modeBtn, activeTab === "chat" && styles.modeBtnActive]}
          onPress={() => setActiveTab("chat")}
        >
          <Text style={styles.modeText}>💬 Chat</Text>
        </TouchableOpacity>
      </View>

      {/* In-Call Controls */}
      <View style={styles.bottomControls}>
        <TouchableOpacity
          style={[styles.controlBtn, micMuted && styles.controlBtnMuted]}
          onPress={() => setMicMuted(!micMuted)}
        >
          <Text style={styles.controlEmoji}>{micMuted ? "🔇" : "🎙️"}</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.controlBtn, cameraOff && styles.controlBtnMuted]}
          onPress={() => setCameraOff(!cameraOff)}
        >
          <Text style={styles.controlEmoji}>{cameraOff ? "🚫" : "📷"}</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.endCallBtn} onPress={onEndCall}>
          <Text style={styles.endCallText}>End Call</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0A0F1D" },
  topBar: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: "#0F172A",
    borderBottomWidth: 1,
    borderBottomColor: "#1E293B",
  },
  doctorInfo: { flex: 1 },
  doctorName: { color: "#FFFFFF", fontSize: 14, fontWeight: "bold" },
  callMeta: { color: "#94A3B8", fontSize: 10, marginTop: 1 },
  liveBadge: { backgroundColor: "rgba(239, 68, 68, 0.2)", paddingHorizontal: 8, paddingVertical: 4, borderRadius: 12, borderWidth: 1, borderColor: "#EF4444" },
  liveText: { color: "#F87171", fontSize: 10, fontWeight: "bold" },
  videoArea: { flex: 1, position: "relative", backgroundColor: "#000000" },
  remoteVideo: { flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: "#111827" },
  videoPlaceholder: { color: "#94A3B8", fontSize: 15, fontWeight: "600" },
  webrtcQuality: { position: "absolute", bottom: 12, left: 12, backgroundColor: "rgba(0,0,0,0.6)", paddingHorizontal: 8, paddingVertical: 4, borderRadius: 6 },
  qualityText: { color: "#2DD4BF", fontSize: 10, fontWeight: "600" },
  selfVideo: { position: "absolute", top: 12, right: 12, width: 88, height: 120, backgroundColor: "#1E293B", borderRadius: 12, borderWidth: 1, borderColor: "#334155", alignItems: "center", justifyContent: "center" },
  selfText: { color: "#FFFFFF", fontSize: 11, fontWeight: "bold" },
  hudArea: { flex: 1, padding: 16 },
  hudTitle: { color: "#FFFFFF", fontSize: 16, fontWeight: "bold", marginBottom: 12 },
  hudCard: { backgroundColor: "#1E293B", borderRadius: 12, padding: 12, marginBottom: 10, borderWidth: 1, borderColor: "#334155" },
  hudLabel: { color: "#2DD4BF", fontSize: 10, fontWeight: "bold", marginBottom: 4 },
  hudVal: { color: "#F8FAFC", fontSize: 12, lineHeight: 18 },
  safetyOk: { color: "#34D399", fontSize: 11, fontWeight: "600", marginTop: 2 },
  chatArea: { flex: 1, padding: 12 },
  chatScroll: { flex: 1, marginBottom: 8 },
  msgRow: { marginVertical: 4, maxWidth: "80%", padding: 8, borderRadius: 10 },
  msgLeft: { alignSelf: "flex-start", backgroundColor: "#1E293B" },
  msgRight: { alignSelf: "flex-end", backgroundColor: "#0D9488" },
  msgSender: { color: "#94A3B8", fontSize: 9, fontWeight: "bold", marginBottom: 2 },
  msgText: { color: "#FFFFFF", fontSize: 12 },
  chatInputRow: { flexDirection: "row", gap: 8 },
  inputField: { flex: 1, backgroundColor: "#1E293B", borderRadius: 8, paddingHorizontal: 12, color: "#FFFFFF", fontSize: 12, borderWidth: 1, borderColor: "#334155" },
  sendBtn: { backgroundColor: "#0D9488", paddingHorizontal: 14, justifyContent: "center", borderRadius: 8 },
  sendBtnText: { color: "#FFFFFF", fontSize: 12, fontWeight: "bold" },
  modeRow: { flexDirection: "row", backgroundColor: "#0F172A", padding: 8, borderTopWidth: 1, borderTopColor: "#1E293B", gap: 8 },
  modeBtn: { flex: 1, paddingVertical: 8, alignItems: "center", borderRadius: 8, backgroundColor: "#1E293B" },
  modeBtnActive: { backgroundColor: "#0D9488" },
  modeText: { color: "#FFFFFF", fontSize: 11, fontWeight: "bold" },
  bottomControls: { flexDirection: "row", justifyContent: "space-around", alignItems: "center", paddingVertical: 14, backgroundColor: "#0F172A", borderTopWidth: 1, borderTopColor: "#1E293B" },
  controlBtn: { width: 48, height: 48, borderRadius: 24, backgroundColor: "#1E293B", alignItems: "center", justifyContent: "center", borderWidth: 1, borderColor: "#334155" },
  controlBtnMuted: { backgroundColor: "#EF4444", borderColor: "#DC2626" },
  controlEmoji: { fontSize: 20 },
  endCallBtn: { backgroundColor: "#DC2626", paddingHorizontal: 22, paddingVertical: 12, borderRadius: 24 },
  endCallText: { color: "#FFFFFF", fontWeight: "bold", fontSize: 13 },
});
