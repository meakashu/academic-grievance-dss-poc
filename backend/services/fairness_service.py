"""
Fairness Monitoring Service
Ensures consistency and detects anomalies in decision-making
"""
from typing import List, Dict, Any, Optional, Tuple
import logging
from collections import Counter
from uuid import UUID



logger = logging.getLogger(__name__)


class FairnessService:
    """
    Service for monitoring fairness in grievance decisions
    
    Implements:
    - Consistency checking across similar cases
    - Anomaly detection for outlier decisions
    - Demographic parity analysis
    """
    
    def __init__(self):
        # Dynamically get database service (could be real or mock)
        try:
            from services.database_service import get_database_service
            self.db_service = get_database_service()
        except:
            from services.mock_database_service import get_mock_database_service
            self.db_service = get_mock_database_service()
        self.consistency_threshold = 0.85  # 85% consistency required
    
    def calculate_consistency_score(
        self,
        current_decision: Dict[str, Any],
        similar_cases: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate consistency score between current decision and historical cases
        
        Score is based on:
        - Outcome consistency (same outcome for similar parameters)
        - Rule consistency (same rule applied)
        - Hierarchy level consistency
        
        Args:
            current_decision: Current decision details
            similar_cases: List of similar historical cases
            
        Returns:
            Consistency score between 0.0 and 1.0
        """
        if not similar_cases:
            logger.warning("No similar cases found for consistency check")
            return 1.0  # No comparison possible
        
        current_outcome = current_decision.get('outcome')
        current_rule = current_decision.get('applicable_rule')
        current_level = current_decision.get('hierarchy_level')
        
        # Count matching outcomes
        outcome_matches = sum(
            1 for case in similar_cases 
            if case.get('outcome') == current_outcome
        )
        
        # Count matching rules
        rule_matches = sum(
            1 for case in similar_cases 
            if case.get('applicable_rule') == current_rule
        )
        
        # Count matching hierarchy levels
        level_matches = sum(
            1 for case in similar_cases 
            if case.get('hierarchy_level') == current_level
        )
        
        total_cases = len(similar_cases)
        
        # Weighted average: outcome (50%), rule (30%), level (20%)
        outcome_score = outcome_matches / total_cases
        rule_score = rule_matches / total_cases
        level_score = level_matches / total_cases
        
        consistency_score = (
            0.5 * outcome_score +
            0.3 * rule_score +
            0.2 * level_score
        )
        
        logger.info(
            f"Consistency score: {consistency_score:.3f} "
            f"(outcome: {outcome_score:.2f}, rule: {rule_score:.2f}, level: {level_score:.2f})"
        )
        
        return round(consistency_score, 4)
    
    def detect_anomaly(
        self,
        consistency_score: float,
        current_decision: Dict[str, Any],
        similar_cases: List[Dict[str, Any]]
    ) -> Tuple[bool, Optional[str]]:
        """
        Detect if current decision is an anomaly
        
        An anomaly is detected if:
        - Consistency score is below threshold
        - Decision outcome differs significantly from historical pattern
        
        Args:
            consistency_score: Calculated consistency score
            current_decision: Current decision details
            similar_cases: List of similar historical cases
            
        Returns:
            Tuple of (is_anomaly, reason)
        """
        if consistency_score < self.consistency_threshold:
            # Analyze why it's inconsistent
            current_outcome = current_decision.get('outcome')
            
            # Get most common outcome in similar cases
            outcomes = [case.get('outcome') for case in similar_cases]
            outcome_counts = Counter(outcomes)
            most_common_outcome, count = outcome_counts.most_common(1)[0]
            
            if current_outcome != most_common_outcome:
                reason = (
                    f"Decision outcome '{current_outcome}' differs from "
                    f"most common outcome '{most_common_outcome}' "
                    f"({count}/{len(similar_cases)} cases). "
                    f"Consistency score: {consistency_score:.3f} "
                    f"(threshold: {self.consistency_threshold})"
                )
                logger.warning(f"Anomaly detected: {reason}")
                return True, reason
        
        return False, None
    
    def analyze_demographic_parity(
        self,
        grievance_type: str,
        student_category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze demographic parity for a grievance type
        
        Checks if decisions are consistent across different student categories
        (e.g., SC/ST, OBC, General)
        
        Args:
            grievance_type: Type of grievance
            student_category: Student category (optional)
            
        Returns:
            Dictionary with parity analysis
        """
        # This would require demographic data in the database
        # For now, return a placeholder
        logger.info(f"Analyzing demographic parity for {grievance_type}")
        
        return {
            "grievance_type": grievance_type,
            "student_category": student_category,
            "analysis": "Demographic parity analysis requires historical demographic data",
            "parity_score": None,
            "recommendation": "Collect demographic data for comprehensive fairness monitoring"
        }
    
    def monitor_fairness(
        self,
        grievance_id: UUID,
        decision: Dict[str, Any],
        grievance_type: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Comprehensive fairness monitoring for a decision
        
        Args:
            grievance_id: Grievance ID
            decision: Decision details
            grievance_type: Type of grievance
            parameters: Grievance parameters
            
        Returns:
            Fairness report with consistency score and anomaly detection
        """
        logger.info(f"Monitoring fairness for grievance {grievance_id}")
        
        # Find similar historical cases
        similar_cases = self.db_service.find_similar_cases(
            grievance_type=grievance_type,
            parameters=parameters,
            limit=10
        )
        
        logger.info(f"Found {len(similar_cases)} similar cases")
        
        # Calculate consistency score
        consistency_score = self.calculate_consistency_score(
            current_decision=decision,
            similar_cases=similar_cases
        )
        
        # Detect anomaly
        is_anomaly, anomaly_reason = self.detect_anomaly(
            consistency_score=consistency_score,
            current_decision=decision,
            similar_cases=similar_cases
        )
        
        # Analyze demographic parity
        demographic_parity = self.analyze_demographic_parity(
            grievance_type=grievance_type,
            student_category=parameters.get('student_category')
        )
        
        # Create fairness report
        fairness_report = {
            "grievance_id": str(grievance_id),
            "consistency_score": consistency_score,
            "consistency_threshold": self.consistency_threshold,
            "meets_threshold": consistency_score >= self.consistency_threshold,
            "anomaly_detected": is_anomaly,
            "anomaly_reason": anomaly_reason,
            "similar_cases_count": len(similar_cases),
            "similar_cases": [
                {
                    "grievance_id": str(case.get('grievance_id')),
                    "outcome": case.get('outcome'),
                    "applicable_rule": case.get('applicable_rule'),
                    "hierarchy_level": case.get('hierarchy_level')
                }
                for case in similar_cases[:5]  # Top 5 for display
            ],
            "demographic_parity": demographic_parity,
            "recommendation": self._generate_recommendation(
                consistency_score, is_anomaly
            )
        }
        
        # Store fairness check in database
        try:
            self.db_service.create_fairness_check(
                grievance_id=grievance_id,
                decision_id=UUID(decision.get('id')) if decision.get('id') else None,
                similar_cases=similar_cases,
                consistency_score=consistency_score,
                anomaly_detected=is_anomaly,
                demographic_parity=demographic_parity
            )
            logger.info(f"Fairness check stored for grievance {grievance_id}")
        except Exception as e:
            logger.error(f"Failed to store fairness check: {str(e)}")
        
        return fairness_report
    
    def _generate_recommendation(
        self,
        consistency_score: float,
        is_anomaly: bool
    ) -> str:
        """Generate recommendation based on fairness analysis"""
        if is_anomaly:
            return (
                "⚠️ HUMAN REVIEW RECOMMENDED: This decision shows significant "
                "deviation from historical patterns. Please review for potential "
                "bias or exceptional circumstances."
            )
        elif consistency_score < 0.90:
            return (
                "ℹ️ REVIEW SUGGESTED: While within acceptable range, this decision "
                "shows some variation from typical outcomes. Consider reviewing "
                "for consistency."
            )
        else:
            return (
                "✓ CONSISTENT: This decision aligns well with historical patterns "
                "for similar cases."
            )
    
    def get_fairness_metrics(self) -> Dict[str, Any]:
        """
        Get overall fairness metrics across all decisions
        
        Returns:
            Dictionary with aggregate fairness statistics
        """
        # This would query the fairness_checks table for aggregate statistics
        # For now, return placeholder
        return {
            "total_checks": 0,
            "average_consistency_score": 0.0,
            "anomalies_detected": 0,
            "anomaly_rate": 0.0,
            "recommendation": "Accumulate more data for comprehensive metrics"
        }


# Singleton instance
_fairness_service: Optional[FairnessService] = None


def get_fairness_service() -> FairnessService:
    """Get or create fairness service instance"""
    global _fairness_service
    if _fairness_service is None:
        _fairness_service = FairnessService()
    return _fairness_service
