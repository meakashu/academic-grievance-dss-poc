# Pilot Dataset Description

## Dataset Overview

**File:** `data/grievance_cases.csv`  
**Size:** 75 academic grievance cases  
**Fields:** 23 structured attributes per case  
**Time Period:** January 2024 – July 2024 (simulated)  
**Purpose:** Proof-of-concept validation only (not for predictive modeling)

---

## Data Source Disclosure

**Source Type:** Simulated cases derived from real policies and regulatory frameworks

**Policy Grounding:**
- University Grants Commission (UGC) Regulations 2018
- National Assessment and Accreditation Council (NAAC) Guidelines 2021
- National Board of Accreditation (NBA) Standards 2020
- Right to Education (RTE) Act 2009
- Representative university statutes from Indian public universities

**Simulation Method:**
All cases are synthetically generated based on:
1. Actual regulatory thresholds (75% attendance, 15-day revaluation deadline, Rs 200,000 income threshold)
2. Real policy conflict scenarios documented in UGC/NAAC/NBA guidelines
3. Boundary conditions explicitly stated in regulations
4. Discretionary language patterns from official policy documents

**Disclosure:** This dataset contains **no real student data**. All cases are simulated to reflect realistic grievance scenarios grounded in documented Indian higher education policies. No institutional data was used.

---

## Anonymization Method

**Identity Protection:**
- **Case IDs:** Synthetic sequential identifiers (GRV2024001–GRV2024075)
- **No Personal Identifiers:** No student names, roll numbers, email addresses, phone numbers, or addresses
- **Program/Department:** Generic categories only (BTech, MSc, Computer Science, etc.)
- **Dates:** Relative timelines only (days since event, submission dates without year context)
- **Income Values:** Rounded to nearest Rs 5,000 to prevent re-identification

**Compliance:** Dataset adheres to:
- General Data Protection Regulation (GDPR) principles
- Indian Personal Data Protection Bill guidelines
- Institutional Review Board (IRB) ethical standards for educational research

---

## Dataset Schema (23 Fields)

### Identity (Anonymized)
1. **case_id** - Unique synthetic identifier
2. **program** - Academic program (BTech, MSc, MBA, etc.)
3. **department** - Department name (generic categories)
4. **semester** - Current semester (1-8)

### Academic Facts
5. **marks** - Exam marks (if applicable, otherwise NA)
6. **attendance_percentage** - Overall attendance percentage
7. **cgpa** - Cumulative GPA

### Timeline
8. **grievance_submission_date** - Date grievance submitted
9. **policy_deadline_date** - Applicable policy deadline
10. **days_since_event** - Days elapsed since triggering event

### Grievance Details
11. **grievance_type** - Category (ATTENDANCE_SHORTAGE, EXAMINATION_REEVAL, FEE_WAIVER, etc.)
12. **grievance_claim** - Textual summary of student claim

### Evidence
13. **medical_proof_present** - Medical certificate submitted (yes/no)
14. **supporting_documents_count** - Number of supporting documents
15. **category_certificate_present** - SC/ST/OBC certificate (yes/no)
16. **income_certificate_present** - Income certificate (yes/no)

### Decision Ground Truth
17. **human_decision** - Expert decision (ACCEPT, REJECT, PENDING)
18. **decision_reason_summary** - Explanation for decision

### Governance Metadata
19. **authority_applied** - Regulatory authority (L1_National, L2_Accreditation, L3_University)
20. **rule_reference_id** - Specific rule applied
21. **conflict_detected** - Whether rule conflict occurred (yes/no)
22. **hierarchy_level_applied** - Governance level of winning rule
23. **salience_score** - Rule priority score (800-2000)

---

## Dataset Composition

### Grievance Type Distribution
- **Attendance Shortage:** 40 cases (53%)
- **Examination Revaluation:** 15 cases (20%)
- **Fee Waiver:** 8 cases (11%)
- **Fee Installment:** 6 cases (8%)
- **Grade Appeal:** 4 cases (5%)
- **Transcript Delay:** 2 cases (3%)

