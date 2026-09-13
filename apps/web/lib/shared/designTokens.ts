/**
 * ZAYVORA OS — Unified Design Tokens
 * Shared across Web App, Mobile App, and Public Website.
 */

export const ZAYVORA_TOKENS = {
  colors: {
    // Primary Brand Palette
    botanicalGreen: "#064E3B", // Deep Forest / Primary Leadership
    botanicalGreenDark: "#022C22",
    botanicalGreenLight: "#065F46",

    clinicalTeal: "#0D9488", // Primary Interactive Teal
    clinicalTealHover: "#14B8A6",
    clinicalTealLight: "rgba(13, 148, 136, 0.15)",

    sageGreen: "#10B981", // Secondary Natural Green / Success
    sageGreenLight: "rgba(16, 185, 129, 0.15)",

    warmIvory: "#FEF3C7", // Classical Parchment Accent
    warmIvoryDark: "#FDE68A",
    warmIvoryText: "#92400E",

    mutedGold: "#D97706", // Unani Classical Accents & Signatures
    mutedGoldLight: "rgba(217, 119, 6, 0.15)",

    // Neutral Slate Palette (Dark Theme / Clinical SaaS)
    bgBase: "#0A0F1D", // Deep clinical background
    bgSurface: "#0F172A", // Primary panel / card surface
    bgElevated: "#1E293B", // Elevated cards & modals
    bgElevatedHover: "#334155",

    borderDefault: "#334155",
    borderSubtle: "#1E293B",
    borderFocus: "#0D9488",

    // Typography
    textPrimary: "#F8FAFC",
    textSecondary: "#CBD5E1",
    textMuted: "#94A3B8",
    textSubtle: "#64748B",

    // Status Colors
    statusSuccess: "#10B981",
    statusWarning: "#F59E0B",
    statusDanger: "#EF4444",
    statusInfo: "#3B82F6",
    statusResearch: "#8B5CF6",
  },
  typography: {
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    fontSize: {
      xs: "0.75rem",     // 12px
      sm: "0.875rem",    // 14px
      base: "1rem",       // 16px
      lg: "1.125rem",    // 18px
      xl: "1.25rem",     // 20px
      "2xl": "1.5rem",   // 24px
      "3xl": "1.875rem", // 30px
      "4xl": "2.25rem",  // 36px
    },
    fontWeight: {
      normal: "400",
      medium: "500",
      semibold: "600",
      bold: "700",
      extrabold: "800",
    }
  },
  radii: {
    sm: "0.375rem", // 6px
    md: "0.5rem",   // 8px
    lg: "0.75rem",  // 12px
    xl: "1rem",     // 16px
    "2xl": "1.25rem",// 20px
    "3xl": "1.5rem", // 24px
    full: "9999px",
  },
  shadows: {
    sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    md: "0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.1)",
    lg: "0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.15)",
    tealGlow: "0 4px 20px -2px rgba(13, 148, 136, 0.25)",
  }
} as const;
