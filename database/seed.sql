-- Seed data for Academic Grievance DSS
-- Historical cases for fairness comparison

-- Insert rules into catalog
INSERT INTO rules_catalog (rule_id, rule_name, hierarchy_level, authority, source, source_url, effective_date, category, rule_type, description, salience, drl_file, active) VALUES
('UGC_Attendance_75Percent_Minimum', 'UGC Attendance 75% Minimum Requirement', 'L1_National', 'University Grants Commission (UGC)', 'UGC Regulations 2018, Section 4.2', 'https://www.ugc.ac.in/pdfnews/4033931_UGC-Minimum-Standard-and-Procedure-Regulations-2018.pdf', '2018-07-01', 'Attendance', 'MANDATORY', 'Mandates minimum 75% attendance for semester eligibility across all higher education institutions', 1500, 'L1_national_laws.drl', TRUE),

('UGC_Medical_Excuse_Exception', 'UGC Medical Excuse Exception', 'L1_National', 'University Grants Commission (UGC)', 'UGC Regulations 2018, Section 4.2.1', 'https://www.ugc.ac.in/pdfnews/4033931_UGC-Minimum-Standard-and-Procedure-Regulations-2018.pdf', '2018-07-01', 'Attendance', 'EXCEPTION', 'Allows attendance relaxation to 65% with valid medical certificate from recognized medical authority', 1600, 'L1_national_laws.drl', TRUE),

('UGC_Examination_Revaluation_Right', 'UGC Examination Re-evaluation Right', 'L1_National', 'University Grants Commission (UGC)', 'UGC Regulations 2018, Section 6.3', 'https://www.ugc.ac.in/pdfnews/4033931_UGC-Minimum-Standard-and-Procedure-Regulations-2018.pdf', '2018-07-01', 'Examination', 'MANDATORY', 'Guarantees student right to request re-evaluation of answer scripts within 15 days of result declaration', 1400, 'L1_national_laws.drl', TRUE),

('Right_To_Education_Fee_Waiver_SC_ST', 'Right to Education Fee Waiver for SC/ST', 'L1_National', 'Ministry of Education, Government of India', 'Right to Education Act 2009, Section 12(1)(c)', 'https://www.education.gov.in/sites/upload_files/mhrd/files/rte.pdf', '2009-08-26', 'Fee', 'MANDATORY', 'Mandates fee waiver for SC/ST category students with family income below ₹200,000 per annum', 1700, 'L1_national_laws.drl', TRUE),

('University_Medical_Excuse_Attendance', 'University Medical Excuse Attendance Policy', 'L3_University', 'University Academic Council', 'University Statute 2020, Chapter 5, Section 5.3', 'https://university.edu/statutes/2020/chapter5.pdf', '2020-01-01', 'Attendance', 'CONDITIONAL', 'Allows attendance relaxation to 70% with valid medical certificate (subject to national law compliance)', 300, 'L3_university_statutes.drl', TRUE),

('University_Fee_Structure_Installment_Policy', 'University Fee Installment Policy', 'L3_University', 'University Finance Committee', 'University Fee Policy 2022, Section 3.2', 'https://university.edu/policies/fee-policy-2022.pdf', '2022-07-01', 'Fee', 'CONDITIONAL', 'Permits fee payment in 3 installments for students with family income below ₹500,000', 350, 'L3_university_statutes.drl', TRUE),

('University_Exam_Policy_Reeval_Fee', 'University Re-evaluation Fee Policy', 'L3_University', 'University Examination Board', 'University Examination Policy 2023, Section 7.1', 'https://university.edu/policies/exam-policy-2023.pdf', '2023-01-01', 'Examination', 'MANDATORY', 'Requires payment of ₹500 re-evaluation fee per course', 320, 'L3_university_statutes.drl', TRUE),

('University_Grade_Appeal_Process', 'University Grade Appeal Process', 'L3_University', 'University Academic Council', 'University Academic Regulations 2021, Section 8.4', 'https://university.edu/regulations/academic-2021.pdf', '2021-08-01', 'Examination', 'CONDITIONAL', 'Permits grade appeal if marks are within 5% of next grade boundary', 310, 'L3_university_statutes.drl', TRUE),

