import React, { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Text, ActivityIndicator, View } from 'react-native';

import AuthScreen from '../screens/AuthScreen';
import { HomeScreen } from '../screens/HomeScreen';
import AppointmentsScreen from '../screens/AppointmentsScreen';
import PrescriptionsScreen from '../screens/PrescriptionsScreen';
import LabResultsScreen from '../screens/LabResultsScreen';
import NotificationsScreen from '../screens/NotificationsScreen';
import ProfileScreen from '../screens/ProfileScreen';
import MizajAssessmentScreen from '../screens/MizajAssessmentScreen';
import { TeleConsultRoom } from '../screens/TeleConsultRoom';
import { LifestyleTrackerScreen } from '../screens/LifestyleTrackerScreen';
import { getStoredToken } from '../services/auth.service';

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

const ICON: Record<string, string> = {
  Home: '🏠',
  Care: '🌿',
  Appointments: '📅',
  Messages: '💬',
  Profile: '👤',
};

function MainTabs({ onLogout, navigation }: { onLogout: () => void; navigation: any }) {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: () => <Text style={{ fontSize: 20 }}>{ICON[route.name] || '•'}</Text>,
        tabBarActiveTintColor: '#2D6A4F',
        tabBarInactiveTintColor: '#9CA3AF',
        tabBarStyle: {
          backgroundColor: '#0F172A',
          borderTopColor: '#1E293B',
          paddingBottom: 8,
          height: 65,
        },
        tabBarLabelStyle: { fontSize: 11, fontWeight: '600' },
        headerShown: false,
      })}
    >
      <Tab.Screen name="Home">
        {() => (
          <HomeScreen
            onNavigate={(screen: string) => {
              if (screen === 'TeleConsultRoom') navigation.navigate('TeleConsult');
              else if (screen === 'MizajAssessment') navigation.navigate('MizajAssessment');
              else if (screen === 'LifestyleTracker') navigation.navigate('LifestyleTracker');
              else if (screen === 'LabResults') navigation.navigate('LabResults');
              else navigation.navigate(screen);
            }}
          />
        )}
      </Tab.Screen>
      <Tab.Screen name="Care" component={PrescriptionsScreen} />
      <Tab.Screen name="Appointments" component={AppointmentsScreen} />
      <Tab.Screen name="Messages" component={NotificationsScreen} />
      <Tab.Screen name="Profile">
        {() => <ProfileScreen onLogout={onLogout} />}
      </Tab.Screen>
    </Tab.Navigator>
  );
}

export default function AppNavigator() {
  const [auth, setAuth] = useState<boolean | null>(null);

  useEffect(() => {
    getStoredToken().then((t) => setAuth(!!t));
  }, []);

  if (auth === null) {
    return (
      <View
        style={{
          flex: 1,
          justifyContent: 'center',
          alignItems: 'center',
          backgroundColor: '#0A0F1D',
        }}
      >
        <ActivityIndicator size="large" color="#2D6A4F" />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {auth ? (
          <>
            <Stack.Screen name="Main">
              {(props) => <MainTabs {...props} onLogout={() => setAuth(false)} />}
            </Stack.Screen>
            <Stack.Screen name="MizajAssessment">
              {(props) => (
                <MizajAssessmentScreen
                  onBack={() => props.navigation.goBack()}
                  onComplete={() => props.navigation.goBack()}
                />
              )}
            </Stack.Screen>
            <Stack.Screen name="TeleConsult">
              {(props) => (
                <TeleConsultRoom onEndCall={() => props.navigation.goBack()} />
              )}
            </Stack.Screen>
            <Stack.Screen name="LifestyleTracker">
              {(props) => (
                <LifestyleTrackerScreen onBack={() => props.navigation.goBack()} />
              )}
            </Stack.Screen>
            <Stack.Screen name="LabResults" component={LabResultsScreen} />
            <Stack.Screen name="Prescriptions" component={PrescriptionsScreen} />
            <Stack.Screen name="Notifications" component={NotificationsScreen} />
            <Stack.Screen name="Appointments" component={AppointmentsScreen} />
          </>
        ) : (
          <Stack.Screen name="Auth">
            {() => <AuthScreen onAuthSuccess={() => setAuth(true)} />}
          </Stack.Screen>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
