package com.grievance.model;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

/**
 * RuleTrace model for tracking rule execution.
 * This is used as a global in Drools to capture the complete execution trace.
 */
public class RuleTrace implements Serializable {
    private static final long serialVersionUID = 1L;

    private List<FiredRule> firedRules;
    private List<Conflict> conflicts;
    private long startTime;
    private long endTime;

    public RuleTrace() {
        this.firedRules = new ArrayList<>();
        this.conflicts = new ArrayList<>();
        this.startTime = System.currentTimeMillis();
    }

    public void addFiredRule(String ruleId, String hierarchyLevel, int salience, 
                            String conditionsSummary, String outcome, String source) {
        FiredRule rule = new FiredRule(ruleId, hierarchyLevel, salience, 
                                      conditionsSummary, outcome, source);
        this.firedRules.add(rule);
    }

    public void addConflict(String type, List<String> conflictingRules, 
                           String resolutionStrategy, String winningRule, String reason) {
        Conflict conflict = new Conflict(type, conflictingRules, resolutionStrategy, 
                                        winningRule, reason);
        this.conflicts.add(conflict);
    }

    public void markComplete() {
        this.endTime = System.currentTimeMillis();
    }

    public long getProcessingTimeMs() {
        return endTime - startTime;
    }

    // Getters and Setters

    public List<FiredRule> getFiredRules() {
        return firedRules;
    }

    public void setFiredRules(List<FiredRule> firedRules) {
        this.firedRules = firedRules;
    }

    public List<Conflict> getConflicts() {
        return conflicts;
    }

    public void setConflicts(List<Conflict> conflicts) {
        this.conflicts = conflicts;
    }

    public long getStartTime() {
        return startTime;
    }

    public long getEndTime() {
        return endTime;
    }

    // Inner class for fired rules
    public static class FiredRule implements Serializable {
        private static final long serialVersionUID = 1L;

        private String ruleId;
        private String hierarchyLevel;
        private int salience;
        private String conditionsSummary;
        private String outcome;
        private String source;
        private long timestamp;

        public FiredRule(String ruleId, String hierarchyLevel, int salience,
                        String conditionsSummary, String outcome, String source) {
            this.ruleId = ruleId;
            this.hierarchyLevel = hierarchyLevel;
            this.salience = salience;
            this.conditionsSummary = conditionsSummary;
            this.outcome = outcome;
            this.source = source;
            this.timestamp = System.currentTimeMillis();
        }

        // Getters
        public String getRuleId() { return ruleId; }
        public String getHierarchyLevel() { return hierarchyLevel; }
        public int getSalience() { return salience; }
        public String getConditionsSummary() { return conditionsSummary; }
        public String getOutcome() { return outcome; }
        public String getSource() { return source; }
        public long getTimestamp() { return timestamp; }

        @Override
        public String toString() {
            return "FiredRule{ruleId='" + ruleId + "', level=" + hierarchyLevel + 
                   ", salience=" + salience + ", outcome='" + outcome + "'}";
        }
    }

    // Inner class for conflicts
    public static class Conflict implements Serializable {
        private static final long serialVersionUID = 1L;

        private String type;
        private List<String> conflictingRules;
        private String resolutionStrategy;
        private String winningRule;
        private String reason;

        public Conflict(String type, List<String> conflictingRules, 
                       String resolutionStrategy, String winningRule, String reason) {
            this.type = type;
            this.conflictingRules = conflictingRules;
            this.resolutionStrategy = resolutionStrategy;
            this.winningRule = winningRule;
            this.reason = reason;
        }

        // Getters
        public String getType() { return type; }
        public List<String> getConflictingRules() { return conflictingRules; }
        public String getResolutionStrategy() { return resolutionStrategy; }
        public String getWinningRule() { return winningRule; }
        public String getReason() { return reason; }

        @Override
        public String toString() {
            return "Conflict{type='" + type + "', winning='" + winningRule + "'}";
        }
    }

    @Override
    public String toString() {
        return "RuleTrace{" +
                "firedRules=" + firedRules.size() +
                ", conflicts=" + conflicts.size() +
                ", processingTime=" + getProcessingTimeMs() + "ms" +
                '}';
    }
}
