/**
 * ZAYVORA Formulation Intelligence Engine™ (ZFIE)
 * Official TypeScript Contracts & Interfaces
 * System: ZAYVORA Health OS™
 * Doctrine: KNOWLEDGE -> INFERENCE -> EVIDENCE -> SAFETY -> VALIDATION -> CLINICIAN -> ACTION -> OUTCOME
 */

// =============================================================================
// 1. CORE ENUMS & PRIMITIVES (Section 38)
// =============================================================================

export type EvidenceLevel =
  | "E0" // Classical ZKB Canonical Knowledge
  | "E1" // Ethnopharmacological / Historical Observation
  | "E2" // In Silico / Computational Prediction (Hypothesis)
  | "E3" // In Vitro Bioassay Validation
  | "E4" // In Vivo Preclinical Model
  | "E5" // Clinical Trial / Cohort Evidence
  | "E6"; // Real-World Evidence (RWE) / Post-Market Pharmacovigilance

export type EvidenceStatus =
  | "ESTABLISHED"
  | "SUPPORTED"
  | "COMPUTATIONALLY_PREDICTED"
  | "TRADITIONAL_CLAIM"
  | "CONFLICTING"
  | "UNKNOWN";

export type SafetyState =
  | "PASS"
  | "CAUTION"
  | "BLOCK"
  | "UNKNOWN";

export type AnalysisMode =
  | "RESEARCH"
  | "SHADOW"
  | "CLINICAL_CDS";

export type ClaimOrigin =
  | "OBSERVED"
  | "CURATED"
  | "CALCULATED"
  | "PREDICTED"
  | "INFERRED"
  | "UNKNOWN";

export type ValidationStatus =
  | "PROPOSED"
  | "IN_PROGRESS"
  | "VALIDATED"
  | "FALSIFIED"
  | "INCONCLUSIVE"
  | "REPLICATED"
  | "RETIRED";

// =============================================================================
// 2. FORMULATION & TWIN CONTRACTS (Sections 39 & 40)
// =============================================================================

export interface Formulation {
  id: string;
  code: string;
  canonicalName: string;
  traditionalName?: string;
  currentVersionId?: string;
  status:
    | "DRAFT"
    | "PENDING_REVIEW"
    | "APPROVED"
    | "REJECTED"
    | "SUPERSEDED";
  therapeuticObjective?: string;
}

export interface FormulationIngredient {
  mufradId: string;
  botanicalName: string;
  vernacularName?: string;
  ratio: number;
  partUsed: string;
  processingMethod: string;
  sequence?: number;
}

export interface CompoundAssociation {
  compoundId: string;
  canonicalName: string;
  smiles?: string;
  chemicalClass?: string;
  abundance?: number;
  abundanceUnit?: string;
  measurementMethod?: string;
  claimOrigin: ClaimOrigin;
  evidenceId?: string;
}

export interface SafetyIssue {
  ruleCode: string;
  severity: SafetyState;
  description: string;
  recommendation?: string;
  context?: Record<string, unknown>;
}

export interface SafetyAssessment {
  state: SafetyState;
  issues: SafetyIssue[];
  evaluatedRuleVersion: string;
  evaluatedAt: string;
}

export interface ScientificEvidenceProfile {
  establishedMechanisms: number;
  computationalHypotheses: number;
  conflictingSignals: number;
  highestEvidenceLevel: EvidenceLevel;
  profileScore: number;
  evidenceBreakdown: Record<EvidenceLevel, number>;
}

export interface ValidationSummary {
  hypothesesCount: number;
  activeExperiments: number;
  validatedCount: number;
  falsifiedCount: number;
  status: ValidationStatus;
}

export interface ExposureProfile {
  suggestedDoseRange?: string;
  routeOfAdministration?: string;
  cypInteractions?: string[];
  bioavailabilityModifiers?: string[];
}

export interface ComputationalFormulationTwin {
  formulationId: string;
  formulationVersionId: string;
  revisionHash: string;

  identity: {
    canonicalName: string;
    traditionalName?: string;
    traditionalSystem?: string;
    classicalSources: string[];
  };

  ingredients: FormulationIngredient[];

  manufacturing: {
    batchIds: string[];
  };

  chemistry: {
    compounds: CompoundAssociation[];
    markers: string[];
    fingerprintIds: string[];
  };

  biology: {
    targets: string[];
    pathways: string[];
    biologicalStates: string[];
    organAxes: string[];
  };

  exposure?: ExposureProfile;

  safety: SafetyAssessment;

  evidence: ScientificEvidenceProfile;

  validation: ValidationSummary;
}

// =============================================================================
// 3. FINDING & CONTRADICTION CONTRACTS (Section 41)
// =============================================================================

