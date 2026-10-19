/** @type {import('tailwindcss').Config} */

/**
 * ZAYVORA Health OS – Shared Tailwind Configuration
 *
 * Brand tokens derived from the Unani / Islamic healing aesthetic:
 *  - Primary: Unani green  (#2D6A4F)
 *  - Secondary: Deep teal  (#1B4332)
 *  - Accent: Warm gold     (#F4A261)
 *  - Background: Cream     (#FAFAF7)
 *  - Text: Dark charcoal   (#1A1A1A)
 */

module.exports = {
  content: [
    './src/**/*.{ts,tsx,js,jsx}',
    // Allow consuming apps to reference this config
    '../../apps/**/*.{ts,tsx,js,jsx}',
  ],

  theme: {
    extend: {
      // ── Brand Colours ──────────────────────────────────────────────
      colors: {
        brand: {
          primary: {
            DEFAULT: '#2D6A4F',
            50:  '#EAF4EE',
            100: '#C5E2CF',
            200: '#9FCFAF',
            300: '#79BC8E',
            400: '#53A96E',
            500: '#2D6A4F',
            600: '#255840',
            700: '#1D4632',
            800: '#143424',
            900: '#0C2216',
          },
          secondary: {
            DEFAULT: '#1B4332',
            50:  '#E6EEE9',
            100: '#B9CFC3',
            200: '#8BB09D',
            300: '#5E9177',
            400: '#307251',
            500: '#1B4332',
            600: '#163829',
            700: '#112C20',
            800: '#0B2016',
            900: '#06140D',
          },
          accent: {
            DEFAULT: '#F4A261',
            50:  '#FEF5EC',
            100: '#FBE0C5',
            200: '#F9CB9E',
            300: '#F7B678',
            400: '#F4A261',
            500: '#F28B40',
            600: '#E07028',
            700: '#B85920',
            800: '#904318',
            900: '#682E10',
          },
        },
        background: {
          DEFAULT: '#FAFAF7',
          muted: '#F3F3EE',
          subtle: '#EBEBЕ5',
        },
        text: {
          DEFAULT:  '#1A1A1A',
          muted:    '#6B7280',
          inverted: '#FAFAF7',
        },
        status: {
          success: { DEFAULT: '#2D6A4F', light: '#EAF4EE' },
          warning: { DEFAULT: '#D97706', light: '#FEF3C7' },
          error:   { DEFAULT: '#DC2626', light: '#FEE2E2' },
          info:    { DEFAULT: '#2563EB', light: '#DBEAFE' },
          neutral: { DEFAULT: '#6B7280', light: '#F3F4F6' },
        },
      },

      // ── Typography ─────────────────────────────────────────────────
      fontFamily: {
        sans:    ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        display: ['Amiri', 'Georgia', 'serif'],   // Urdu / Arabic script
      },

      // ── Border Radius ──────────────────────────────────────────────
      borderRadius: {
        sm:   '4px',
        md:   '8px',
        lg:   '12px',
        xl:   '16px',
        '2xl':'24px',
        full: '9999px',
      },

      // ── Box Shadows ────────────────────────────────────────────────
      boxShadow: {
        card:         '0 1px 3px 0 rgb(0 0 0 / 0.08), 0 1px 2px -1px rgb(0 0 0 / 0.06)',
        'card-hover': '0 4px 12px 0 rgb(0 0 0 / 0.12), 0 2px 4px -1px rgb(0 0 0 / 0.08)',
        modal:        '0 20px 48px -8px rgb(0 0 0 / 0.24), 0 8px 16px -4px rgb(0 0 0 / 0.12)',
        'inner-sm':   'inset 0 1px 2px 0 rgb(0 0 0 / 0.06)',
        'focus-ring': '0 0 0 3px rgb(45 106 79 / 0.30)',
      },

      // ── Spacing extras ─────────────────────────────────────────────
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128':'32rem',
      },
    },
  },

  plugins: [],
};
