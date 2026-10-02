/**
 * ZAYVORA Health OS™ — Centralized Design System Public API
 * Single source of truth for foundation tokens, primitive UI components,
 * and specialized clinical components.
 */

// ── Foundational UI Components ──────────────────────────────────────────────
export { Button }              from './components/Button';
export { Card }                from './components/Card';
export { Badge }               from './components/Badge';
export { Input }               from './components/Input';
export { Modal, ModalBody, ModalFooter } from './components/Modal';
export { Spinner }             from './components/Spinner';
export { Textarea }            from './components/Textarea';
export { Select }              from './components/Select';
export { Tabs }                from './components/Tabs';
export { Alert }               from './components/Alert';
export { LoadingSkeleton }     from './components/LoadingSkeleton';
export { EmptyState }          from './components/EmptyState';
export { ConfirmationDialog }  from './components/ConfirmationDialog';
export { Breadcrumb }          from './components/Breadcrumb';
export { Stepper }             from './components/Stepper';
export { Timeline }            from './components/Timeline';
export { Avatar }              from './components/Avatar';
export { Switch }              from './components/Switch';

// ── Foundational UI Primitives ───────────────────────────────────────────────
export { Drawer }              from './primitives/Drawer';
export { Search }              from './primitives/Search';
export { Tooltip }             from './primitives/Tooltip';
export { Toast, ToastContainer } from './primitives/Toast';
export { Table }               from './primitives/Table';
export { Progress }            from './primitives/Progress';
export { ErrorState }          from './primitives/ErrorState';
export { OfflineState }        from './primitives/OfflineState';
export { ForbiddenState }      from './primitives/ForbiddenState';

// ── Specialized Clinical Components ─────────────────────────────────────────
export { ClinicalStatus }      from './components/ClinicalStatus';
export { PrescriptionItem }    from './components/PrescriptionItem';
export { AppointmentItem }     from './components/AppointmentItem';
export { PatientHeader }       from './clinical/PatientHeader';
export { ClinicalThread, DEFAULT_CLINICAL_THREAD_STAGES } from './clinical/ClinicalThread';
export { AttentionFeed }       from './clinical/AttentionFeed';
export { MizajStatus }         from './clinical/MizajStatus';
export { AxisRow }             from './clinical/AxisRow';
export { AxisDetail }          from './clinical/AxisDetail';
export { EvidenceCard }        from './clinical/EvidenceCard';
export { EvidenceDrawer }      from './clinical/EvidenceDrawer';
export { SafetyRail }          from './clinical/SafetyRail';
export { SafetyDecision }      from './clinical/SafetyDecision';
export { HakeemInsight }       from './clinical/HakeemInsight';
export { KnowledgeProvenance } from './clinical/KnowledgeProvenance';
export { TrustLedger }         from './clinical/TrustLedger';
export { NuskhaComposer }      from './clinical/NuskhaComposer';
export { NuskhaPreflight, DEFAULT_PREFLIGHT_CHECKS } from './clinical/NuskhaPreflight';
export { ApprovalPanel }       from './clinical/ApprovalPanel';
export { SignatureSummary }    from './clinical/SignatureSummary';
export { CareProgressRibbon, DEFAULT_CARE_STEPS } from './clinical/CareProgressRibbon';
export { OutcomeCard }         from './clinical/OutcomeCard';
export { AdherenceCard }       from './clinical/AdherenceCard';
export { DataFreshness }       from './clinical/DataFreshness';
export { ConsentStatus }       from './clinical/ConsentStatus';

