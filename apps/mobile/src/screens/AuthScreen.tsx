import React, { useState } from 'react';
import {
  View, Text, TextInput, TouchableOpacity, StyleSheet,
  Alert, ActivityIndicator, KeyboardAvoidingView, Platform, ScrollView,
} from 'react-native';
import { login, register } from '../services/auth.service';

type Tab = 'login' | 'register';

interface Props { onAuthSuccess: () => void; }

export default function AuthScreen({ onAuthSuccess }: Props) {
  const [tab, setTab] = useState<Tab>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    setError('');
    if (!email || !password) { setError('Email and password are required.'); return; }
    setLoading(true);
    try {
      if (tab === 'login') {
        await login(email, password);
      } else {
        if (!name) { setError('Name is required.'); setLoading(false); return; }
        await register({ email, password, name });
        await login(email, password);
      }
      onAuthSuccess();
    } catch (err: any) {
      setError(err.message || 'Authentication failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView style={styles.container} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <ScrollView contentContainerStyle={styles.scroll} keyboardShouldPersistTaps="handled">
        {/* Brand Header */}
        <View style={styles.header}>
          <Text style={styles.brandLogo}>🌿</Text>
          <Text style={styles.brandName}>ZAYVORA</Text>
          <Text style={styles.brandSubtitle}>Clinical Operating System</Text>
          <Text style={styles.brandTagline}>Ancient Wisdom. Modern Science.</Text>
        </View>

        {/* Tabs */}
        <View style={styles.tabs}>
          {(['login', 'register'] as Tab[]).map((t) => (
            <TouchableOpacity key={t} onPress={() => { setTab(t); setError(''); }} style={[styles.tab, tab === t && styles.tabActive]}>
              <Text style={[styles.tabText, tab === t && styles.tabTextActive]}>
                {t === 'login' ? 'Sign In' : 'Register'}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Form */}
        <View style={styles.form}>
          {tab === 'register' && (
            <TextInput style={styles.input} placeholder="Full Name" value={name} onChangeText={setName}
              autoCapitalize="words" placeholderTextColor="#9CA3AF" />
          )}
          <TextInput style={styles.input} placeholder="Email Address" value={email} onChangeText={setEmail}
            keyboardType="email-address" autoCapitalize="none" placeholderTextColor="#9CA3AF" />
          <TextInput style={styles.input} placeholder="Password" value={password} onChangeText={setPassword}
            secureTextEntry placeholderTextColor="#9CA3AF" />

          {error ? <Text style={styles.error}>{error}</Text> : null}

          <TouchableOpacity style={styles.btn} onPress={handleSubmit} disabled={loading}>
            {loading ? <ActivityIndicator color="#fff" /> : (
              <Text style={styles.btnText}>{tab === 'login' ? 'Sign In' : 'Create Account'}</Text>
            )}
          </TouchableOpacity>

          {tab === 'login' && (
            <TouchableOpacity>
              <Text style={styles.forgotLink}>Forgot password?</Text>
            </TouchableOpacity>
          )}
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const PRIMARY = '#2D6A4F';
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#FAFAF7' },
  scroll: { flexGrow: 1, justifyContent: 'center', padding: 24 },
  header: { alignItems: 'center', marginBottom: 36 },
  brandLogo: { fontSize: 56, marginBottom: 8 },
  brandName: { fontSize: 28, fontWeight: '800', color: PRIMARY, letterSpacing: 3 },
  brandSubtitle: { fontSize: 16, color: '#1B4332', marginTop: 2 },
  brandTagline: { fontSize: 12, color: '#6B7280', marginTop: 8 },
  tabs: { flexDirection: 'row', backgroundColor: '#F3F4F6', borderRadius: 12, padding: 4, marginBottom: 24 },
  tab: { flex: 1, paddingVertical: 10, borderRadius: 10, alignItems: 'center' },
  tabActive: { backgroundColor: '#fff', shadowColor: '#000', shadowOpacity: 0.08, shadowRadius: 4, elevation: 2 },
  tabText: { fontSize: 14, color: '#6B7280', fontWeight: '500' },
  tabTextActive: { color: PRIMARY, fontWeight: '700' },
  form: { gap: 12 },
  input: { backgroundColor: '#fff', borderWidth: 1, borderColor: '#E5E7EB', borderRadius: 12, paddingHorizontal: 16, paddingVertical: 14, fontSize: 15, color: '#111827' },
  error: { color: '#DC2626', fontSize: 13, textAlign: 'center' },
  btn: { backgroundColor: PRIMARY, borderRadius: 12, paddingVertical: 16, alignItems: 'center', marginTop: 8 },
  btnText: { color: '#fff', fontSize: 16, fontWeight: '700' },
  forgotLink: { color: PRIMARY, textAlign: 'center', fontSize: 14, marginTop: 12 },
});
