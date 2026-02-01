"""
Mock Database Service (for testing without PostgreSQL)
Stores data in memory
"""
from typing import Dict, Any, List, Optional
from uuid import uuid4
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MockDatabaseService:
    """Mock database service using in-memory storage"""
    
    def __init__(self):
        self.grievances: Dict[str, Dict[str, Any]] = {}
        self.decisions: Dict[str, Dict[str, Any]] = {}
        self.rule_traces: Dict[str, Dict[str, Any]] = {}
        self.fairness_checks: Dict[str, Dict[str, Any]] = {}
        logger.info("Mock Database Service initialized (in-memory storage)")
    
    def create_grievance(
        self,
        student_id: str,
        grievance_type: str,
        narrative: str,
        parameters: Dict[str, Any],
        status: str = "PENDING"
    ) -> str:
        """Create a new grievance"""
        grievance_id = str(uuid4())
        now = datetime.utcnow().isoformat()
        
        self.grievances[grievance_id] = {
            "id": grievance_id,
            "student_id": student_id,
            "grievance_type": grievance_type,
            "narrative": narrative,
            "parameters": parameters,
            "status": status,
            "submitted_at": now,
            "created_at": now,
            "updated_at": now
        }
        
        logger.info(f"Created grievance: {grievance_id}")
        return grievance_id
    
    def get_grievance(self, grievance_id: str) -> Optional[Dict[str, Any]]:
        """Get grievance by ID"""
        return self.grievances.get(grievance_id)
    
    def update_grievance_status(self, grievance_id: str, status: str):
        """Update grievance status"""
        if grievance_id in self.grievances:
            self.grievances[grievance_id]["status"] = status
            self.grievances[grievance_id]["updated_at"] = datetime.utcnow().isoformat()
    
    def create_decision(
        self,
        grievance_id: str,
        outcome: str,
        applicable_rule: str,
        regulatory_source: str,
        hierarchy_level: str,
        salience: int,
        reason: str,
        explanation: Optional[str] = None,
        action_required: Optional[str] = None,
        human_review_required: bool = False
    ) -> str:
        """Create a new decision"""
        decision_id = str(uuid4())
        now = datetime.utcnow().isoformat()
        
        self.decisions[decision_id] = {
            "id": decision_id,
            "grievance_id": grievance_id,
            "outcome": outcome,
            "applicable_rule": applicable_rule,
            "regulatory_source": regulatory_source,
            "hierarchy_level": hierarchy_level,
            "salience": salience,
            "reason": reason,
            "explanation": explanation,
            "action_required": action_required,
            "human_review_required": human_review_required,
            "decided_at": now,
            "created_at": now
        }
        
        logger.info(f"Created decision: {decision_id} for grievance: {grievance_id}")
        return decision_id
    
    def get_decision(self, decision_id: str) -> Optional[Dict[str, Any]]:
        """Get decision by ID"""
        return self.decisions.get(decision_id)
    
    def get_decision_by_grievance(self, grievance_id: str) -> Optional[Dict[str, Any]]:
        """Get decision for a grievance"""
        for decision in self.decisions.values():
            if decision["grievance_id"] == grievance_id:
                return decision
        return None
    
    def create_rule_trace(
        self,
        grievance_id: str,
        decision_id: Optional[str],
        rules_evaluated: List[Dict[str, Any]],
        conflicts_detected: List[Dict[str, Any]],
        final_decision: Dict[str, Any],
        processing_time_ms: int
    ) -> str:
        """Create a new rule trace"""
        trace_id = str(uuid4())
        now = datetime.utcnow().isoformat()
        
        self.rule_traces[trace_id] = {
            "id": trace_id,
            "grievance_id": grievance_id,
            "decision_id": decision_id,
            "rules_evaluated": rules_evaluated,
            "conflicts_detected": conflicts_detected,
            "final_decision": final_decision,
            "processing_time_ms": processing_time_ms,
            "created_at": now
        }
        
        logger.info(f"Created rule trace: {trace_id}")
        return trace_id
    
    def get_rule_trace(self, trace_id: str) -> Optional[Dict[str, Any]]:
        """Get rule trace by ID"""
        return self.rule_traces.get(trace_id)
    
    def get_rule_trace_by_grievance(self, grievance_id: str) -> Optional[Dict[str, Any]]:
        """Get rule trace for a grievance"""
        for trace in self.rule_traces.values():
            if trace["grievance_id"] == grievance_id:
                return trace
        return None
    
    def find_similar_cases(
        self,
        grievance_type: str,
        parameters: Dict[str, Any],
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Find similar historical cases"""
        similar = []
        
        for grievance_id, grievance in self.grievances.items():
            if grievance["grievance_type"] == grievance_type:
                decision = self.get_decision_by_grievance(grievance_id)
                if decision:
                    similar.append({
                        "grievance_id": grievance_id,
                        "outcome": decision["outcome"],
                        "applicable_rule": decision["applicable_rule"],
                        "hierarchy_level": decision["hierarchy_level"],
                        "parameters": grievance["parameters"]
                    })
        
        return similar[:limit]
    
    def create_fairness_check(
        self,
        grievance_id: str,
        decision_id: str,
        consistency_score: float,
        anomaly_detected: bool,
        similar_cases_count: int,
        recommendation: str
    ) -> str:
        """Create a fairness check record"""
        check_id = str(uuid4())
        now = datetime.utcnow().isoformat()
        
        self.fairness_checks[check_id] = {
            "id": check_id,
            "grievance_id": grievance_id,
            "decision_id": decision_id,
            "consistency_score": consistency_score,
            "anomaly_detected": anomaly_detected,
            "similar_cases_count": similar_cases_count,
            "recommendation": recommendation,
            "created_at": now
        }
        
        logger.info(f"Created fairness check: {check_id}")
        return check_id
    
    def close(self):
        """Close database connection (no-op for mock)"""
        logger.info("Mock database closed")


# Singleton instance
_mock_db_service = None


def get_mock_database_service():
    """Get or create mock database service instance"""
    global _mock_db_service
    if _mock_db_service is None:
        _mock_db_service = MockDatabaseService()
    return _mock_db_service
