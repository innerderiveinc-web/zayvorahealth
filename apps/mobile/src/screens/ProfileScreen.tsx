import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView, Alert } from 'react-native';
import { logout } from '../services/auth.service';

interface Props { onLogout: () => void; }

const SETTINGS = [
  { icon: '🔒', label: 'Change Password', action: 'change_password' },
  { icon: '🔔', label: 'Notifications', action: 'notifications' },
  { icon: '🌐', label: 'Language', value: 'English', action: 'language' },
  { icon: '🛡️', label: 'Privacy & Data', action: 'privacy' },
  { icon: '❓', label: 'Help & Support', action: 'help' },
];

export default function ProfileScreen({ onLogout }: Props) {
  const handleLogout = () => {
    Alert.alert('Sign Out', 'Are you sure you want to sign out?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Sign Out', style: 'destructive', onPress: async () => { await logout(); onLogout(); } },
    ]);
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={{ paddingBottom: 40 }}>
      {/* Avatar & Name */}
      <View style={styles.profileCard}>
        <View style={styles.avatar}><Text style={styles.avatarText}>A</Text></View>
        <Text style={styles.name}>Dr. Ali Hassan</Text>
        <Text style={styles.role}>Clinician · Zayvora Clinic</Text>
        <View style={styles.mizajBadge}><Text style={styles.mizajText}>Mizaj: Damawi</Text></View>
      </View>

      {/* Health Stats */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Health Summary</Text>
        <View style={styles.statsRow}>
          {[['BMI', '22.4'], ['Last Visit', '3d ago'], ['Prescriptions', '2']].map(([label, val]) => (
            <View key={label} style={styles.statBox}>
              <Text style={styles.statValue}>{val}</Text>
              <Text style={styles.statLabel}>{label}</Text>
            </View>
          ))}
        </View>
      </View>

      {/* Settings */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Settings</Text>
        {SETTINGS.map((item) => (
          <TouchableOpacity key={item.action} style={styles.settingRow}>
            <Text style={styles.settingIcon}>{item.icon}</Text>
            <Text style={styles.settingLabel}>{item.label}</Text>
            {item.value && <Text style={styles.settingValue}>{item.value}</Text>}
            <Text style={styles.chevron}>›</Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Logout */}
      <TouchableOpacity style={styles.logoutBtn} onPress={handleLogout}>
        <Text style={styles.logoutText}>🚪 Sign Out</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const PRIMARY = '#2D6A4F';
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#FAFAF7' },
  profileCard: { alignItems: 'center', backgroundColor: PRIMARY, paddingTop: 48, paddingBottom: 32 },
  avatar: { width: 80, height: 80, borderRadius: 40, backgroundColor: '#F4A261', alignItems: 'center', justifyContent: 'center', marginBottom: 12 },
  avatarText: { fontSize: 32, color: '#fff' },
  name: { fontSize: 20, fontWeight: '700', color: '#fff' },
  role: { fontSize: 13, color: '#B7E4C7', marginTop: 4 },
  mizajBadge: { marginTop: 10, backgroundColor: 'rgba(255,255,255,0.2)', paddingHorizontal: 14, paddingVertical: 4, borderRadius: 20 },
  mizajText: { color: '#fff', fontSize: 12, fontWeight: '600' },
  section: { margin: 16, backgroundColor: '#fff', borderRadius: 16, padding: 16, shadowColor: '#000', shadowOpacity: 0.04, shadowRadius: 8, elevation: 2 },
  sectionTitle: { fontSize: 13, fontWeight: '700', color: '#6B7280', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 12 },
  statsRow: { flexDirection: 'row', justifyContent: 'space-around' },
  statBox: { alignItems: 'center' },
  statValue: { fontSize: 18, fontWeight: '700', color: '#1A1A1A' },
  statLabel: { fontSize: 11, color: '#9CA3AF', marginTop: 2 },
  settingRow: { flexDirection: 'row', alignItems: 'center', paddingVertical: 14, borderBottomWidth: 1, borderBottomColor: '#F9FAFB' },
  settingIcon: { fontSize: 18, marginRight: 12 },
  settingLabel: { flex: 1, fontSize: 15, color: '#1A1A1A' },
  settingValue: { fontSize: 14, color: '#9CA3AF', marginRight: 8 },
  chevron: { fontSize: 18, color: '#D1D5DB' },
  logoutBtn: { margin: 16, borderWidth: 1.5, borderColor: '#EF4444', borderRadius: 14, padding: 16, alignItems: 'center' },
  logoutText: { color: '#EF4444', fontWeight: '700', fontSize: 15 },
});