### Decision Outcome Distribution
- **ACCEPT:** 52 cases (69%)
- **REJECT:** 20 cases (27%)
- **PENDING:** 3 cases (4%)

### Governance Level Distribution
- **L1 (National):** 48 cases (64%)
- **L2 (Accreditation):** 12 cases (16%)
- **L3 (University):** 15 cases (20%)

### Conflict Cases
- **Authority Conflicts:** 6 cases (8%) - L1 vs L3 hierarchy
- **Temporal Conflicts:** 1 case (1%) - 2019 vs 2023 policy
- **No Conflicts:** 68 cases (91%)

### Boundary Cases
- **Exactly 75% attendance:** 4 cases
- **Exactly on 15-day deadline:** 3 cases
- **Just below threshold (74.9%):** 2 cases
- **Just above threshold (75.1%):** 2 cases

### Discretionary Cases
- **NAAC 70-75% monitoring range:** 3 cases (require committee review)
- **"Exceptional circumstances":** 0 cases (avoided ambiguous language)
- **Medical exception threshold (65%):** 15 cases

---

## Intended Use

**Appropriate Uses:**
✅ Validating rule engine correctness (rule firing, conflict detection)  
✅ Testing hierarchical precedence logic (L1 > L2 > L3)  
✅ Demonstrating explainability and traceability  
✅ Evaluating fairness consistency across similar cases  
✅ Proof-of-concept system demonstration  

**Inappropriate Uses:**
❌ Training machine learning models for prediction  
❌ Claiming statistical generalizability to real populations  
❌ Performance benchmarking or accuracy claims  
❌ Production deployment without real institutional data  
❌ Policy recommendations without domain expert validation  

---

## Ethical Compliance

**Institutional Review:** Not required (no human subjects, fully simulated data)

**Data Protection:** Complies with GDPR and Indian data protection principles

**Transparency:** Full disclosure of simulation method and policy sources

**Reproducibility:** Dataset and generation logic available in repository

**Limitations Acknowledged:**
- Simulated data may not capture all real-world complexity
- Policy interpretations based on publicly available documents
- No validation against actual institutional grievance outcomes
- Intended solely for technical system validation, not policy evaluation

---

## Validation Checklist

✅ **Schema Validation:** All 23 required fields present  
✅ **Anonymization:** No personal identifiers  
✅ **Governance Coverage:** All 3 hierarchy levels represented  
✅ **Conflict Cases:** 6 authority conflicts, 1 temporal conflict  
✅ **Boundary Cases:** 11 threshold boundary cases  
✅ **Discretionary Cases:** 3 NAAC monitoring cases  
✅ **Reviewer Reproducibility:** CSV loads directly without preprocessing  
✅ **Rule Engine Compatibility:** Fields map to Drools rule conditions  

---

## Reviewer Statement

**For Journal Reviewers:**

This dataset is **realistic** (grounded in actual UGC/NAAC/NBA policies), **ethically sound** (fully anonymized, no real student data), **governance-aware** (covers all 3 hierarchy levels with conflict scenarios), and **sufficient** to validate the proposed decision support framework's core capabilities: rule-based reasoning, hierarchical conflict resolution, complete traceability, and fairness monitoring.

The dataset is **not intended** for statistical claims, predictive modeling, or production deployment. It serves exclusively as a proof-of-concept validation artifact demonstrating system functionality.

---

## Citation

If using this dataset, cite as:

```
Singh, Akash Kumar (2026). Academic Grievance Pilot Dataset. 
Part of "A Rule-Based Decision Support System for Automated Academic 
Grievance Resolution" research project. 
Available at: https://github.com/akashsingh/academic-grievance-dss-poc
```

---

**Dataset Version:** 1.0  
**Last Updated:** February 1, 2026  
**Contact:** meakash22dotin@gmail.com  
**License:** Educational and Research Use Only
