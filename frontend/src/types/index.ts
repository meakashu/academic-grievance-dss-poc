/**
 * TypeScript type definitions for Academic Grievance DSS
 */

export enum GrievanceType {
    ATTENDANCE_SHORTAGE = 'ATTENDANCE_SHORTAGE',
    EXAMINATION_REEVAL = 'EXAMINATION_REEVAL',
    GRADE_APPEAL = 'GRADE_APPEAL',
    FEE_WAIVER = 'FEE_WAIVER',
    FEE_INSTALLMENT_REQUEST = 'FEE_INSTALLMENT_REQUEST',
    TRANSCRIPT_DELAY = 'TRANSCRIPT_DELAY',
    OTHER = 'OTHER'
}

export enum GrievanceStatus {
    PENDING = 'PENDING',
    UNDER_REVIEW = 'UNDER_REVIEW',
    RESOLVED = 'RESOLVED',
    REJECTED = 'REJECTED',
    PENDING_CLARIFICATION = 'PENDING_CLARIFICATION'
}

export enum DecisionOutcome {
    ACCEPT = 'ACCEPT',
    REJECT = 'REJECT',
    PARTIAL_ACCEPT = 'PARTIAL_ACCEPT',
    PENDING_CLARIFICATION = 'PENDING_CLARIFICATION'
}

export enum HierarchyLevel {
    L1_NATIONAL = 'L1_National',
    L2_ACCREDITATION = 'L2_Accreditation',
    L3_UNIVERSITY = 'L3_University'
}

export interface Grievance {
    id: string;
    student_id: string;
    grievance_type: GrievanceType;
    narrative: string;
    parameters: Record<string, any>;
    status: GrievanceStatus;
    submitted_at: string;
    created_at: string;
    updated_at: string;
}

export interface GrievanceCreate {
    student_id: string;
    grievance_type: GrievanceType;
    narrative: string;
    parameters: Record<string, any>;
}

export interface Decision {
    id: string;
    grievance_id: string;
    outcome: DecisionOutcome;
    applicable_rule: string;
    regulatory_source: string;
    hierarchy_level: HierarchyLevel;
    salience: number;
    reason: string;
    explanation?: string;
    action_required?: string;
    human_review_required: boolean;
    decided_at: string;
    created_at: string;
}

export interface ConditionCheck {
    condition: string;
    satisfied: boolean;
    value?: any;
}

export interface FiredRuleInfo {
    rule_id: string;
    hierarchy_level: string;
    salience: number;
    conditions_checked?: ConditionCheck[];
    fired?: boolean;
    outcome?: string;
    reason?: string;
    source?: string;
    timestamp?: string;
}

export interface ConflictInfo {
    type: string;
    conflicting_rules: string[];
    resolution_strategy: string;
    winning_rule: string;
    reason: string;
}

export interface RuleTrace {
    id: string;
    grievance_id: string;
    decision_id?: string;
    rules_evaluated: FiredRuleInfo[];
    conflicts_detected: ConflictInfo[];
    final_decision: Record<string, any>;
    processing_time_ms: number;
    created_at: string;
}

export interface AmbiguousTerm {
    term: string;
    type: 'subjective' | 'permissive' | 'context-dependent';
    reason: string;
}

export interface AmbiguityReport {
    requires_human_review: boolean;
    ambiguous_terms_count: number;
    clarification_questions: string[];
}

export interface FairnessReport {
    grievance_id: string;
    consistency_score: number;
    consistency_threshold: number;
    meets_threshold: boolean;
    anomaly_detected: boolean;
    anomaly_reason?: string;
    similar_cases_count: number;
    similar_cases: Array<{
        grievance_id: string;
        outcome: string;
        applicable_rule: string;
        hierarchy_level: string;
    }>;
    recommendation: string;
}

export interface GrievanceSubmissionResponse {
    success: boolean;
    message: string;
    grievance_id: string;
    decision?: Decision;
    trace?: {
        trace_id: string;
        rules_fired: number;
        conflicts_detected: number;
        processing_time_ms: number;
    };
    ambiguity?: AmbiguityReport;
    fairness?: FairnessReport;
}

export interface APIResponse<T = any> {
    success: boolean;
    message?: string;
    data?: T;
    error?: string;
}
