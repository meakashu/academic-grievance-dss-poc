/**
 * Main App Component
 * Academic Grievance Decision Support System
 */
import React, { useState } from 'react';
import GrievanceForm from './components/GrievanceForm';
import DecisionDisplay from './components/DecisionDisplay';
import { GrievanceSubmissionResponse } from './types';
import './App.css';

function App() {
    const [submissionResponse, setSubmissionResponse] = useState<GrievanceSubmissionResponse | null>(null);
    const [showForm, setShowForm] = useState(true);

    const handleSubmitSuccess = (response: GrievanceSubmissionResponse) => {
        setSubmissionResponse(response);
        setShowForm(false);
    };

    const handleNewGrievance = () => {
        setSubmissionResponse(null);
        setShowForm(true);
    };

    return (
        <div className="app">
            {/* Header */}
            <header className="app-header">
                <div className="container">
                    <h1 className="app-title">Academic Grievance Decision Support System</h1>
                    <p className="app-subtitle">
                        Rule-based, Hierarchy-aware, Explainable Decision Making
                    </p>
                </div>
            </header>

            {/* Main Content */}
            <main className="app-main">
                <div className="container">
                    {showForm ? (
                        <GrievanceForm onSubmitSuccess={handleSubmitSuccess} />
                    ) : (
                        <>
                            {/* Success Message */}
                            <div className="success-container">
                                <div className="alert alert-success">
                                    <h3 style={{ marginTop: 0 }}>✓ Grievance Submitted Successfully</h3>
                                    <p style={{ marginBottom: 0 }}>
                                        Your grievance has been processed. Review the decision below.
                                    </p>
                                </div>
                            </div>

                            {/* Decision */}
                            {submissionResponse?.decision && (
                                <DecisionDisplay decision={submissionResponse.decision} />
                            )}

                            {/* Trace Summary */}
                            {submissionResponse?.trace && (
                                <div className="trace-summary card">
                                    <div className="card-header">
                                        <h3 className="card-title">Processing Summary</h3>
                                    </div>
                                    <div className="card-body">
                                        <div className="trace-stats">
                                            <div className="stat-item">
                                                <div className="stat-value">{submissionResponse.trace.rules_fired}</div>
                                                <div className="stat-label">Rules Fired</div>
                                            </div>
                                            <div className="stat-item">
                                                <div className="stat-value">{submissionResponse.trace.conflicts_detected}</div>
                                                <div className="stat-label">Conflicts Detected</div>
                                            </div>
                                            <div className="stat-item">
                                                <div className="stat-value">{submissionResponse.trace.processing_time_ms}ms</div>
                                                <div className="stat-label">Processing Time</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* Ambiguity Report */}
                            {submissionResponse?.ambiguity && submissionResponse.ambiguity.requires_human_review && (
                                <div className="ambiguity-report card">
                                    <div className="card-header">
                                        <h3 className="card-title">Ambiguity Detected</h3>
                                    </div>
                                    <div className="card-body">
                                        <div className="alert alert-warning">
                                            <p>
                                                <strong>Human Review Required:</strong> The system detected{' '}
                                                {submissionResponse.ambiguity.ambiguous_terms_count} ambiguous term(s) in your narrative.
                                            </p>
                                        </div>
                                        {submissionResponse.ambiguity.clarification_questions.length > 0 && (
                                            <div>
                                                <h4>Clarification Questions:</h4>
                                                <ul>
                                                    {submissionResponse.ambiguity.clarification_questions.map((q, i) => (
                                                        <li key={i}>{q}</li>
                                                    ))}
                                                </ul>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}

                            {/* Fairness Report */}
                            {submissionResponse?.fairness && (
                                <div className="fairness-report card">
                                    <div className="card-header">
                                        <h3 className="card-title">Fairness Analysis</h3>
                                    </div>
                                    <div className="card-body">
                                        <div className="fairness-score">
                                            <div className="score-circle">
                                                <div className="score-value">
                                                    {(submissionResponse.fairness.consistency_score * 100).toFixed(0)}%
                                                </div>
                                                <div className="score-label">Consistency</div>
                                            </div>
                                            <div className="score-details">
                                                <p>
                                                    <strong>Similar Cases Found:</strong> {submissionResponse.fairness.similar_cases_count}
                                                </p>
                                                <p>
                                                    <strong>Threshold:</strong> {(submissionResponse.fairness.consistency_threshold * 100).toFixed(0)}%
                                                </p>
                                                <p>
                                                    <strong>Status:</strong>{' '}
                                                    <span className={submissionResponse.fairness.meets_threshold ? 'text-success' : 'text-warning'}>
                                                        {submissionResponse.fairness.meets_threshold ? '✓ Meets Threshold' : '⚠ Below Threshold'}
                                                    </span>
                                                </p>
                                            </div>
                                        </div>
                                        <div className="recommendation-box">
                                            <h4>Recommendation</h4>
                                            <p>{submissionResponse.fairness.recommendation}</p>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* New Grievance Button */}
                            <div className="action-container">
                                <button onClick={handleNewGrievance} className="btn btn-primary btn-lg">
                                    Submit Another Grievance
                                </button>
                            </div>
                        </>
                    )}
                </div>
            </main>

            {/* Footer */}
            <footer className="app-footer">
                <div className="container">
                    <p>
                        Academic Grievance DSS - Proof of Concept |
                        Powered by Drools 8.44.0 + GPT-4 + PostgreSQL
                    </p>
                </div>
            </footer>
        </div>
    );
}

export default App;
