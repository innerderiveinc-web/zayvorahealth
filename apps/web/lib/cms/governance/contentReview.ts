/**
 * ZAYVORA Health™ — Clinical Content Governance & Editorial Review
 * 
 * Strict editorial governance standard:
 * - Every medical assertion or page must have an identifiable clinical author
 * - Mandatory senior clinical reviewer with verified NCISM registration number
 * - Scheduled audit frequency (annual or bi-annual review)
 * - Version control and transparent evidence grading
 */

export type EditorialStatus =
  | "Draft"
  | "Under Clinical Review"
  | "Approved"
  | "Published"
  | "Review Due"
  | "Superseded"
  | "Archived";

export type EvidenceCategory =
  | "GRADE_A_RCT_CONCORDANCE"
  | "GRADE_B_CLINICAL_COHORT"
  | "GRADE_C_CLASSICAL_MONOGRAPH"
  | "OBSERVATIONAL_RWE"
  | "PHARMACOPOEIAL_STANDARD";

export interface ContentEditorialMetadata {
  title: string;
  summary: string;
  author: {
    name: string;
    qualification: string;
    role: string;
  };
  clinicalReviewer: {
    name: string;
    qualification: string;
    ncismRegNumber: string;
    reviewDate: string;
    nextReviewDate: string;
  };
  version: string;
  status: EditorialStatus;
  evidenceCategory: EvidenceCategory;
  evidenceLimitations: string[];
  references: string[];
  lastAuditedAt: string;
  language: "en" | "ur" | "hi";
}

export const INSTITUTIONAL_EDITORIAL_DISCLAIMER =
  "All clinical content published by ZAYVORA Health™ is prepared by healthcare professionals and reviewed by certified clinicians registered under the National Commission for Indian System of Medicine (NCISM) Act 2020. This content is intended for health education and clinical transparency. It does not replace individualized diagnosis and care planning by a certified physician.";

export const STATUTORY_EMERGENCY_ADVISORY =
  "ACUTE EMERGENCY NOTICE: If you or someone in your care experiences severe crushing chest pain, sudden difficulty breathing, slurred speech, facial weakness, or uncontrollable bleeding, immediately call 112 (National Emergency) or proceed to the nearest hospital emergency department.";
