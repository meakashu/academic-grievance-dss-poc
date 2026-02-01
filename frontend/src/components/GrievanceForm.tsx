/**
 * Grievance Submission Form Component
 * Allows students to submit grievances with structured parameters
 */
import React, { useState } from 'react';
import { GrievanceType, GrievanceCreate, GrievanceSubmissionResponse } from '../types';
import { apiService } from '../services/api';
import './GrievanceForm.css';

interface GrievanceFormProps {
    onSubmitSuccess: (response: GrievanceSubmissionResponse) => void;
}

const GrievanceForm: React.FC<GrievanceFormProps> = ({ onSubmitSuccess }) => {
    const [studentId, setStudentId] = useState('');
    const [grievanceType, setGrievanceType] = useState<GrievanceType>(GrievanceType.ATTENDANCE_SHORTAGE);
    const [narrative, setNarrative] = useState('');
    const [parameters, setParameters] = useState<Record<string, any>>({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleParameterChange = (key: string, value: any) => {
        setParameters(prev => ({ ...prev, [key]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setLoading(true);

        try {
            const grievance: GrievanceCreate = {
                student_id: studentId,
                grievance_type: grievanceType,
                narrative,
                parameters
            };

            const response = await apiService.submitGrievance(grievance);
            onSubmitSuccess(response);
        } catch (err: any) {
            setError(err.message || 'Failed to submit grievance');
        } finally {
            setLoading(false);
        }
    };

    const renderParameterFields = () => {
        switch (grievanceType) {
            case GrievanceType.ATTENDANCE_SHORTAGE:
                return (
                    <>
                        <div className="form-group">
                            <label className="form-label required">Attendance Percentage</label>
                            <input
                                type="number"
                                className="form-input"
                                min="0"
                                max="100"
                                step="0.1"
                                value={parameters.attendance_percentage || ''}
                                onChange={(e) => handleParameterChange('attendance_percentage', parseFloat(e.target.value))}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label className="form-label">Do you have a medical certificate?</label>
                            <select
                                className="form-select"
                                value={parameters.has_medical_certificate ? 'yes' : 'no'}
                                onChange={(e) => handleParameterChange('has_medical_certificate', e.target.value === 'yes')}
                            >
                                <option value="no">No</option>
                                <option value="yes">Yes</option>
                            </select>
                        </div>
                        {parameters.has_medical_certificate && (
                            <>
                                <div className="form-group">
                                    <label className="form-label">Is the medical certificate valid?</label>
                                    <select
                                        className="form-select"
                                        value={parameters.medical_certificate_valid ? 'yes' : 'no'}
                                        onChange={(e) => handleParameterChange('medical_certificate_valid', e.target.value === 'yes')}
                                    >
                                        <option value="yes">Yes</option>
                                        <option value="no">No</option>
                                    </select>
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Is it from a recognized authority?</label>
                                    <select
                                        className="form-select"
                                        value={parameters.medical_certificate_from_recognized_authority ? 'yes' : 'no'}
                                        onChange={(e) => handleParameterChange('medical_certificate_from_recognized_authority', e.target.value === 'yes')}
                                    >
                                        <option value="yes">Yes</option>
                                        <option value="no">No</option>
                                    </select>
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Days Absent</label>
                                    <input
                                        type="number"
                                        className="form-input"
                                        min="0"
                                        value={parameters.days_absent || ''}
                                        onChange={(e) => handleParameterChange('days_absent', parseInt(e.target.value))}
                                    />
                                </div>
                            </>
                        )}
                    </>
                );

            case GrievanceType.EXAMINATION_REEVAL:
                return (
                    <>
                        <div className="form-group">
                            <label className="form-label required">Course Code</label>
                            <input
                                type="text"
                                className="form-input"
                                value={parameters.course_code || ''}
                                onChange={(e) => handleParameterChange('course_code', e.target.value)}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label className="form-label required">Marks Obtained</label>
                            <input
                                type="number"
                                className="form-input"
                                min="0"
                                max="100"
                                value={parameters.marks_obtained || ''}
                                onChange={(e) => handleParameterChange('marks_obtained', parseInt(e.target.value))}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label className="form-label required">Days Since Result Declaration</label>
                            <input
                                type="number"
                                className="form-input"
                                min="0"
                                value={parameters.days_since_result_declaration || ''}
                                onChange={(e) => handleParameterChange('days_since_result_declaration', parseInt(e.target.value))}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label className="form-label">Revaluation Fee Paid?</label>
                            <select
                                className="form-select"
                                value={parameters.revaluation_fee_paid ? 'yes' : 'no'}
                                onChange={(e) => handleParameterChange('revaluation_fee_paid', e.target.value === 'yes')}
                            >
                                <option value="no">No</option>
                                <option value="yes">Yes</option>
                            </select>
                        </div>
                    </>
                );

            case GrievanceType.FEE_WAIVER:
                return (
                    <>
                        <div className="form-group">
                            <label className="form-label required">Student Category</label>
                            <select
                                className="form-select"
                                value={parameters.student_category || 'GENERAL'}
                                onChange={(e) => handleParameterChange('student_category', e.target.value)}
                                required
                            >
                                <option value="GENERAL">General</option>
                                <option value="SC">SC</option>
                                <option value="ST">ST</option>
                                <option value="OBC">OBC</option>
                                <option value="EWS">EWS</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label required">Family Income (Annual)</label>
                            <input
                                type="number"
                                className="form-input"
                                min="0"
                                value={parameters.family_income || ''}
                                onChange={(e) => handleParameterChange('family_income', parseFloat(e.target.value))}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label className="form-label">Do you have an income certificate?</label>
                            <select
                                className="form-select"
                                value={parameters.has_income_certificate ? 'yes' : 'no'}
                                onChange={(e) => handleParameterChange('has_income_certificate', e.target.value === 'yes')}
                            >
                                <option value="no">No</option>
                                <option value="yes">Yes</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">Do you have a category certificate?</label>
                            <select
                                className="form-select"
                                value={parameters.has_category_certificate ? 'yes' : 'no'}
                                onChange={(e) => handleParameterChange('has_category_certificate', e.target.value === 'yes')}
                            >
                                <option value="no">No</option>
                                <option value="yes">Yes</option>
                            </select>
                        </div>
                    </>
                );

            default:
                return null;
        }
    };

    return (
        <div className="grievance-form-container">
            <div className="card">
                <div className="card-header">
                    <h2 className="card-title">Submit Grievance</h2>
                    <p>Fill in the details below to submit your academic grievance</p>
                </div>

                <form onSubmit={handleSubmit} className="card-body">
                    {error && (
                        <div className="alert alert-error mb-3">
                            <strong>Error:</strong> {error}
                        </div>
                    )}

                    <div className="form-group">
                        <label className="form-label required">Student ID</label>
                        <input
                            type="text"
                            className="form-input"
                            value={studentId}
                            onChange={(e) => setStudentId(e.target.value)}
                            placeholder="e.g., STU2024001"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label required">Grievance Type</label>
                        <select
                            className="form-select"
                            value={grievanceType}
                            onChange={(e) => {
                                setGrievanceType(e.target.value as GrievanceType);
                                setParameters({});
                            }}
                            required
                        >
                            <option value={GrievanceType.ATTENDANCE_SHORTAGE}>Attendance Shortage</option>
                            <option value={GrievanceType.EXAMINATION_REEVAL}>Examination Revaluation</option>
                            <option value={GrievanceType.GRADE_APPEAL}>Grade Appeal</option>
                            <option value={GrievanceType.FEE_WAIVER}>Fee Waiver</option>
                            <option value={GrievanceType.FEE_INSTALLMENT_REQUEST}>Fee Installment Request</option>
                            <option value={GrievanceType.TRANSCRIPT_DELAY}>Transcript Delay</option>
                            <option value={GrievanceType.OTHER}>Other</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label className="form-label required">Narrative</label>
                        <textarea
                            className="form-textarea"
                            value={narrative}
                            onChange={(e) => setNarrative(e.target.value)}
                            placeholder="Describe your grievance in detail..."
                            required
                            minLength={10}
                        />
                        <span className="form-help">
                            Minimum 10 characters. Be specific and include all relevant details.
                        </span>
                    </div>

                    {renderParameterFields()}

                    <div className="form-actions">
                        <button
                            type="submit"
                            className="btn btn-primary btn-lg"
                            disabled={loading}
                        >
                            {loading ? (
                                <>
                                    <span className="spinner spinner-sm"></span>
                                    Processing...
                                </>
                            ) : (
                                'Submit Grievance'
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default GrievanceForm;
