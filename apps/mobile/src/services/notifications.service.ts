/**
 * ZAYVORA Health OS™ Mobile Push & Local Notification Service
 * Handles Expo push token registration, daily dosage alerts, and tele-consult reminders.
 */

import { Platform } from 'react-native';

export interface PushTokenResult {
  token: string | null;
  error?: string;
}

export interface NotificationPayload {
  title: string;
  body: string;
  data?: Record<string, any>;
  categoryIdentifier?: 'APPOINTMENT' | 'POSOLOGY' | 'LAB_RESULT' | 'SYSTEM';
}

/**
 * Register device for push notifications
 */
export async function registerForPushNotificationsAsync(): Promise<PushTokenResult> {
  try {
    // If running in Expo environment with expo-notifications
    let Notifications: any = null;
    try {
      Notifications = require('expo-notifications');
    } catch {
      // Mock / fallback if native module not compiled
      return { token: 'mock-expo-push-token-zayvora-mobile' };
    }

    if (Platform.OS === 'android') {
      await Notifications.setNotificationChannelAsync('default', {
        name: 'ZAYVORA Default',
        importance: Notifications.AndroidImportance.MAX,
        vibrationPattern: [0, 250, 250, 250],
        lightColor: '#2D6A4F',
      });
    }

    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;
    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }

    if (finalStatus !== 'granted') {
      return { token: null, error: 'Permission not granted for push notifications' };
    }

    const tokenData = await Notifications.getExpoPushTokenAsync();
    return { token: tokenData.data };
  } catch (err: any) {
    return { token: null, error: err.message || 'Notification setup error' };
  }
}

/**
 * Schedule a local posology dosage reminder
 */
export async function scheduleDosageReminder(
  medicineName: string,
  dosageText: string,
  secondsFromNow: number
): Promise<string> {
  try {
    const Notifications = require('expo-notifications');
    const id = await Notifications.scheduleNotificationAsync({
      content: {
        title: `🌿 ZAYVORA Regimen: ${medicineName}`,
        body: `Time to take your scheduled dose: ${dosageText}`,
        sound: true,
        data: { type: 'POSOLOGY', medicineName },
      },
      trigger: {
        seconds: Math.max(secondsFromNow, 1),
      },
    });
    return id;
  } catch {
    console.log(`[Scheduled Reminder] ${medicineName} in ${secondsFromNow}s`);
    return `mock-timer-${Date.now()}`;
  }
}

/**
 * Register push token with ZAYVORA Gateway / Identity service
 */
export async function syncPushTokenWithServer(token: string, userId: string): Promise<boolean> {
  try {
    const gateway = process.env.EXPO_PUBLIC_GATEWAY_URL || 'http://localhost:8000';
    const res = await fetch(`${gateway}/api/v1/auth/push-token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, push_token: token, platform: Platform.OS }),
    });
    return res.ok;
  } catch {
    return false;
  }
}
