/**
 * Decision Display Component
 * Shows the decision outcome with explanation and regulatory source
 */
import React from 'react';
import { Decision, DecisionOutcome, HierarchyLevel } from '../types';
import './DecisionDisplay.css';

interface DecisionDisplayProps {
    decision: Decision;
}

const DecisionDisplay: React.FC<DecisionDisplayProps> = ({ decision }) => {
    const getOutcomeBadgeClass = (outcome: DecisionOutcome): string => {
        switch (outcome) {
            case DecisionOutcome.ACCEPT:
                return 'badge-success';
            case DecisionOutcome.REJECT:
                return 'badge-error';
            case DecisionOutcome.PARTIAL_ACCEPT:
                return 'badge-warning';
            case DecisionOutcome.PENDING_CLARIFICATION:
                return 'badge-info';
            default:
                return 'badge-info';
        }
    };

    const getHierarchyColor = (level: HierarchyLevel): string => {
        switch (level) {
            case HierarchyLevel.L1_NATIONAL:
                return '#ef4444'; // Red
            case HierarchyLevel.L2_ACCREDITATION:
                return '#f59e0b'; // Orange
            case HierarchyLevel.L3_UNIVERSITY:
                return '#3b82f6'; // Blue
            default:
                return '#6b7280'; // Gray
        }
    };

    const getHierarchyLabel = (level: HierarchyLevel): string => {
        switch (level) {
            case HierarchyLevel.L1_NATIONAL:
                return 'National Law';
            case HierarchyLevel.L2_ACCREDITATION:
                return 'Accreditation Standard';
            case HierarchyLevel.L3_UNIVERSITY:
                return 'University Statute';
            default:
                return level;
        }
    };

    return (
        <div className="decision-display">
            <div className="card">
                <div className="card-header">
                    <div className="decision-header">
                        <h2 className="card-title">Decision</h2>
                        <span className={`badge ${getOutcomeBadgeClass(decision.outcome)}`}>
                            {decision.outcome.replace('_', ' ')}
                        </span>
                    </div>
                </div>

                <div className="card-body">
                    {/* Hierarchy Level */}
                    <div className="decision-section">
                        <h3 className="section-title">Regulatory Authority</h3>
                        <div className="hierarchy-badge" style={{ borderLeftColor: getHierarchyColor(decision.hierarchy_level) }}>
                            <div className="hierarchy-level">{getHierarchyLabel(decision.hierarchy_level)}</div>
                            <div className="hierarchy-salience">Priority: {decision.salience}</div>
                        </div>
                    </div>

                    {/* Applicable Rule */}
                    <div className="decision-section">
                        <h3 className="section-title">Applicable Rule</h3>
                        <div className="rule-info">
                            <code className="rule-id">{decision.applicable_rule}</code>
                            <p className="rule-source">{decision.regulatory_source}</p>
                        </div>
                    </div>

                    {/* Reason */}
                    <div className="decision-section">
                        <h3 className="section-title">Reason</h3>
                        <p className="decision-reason">{decision.reason}</p>
                    </div>

                    {/* Explanation */}
                    {decision.explanation && (
                        <div className="decision-section">
                            <h3 className="section-title">Detailed Explanation</h3>
                            <div className="explanation-box">
                                <p>{decision.explanation}</p>
                            </div>
                        </div>
                    )}

                    {/* Action Required */}
                    {decision.action_required && (
                        <div className="decision-section">
                            <div className="alert alert-info">
                                <h4 style={{ marginTop: 0 }}>Action Required</h4>
                                <p style={{ marginBottom: 0 }}>{decision.action_required}</p>
                            </div>
                        </div>
                    )}

                    {/* Human Review Flag */}
                    {decision.human_review_required && (
                        <div className="decision-section">
                            <div className="alert alert-warning">
                                <h4 style={{ marginTop: 0 }}>⚠️ Human Review Required</h4>
                                <p style={{ marginBottom: 0 }}>
                                    This decision requires human review due to ambiguity or exceptional circumstances.
                                    A committee member will review your case shortly.
                                </p>
                            </div>
                        </div>
                    )}

                    {/* Metadata */}
                    <div className="decision-metadata">
                        <div className="metadata-item">
                            <span className="metadata-label">Decision ID:</span>
                            <span className="metadata-value">{decision.id}</span>
                        </div>
                        <div className="metadata-item">
                            <span className="metadata-label">Decided At:</span>
                            <span className="metadata-value">
                                {new Date(decision.decided_at).toLocaleString()}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DecisionDisplay;
