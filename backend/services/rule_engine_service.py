"""
Rule Engine Service - Python-Java Bridge
Integrates Drools rule engine via JPype1
"""
import jpype
import jpype.imports
from jpype.types import *
from typing import Dict, Any, List, Optional
import logging
import os
from pathlib import Path

from config import settings
from models import Grievance, Decision, RuleTrace, FiredRuleInfo, ConflictInfo

logger = logging.getLogger(__name__)


class RuleEngineService:
    """
    Service for rule engine integration via JPype1
    
    Bridges Python and Java to execute Drools rules
    """
    
    def __init__(self):
        self.jvm_started = False
        self.drools_engine = None
        self._initialize_jvm()
        self._initialize_drools()
    
    def _initialize_jvm(self):
        """Initialize JVM with JPype1"""
        if jpype.isJVMStarted():
            logger.info("JVM already started")
            self.jvm_started = True
            return
        
        try:
            # Find JAR file
            jar_path = self._find_jar_file()
            
            if not jar_path:
                raise FileNotFoundError(
                    "Drools JAR not found. Please run: cd java-bridge && mvn clean package"
                )
            
            # Set JAVA_HOME if configured
            if settings.java_home:
                os.environ['JAVA_HOME'] = settings.java_home
            
            # Start JVM with classpath
            jpype.startJVM(
                classpath=[str(jar_path)],
                convertStrings=True
            )
            
            logger.info(f"JVM started successfully with JAR: {jar_path}")
            self.jvm_started = True
            
        except Exception as e:
            logger.error(f"Failed to start JVM: {str(e)}")
            raise
    
    def _find_jar_file(self) -> Optional[Path]:
        """Find the Drools JAR file"""
        # Look in java-bridge/target directory
        target_dir = Path("java-bridge/target")
        
        if not target_dir.exists():
            logger.warning(f"Target directory not found: {target_dir}")
            return None
        
        # Find JAR with dependencies (shaded JAR)
        jar_files = list(target_dir.glob("*-jar-with-dependencies.jar"))
        
        if not jar_files:
            # Try regular JAR
            jar_files = list(target_dir.glob("grievance-dss-java-bridge-*.jar"))
        
        if jar_files:
            jar_path = jar_files[0]
            logger.info(f"Found JAR: {jar_path}")
            return jar_path
        
        return None
    
    def _initialize_drools(self):
        """Initialize Drools engine"""
        if not self.jvm_started:
            raise RuntimeError("JVM not started")
        
        try:
            # Import Java classes
            from com.grievance.engine import DroolsEngine
            from com.grievance.model import Grievance as JavaGrievance
            from com.grievance.model import Decision as JavaDecision
            from com.grievance.model import RuleTrace as JavaRuleTrace
            
            # Store class references
            self.DroolsEngine = DroolsEngine
            self.JavaGrievance = JavaGrievance
            self.JavaDecision = JavaDecision
            self.JavaRuleTrace = JavaRuleTrace
            
            # Create Drools engine instance
            rules_path = settings.drools_rules_path
            self.drools_engine = DroolsEngine(rules_path)
            
            logger.info(f"Drools engine initialized with rules from: {rules_path}")
            logger.info(f"Loaded {self.drools_engine.getLoadedRulesCount()} rule files")
            
        except Exception as e:
            logger.error(f"Failed to initialize Drools: {str(e)}")
            raise
    
    def _convert_to_java_grievance(self, grievance: Dict[str, Any]) -> Any:
        """Convert Python grievance dict to Java Grievance object"""
        java_grievance = self.JavaGrievance()
        
        # Set basic fields
        java_grievance.setId(str(grievance.get('id', '')))
        java_grievance.setStudentId(grievance.get('student_id', ''))
        java_grievance.setType(grievance.get('grievance_type', ''))
        java_grievance.setNarrative(grievance.get('narrative', ''))
        
        # Set parameters based on grievance type
        params = grievance.get('parameters', {})
        
        # Attendance fields
        if 'attendance_percentage' in params:
            java_grievance.setAttendancePercentage(
                JDouble(params['attendance_percentage'])
            )
        if 'has_medical_certificate' in params:
            java_grievance.setHasMedicalCertificate(
                JBoolean(params['has_medical_certificate'])
            )
        if 'medical_certificate_valid' in params:
            java_grievance.setMedicalCertificateValid(
                JBoolean(params['medical_certificate_valid'])
            )
        if 'medical_certificate_from_recognized_authority' in params:
            java_grievance.setMedicalCertificateFromRecognizedAuthority(
                JBoolean(params['medical_certificate_from_recognized_authority'])
            )
        if 'days_absent' in params:
            java_grievance.setDaysAbsent(JInt(params['days_absent']))
        
        # Examination fields
        if 'exam_type' in params:
            java_grievance.setExamType(params['exam_type'])
        if 'course_code' in params:
            java_grievance.setCourseCode(params['course_code'])
        if 'marks_obtained' in params:
            java_grievance.setMarksObtained(JInt(params['marks_obtained']))
        if 'days_since_result_declaration' in params:
            java_grievance.setDaysSinceResultDeclaration(
                JInt(params['days_since_result_declaration'])
            )
        if 'revaluation_fee_paid' in params:
            java_grievance.setReevaluationFeePaid(
                JBoolean(params['revaluation_fee_paid'])
            )
        
        # Fee fields
        if 'student_category' in params:
            java_grievance.setStudentCategory(params['student_category'])
        if 'family_income' in params:
            java_grievance.setFamilyIncome(JDouble(params['family_income']))
        if 'has_income_certificate' in params:
            java_grievance.setHasIncomeCertificate(
                JBoolean(params['has_income_certificate'])
            )
        if 'has_category_certificate' in params:
            java_grievance.setHasCategoryCertificate(
                JBoolean(params['has_category_certificate'])
            )
        
        return java_grievance
    
    def _convert_from_java_decision(self, java_decision: Any) -> Dict[str, Any]:
        """Convert Java Decision object to Python dict"""
        if java_decision is None:
            return None
        
        return {
            'outcome': str(java_decision.getOutcome()),
            'applicable_rule': str(java_decision.getApplicableRule()),
            'regulatory_source': str(java_decision.getRegulatorySource()),
            'hierarchy_level': str(java_decision.getHierarchyLevel()),
            'salience': int(java_decision.getSalience()) if java_decision.getSalience() else 0,
            'reason': str(java_decision.getReason()),
            'explanation': str(java_decision.getExplanation()) if java_decision.getExplanation() else None,
            'action_required': str(java_decision.getActionRequired()) if java_decision.getActionRequired() else None,
            'human_review_required': bool(java_decision.getHumanReviewRequired())
        }
    
    def _convert_from_java_trace(self, java_trace: Any) -> Dict[str, Any]:
        """Convert Java RuleTrace object to Python dict"""
        if java_trace is None:
            return {
                'rules_evaluated': [],
                'conflicts_detected': [],
                'final_decision': {},
                'processing_time_ms': 0
            }
        
        # Convert fired rules
        rules_evaluated = []
        for fired_rule in java_trace.getFiredRules():
            rules_evaluated.append({
                'rule_id': str(fired_rule.getRuleId()),
                'hierarchy_level': str(fired_rule.getHierarchyLevel()),
                'salience': int(fired_rule.getSalience()),
                'conditions_summary': str(fired_rule.getConditionsSummary()),
                'outcome': str(fired_rule.getOutcome()),
                'source': str(fired_rule.getSource())
            })
        
        # Convert conflicts
        conflicts_detected = []
        for conflict in java_trace.getConflicts():
            conflicting_rules = []
            for rule in conflict.getConflictingRules():
                conflicting_rules.append(str(rule))
            
            conflicts_detected.append({
                'type': str(conflict.getType()),
                'conflicting_rules': conflicting_rules,
                'resolution_strategy': str(conflict.getResolutionStrategy()),
                'winning_rule': str(conflict.getWinningRule()),
                'reason': str(conflict.getReason())
            })
        
        return {
            'rules_evaluated': rules_evaluated,
            'conflicts_detected': conflicts_detected,
            'processing_time_ms': int(java_trace.getProcessingTimeMs())
        }
    
    def evaluate_grievance(self, grievance: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a grievance using Drools rule engine
        
        Args:
            grievance: Grievance dictionary with parameters
            
        Returns:
            Dictionary with decision and rule trace
        """
        if not self.drools_engine:
            raise RuntimeError("Drools engine not initialized")
        
        logger.info(f"Evaluating grievance: {grievance.get('id')}")
        
        try:
            # Convert to Java object
            java_grievance = self._convert_to_java_grievance(grievance)
            
            # Evaluate using Drools
            result = self.drools_engine.evaluateGrievance(java_grievance)
            
            # Extract decision
            java_decision = result.getFinalDecision()
            decision = self._convert_from_java_decision(java_decision)
            
            # Extract trace
            java_trace = result.getRuleTrace()
            trace = self._convert_from_java_trace(java_trace)
            
            # Add final decision to trace
            if decision:
                trace['final_decision'] = decision
            
            logger.info(
                f"Evaluation complete: {result.getRulesFired()} rules fired, "
                f"outcome: {decision.get('outcome') if decision else 'None'}"
            )
            
            return {
                'decision': decision,
                'trace': trace,
                'rules_fired': int(result.getRulesFired())
            }
            
        except Exception as e:
            logger.error(f"Error evaluating grievance: {str(e)}")
            raise
    
    def reload_rules(self):
        """Reload all rules from the rules directory"""
        if self.drools_engine:
            logger.info("Reloading rules...")
            self.drools_engine.reloadRules()
            logger.info(f"Reloaded {self.drools_engine.getLoadedRulesCount()} rule files")
    
    def shutdown(self):
        """Shutdown JVM"""
        if self.jvm_started and jpype.isJVMStarted():
            jpype.shutdownJVM()
            logger.info("JVM shutdown complete")


# Singleton instance
_rule_engine_service: Optional[RuleEngineService] = None


def get_rule_engine_service() -> RuleEngineService:
    """Get or create rule engine service instance"""
    global _rule_engine_service
    if _rule_engine_service is None:
        _rule_engine_service = RuleEngineService()
    return _rule_engine_service
