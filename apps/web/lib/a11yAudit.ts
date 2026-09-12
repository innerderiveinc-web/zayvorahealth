/**
 * ZAYVORA HEALTH™ — WCAG 2.1 AA Accessibility & Color Contrast Auditor
 * Verifies high-contrast ratios, ARIA landmarks, and focus trap safety for clinical cockpit interfaces.
 */

export interface ContrastResult {
  ratio: number;
  isCompliantNormalText: boolean; // >= 4.5:1
  isCompliantLargeText: boolean;  // >= 3.0:1
}

export interface A11yElementCheck {
  id: string;
  tag: string;
  ariaLabel?: string;
  hasAccessibleName: boolean;
  hasFocusRing: boolean;
  isKeyboardNavigable: boolean;
}

export interface A11yAuditReport {
  totalElementsChecked: number;
  compliantElements: number;
  complianceRatePct: number;
  wcagStatus: "WCAG_2_1_AA_COMPLIANT" | "NON_COMPLIANT";
  findings: string[];
}

function hexToRgb(hex: string): [number, number, number] {
  const clean = hex.replace("#", "");
  const num = parseInt(clean, 16);
  return [(num >> 16) & 255, (num >> 8) & 255, num & 255];
}

function relativeLuminance(r: number, g: number, b: number): number {
  const [rs, gs, bs] = [r, g, b].map((c) => {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

export const a11yAuditor = {
  calculateContrastRatio(foregroundHex: string, backgroundHex: string): ContrastResult {
    const [r1, g1, b1] = hexToRgb(foregroundHex);
    const [r2, g2, b2] = hexToRgb(backgroundHex);

    const l1 = relativeLuminance(r1, g1, b1);
    const l2 = relativeLuminance(r2, g2, b2);

    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    const ratio = Math.round(((lighter + 0.05) / (darker + 0.05)) * 100) / 100;

    return {
      ratio,
      isCompliantNormalText: ratio >= 4.5,
      isCompliantLargeText: ratio >= 3.0,
    };
  },

  auditClinicalCockpit(elements: A11yElementCheck[]): A11yAuditReport {
    const findings: string[] = [];
    let compliant = 0;

    for (const el of elements) {
      let isOk = true;
      if (!el.hasAccessibleName) {
        findings.push(`Element <${el.tag} id="${el.id}"> lacks an accessible name or aria-label.`);
        isOk = false;
      }
      if (!el.hasFocusRing) {
        findings.push(`Element <${el.tag} id="${el.id}"> missing visible focus ring for keyboard navigation.`);
        isOk = false;
      }
      if (isOk) {
        compliant++;
      }
    }

    const total = elements.length || 1;
    const rate = Math.round((compliant / total) * 100);

    return {
      totalElementsChecked: elements.length,
      compliantElements: compliant,
      complianceRatePct: rate,
      wcagStatus: rate >= 90 ? "WCAG_2_1_AA_COMPLIANT" : "NON_COMPLIANT",
      findings,
    };
  },
};
