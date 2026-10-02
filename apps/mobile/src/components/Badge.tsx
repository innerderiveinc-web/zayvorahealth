import React from 'react';
import { View, Text, StyleSheet, ViewStyle, TextStyle } from 'react-native';

export type BadgeVariant = 'success' | 'warning' | 'error' | 'info' | 'neutral' | 'schedule_e1' | 'ai';

export interface BadgeProps {
  label: string;
  variant?: BadgeVariant;
  style?: ViewStyle;
  textStyle?: TextStyle;
}

export const Badge: React.FC<BadgeProps> = ({
  label,
  variant = 'neutral',
  style,
  textStyle,
}) => {
  const getColors = () => {
    switch (variant) {
      case 'success':
        return { bg: 'rgba(45, 106, 79, 0.25)', border: '#2D6A4F', text: '#53A96E' };
      case 'warning':
        return { bg: 'rgba(217, 119, 6, 0.2)', border: '#D97706', text: '#FBBF24' };
      case 'error':
        return { bg: 'rgba(220, 38, 38, 0.2)', border: '#DC2626', text: '#F87171' };
      case 'info':
        return { bg: 'rgba(37, 99, 235, 0.2)', border: '#2563EB', text: '#60A5FA' };
      case 'schedule_e1':
        return { bg: 'rgba(139, 92, 246, 0.2)', border: '#8B5CF6', text: '#C084FC' };
      case 'ai':
        return { bg: 'rgba(99, 102, 241, 0.2)', border: '#6366F1', text: '#A5B4FC' };
      default:
        return { bg: 'rgba(100, 116, 139, 0.2)', border: '#475569', text: '#94A3B8' };
    }
  };

  const colors = getColors();

  return (
    <View
      style={[
        styles.badge,
        { backgroundColor: colors.bg, borderColor: colors.border },
        style,
      ]}
    >
      <Text style={[styles.text, { color: colors.text }, textStyle]}>{label}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  badge: {
    paddingVertical: 3,
    paddingHorizontal: 8,
    borderRadius: 8,
    borderWidth: 1,
    alignSelf: 'flex-start',
  },
  text: {
    fontSize: 11,
    fontWeight: '700',
    textTransform: 'uppercase',
    letterSpacing: 0.4,
  },
});
