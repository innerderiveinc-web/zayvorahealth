import React, { useState } from "react";
import { SafeAreaView, View, Text, StyleSheet, TouchableOpacity, StatusBar, Image } from "react-native";
import { HomeScreen } from "./src/screens/HomeScreen";
import { PrescriptionsScreen } from "./src/screens/PrescriptionsScreen";
import { LifestyleTrackerScreen } from "./src/screens/LifestyleTrackerScreen";
import { AppointmentsScreen } from "./src/screens/AppointmentsScreen";
import { ClinicianCompanionScreen } from "./src/screens/ClinicianCompanionScreen";
import { TeleConsultRoom } from "./src/screens/TeleConsultRoom";

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<string>("home");

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="light-content" backgroundColor="#0A0F1D" />

      {/* Top Mobile SaaS Header */}
      <View style={styles.topBar}>
        <View style={styles.brandGroup}>
          <View style={styles.logoBox}>
            <Text style={styles.logoLetter}>Z</Text>
          </View>
          <View>
            <View style={styles.brandRow}>
              <Text style={styles.brandTitle}>ZAYVORA</Text>
              <Text style={styles.brandTag}>HEALTH OS</Text>
            </View>
            <Text style={styles.brandSub}>Jamia Hamdard AUTC</Text>
          </View>
        </View>
        <View style={styles.badgeOnline}>
          <View style={styles.pulseDot} />
          <Text style={styles.badgeText}>Open</Text>
        </View>
      </View>

      {/* Main Screen Container */}
      <View style={styles.body}>
        {currentScreen === "home" && <HomeScreen onNavigate={(s) => setCurrentScreen(s)} />}
        {currentScreen === "prescriptions" && <PrescriptionsScreen onBack={() => setCurrentScreen("home")} />}
        {currentScreen === "lifestyle" && <LifestyleTrackerScreen onBack={() => setCurrentScreen("home")} />}
        {currentScreen === "appointments" && (
          <AppointmentsScreen onBack={() => setCurrentScreen("home")} onNavigate={(s) => setCurrentScreen(s)} />
        )}
        {currentScreen === "teleconsult" && <TeleConsultRoom onEndCall={() => setCurrentScreen("home")} />}
        {currentScreen === "clinician" && <ClinicianCompanionScreen onBack={() => setCurrentScreen("home")} />}
      </View>

      {/* Bottom Navigation Tabs */}
      <View style={styles.bottomNav}>
        <TouchableOpacity
          style={[styles.navTab, currentScreen === "home" && styles.navTabActive]}
          onPress={() => setCurrentScreen("home")}
        >
          <Text style={styles.navIcon}>📊</Text>
          <Text style={[styles.navLabel, currentScreen === "home" && styles.navLabelActive]}>Dashboard</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.navTab, currentScreen === "prescriptions" && styles.navTabActive]}
          onPress={() => setCurrentScreen("prescriptions")}
        >
          <Text style={styles.navIcon}>💊</Text>
          <Text style={[styles.navLabel, currentScreen === "prescriptions" && styles.navLabelActive]}>Dawa (Rx)</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.navTab, currentScreen === "lifestyle" && styles.navTabActive]}
          onPress={() => setCurrentScreen("lifestyle")}
        >
          <Text style={styles.navIcon}>🌿</Text>
          <Text style={[styles.navLabel, currentScreen === "lifestyle" && styles.navLabelActive]}>Lifestyle</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.navTab, currentScreen === "appointments" && styles.navTabActive]}
          onPress={() => setCurrentScreen("appointments")}
        >
          <Text style={styles.navIcon}>📅</Text>
          <Text style={[styles.navLabel, currentScreen === "appointments" && styles.navLabelActive]}>Consult</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.navTab, currentScreen === "clinician" && styles.navTabActive]}
          onPress={() => setCurrentScreen("clinician")}
        >
          <Text style={styles.navIcon}>🛡️</Text>
          <Text style={[styles.navLabel, currentScreen === "clinician" && styles.navLabelActive]}>Doctor</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: "#0A0F1D" },
  topBar: {
    height: 56,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 14,
    borderBottomWidth: 1,
    borderBottomColor: "#1E293B",
    backgroundColor: "#0F172A"
  },
  brandGroup: { flexDirection: "row", alignItems: "center", gap: 10 },
  logoBox: { width: 32, height: 32, borderRadius: 8, backgroundColor: "#0D9488", alignItems: "center", justifyContent: "center" },
  logoLetter: { color: "#FFFFFF", fontWeight: "bold", fontSize: 18 },
  brandRow: { flexDirection: "row", alignItems: "center", gap: 4 },
  brandTitle: { color: "#FFFFFF", fontSize: 13, fontWeight: "bold" },
  brandTag: { color: "#2DD4BF", fontSize: 8, fontWeight: "bold", backgroundColor: "rgba(13, 148, 136, 0.2)", paddingHorizontal: 4, borderRadius: 4 },
  brandSub: { color: "#94A3B8", fontSize: 9, fontWeight: "500" },
  badgeOnline: { backgroundColor: "rgba(16, 185, 129, 0.2)", paddingHorizontal: 8, paddingVertical: 4, borderRadius: 12, borderWidth: 1, borderColor: "#10B981", flexDirection: "row", alignItems: "center", gap: 4 },
  pulseDot: { width: 6, height: 6, borderRadius: 3, backgroundColor: "#10B981" },
  badgeText: { color: "#10B981", fontSize: 9, fontWeight: "bold" },
  body: { flex: 1 },
  bottomNav: {
    height: 58,
    flexDirection: "row",
    borderTopWidth: 1,
    borderTopColor: "#1E293B",
    backgroundColor: "#0F172A",
    alignItems: "center",
    justifyContent: "space-around"
  },
  navTab: { alignItems: "center", paddingVertical: 6, flex: 1 },
  navTabActive: { borderTopWidth: 2, borderTopColor: "#2DD4BF" },
  navIcon: { fontSize: 17 },
  navLabel: { color: "#64748B", fontSize: 9, marginTop: 2, fontWeight: "500" },
  navLabelActive: { color: "#2DD4BF", fontWeight: "bold" }
});
