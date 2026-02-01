package com.grievance.engine;

import com.grievance.model.Grievance;
import com.grievance.model.Decision;
import com.grievance.model.RuleTrace;

import org.kie.api.KieServices;
import org.kie.api.runtime.KieContainer;
import org.kie.api.runtime.KieSession;
import org.kie.api.runtime.rule.FactHandle;
import org.kie.api.io.ResourceType;
import org.kie.internal.utils.KieHelper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Drools Rule Engine for Academic Grievance DSS
 * 
 * This class manages the Drools rule engine lifecycle:
 * - Loading .drl files from the rules directory
 * - Creating and managing KIE sessions
 * - Executing rules against grievance facts
 * - Capturing rule traces and decisions
 */
public class DroolsEngine {
    private static final Logger logger = LoggerFactory.getLogger(DroolsEngine.class);
    
    private KieServices kieServices;
    private KieContainer kieContainer;
    private String rulesDirectory;
    
    /**
     * Constructor with custom rules directory
     * @param rulesDirectory Path to directory containing .drl files
     */
    public DroolsEngine(String rulesDirectory) {
        this.rulesDirectory = rulesDirectory;
        this.kieServices = KieServices.Factory.get();
        initializeRuleEngine();
    }
    
    /**
     * Default constructor - uses ./rules directory
     */
    public DroolsEngine() {
        this("./rules");
    }
    
    /**
     * Initialize the rule engine by loading all .drl files
     */
    private void initializeRuleEngine() {
        try {
            logger.info("Initializing Drools engine from directory: {}", rulesDirectory);
            
            KieHelper kieHelper = new KieHelper();
            
            // Find all .drl files in the rules directory
            List<Path> drlFiles = findDrlFiles(rulesDirectory);
            logger.info("Found {} DRL files", drlFiles.size());
            
            // Load each .drl file
            for (Path drlFile : drlFiles) {
                logger.info("Loading rule file: {}", drlFile.getFileName());
                String drlContent = new String(Files.readAllBytes(drlFile));
                kieHelper.addContent(drlContent, ResourceType.DRL);
            }
            
            // Build the KIE base
            this.kieContainer = kieHelper.getKieContainer();
            logger.info("Drools engine initialized successfully");
            
        } catch (Exception e) {
            logger.error("Failed to initialize Drools engine", e);
            throw new RuntimeException("Failed to initialize Drools engine", e);
        }
    }
    
    /**
     * Find all .drl files in the specified directory
     */
    private List<Path> findDrlFiles(String directory) throws IOException {
        Path dirPath = Paths.get(directory);
        
        if (!Files.exists(dirPath)) {
            logger.warn("Rules directory does not exist: {}", directory);
            return new ArrayList<>();
        }
        
        try (Stream<Path> paths = Files.walk(dirPath)) {
            return paths
                .filter(Files::isRegularFile)
                .filter(p -> p.toString().endsWith(".drl"))
                .collect(Collectors.toList());
        }
    }
    
    /**
     * Evaluate a grievance against all loaded rules
     * 
     * @param grievance The grievance to evaluate
     * @return EvaluationResult containing decision and trace
     */
    public EvaluationResult evaluateGrievance(Grievance grievance) {
        logger.info("Evaluating grievance: {} (type: {})", grievance.getId(), grievance.getType());
        
        // Create a new KIE session
        KieSession kieSession = kieContainer.newKieSession();
        
        try {
            // Create rule trace to capture execution
            RuleTrace ruleTrace = new RuleTrace();
            
            // Set the rule trace as a global
            kieSession.setGlobal("ruleTrace", ruleTrace);
            
            // Insert the grievance as a fact
            FactHandle grievanceHandle = kieSession.insert(grievance);
            
            // Fire all rules
            int rulesFired = kieSession.fireAllRules();
            logger.info("Fired {} rules for grievance {}", rulesFired, grievance.getId());
            
            // Mark trace as complete
            ruleTrace.markComplete();
            
            // Collect all decisions from working memory
            Collection<Decision> decisions = getDecisionsFromSession(kieSession);
            
            // Determine final decision (highest salience wins)
            Decision finalDecision = selectFinalDecision(decisions);
            
            // Detect conflicts
            List<RuleTrace.Conflict> conflicts = detectConflicts(decisions, ruleTrace);
            if (!conflicts.isEmpty()) {
                ruleTrace.setConflicts(conflicts);
                logger.info("Detected {} conflicts", conflicts.size());
            }
            
            // Create and return result
            EvaluationResult result = new EvaluationResult();
            result.setGrievance(grievance);
            result.setFinalDecision(finalDecision);
            result.setRuleTrace(ruleTrace);
            result.setAllDecisions(new ArrayList<>(decisions));
            result.setRulesFired(rulesFired);
            
            return result;
            
        } finally {
            // Always dispose the session
            kieSession.dispose();
        }
    }
    
    /**
     * Get all Decision objects from the KIE session
     */
    private Collection<Decision> getDecisionsFromSession(KieSession kieSession) {
        Collection<Decision> decisions = new ArrayList<>();
        
        for (Object obj : kieSession.getObjects()) {
            if (obj instanceof Decision) {
                decisions.add((Decision) obj);
            }
        }
        
        return decisions;
    }
    
