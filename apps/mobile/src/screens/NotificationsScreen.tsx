import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet } from 'react-native';
import type { Notification } from '../types';

const CATEGORIES: Record<string, { icon: string; color: string; bg: string }> = {
  appointment: { icon: '📅', color: '#6366F1', bg: '#EEF2FF' },
  prescription: { icon: '💊', color: '#2D6A4F', bg: '#ECFDF5' },
  lab_result: { icon: '🧪', color: '#D97706', bg: '#FFFBEB' },
  system: { icon: '⚙️', color: '#6B7280', bg: '#F9FAFB' },
};

const API = "http://localhost:8000";

function timeAgo(date: string) {
  const diff = (Date.now() - new Date(date).getTime()) / 1000;
  if (diff < 60) return `${Math.floor(diff)}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

export default function NotificationsScreen() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadNotifications() {
      try {
        const res = await fetch(`${API}/api/v1/qsura/notifications`);
        if (res.ok) {
          const data = await res.json();
          if (data.ok && Array.isArray(data.notifications)) {
            setNotifications(data.notifications.map((n: any) => ({
              id: n.id || n.notification_id || String(Math.random()),
              title: n.template_id || n.channel || "Clinical Alert",
              body: n.message_text || n.body || "New notification from ZAYVORA Care Team",
              category: (n.category || "system") as any,
              read: n.status === "READ" || n.status === "SENT",
              created_at: n.created_at || new Date().toISOString()
            })));
          }
        }
      } catch {
        // Offline or unreachable - empty state rendered cleanly
      } finally {
        setLoading(false);
      }
    }
    loadNotifications();
  }, []);

  const unread = notifications.filter(n => !n.read).length;

  const markRead = (id: string) => setNotifications(prev => prev.map(n => n.id === id ? { ...n, read: true } : n));
  const markAllRead = () => setNotifications(prev => prev.map(n => ({ ...n, read: true })));
  const deleteNotif = (id: string) => setNotifications(prev => prev.filter(n => n.id !== id));

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View>
          <Text style={styles.title}>Notifications</Text>
          {unread > 0 && <Text style={styles.unreadCount}>{unread} unread</Text>}
        </View>
        {unread > 0 && (
          <TouchableOpacity onPress={markAllRead}>
            <Text style={styles.markAllBtn}>Mark all read</Text>
          </TouchableOpacity>
        )}
      </View>

      <FlatList
        data={notifications}
        keyExtractor={item => item.id}
        contentContainerStyle={{ paddingBottom: 32 }}
        ItemSeparatorComponent={() => <View style={styles.divider} />}
        ListEmptyComponent={() => (
          <View style={styles.empty}><Text style={styles.emptyIcon}>🔔</Text><Text style={styles.emptyText}>No notifications</Text></View>
        )}
        renderItem={({ item }) => {
          const cat = CATEGORIES[item.category] || CATEGORIES.system;
          return (
            <TouchableOpacity style={[styles.item, !item.read && styles.itemUnread]} onPress={() => markRead(item.id)}>
              <View style={[styles.iconContainer, { backgroundColor: cat.bg }]}>
                <Text style={styles.icon}>{cat.icon}</Text>
              </View>
              <View style={styles.content}>
                <Text style={[styles.notifTitle, !item.read && styles.notifTitleBold]}>{item.title}</Text>
                <Text style={styles.body} numberOfLines={2}>{item.body}</Text>
                <Text style={styles.time}>{timeAgo(item.created_at)}</Text>
              </View>
              {!item.read && <View style={styles.dot} />}
              <TouchableOpacity onPress={() => deleteNotif(item.id)} style={styles.deleteBtn}>
                <Text style={styles.deleteText}>✕</Text>
              </TouchableOpacity>
            </TouchableOpacity>
          );
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#FAFAF7' },
  header: { flexDirection: 'row', alignItems: 'flex-end', justifyContent: 'space-between', padding: 20, paddingTop: 56 },
  title: { fontSize: 22, fontWeight: '800', color: '#1A1A1A' },
  unreadCount: { fontSize: 12, color: '#9CA3AF', marginTop: 2 },
  markAllBtn: { fontSize: 13, color: '#2D6A4F', fontWeight: '600' },
  divider: { height: 1, backgroundColor: '#F3F4F6', marginLeft: 76 },
  item: { flexDirection: 'row', alignItems: 'center', padding: 16, backgroundColor: '#fff' },
  itemUnread: { backgroundColor: '#F0FDF4' },
  iconContainer: { width: 44, height: 44, borderRadius: 22, alignItems: 'center', justifyContent: 'center', marginRight: 12 },
  icon: { fontSize: 20 },
  content: { flex: 1 },
  notifTitle: { fontSize: 14, color: '#374151', marginBottom: 2 },
  notifTitleBold: { fontWeight: '700', color: '#1A1A1A' },
  body: { fontSize: 13, color: '#6B7280', lineHeight: 18 },
  time: { fontSize: 11, color: '#9CA3AF', marginTop: 4 },
  dot: { width: 8, height: 8, borderRadius: 4, backgroundColor: '#2D6A4F', marginHorizontal: 8 },
  deleteBtn: { padding: 8 },
  deleteText: { color: '#D1D5DB', fontSize: 13 },
  empty: { flex: 1, alignItems: 'center', paddingTop: 80 },
  emptyIcon: { fontSize: 48, marginBottom: 16 },
  emptyText: { fontSize: 15, color: '#9CA3AF' },
});