export interface ZFIEFinding {
  findingId: string;
  subjectId: string;
  subjectVersion: string;
  statement: string;
  origin: ClaimOrigin;
  evidenceStatus: EvidenceStatus;
  evidenceLevel: EvidenceLevel;
  evidenceIds: string[];
  confidence?: {
    traditional?: string;
    chemical?: string;
    biological?: string;
    clinical?: string;
  };
  uncertaintyScore?: number;
  falsificationCriteria?: string;
  metadata?: Record<string, unknown>;
}

export interface Contradiction {
  contradictionId: string;
  subjectType: string;
  subjectId: string;
  evidenceAId: string;
  evidenceBId: string;
  type: string;
  possibleExplanations: string[];
  status: "OPEN" | "INVESTIGATING" | "RESOLVED" | "ACCEPTED_PARADOX";
  resolution?: string;
  reviewerId?: string;
  detectedAt: string;
}

// =============================================================================
// 4. ANALYSIS REQUEST & RESULT (Sections 42 & 43)
// =============================================================================

export interface FormulationAnalysisRequest {
  formulationId: string;
  formulationVersionId?: string;
  batchId?: string;
  biologicalObjective?: string;
  mode: AnalysisMode;
  requestedDomains: (
    | "CHEMISTRY"
    | "MOLECULAR"
    | "NETWORK"
    | "EXPOSURE"
    | "SAFETY"
    | "EVIDENCE"
    | "CONTRADICTION"
    | "SYNERGY"
    | "BIOLOGICAL_STATE"
  )[];
  requestedBy: string;
}

export interface FormulationAnalysisResult {
  analysisId: string;
  formulationId: string;
  formulationVersionId: string;
  batchId?: string;
  status:
    | "QUEUED"
    | "RUNNING"
    | "PARTIAL"
    | "COMPLETED"
    | "FAILED"
    | "STALE";
  findings: ZFIEFinding[];
  safety: SafetyAssessment;
  contradictions: Contradiction[];
  evidenceProfile: ScientificEvidenceProfile;
  knowledgeSnapshotId: string;
  modelVersions: Record<string, string>;
  createdAt: string;
  completedAt?: string;
}

// =============================================================================
// 5. HAKEEM SAHAB CLINICAL RESPONSE CONTRACT (Sections 45 & 53)
// =============================================================================

export interface EvidenceSummary {
  evidenceId: string;
  citation: string;
  level: EvidenceLevel;
  direction: string;
}

export interface BiologicalContextEntry {
  state: string;
  status: EvidenceStatus;
}

export interface HakeemZFIEResponse {
  clinicalObjective: string;
  biologicalContext: BiologicalContextEntry[];
  relevantMechanisms: ZFIEFinding[];
  evidence: EvidenceSummary[];
  safety: SafetyAssessment;
  contradictions: Contradiction[];
  unknowns: string[];
  clinicalConsiderations: string[];
  requiresClinicianReview: true;
  autonomousActionAllowed: false;
  approval: {
    required: true;
    approvedBy?: string;
    approvedAt?: string;
  };
}

// =============================================================================
// 6. EVENT & AGENT CONTRACTS (Sections 54 & 57)
// =============================================================================

export type ZFIEEventType =
  | "FORMULATION_CREATED"
  | "FORMULATION_VERSION_CREATED"
  | "BATCH_REGISTERED"
  | "FINGERPRINT_CREATED"
  | "COMPOUND_MAPPED"
  | "TARGET_ASSOCIATION_CREATED"
  | "PATHWAY_ASSOCIATION_CREATED"
  | "EVIDENCE_ATTACHED"
  | "HYPOTHESIS_CREATED"
  | "CONTRADICTION_DETECTED"
  | "SAFETY_CHECK_COMPLETED"
  | "EXPERIMENT_CREATED"
  | "EXPERIMENT_RESULT_RECORDED"
  | "VALIDATION_CHANGED"
  | "AI_ANALYSIS_COMPLETED"
  | "CLINICIAN_REVIEWED"
  | "OUTCOME_RECORDED";

export interface ZFIEEvent {
  eventId: string;
  eventType: ZFIEEventType;
  entityType: string;
  entityId: string;
  entityVersion?: string;
  actorId: string;
  actorType: "USER" | "SYSTEM" | "AI_AGENT";
  modelVersion?: string;
  knowledgeVersion?: string;
  correlationId: string;
  timestamp: string;
  payloadHash?: string;
  details?: Record<string, unknown>;
}

export type AgentType =
  | "LITERATURE_CURATOR"
  | "ENTITY_RESOLUTION"
  | "EVIDENCE_AUDITOR"
  | "MECHANISM_ANALYST"
  | "SYNERGY_ANALYST"
  | "SAFETY_ANALYST"
  | "FORMULATION_COPILOT"
  | "VALIDATION_PLANNER";

export interface AgentTask {
  taskId: string;
  agentType: AgentType;
  subjectId: string;
  knowledgeSnapshotId: string;
  permissions: string[];
  input: unknown;
}
