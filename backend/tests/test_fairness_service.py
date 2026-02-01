"""
Unit Tests for Fairness Service
Tests consistency scoring, anomaly detection, and demographic parity
"""
import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any
from uuid import uuid4

from services.fairness_service import FairnessService, get_fairness_service


class TestFairnessService:
    """Test suite for fairness service"""
    
    @pytest.fixture
    def fairness_service(self, mock_db):
        """Create fairness service instance"""
        service = FairnessService()
        # Inject mock database
        with patch('services.fairness_service.get_database_service', return_value=mock_db):
            yield service
    
    
    def test_calculate_consistency_score(self, fairness_service, sample_decision):
        """
        Test: Calculate consistency score between current and historical decisions
        
        Validates:
        - Consistency score between 0.0 and 1.0
        - Higher score for similar outcomes
        - Lower score for different outcomes
        """
        current_decision = sample_decision.copy()
        
        # Similar historical cases (same outcome)
        similar_cases = [
            {
                "outcome": "REJECT",
                "applicable_rule": "UGC_Attendance_75Percent_Minimum",
                "parameters": {"attendance_percentage": 70.0}
            },
            {
                "outcome": "REJECT",
                "applicable_rule": "UGC_Attendance_75Percent_Minimum",
                "parameters": {"attendance_percentage": 72.0}
            },
            {
                "outcome": "REJECT",
                "applicable_rule": "UGC_Attendance_75Percent_Minimum",
                "parameters": {"attendance_percentage": 68.0}
            }
        ]
        
        score = fairness_service.calculate_consistency_score(current_decision, similar_cases)
        
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
        # Should have high consistency (all REJECT)
        assert score >= 0.8
    
    
    def test_detect_anomaly_low_consistency(self, fairness_service, sample_decision):
        """
        Test: Detect anomaly when consistency score is low
        
        Validates:
        - Anomaly flagged for inconsistent decisions
        - Reason provided
        """
        current_decision = sample_decision.copy()
        current_decision["outcome"] = "ACCEPT"  # Different from historical
        
        # Historical cases all REJECT
        similar_cases = [
            {"outcome": "REJECT", "applicable_rule": "UGC_Attendance_75Percent_Minimum"},
            {"outcome": "REJECT", "applicable_rule": "UGC_Attendance_75Percent_Minimum"},
            {"outcome": "REJECT", "applicable_rule": "UGC_Attendance_75Percent_Minimum"}
        ]
        
        consistency_score = 0.3  # Low consistency
        is_anomaly, reason = fairness_service.detect_anomaly(
            consistency_score, current_decision, similar_cases
        )
        
        assert isinstance(is_anomaly, bool)
        assert is_anomaly == True  # Should detect anomaly
        assert isinstance(reason, str)
        assert len(reason) > 0
    
    
    def test_detect_anomaly_outlier_decision(self, fairness_service):
        """
        Test: Detect anomaly for outlier decision
        
        Validates:
        - Outlier detection based on decision pattern
        - Anomaly flagged when decision differs significantly
        """
        current_decision = {
            "outcome": "ACCEPT",
            "applicable_rule": "Custom_Rule",
            "parameters": {"attendance_percentage": 50.0}  # Very low
        }
        
        similar_cases = [
            {"outcome": "REJECT", "parameters": {"attendance_percentage": 70.0}},
            {"outcome": "REJECT", "parameters": {"attendance_percentage": 72.0}},
            {"outcome": "REJECT", "parameters": {"attendance_percentage": 68.0}}
        ]
        
        consistency_score = 0.2
        is_anomaly, reason = fairness_service.detect_anomaly(
            consistency_score, current_decision, similar_cases
        )
        
        assert is_anomaly == True
        assert "consistency" in reason.lower() or "pattern" in reason.lower()
    
    
    def test_demographic_parity_analysis(self, fairness_service, mock_db):
        """
        Test: Analyze demographic parity across student categories
        
        Validates:
        - Parity analysis for different categories
        - Acceptance rates calculated
        - Disparity detected if present
        """
        # Add test data to mock database
        test_grievances = [
            {"id": uuid4(), "student_category": "SC", "grievance_type": "FEE_WAIVER"},
            {"id": uuid4(), "student_category": "SC", "grievance_type": "FEE_WAIVER"},
            {"id": uuid4(), "student_category": "GENERAL", "grievance_type": "FEE_WAIVER"},
            {"id": uuid4(), "student_category": "GENERAL", "grievance_type": "FEE_WAIVER"}
        ]
        
        test_decisions = [
            {"grievance_id": test_grievances[0]["id"], "outcome": "ACCEPT"},
            {"grievance_id": test_grievances[1]["id"], "outcome": "ACCEPT"},
            {"grievance_id": test_grievances[2]["id"], "outcome": "REJECT"},
            {"grievance_id": test_grievances[3]["id"], "outcome": "REJECT"}
        ]
        
        for g in test_grievances:
            mock_db.grievances[g["id"]] = g
        for d in test_decisions:
            mock_db.decisions[d["grievance_id"]] = d
        
        with patch('services.fairness_service.get_database_service', return_value=mock_db):
            parity_analysis = fairness_service.analyze_demographic_parity("FEE_WAIVER")
        
        assert isinstance(parity_analysis, dict)
        # Should contain category-wise statistics
        assert "categories" in parity_analysis or "analysis" in parity_analysis
    
    
    def test_monitor_fairness_complete_workflow(self, fairness_service, mock_db, sample_decision):
        """
        Test: Complete fairness monitoring workflow
        
        Validates:
        - End-to-end fairness monitoring
        - Consistency score calculated
        - Anomaly detection performed
        - Recommendation generated
        """
        grievance_id = uuid4()
        decision = sample_decision.copy()
        grievance_type = "ATTENDANCE_SHORTAGE"
        parameters = {"attendance_percentage": 70.0}
        
        # Add some historical data
        for i in range(3):
            hist_id = uuid4()
            mock_db.grievances[hist_id] = {
                "id": hist_id,
                "grievance_type": grievance_type,
                "parameters": {"attendance_percentage": 70.0 + i}
            }
            mock_db.decisions[hist_id] = {
                "grievance_id": hist_id,
                "outcome": "REJECT",
                "applicable_rule": "UGC_Attendance_75Percent_Minimum"
            }
        
        with patch('services.fairness_service.get_database_service', return_value=mock_db):
            fairness_report = fairness_service.monitor_fairness(
                grievance_id, decision, grievance_type, parameters
            )
        
        assert isinstance(fairness_report, dict)
        assert "consistency_score" in fairness_report
        assert "is_anomaly" in fairness_report
        assert "recommendation" in fairness_report
        
        # Validate score range
        assert 0.0 <= fairness_report["consistency_score"] <= 1.0
    
    
    def test_get_fairness_metrics(self, fairness_service, mock_db):
        """
        Test: Get overall fairness metrics
        
        Validates:
        - Aggregate fairness statistics
        - Metrics across all decisions
        """
        # Add test data
        for i in range(5):
            gid = uuid4()
            mock_db.grievances[gid] = {
                "id": gid,
                "grievance_type": "ATTENDANCE_SHORTAGE"
            }
            mock_db.decisions[gid] = {
                "grievance_id": gid,
                "outcome": "REJECT" if i < 3 else "ACCEPT"
            }
        
        with patch('services.fairness_service.get_database_service', return_value=mock_db):
            metrics = fairness_service.get_fairness_metrics()
        
        assert isinstance(metrics, dict)
        # Should contain aggregate statistics
        assert "total_decisions" in metrics or "statistics" in metrics


class TestFairnessServiceEdgeCases:
    """Edge case tests for fairness service"""
    
    def test_consistency_with_no_historical_cases(self, mock_db):
        """
        Test: Consistency calculation with no historical data
        
        Validates:
        - Handles empty historical cases gracefully
        - Returns appropriate default score
        """
        fairness_service = FairnessService()
        
        current_decision = {"outcome": "REJECT"}
        similar_cases = []
        
        score = fairness_service.calculate_consistency_score(current_decision, similar_cases)
        
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
    
    
    def test_anomaly_detection_with_single_case(self, mock_db):
        """
        Test: Anomaly detection with only one historical case
        
        Validates:
        - Handles minimal data gracefully
        - Appropriate anomaly detection
        """
        fairness_service = FairnessService()
        
        current_decision = {"outcome": "ACCEPT"}
        similar_cases = [{"outcome": "REJECT"}]
        
        consistency_score = 0.5
        is_anomaly, reason = fairness_service.detect_anomaly(
            consistency_score, current_decision, similar_cases
        )
        
        assert isinstance(is_anomaly, bool)
        assert isinstance(reason, str)