// ── Component & Model Types ─────────────────────────────────────────────────
export type { ButtonProps, ButtonVariant, ButtonSize }   from './components/Button';
export type { CardProps, CardShadow }                    from './components/Card';
export type { BadgeProps, BadgeVariant, BadgeSize }      from './components/Badge';
export type { InputProps, InputSize }                    from './components/Input';
export type { ModalProps, ModalSize, ModalSectionProps } from './components/Modal';
export type { SpinnerProps, SpinnerSize, SpinnerVariant } from './components/Spinner';
export type { TextareaProps }                            from './components/Textarea';
export type { SelectProps, SelectOption }                from './components/Select';
export type { TabsProps, TabItem }                       from './components/Tabs';
export type { AlertProps, AlertVariant }                 from './components/Alert';
export type { LoadingSkeletonProps }                     from './components/LoadingSkeleton';
export type { EmptyStateProps }                          from './components/EmptyState';
export type { ConfirmationDialogProps }                  from './components/ConfirmationDialog';
export type { BreadcrumbProps, BreadcrumbItem }          from './components/Breadcrumb';
export type { StepperProps, StepItem }                   from './components/Stepper';
export type { TimelineProps, TimelineEvent }             from './components/Timeline';
export type { AvatarProps }                              from './components/Avatar';
export type { SwitchProps }                              from './components/Switch';
export type { ClinicalStatusProps, ClinicalMizaj }       from './components/ClinicalStatus';
export type { PrescriptionItemProps }                    from './components/PrescriptionItem';
export type { AppointmentItemProps }                     from './components/AppointmentItem';

export type { DrawerProps, DrawerPlacement, DrawerSize } from './primitives/Drawer';
export type { SearchProps }                              from './primitives/Search';
export type { TooltipProps, TooltipPlacement }           from './primitives/Tooltip';
export type { ToastProps, ToastContainerProps, ToastVariant } from './primitives/Toast';
export type { TableProps, Column }                       from './primitives/Table';
export type { ProgressProps, ProgressVariant, ProgressSize } from './primitives/Progress';
export type { ErrorStateProps }                          from './primitives/ErrorState';
export type { OfflineStateProps }                        from './primitives/OfflineState';
export type { ForbiddenStateProps }                      from './primitives/ForbiddenState';

export type { PatientHeaderProps }                       from './clinical/PatientHeader';
export type { ClinicalThreadProps, ClinicalThreadStageId, ClinicalStageDef } from './clinical/ClinicalThread';
export type { AttentionFeedProps, AttentionItem, NextPatientSummary } from './clinical/AttentionFeed';
export type { MizajStatusProps, MizajType }              from './clinical/MizajStatus';
export type { AxisRowProps }                             from './clinical/AxisRow';
export type { AxisDetailProps, AxisMetric }              from './clinical/AxisDetail';
export type { EvidenceCardProps, GradeLevel }            from './clinical/EvidenceCard';
export type { EvidenceDrawerProps, EvidenceDrawerData }  from './clinical/EvidenceDrawer';
export type { SafetyRailProps, SafetyRailStatus, SafetyCheck } from './clinical/SafetyRail';
export type { SafetyDecisionProps }                      from './clinical/SafetyDecision';
export type { HakeemInsightProps, ClassicalCitation }    from './clinical/HakeemInsight';
export type { KnowledgeProvenanceProps, KnowledgeTier }  from './clinical/KnowledgeProvenance';
export type { TrustLedgerProps }                         from './clinical/TrustLedger';
export type { NuskhaComposerProps, NuskhaItem }          from './clinical/NuskhaComposer';
export type { NuskhaPreflightProps, PreflightCheckItem } from './clinical/NuskhaPreflight';
export type { ApprovalPanelProps }                       from './clinical/ApprovalPanel';
export type { SignatureSummaryProps }                    from './clinical/SignatureSummary';
export type { CareProgressRibbonProps, CareProgressStep } from './clinical/CareProgressRibbon';
export type { OutcomeCardProps, OutcomeMetric }          from './clinical/OutcomeCard';
export type { AdherenceCardProps, AdherenceItem, AdherenceStatus } from './clinical/AdherenceCard';
export type { DataFreshnessProps, FreshnessState }       from './clinical/DataFreshness';
export type { ConsentStatusProps, ConsentLevel }         from './clinical/ConsentStatus';
