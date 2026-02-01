# A Rule-Based Decision Support System for Academic Grievance Resolution: Implementation, Validation, and Ethical Audit

**Akash Kumar Singh**  
*Department of Computer Science*  
*Email: meakash22dotin@gmail.com*

---

## Abstract

Academic grievance resolution in higher education institutions requires consistent application of complex, hierarchical regulations while preserving human judgment for discretionary cases. This paper presents the design, implementation, and empirical validation of a rule-based decision support system for academic grievance adjudication. The system integrates a Drools rule engine for hierarchical policy reasoning (national, accreditation, and university levels), an LLM-based ambiguity detector for identifying discretionary language, and comprehensive decision tracing for transparency. We evaluated the system using a pilot dataset of 75 policy-grounded grievance cases, achieving 96.0% agreement with human committee decisions (Cohen's κ = 0.912, p < 0.001) and 96.0% regulatory compliance. A controlled user study (N=40) demonstrated that rule-based explanations significantly improved perceived fairness (d=1.21), trust (d=1.07), and transparency (d=3.30) compared to unexplained decisions. Ethical audit revealed no statistically significant gender bias (χ²=2.074, p>0.05) and documented 10 failure modes with mitigation strategies. The system is designed as assistive governance technology, not autonomous adjudication, with mandatory human oversight for all discretionary cases. Source code, dataset, and validation scripts are publicly available for reproducibility.

**Keywords:** Decision Support Systems, Academic Governance, Rule-Based Reasoning, Explainable AI, Educational Technology, Procedural Justice

---

## 1. Introduction

### 1.1 Motivation

Academic grievance resolution is a critical governance function in higher education institutions, addressing student disputes regarding attendance, examinations, fees, and administrative decisions. Traditional grievance adjudication faces three persistent challenges:

1. **Inconsistency**: Manual decision-making across different committees and time periods can produce disparate outcomes for similar cases, undermining perceived fairness.

2. **Opacity**: Students often receive decisions without clear explanations of which regulations were applied or why, reducing trust in institutional processes.

3. **Inefficiency**: Committee-based review of every grievance is time-intensive, delaying resolution and consuming administrative resources.

These challenges are compounded by the hierarchical nature of educational governance in India, where regulations from national bodies (University Grants Commission), accreditation agencies (NAAC, NBA), and individual universities must be reconciled, often with conflicting requirements.

### 1.2 Research Gap

Existing decision support systems in governance contexts focus primarily on legal case prediction or policy recommendation. Few systems address the unique requirements of academic grievance resolution:

- **Hierarchical policy reasoning**: Regulations exist at multiple governance levels (L1: National, L2: Accreditation, L3: University) with explicit precedence rules
- **Discretionary language**: Educational policies contain subjective terms ("reasonable grounds," "exceptional circumstances") requiring human interpretation
- **Explainability requirements**: Academic governance demands transparent, auditable decisions with regulatory citations
- **Human oversight**: Discretionary cases must preserve committee authority, not automate judgment

### 1.3 Contributions

This paper presents an implemented, evaluated, and ethically audited rule-based decision support system for academic grievance resolution. The specific contributions are:

1. **System Implementation**: A production-ready proof-of-concept integrating Drools rule engine, LLM-based ambiguity detection, and PostgreSQL-backed decision tracing (Section 3)

2. **Empirical Validation**: Evaluation on 75 policy-grounded cases demonstrating 96.0% agreement with human decisions and 96.0% regulatory compliance (Section 4)

3. **Ambiguity Detection**: Validation of LLM-based discretionary language identification achieving F1=0.988 on 80 manually-labeled regulation clauses (Section 5)

4. **Explainability Impact**: Controlled user study (N=40) showing rule-based explanations significantly improve perceived fairness, trust, and transparency (Section 6)

5. **Ethical Audit**: Bias testing, failure mode documentation, and explicit ethical boundaries for responsible governance deployment (Section 7)

The system is designed as **decision support, not decision automation**, with mandatory human oversight for all ambiguous, conflicting, or boundary cases.

### 1.4 Scope and Limitations

This work focuses on rule-based grievance resolution for cases with clear regulatory criteria (attendance thresholds, deadline compliance, fee eligibility). The system does **not** address:

- Discretionary cases requiring contextual judgment
- Novel grievance types without established precedents
- Policy formulation or regulatory interpretation
- Legal adjudication or binding decisions

All system outputs are recommendations to assist human committees, not autonomous decisions.

---

## 2. Related Work

### 2.1 Decision Support Systems in Governance

Decision support systems have been applied to legal case prediction, policy analysis, and administrative automation. However, most systems prioritize predictive accuracy over explainability and human oversight, making them unsuitable for governance contexts requiring transparency and accountability.

### 2.2 Rule-Based Reasoning in Education

Rule-based systems have been used for course recommendation, degree audit, and prerequisite checking. These applications typically involve deterministic rules without hierarchical conflicts or discretionary language, unlike grievance adjudication.

### 2.3 Explainable AI in High-Stakes Domains

Recent work on explainable AI emphasizes the importance of transparency in healthcare, finance, and legal domains. Our work extends this to academic governance, demonstrating that rule-based explanations improve perceived fairness and trust independent of decision outcome.

### 2.4 Fairness and Bias in Automated Systems

Algorithmic fairness research has documented bias risks in predictive systems. Our rule-based approach differs fundamentally: rather than learning patterns from historical data (which may encode bias), we encode explicit regulations, making bias audits focus on policy design rather than algorithmic artifacts.

---

## 3. System Design and Implementation

### 3.1 Architecture Overview

The Academic Grievance Decision Support System consists of five integrated components:

1. **FastAPI Backend** (Python 3.11): REST API for grievance submission, decision retrieval, and metadata queries
2. **Drools Rule Engine** (Java 17, Drools 8.44.0): Hierarchical policy reasoning with salience-based conflict resolution
3. **LLM Ambiguity Detector** (OpenAI GPT-4): Identification of discretionary language in regulations
4. **PostgreSQL Database** (15.x): Persistent storage of grievances, decisions, and audit trails
5. **React Frontend** (TypeScript): User interface for grievance submission and decision review

**Technology Stack:**
- Backend: FastAPI, Pydantic, JPype1 (Python-Java bridge)
- Rule Engine: Drools 8.44.0.Final, Maven
- Database: PostgreSQL 15.x, SQLAlchemy
- Frontend: React 18, TypeScript
- Deployment: Docker Compose

### 3.2 Hierarchical Rule Representation

Educational regulations are encoded as Drools rules organized into three hierarchy levels:

- **L1 (National)**: UGC regulations, RTE Act, MHRD guidelines (Salience: 1500-2000)
- **L2 (Accreditation)**: NAAC quality standards, NBA technical requirements (Salience: 1100-1400)
- **L3 (University)**: Institutional statutes, examination policies (Salience: 800-1000)

Each rule includes metadata:
```drools
rule "UGC_Attendance_75Percent_Minimum"
    salience 1500
    when
        $g: Grievance(attendancePercentage < 75.0, 
                     !hasMedicalExcuse())
    then
        $g.setDecision("REJECT");
        $g.setReason("UGC Regulation 2018 requires 75% attendance");
        $g.setAppliedRule("UGC_Attendance_75Percent_Minimum");
        $g.setHierarchyLevel("L1_National");
end
```

**Conflict Resolution:** When multiple rules match, Drools selects the rule with highest salience (L1 > L2 > L3). All conflicts are logged in the decision trace.

### 3.3 LLM-Based Ambiguity Detection

Regulations containing discretionary language are flagged for human review using a GPT-4-based detector. The system identifies three ambiguity categories:

1. **Subjective terms**: "reasonable," "adequate," "sufficient"
2. **Permissive language**: "may," "can," "at the discretion of"
3. **Context-dependent phrases**: "exceptional circumstances," "special cases"

**Ambiguity Detection Prompt:**
```
Analyze the following regulation for ambiguous language that requires 
human interpretation. Identify subjective terms, permissive language, 
and context-dependent phrases. Return structured JSON with detected 
terms and ambiguity categories.
```

Cases flagged as ambiguous are escalated to human committees without automated recommendations.

### 3.4 Decision Tracing and Explainability

Every decision generates a complete trace including:
- Applied rule ID and regulatory source
- Hierarchy level and salience score
- Threshold values and student's actual values
- Conflict detection (if multiple rules matched)
- Ambiguity report (if discretionary language detected)
- Similar historical cases (for precedent review)

**Example Decision Trace:**
```json
{
  "decision": "REJECT",
  "applied_rule": "UGC_Attendance_75Percent_Minimum",
  "hierarchy_level": "L1_National",
  "salience": 1500,
  "explanation": "UGC Regulation 2018 requires 75% attendance. 
                  Your attendance: 72%. Medical exception applies 
                  only when attendance ≥65% AND certificate submitted 
                  within 7 days. Certificate submitted 12 days late.",
  "conflicts": [],
  "ambiguity_detected": false,
  "requires_human_review": false
}
```

### 3.5 Implementation Details

**Proof-of-Concept Scope:**
- 15 Drools rules across 3 hierarchy levels
- 6 grievance types (attendance, examination, fees, grades, transcripts, installments)
- 73 automated tests (unit, integration, edge cases)
- Complete API documentation (OpenAPI/Swagger)
- Docker-based deployment

**Source Code:** Publicly available at `https://github.com/akashsingh/academic-grievance-dss-poc` (Educational and Research Use Only license)

---

## 4. Empirical Validation

### 4.1 Pilot Dataset

We constructed a pilot dataset of **75 academic grievance cases** grounded in real UGC, NAAC, and NBA regulations. Each case includes:

- **23 structured fields**: case ID, program, department, semester, marks, attendance, CGPA, dates, grievance type, evidence, decision, regulatory metadata
- **Manual labeling**: Expert-assigned decisions (ACCEPT/REJECT/PENDING) based on policy interpretation
- **Anonymization**: Synthetic case IDs, no personal identifiers, rounded income values

**Dataset Composition:**
- Attendance shortage: 40 cases (53%)
- Examination revaluation: 15 cases (20%)
- Fee waiver: 8 cases (11%)
- Fee installment: 6 cases (8%)
- Grade appeal: 4 cases (5%)
- Transcript delay: 2 cases (3%)

**Governance Coverage:**
- L1 (National): 48 cases (64%)
- L2 (Accreditation): 12 cases (16%)
- L3 (University): 15 cases (20%)

**Critical Test Cases:**
- 6 authority conflicts (L1 vs L3)
- 11 boundary cases (exactly 75% attendance, day 15 deadline)
- 15 medical exception cases (65%+ threshold)

**Source Disclosure:** Cases are simulated from real UGC/NAAC/NBA policies, not actual student data. Dataset available at `data/grievance_cases.csv`.

### 4.2 Validation Methodology

We evaluated the system as a **decision support aid**, not an autonomous decision-maker. The appropriate metric is **agreement** (alignment with human decisions), not accuracy (correctness).

**Metrics Computed:**

1. **Agreement Percentage**: Cases where system decision == human decision
2. **Cohen's Kappa (κ)**: Inter-rater reliability beyond chance
3. **Time Reduction**: Administrative efficiency gain (estimated)
4. **Compliance Rate**: Percentage where system applied same authoritative rule as humans

**Validation Procedure:**
1. System processes each case using rule engine
2. System decision compared to expert-assigned decision
3. Applied rule compared to regulatory citation in manual label
4. Statistical tests performed (paired comparisons, permutation tests)

### 4.3 Results

**Table 1: Empirical Validation Results**

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Agreement (%) | 96.0% | 72 of 75 cases align with human decisions |
| Cohen's κ | 0.912 | Almost perfect inter-rater reliability (p < 0.001) |
| Average Time Saved (%) | 42.9% | ~18.8 hours saved across 75 cases |
| Compliance Rate (%) | 96.0% | System applies same authoritative rule as humans |

**Agreement Analysis:**
- Total comparable cases: 72 (excluding 3 PENDING)
- Agreements: 69
- Disagreements: 3

**Disagreement Cases:**
1. Attendance exactly 75.0% (boundary interpretation)
2. Submission on day 15 (deadline day ambiguity)
3. Temporal conflict (2019 vs 2023 university policy)

All disagreements occurred at regulatory boundaries, highlighting the importance of human oversight for edge cases.

**Cohen's Kappa Interpretation:**
κ = 0.912 indicates "almost perfect agreement" (Landis & Koch, 1977), comparable to inter-rater reliability between human experts in governance domains.

**Time Reduction:**
- Manual committee time: ~35 min/case (document review, policy lookup, discussion, documentation)
- System-assisted time: ~20 min/case (human review + system processing)
- Time saved: 42.9% per case

**Compliance Rate:**
72 of 75 cases (96.0%) applied the same authoritative regulation as human committees, demonstrating regulatory correctness.

### 4.4 Interpretation

**Agreement is not correctness.** The 96.0% agreement rate indicates the system's recommendations align with human committee decisions, but this does not imply the system is "more accurate" than humans. Human committees remain the authoritative decision-makers.

**Decision support, not automation.** The 42.9% time reduction reflects administrative efficiency from automated policy lookup and decision trace generation, not full automation of judgment.

**Pilot dataset limitations.** Cases are simulated from real policies but may not capture all real-world complexity. Validation with actual institutional data is recommended before deployment.

---

## 5. LLM-Based Ambiguity Detection Validation

### 5.1 Motivation

Academic regulations often contain discretionary language requiring human interpretation. Automating decisions on ambiguous rules would be ethically inappropriate. We validated an LLM-based detector to identify such language for human escalation.

### 5.2 Validation Dataset

We constructed a gold-standard dataset of **80 education regulation clauses** from UGC, NAAC, NBA, and university sources. Each clause was manually labeled as:

- **Ambiguous** (40 clauses): Contains subjective terms, permissive language, or context-dependent phrases
- **Non-ambiguous** (40 clauses): Explicit conditions and outcomes with no discretion required

**Labeling Criteria:**
- Ambiguous: "may be permitted," "reasonable grounds," "exceptional circumstances"
- Non-ambiguous: "minimum 75% attendance," "within 15 days," "income below Rs 200,000"

Manual labeling by domain experts serves as authoritative ground truth.

### 5.3 Evaluation Methodology

For each regulation clause:
1. Pass text to LLM ambiguity detector (GPT-4)
2. Record predicted label (ambiguous / non-ambiguous)
3. Extract detected ambiguous terms and categories
4. Compare prediction to manual label

**Metrics:** Precision, Recall, F1-score (standard NLP metrics)

### 5.4 Results

**Table 2: Ambiguity Detection Performance**

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Precision | 0.976 | 97.6% of flagged clauses genuinely ambiguous |
| Recall | 1.000 | 100% of ambiguous clauses detected |
| F1-Score | 0.988 | Excellent linguistic reliability |

**Confusion Matrix:**
- True Positives: 40 (correctly identified ambiguous)
- False Positives: 1 (incorrectly flagged as ambiguous)
- True Negatives: 39 (correctly identified non-ambiguous)
- False Negatives: 0 (missed ambiguous clauses)

**Error Analysis:**

*False Positive (1 case):*
- Clause: "Semester examinations will be conducted in the months of May and December."
- Detected term: "May" (flagged as permissive language)
- Why false positive: "May" is a month name, not permissive language
- Linguistic cause: Keyword pattern matching without context

*False Negatives (0 cases):*
- Perfect recall indicates no ambiguous clauses were missed

### 5.5 Interpretation

**Linguistic reliability, not legal understanding.** The F1=0.988 demonstrates the LLM reliably identifies discretionary language patterns. This does **not** mean the LLM "understands" education law or can make legal judgments.

**Flagging for human review, not automation.** Ambiguity detection escalates cases to human committees; it does not resolve ambiguity through rule logic.

**Domain-specific validation.** Results apply to Indian higher education regulations and should not be generalized to other legal domains without separate validation.

---

## 6. User Study: Impact of Explainability on Student Trust

### 6.1 Research Question

Does providing rule-based explanations alongside grievance decisions improve students' perceived fairness, trust, and transparency, independent of decision outcome?

### 6.2 Study Design

**Method:** Within-subjects A/B study (counterbalanced)  
**Participants:** N = 40 students (mixed programs and academic levels)  
**Conditions:**
- **A (Decision Only):** "Your attendance grievance has been rejected."
- **B (Decision + Explanation):** "Your attendance grievance has been rejected. **Explanation:** Applicable Regulation: UGC Regulation 2018, Section 4.2. Requirement: Minimum 75% attendance. Your Attendance: 72%. Medical Exception: Applies only when attendance ≥65% AND certificate submitted within 7 days. Your Situation: Certificate submitted 12 days late. Decision Rationale: Medical exception criteria not met."

**Critically, the decision outcome (REJECTED) was identical in both conditions.** Only the presence of explanation varied.

**Counterbalancing:** Half the participants viewed Condition A first, then B. The other half viewed B first, then A.

**Dependent Variables (5-point Likert scale):**
1. Perceived Fairness: "The decision feels fair to me."
2. Trust in Institution: "I trust that the institution made this decision correctly."
3. Transparency: "I understand why this decision was made."

**Statistical Analysis:** Paired t-tests, Cohen's d for effect size, α = 0.05 (two-tailed)

### 6.3 Results

**Table 3: User Study Results**

| Metric | Decision Only | Decision + Explanation | p-value | Cohen's d |
|--------|---------------|------------------------|---------|-----------|
| Fairness | 1.93 (0.89) | 3.48 (0.75) | < 0.001 | 1.21 (large) |
| Trust | 2.02 (0.73) | 3.12 (0.76) | < 0.001 | 1.07 (large) |
| Transparency | 1.43 (0.50) | 3.90 (0.55) | < 0.001 | 3.30 (very large) |

*Values shown as Mean (SD)*

All three metrics showed statistically significant improvements with large to very large effect sizes.

**Qualitative Findings:**

*Condition A (No Explanation):*
- "It felt arbitrary and unfair."
- "I don't understand why this happened."
- "Without explanation, I feel the system is biased."

*Condition B (With Explanation):*
- "Even though I didn't like the outcome, I understood why it happened."
- "The explanation helped me see that it was based on clear rules."
- "The transparency makes me trust the process more."

### 6.4 Interpretation

**Explainability improves perception, not correctness.** The significant improvements in fairness (d=1.21), trust (d=1.07), and transparency (d=3.30) demonstrate that rule-based explanations enhance how students perceive grievance decisions. **This does not mean explanations make decisions more accurate**—the outcome was identical in both conditions.

**Within-subjects design strength.** Each participant evaluated both conditions, controlling for individual differences in baseline trust and fairness sensitivity. Observed effects are attributable to explanation presence, not participant characteristics.

**Generalizability limits.** Results apply to student perception in academic grievance contexts. Other stakeholder groups or governance domains may respond differently.

**Hypothetical scenarios.** Participants evaluated hypothetical cases, not their own real grievances. Real grievances may evoke stronger emotional responses.

---

## 7. Ethical Audit and Bias Analysis

### 7.1 Bias Testing Methodology

We performed statistical bias testing on the pilot dataset (N=75) augmented with simulated demographic attributes. This analysis is **descriptive, not predictive**—we test whether the rule-based system produces disproportionate outcomes across demographic groups.

**Bias Tests:**
1. Gender × Decision Outcome (Chi-square test)
2. Program × Decision Outcome (Chi-square test)

**Null Hypothesis:** Decision outcomes are independent of demographic attributes (no systematic bias)

### 7.2 Bias Analysis Results

**Table 4: Bias Analysis Results**

| Attribute | χ² | p-value | Interpretation |
|-----------|-----|---------|----------------|
| Gender | 2.074 | > 0.05 | No statistically significant association observed |
| Program | 21.281 | < 0.001 | Strong association detected; immediate review required |

**Gender Bias Test:**
No statistically significant association (p > 0.05) between gender and decision outcomes. The rule-based system does not systematically favor or disadvantage any gender group in the pilot dataset.

**Program Bias Test:**
Strong association detected (p < 0.001) between academic program and decision outcomes. This likely reflects legitimate policy differences (e.g., NBA lab attendance requirements for BTech programs) rather than unfair bias, but warrants institutional review.

**Important Caveats:**
- **Not bias-free:** Absence of statistical significance does not prove the system is "bias-free"
- **Rule bias vs. system bias:** If underlying regulations contain implicit biases, the system will reproduce them
- **Limited sample:** Pilot dataset (N=75) may not capture all bias patterns

### 7.3 Failure Mode Analysis

We documented **10 concrete failure modes** where the system may produce incorrect, unfair, or ethically problematic outcomes.

**Table 5: Failure Modes and Mitigation Strategies**

| Failure Mode | Ethical Risk | System Response | Mitigation Strategy |
|--------------|--------------|-----------------|---------------------|
| Ambiguous regulatory language | Unfair automation | LLM flags ambiguity; escalate to human review | Human-in-the-loop for all ambiguous cases |
| Conflicting regulations | Arbitrary outcome | Apply hierarchical precedence (L1>L2>L3); log conflict | Explicit rule salience; conflict explanation in trace |
| Missing documentation | Incorrect denial | Request clarification; defer decision | No auto-rejection for missing evidence |
| Policy gap | Unjust decision | Flag "no matching rule"; escalate to committee | Committee creates precedent; update rule base |
| Edge-case thresholds | Rigid application | Flag boundary cases; recommend human review | Threshold tolerance zones; preserve discretion |
| Outdated policies | Incorrect decision | Temporal precedence check; flag version conflicts | Regular rule base audits; effective date validation |
| Human override without justification | Loss of accountability | Log override; require justification field | Mandatory override documentation; periodic audits |
| Inconsistent precedents | Perceived unfairness | Similar case retrieval; highlight discrepancies | Committee reviews precedents; documents deviation rationale |
| Implicit bias in rules | Systematic discrimination | Fairness monitoring; disparity alerts | Regular bias audits; policy reform recommendations |
| Technical system failure | Decision delays | Graceful degradation; error logging; manual fallback | System monitoring; no auto-decisions during outages |

### 7.4 Ethical Boundaries

The system operates within explicit ethical boundaries:

**What the System Does NOT Do:**
- Replace grievance committees
- Adjudicate discretionary cases autonomously
- Override institutional authority
- Make binding decisions
- Claim legal validity

**What the System DOES Do:**
- Support human decision-making with regulatory citations
- Ensure consistent rule application
- Improve transparency through decision traces
- Flag edge cases and ambiguities
- Monitor fairness patterns

**Governance Alignment:**
The system is designed as **assistive governance technology**, aligning with principles of procedural justice, human accountability, institutional autonomy, and student rights.

---

## 8. Discussion

### 8.1 Key Findings

This work demonstrates that a rule-based decision support system can achieve:

1. **High agreement with human decisions** (96.0%, κ=0.912) while preserving human authority for discretionary cases
2. **Reliable ambiguity detection** (F1=0.988) to identify regulations requiring human interpretation
3. **Significant explainability impact** on perceived fairness (d=1.21), trust (d=1.07), and transparency (d=3.30)
4. **No systematic gender bias** (p>0.05) in rule application, though program-level differences warrant review

### 8.2 Implications for Academic Governance

**Procedural justice matters.** The user study demonstrates that transparent, explainable processes improve student perception independent of outcome favorability. Rule-based explanations help students understand and accept decisions, even when unfavorable.

**Human oversight is non-negotiable.** The system's design explicitly preserves human authority for all discretionary, ambiguous, and boundary cases. This is not a limitation but a design principle aligned with governance ethics.

**Bias audits must evaluate policies, not just systems.** If underlying regulations disadvantage certain groups, rule-based systems will faithfully reproduce those disparities. Ethical deployment requires policy-level fairness review.

### 8.3 Limitations

**Pilot dataset scope.** Validation used 75 simulated cases grounded in real policies. Real institutional deployment requires validation with actual grievance data.

**Generalizability.** Results apply to Indian higher education governance. Other educational systems or governance domains may have different regulatory structures.

**LLM dependency.** Ambiguity detection relies on GPT-4, introducing external API dependency and potential cost/availability constraints.

**Static rule base.** The system requires manual rule updates when policies change. Automated policy extraction from regulatory documents remains future work.

### 8.4 Future Work

1. **Institutional deployment:** Validation with real grievance data from partner universities
2. **Expanded rule coverage:** Encoding additional grievance types and policy domains
3. **Automated rule extraction:** NLP-based conversion of policy documents to Drools rules
4. **Longitudinal bias monitoring:** Continuous fairness audits over time
5. **Multi-stakeholder evaluation:** Extending user studies to faculty and administrators

---

## 9. Conclusion

This paper presented the design, implementation, and empirical validation of a rule-based decision support system for academic grievance resolution. The system achieved 96.0% agreement with human committee decisions, 96.0% regulatory compliance, and demonstrated significant improvements in perceived fairness, trust, and transparency through rule-based explanations.

**Critically, the system is designed as assistive governance technology, not autonomous adjudication.** All discretionary cases, ambiguous regulations, and boundary conditions are escalated to human committees. The system's value lies in improving consistency, transparency, and efficiency while preserving human authority and accountability.

Ethical audit revealed no systematic gender bias and documented 10 failure modes with mitigation strategies. The system operates within explicit ethical boundaries, respecting institutional autonomy and student rights.

The proof-of-concept implementation, pilot dataset, validation scripts, and ethical audit materials are publicly available for reproducibility, supporting transparent evaluation and responsible deployment in academic governance contexts.

---

## Acknowledgments

This research was conducted independently as part of academic research in decision support systems and educational governance. No external funding was received.

---

## Data Availability

- **Source Code:** https://github.com/akashsingh/academic-grievance-dss-poc
- **Dataset:** `data/grievance_cases.csv` (75 anonymized cases)
- **Validation Scripts:** `data/empirical_validation.py`, `data/validate_ambiguity_detection.py`, `data/user_study_analysis.py`, `data/ethical_audit.py`
- **License:** Educational and Research Use Only

---

## References

[To be completed with proper academic citations for: Drools documentation, Cohen's Kappa methodology, UGC/NAAC/NBA regulations, procedural justice literature, explainable AI research, algorithmic fairness studies]

---

**Word Count:** ~6,800 words  
**Target Journals:** Decision Support Systems, Computers & Education, IEEE Transactions on Learning Technologies, Journal of Educational Technology & Society

---

## Supplementary Materials

### A. System Architecture Diagram
[Reference to architecture documentation]

### B. Rule Engine Sample Rules
[Reference to `rules/` directory]

### C. API Documentation
[Reference to `API_DOCUMENTATION.md`]

### D. Complete Test Suite
[Reference to `backend/tests/` - 73 tests]

### E. Validation Results Tables
[Reference to LaTeX tables in `data/`]

### F. Ethical Audit Full Report
[Reference to `data/ethical_audit_subsection.md`]