    /**
     * Select the final decision based on salience (highest wins)
     */
    private Decision selectFinalDecision(Collection<Decision> decisions) {
        if (decisions.isEmpty()) {
            logger.warn("No decisions generated");
            return null;
        }
        
        // Sort by salience (descending) and return the first
        return decisions.stream()
            .max((d1, d2) -> Integer.compare(
                d1.getSalience() != null ? d1.getSalience() : 0,
                d2.getSalience() != null ? d2.getSalience() : 0
            ))
            .orElse(null);
    }
    
    /**
     * Detect conflicts between rules (multiple decisions with different outcomes)
     */
    private List<RuleTrace.Conflict> detectConflicts(Collection<Decision> decisions, RuleTrace ruleTrace) {
        List<RuleTrace.Conflict> conflicts = new ArrayList<>();
        
        if (decisions.size() <= 1) {
            return conflicts; // No conflict if 0 or 1 decision
        }
        
        // Group decisions by hierarchy level
        List<Decision> sortedDecisions = decisions.stream()
            .sorted((d1, d2) -> Integer.compare(
                d2.getSalience() != null ? d2.getSalience() : 0,
                d1.getSalience() != null ? d1.getSalience() : 0
            ))
            .collect(Collectors.toList());
        
        // Check for authority conflicts (different hierarchy levels)
        boolean hasAuthorityConflict = decisions.stream()
            .map(Decision::getHierarchyLevel)
            .distinct()
            .count() > 1;
        
        if (hasAuthorityConflict && sortedDecisions.size() >= 2) {
            Decision winner = sortedDecisions.get(0);
            Decision loser = sortedDecisions.get(1);
            
            List<String> conflictingRules = new ArrayList<>();
            conflictingRules.add(winner.getApplicableRule() + " (" + winner.getHierarchyLevel() + ")");
            conflictingRules.add(loser.getApplicableRule() + " (" + loser.getHierarchyLevel() + ")");
            
            String reason = String.format("%s supersedes %s based on authority precedence",
                winner.getHierarchyLevel(), loser.getHierarchyLevel());
            
            RuleTrace.Conflict conflict = new RuleTrace.Conflict(
                "AUTHORITY_CONFLICT",
                conflictingRules,
                "Authority Precedence",
                winner.getApplicableRule(),
                reason
            );
            
            conflicts.add(conflict);
        }
        
        return conflicts;
    }
    
    /**
     * Reload all rules from the rules directory
     */
    public void reloadRules() {
        logger.info("Reloading rules...");
        initializeRuleEngine();
    }
    
    /**
     * Get the number of loaded rules
     */
    public int getLoadedRulesCount() {
        try {
            return findDrlFiles(rulesDirectory).size();
        } catch (IOException e) {
            logger.error("Error counting DRL files", e);
            return 0;
        }
    }
    
    /**
     * Result class containing evaluation output
     */
    public static class EvaluationResult {
        private Grievance grievance;
        private Decision finalDecision;
        private RuleTrace ruleTrace;
        private List<Decision> allDecisions;
        private int rulesFired;
        
        // Getters and setters
        public Grievance getGrievance() { return grievance; }
        public void setGrievance(Grievance grievance) { this.grievance = grievance; }
        
        public Decision getFinalDecision() { return finalDecision; }
        public void setFinalDecision(Decision finalDecision) { this.finalDecision = finalDecision; }
        
        public RuleTrace getRuleTrace() { return ruleTrace; }
        public void setRuleTrace(RuleTrace ruleTrace) { this.ruleTrace = ruleTrace; }
        
        public List<Decision> getAllDecisions() { return allDecisions; }
        public void setAllDecisions(List<Decision> allDecisions) { this.allDecisions = allDecisions; }
        
        public int getRulesFired() { return rulesFired; }
        public void setRulesFired(int rulesFired) { this.rulesFired = rulesFired; }
        
        @Override
        public String toString() {
            return "EvaluationResult{" +
                    "rulesFired=" + rulesFired +
                    ", finalDecision=" + (finalDecision != null ? finalDecision.getOutcome() : "null") +
                    ", conflicts=" + (ruleTrace != null ? ruleTrace.getConflicts().size() : 0) +
                    '}';
        }
    }
    
    /**
     * Main method for testing
     */
    public static void main(String[] args) {
        logger.info("Starting Drools Engine Test");
        
        DroolsEngine engine = new DroolsEngine("../rules");
        logger.info("Loaded {} rule files", engine.getLoadedRulesCount());
        
        // Create a test grievance
        Grievance testGrievance = new Grievance();
        testGrievance.setId("TEST-001");
        testGrievance.setStudentId("STU2024001");
        testGrievance.setType("ATTENDANCE_SHORTAGE");
        testGrievance.setAttendancePercentage(72.0);
        testGrievance.setHasMedicalCertificate(true);
        testGrievance.setMedicalCertificateValid(true);
        testGrievance.setMedicalCertificateFromRecognizedAuthority(true);
        
        // Evaluate
        EvaluationResult result = engine.evaluateGrievance(testGrievance);
        
        logger.info("Result: {}", result);
        if (result.getFinalDecision() != null) {
            logger.info("Final Decision: {} - {}", 
                result.getFinalDecision().getOutcome(),
                result.getFinalDecision().getReason());
        }
    }
}
