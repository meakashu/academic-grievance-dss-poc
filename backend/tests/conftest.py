"""
Pytest Configuration and Shared Fixtures
Provides test infrastructure for all backend tests
"""
import pytest
from fastapi.testclient import TestClient
from typing import Dict, Any
from uuid import uuid4
from datetime import datetime

# Import main app
import sys
from pathlib import Path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from main import app
from services.mock_database_service import MockDatabaseService
from services.mock_rule_engine_service import MockRuleEngineService


@pytest.fixture
def test_client():
    """
    FastAPI test client fixture
    
    Returns:
        TestClient instance for API testing
    """
    return TestClient(app)


@pytest.fixture
def mock_db():
    """
    Mock database service fixture
    
    Returns:
        MockDatabaseService instance with clean state
    """
    db = MockDatabaseService()
    # Clear any existing data
    db.grievances.clear()
    db.decisions.clear()
    return db


@pytest.fixture
def sample_grievance() -> Dict[str, Any]:
    """
    Sample grievance data for testing
    
    Returns:
        Dictionary with test grievance data
    """
    return {
        "student_id": "STU2024001",
        "grievance_type": "ATTENDANCE_SHORTAGE",
        "narrative": "I was absent due to medical reasons",
        "parameters": {
            "attendance_percentage": 70.0,
            "has_medical_certificate": False,
            "total_classes": 100,
            "classes_attended": 70
        }
    }


@pytest.fixture
def sample_grievance_with_medical() -> Dict[str, Any]:
    """
    Sample grievance with medical certificate
    
    Returns:
        Dictionary with test grievance data including medical certificate
    """
    return {
        "student_id": "STU2024002",
        "grievance_type": "ATTENDANCE_SHORTAGE",
        "narrative": "I have valid medical certificate for absences",
        "parameters": {
            "attendance_percentage": 68.5,
            "has_medical_certificate": True,
            "medical_certificate_valid": True,
            "medical_certificate_from_recognized_authority": True,
            "medical_certificate_days": 15
        }
    }


@pytest.fixture
def sample_examination_grievance() -> Dict[str, Any]:
    """
    Sample examination revaluation grievance
    
    Returns:
        Dictionary with examination grievance data
    """
    return {
        "student_id": "STU2024003",
        "grievance_type": "EXAMINATION_REEVAL",
        "narrative": "Request revaluation for CS101 examination",
        "parameters": {
            "course_code": "CS101",
            "marks_obtained": 45,
            "days_since_result_declaration": 10,
            "has_already_requested_reeval": False,
            "revaluation_fee_paid": True
        }
    }


@pytest.fixture
def sample_fee_waiver_grievance() -> Dict[str, Any]:
    """
    Sample fee waiver grievance
    
    Returns:
        Dictionary with fee waiver grievance data
    """
    return {
        "student_id": "STU2024004",
        "grievance_type": "FEE_WAIVER",
        "narrative": "Request fee waiver as SC category student",
        "parameters": {
            "student_category": "SC",
            "family_income": 150000,
            "has_income_certificate": True,
            "has_category_certificate": True
        }
    }


@pytest.fixture
def sample_decision() -> Dict[str, Any]:
    """
    Sample decision data for testing
    
    Returns:
        Dictionary with test decision data
    """
    return {
        "outcome": "REJECT",
        "reason": "Attendance below UGC-mandated 75% minimum without medical excuse",
        "applicable_rule": "UGC_Attendance_75Percent_Minimum",
        "regulatory_source": "UGC Regulations 2018, Section 4.2",
        "hierarchy_level": "L1_National",
        "salience": 1500,
        "confidence": 0.95,
        "human_review_required": False
    }


@pytest.fixture
def sample_rule_trace() -> Dict[str, Any]:
    """
    Sample rule trace data for testing
    
    Returns:
        Dictionary with test rule trace data
    """
    return {
        "rules_fired": 1,
        "conflicts_detected": 0,
        "processing_time_ms": 245,
        "fired_rules": [
            {
                "rule_name": "UGC_Attendance_75Percent_Minimum",
                "hierarchy_level": "L1_National",
                "salience": 1500,
                "condition_matched": "Attendance 70.0% < 75% threshold, no medical certificate",
                "outcome": "REJECT",
                "regulatory_source": "UGC Regulations 2018, Section 4.2",
                "timestamp": datetime.now().isoformat()
            }
        ],
        "conflicts": []
    }


@pytest.fixture
def sample_conflict_trace() -> Dict[str, Any]:
    """
    Sample rule trace with conflicts
    
    Returns:
        Dictionary with rule trace containing conflicts
    """
    return {
        "rules_fired": 2,
        "conflicts_detected": 1,
        "processing_time_ms": 320,
        "fired_rules": [
            {
                "rule_name": "UGC_Attendance_75Percent_Minimum",
                "hierarchy_level": "L1_National",
                "salience": 1500,
                "condition_matched": "National rule fired",
                "outcome": "REJECT",
                "regulatory_source": "UGC Regulations 2018",
                "timestamp": datetime.now().isoformat()
            },
            {
                "rule_name": "University_Medical_Excuse_Attendance",
                "hierarchy_level": "L3_University",
                "salience": 800,
                "condition_matched": "University rule fired",
                "outcome": "ACCEPT",
                "regulatory_source": "University Statute 2023",
                "timestamp": datetime.now().isoformat()
            }
        ],
        "conflicts": [
            {
                "conflict_type": "AUTHORITY_CONFLICT",
                "conflicting_rules": [
                    "UGC_Attendance_75Percent_Minimum (L1_National)",
                    "University_Medical_Excuse_Attendance (L3_University)"
                ],
                "resolution_strategy": "Authority Precedence",
                "winner": "UGC_Attendance_75Percent_Minimum",
                "reason": "L1_National supersedes L3_University based on authority precedence"
            }
        ]
    }


@pytest.fixture
def mock_rule_engine():
    """
    Mock rule engine service fixture
    
    Returns:
        MockRuleEngineService instance
    """
    return MockRuleEngineService()


@pytest.fixture
def sample_ambiguity_report() -> Dict[str, Any]:
    """
    Sample ambiguity detection report
    
    Returns:
        Dictionary with ambiguity report data
    """
    return {
        "ambiguous_terms": [
            {
                "term": "reasonable",
                "type": "subjective",
                "reason": "Subjective term requiring human interpretation"
            },
            {
                "term": "may",
                "type": "permissive",
                "reason": "Permissive language indicating discretion"
            }
        ],
        "requires_human_review": True,
        "clarification_questions": [
            "What constitutes 'reasonable' in this context?",
            "Under what circumstances 'may' this rule apply?"
        ]
    }


@pytest.fixture
def sample_fairness_metrics() -> Dict[str, Any]:
    """
    Sample fairness metrics data
    
    Returns:
        Dictionary with fairness metrics
    """
    return {
        "consistency_score": 0.95,
        "similar_cases_count": 5,
        "is_anomaly": False,
        "anomaly_reason": None,
        "recommendation": "Decision is consistent with historical cases"
    }
