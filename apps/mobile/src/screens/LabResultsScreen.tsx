import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, ActivityIndicator } from 'react-native';
import { apiGet } from '../services/api.service';
import type { LabResult } from '../types';

const FLAG_STYLE = {
  H: { text: '▲ High', color: '#DC2626', bg: '#FEF2F2' },
  L: { text: '▼ Low', color: '#D97706', bg: '#FFFBEB' },
  N: { text: 'Normal', color: '#059669', bg: '#ECFDF5' },
};

export default function LabResultsScreen() {
  const [results, setResults] = useState<LabResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<string | null>(null);

  useEffect(() => {
    apiGet<LabResult[]>('/api/clinical/lab-results/my')
      .then(setResults)
      .catch(() => setResults(MOCK))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <View style={styles.center}><ActivityIndicator size="large" color="#2D6A4F" /></View>;

  return (
    <View style={styles.container}>
      <View style={styles.header}><Text style={styles.title}>Lab Results</Text><Text style={styles.count}>{results.length} panels</Text></View>
      <FlatList
        data={results}
        keyExtractor={item => item.id}
        contentContainerStyle={{ paddingBottom: 32 }}
        renderItem={({ item }) => {
          const isOpen = expanded === item.id;
          const hasAbnormal = item.tests.some(t => t.flag === 'H' || t.flag === 'L');
          return (
            <TouchableOpacity style={styles.card} onPress={() => setExpanded(isOpen ? null : item.id)}>
              <View style={styles.cardHeader}>
                <View style={{ flex: 1 }}>
                  <Text style={styles.panelName}>{item.panel_name}</Text>
                  <Text style={styles.date}>{new Date(item.collected_at).toLocaleDateString()}</Text>
                </View>
                <View style={[styles.statusBadge, { backgroundColor: hasAbnormal ? '#FEF2F2' : '#ECFDF5' }]}>
                  <Text style={{ color: hasAbnormal ? '#DC2626' : '#059669', fontSize: 11, fontWeight: '700' }}>
                    {hasAbnormal ? '⚠ Abnormal' : '✓ Normal'}
                  </Text>
                </View>
              </View>
              {isOpen && (
                <View style={styles.testsContainer}>
                  {item.tests.map((test, idx) => {
                    const f = FLAG_STYLE[test.flag || 'N'];
                    return (
                      <View key={idx} style={styles.testRow}>
                        <View style={{ flex: 1 }}>
                          <Text style={styles.testName}>{test.name}</Text>
                          <Text style={styles.testRef}>Ref: {test.reference_range}</Text>
                        </View>
                        <View style={{ alignItems: 'flex-end' }}>
                          <Text style={styles.testValue}>{test.value} <Text style={styles.testUnit}>{test.unit}</Text></Text>
                          <View style={[styles.flagBadge, { backgroundColor: f.bg }]}>
                            <Text style={{ color: f.color, fontSize: 10, fontWeight: '700' }}>{f.text}</Text>
                          </View>
                        </View>
                      </View>
                    );
                  })}
                </View>
              )}
            </TouchableOpacity>
          );
        }}
      />
    </View>
  );
}

const MOCK: LabResult[] = [{
  id: '1', patient_id: 'p1', panel_name: 'Complete Blood Count', collected_at: new Date().toISOString(), status: 'abnormal',
  tests: [
    { name: 'Hemoglobin', value: '11.2', unit: 'g/dL', reference_range: '12.0-17.5', flag: 'L' },
    { name: 'WBC', value: '7.2', unit: 'K/µL', reference_range: '4.5-11.0', flag: 'N' },
    { name: 'Platelets', value: '250', unit: 'K/µL', reference_range: '150-400', flag: 'N' },
  ],
}];

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#FAFAF7' },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: 20, paddingTop: 56 },
  title: { fontSize: 22, fontWeight: '800', color: '#1A1A1A' },
  count: { fontSize: 13, color: '#9CA3AF' },
  card: { margin: 12, marginTop: 0, backgroundColor: '#fff', borderRadius: 16, padding: 16, shadowColor: '#000', shadowOpacity: 0.04, shadowRadius: 8, elevation: 2 },
  cardHeader: { flexDirection: 'row', alignItems: 'center' },
  panelName: { fontSize: 15, fontWeight: '700', color: '#1A1A1A' },
  date: { fontSize: 12, color: '#9CA3AF', marginTop: 2 },
  statusBadge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12 },
  testsContainer: { marginTop: 14, borderTopWidth: 1, borderTopColor: '#F3F4F6', paddingTop: 12, gap: 12 },
  testRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  testName: { fontSize: 13, fontWeight: '600', color: '#374151' },
  testRef: { fontSize: 11, color: '#9CA3AF', marginTop: 1 },
  testValue: { fontSize: 14, fontWeight: '700', color: '#1A1A1A', textAlign: 'right' },
  testUnit: { fontSize: 11, color: '#9CA3AF', fontWeight: '400' },
  flagBadge: { paddingHorizontal: 8, paddingVertical: 2, borderRadius: 8, marginTop: 3 },
});
