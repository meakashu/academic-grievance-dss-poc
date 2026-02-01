package com.grievance.model;

import java.io.Serializable;

/**
 * Decision model representing the outcome of grievance evaluation.
 * This class is inserted as a fact by Drools rules.
 */
public class Decision implements Serializable {
    private static final long serialVersionUID = 1L;

    private String id;
    private String grievanceId;
    private String outcome; // ACCEPT, REJECT, PARTIAL_ACCEPT, PENDING_CLARIFICATION
    private String applicableRule;
    private String regulatorySource;
    private String hierarchyLevel;
    private Integer salience;
    private String reason;
    private String explanation;
    private String actionRequired;
    private Boolean humanReviewRequired;

    public Decision() {
        this.humanReviewRequired = false;
    }

    // Getters and Setters

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getGrievanceId() {
        return grievanceId;
    }

    public void setGrievanceId(String grievanceId) {
        this.grievanceId = grievanceId;
    }

    public String getOutcome() {
        return outcome;
    }

    public void setOutcome(String outcome) {
        this.outcome = outcome;
    }

    public String getApplicableRule() {
        return applicableRule;
    }

    public void setApplicableRule(String applicableRule) {
        this.applicableRule = applicableRule;
    }

    public String getRegulatorySource() {
        return regulatorySource;
    }

    public void setRegulatorySource(String regulatorySource) {
        this.regulatorySource = regulatorySource;
    }

    public String getHierarchyLevel() {
        return hierarchyLevel;
    }

    public void setHierarchyLevel(String hierarchyLevel) {
        this.hierarchyLevel = hierarchyLevel;
    }

    public Integer getSalience() {
        return salience;
    }

    public void setSalience(Integer salience) {
        this.salience = salience;
    }

    public String getReason() {
        return reason;
    }

    public void setReason(String reason) {
        this.reason = reason;
    }

    public String getExplanation() {
        return explanation;
    }

    public void setExplanation(String explanation) {
        this.explanation = explanation;
    }

    public String getActionRequired() {
        return actionRequired;
    }

    public void setActionRequired(String actionRequired) {
        this.actionRequired = actionRequired;
    }

    public Boolean getHumanReviewRequired() {
        return humanReviewRequired;
    }

    public void setHumanReviewRequired(Boolean humanReviewRequired) {
        this.humanReviewRequired = humanReviewRequired;
    }

    @Override
    public String toString() {
        return "Decision{" +
                "outcome='" + outcome + '\'' +
                ", applicableRule='" + applicableRule + '\'' +
                ", hierarchyLevel='" + hierarchyLevel + '\'' +
                ", salience=" + salience +
                ", reason='" + reason + '\'' +
                '}';
    }
}