('University_Transcript_Delay_Compensation', 'University Transcript Delay Compensation', 'L3_University', 'University Registrar Office', 'University Administrative Policy 2022, Section 12.5', 'https://university.edu/policies/admin-policy-2022.pdf', '2022-01-01', 'Administrative', 'CONDITIONAL', 'Provides expedited processing if transcript delay exceeds 30 days from standard timeline', 280, 'L3_university_statutes.drl', TRUE);

-- Insert historical grievances for fairness comparison
INSERT INTO grievances (id, student_id, grievance_type, narrative, parameters, status) VALUES
('11111111-1111-1111-1111-111111111111', 'HIST-001', 'ATTENDANCE_SHORTAGE', 'I have 72% attendance with valid medical certificate for 15 days absence.', '{"attendance_percentage": 72, "has_medical_certificate": true, "medical_certificate_valid": true, "medical_certificate_from_recognized_authority": true, "days_absent": 15}', 'RESOLVED'),

('22222222-2222-2222-2222-222222222222', 'HIST-002', 'ATTENDANCE_SHORTAGE', 'I have 73% attendance with valid medical certificate for 12 days absence.', '{"attendance_percentage": 73, "has_medical_certificate": true, "medical_certificate_valid": true, "medical_certificate_from_recognized_authority": true, "days_absent": 12}', 'RESOLVED'),

('33333333-3333-3333-3333-333333333333', 'HIST-003', 'ATTENDANCE_SHORTAGE', 'I have 74% attendance with valid medical certificate for 10 days absence.', '{"attendance_percentage": 74, "has_medical_certificate": true, "medical_certificate_valid": true, "medical_certificate_from_recognized_authority": true, "days_absent": 10}', 'RESOLVED'),

('44444444-4444-4444-4444-444444444444', 'HIST-004', 'ATTENDANCE_SHORTAGE', 'I have 72.5% attendance with valid medical certificate for 13 days absence.', '{"attendance_percentage": 72.5, "has_medical_certificate": true, "medical_certificate_valid": true, "medical_certificate_from_recognized_authority": true, "days_absent": 13}', 'RESOLVED');

-- Insert historical decisions
INSERT INTO decisions (grievance_id, outcome, applicable_rule, regulatory_source, hierarchy_level, salience, reason, explanation, human_review_required) VALUES
('11111111-1111-1111-1111-111111111111', 'REJECT', 'UGC_Attendance_75Percent_Minimum', 'UGC Regulations 2018, Section 4.2', 'L1_National', 1500, 'Attendance below UGC-mandated 75% minimum', 'Despite having a valid medical certificate, the attendance of 72% does not meet the UGC-mandated minimum of 75%. The medical excuse exception requires attendance of at least 65%, which is met, but the national law takes precedence over university policy.', FALSE),

('22222222-2222-2222-2222-222222222222', 'REJECT', 'UGC_Attendance_75Percent_Minimum', 'UGC Regulations 2018, Section 4.2', 'L1_National', 1500, 'Attendance below UGC-mandated 75% minimum', 'Attendance of 73% with medical certificate does not qualify for acceptance under UGC regulations.', FALSE),

('33333333-3333-3333-3333-333333333333', 'REJECT', 'UGC_Attendance_75Percent_Minimum', 'UGC Regulations 2018, Section 4.2', 'L1_National', 1500, 'Attendance below UGC-mandated 75% minimum', 'Attendance of 74% with medical certificate does not meet the 75% threshold.', FALSE),

('44444444-4444-4444-4444-444444444444', 'REJECT', 'UGC_Attendance_75Percent_Minimum', 'UGC Regulations 2018, Section 4.2', 'L1_National', 1500, 'Attendance below UGC-mandated 75% minimum', 'Attendance of 72.5% with medical certificate does not meet UGC requirements.', FALSE);

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Database seeded successfully with % rules and % historical cases!', 
        (SELECT COUNT(*) FROM rules_catalog),
        (SELECT COUNT(*) FROM grievances);
END $$;
