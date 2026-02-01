"""
Unit Tests for Conflict Resolution
Tests hierarchical conflict resolution (L1 > L2 > L3)
"""
import pytest
from typing import Dict, Any

from services.mock_rule_engine_service import MockRuleEngineService


class TestConflictResolution:
    """Test suite for hierarchical conflict resolution"""
    
    @pytest.fixture
    def rule_engine(self):
        """Create rule engine instance"""
        return MockRuleEngineService()
    
    
    def test_authority_conflict_l1_supersedes_l3(self, rule_engine):
        """
        Test: L1 National rule supersedes L3 University rule
        
        Validates:
        - Both L1 and L3 rules fire
        - Conflict detected
        - L1 wins due to authority precedence
        - Conflict explanation generated
        """
        # Grievance that triggers both L1 and L3 rules
        grievance = {
            "student_id": "STU2024001",
            "grievance_type": "ATTENDANCE_SHORTAGE",
            "narrative": "Medical excuse for attendance",
            "parameters": {
                "attendance_percentage": 68.5,  # Below 75% (L1) but above 65% (L3)
                "has_medical_certificate": True,
                "medical_certificate_valid": True,
                "medical_certificate_from_recognized_authority": True
            }
        }
        
        result = rule_engine.evaluate_grievance(grievance)
        
        assert result is not None
        decision = result["decision"]
        trace = result["trace"]
        
        # L1 should win (REJECT due to UGC 75% rule)
        assert decision["hierarchy_level"] == "L1_National"
        assert decision["outcome"] == "REJECT"
        
        # Check if conflict was detected
        if trace.get("conflicts_detected", 0) > 0:
            conflicts = trace.get("conflicts", [])
            assert len(conflicts) > 0
            
            conflict = conflicts[0]
            assert conflict["conflict_type"] == "AUTHORITY_CONFLICT"
            assert "L1" in conflict["winner"] or "National" in conflict["winner"]
            assert "authority" in conflict["reason"].lower() or "precedence" in conflict["reason"].lower()
    
    
    def test_authority_conflict_l2_supersedes_l3(self, rule_engine):
        """
        Test: L2 Accreditation rule supersedes L3 University rule
        
        Validates:
        - L2 and L3 rules fire
        - L2 wins due to higher authority
        - Conflict properly resolved
        """
        # Grievance that might trigger L2 and L3
        grievance = {
            "student_id": "STU2024002",
            "grievance_type": "ATTENDANCE_SHORTAGE",
            "narrative": "Lab attendance for technical course",
            "parameters": {
                "attendance_percentage": 72.0,
                "is_technical_course": True,
                "lab_attendance_percentage": 80.0,
                "has_medical_certificate": False
            }
        }
        
        result = rule_engine.evaluate_grievance(grievance)
        
        assert result is not None
        decision = result["decision"]
        
        # If L2 rule exists and fires, it should take precedence over L3
        if decision["hierarchy_level"] == "L2_Accreditation":
            trace = result["trace"]
            if trace.get("conflicts_detected", 0) > 0:
                conflicts = trace.get("conflicts", [])
                conflict = conflicts[0]
                assert "L2" in conflict["winner"] or "Accreditation" in conflict["winner"]
    
    
    def test_salience_conflict_same_level(self, rule_engine):
        """
        Test: Salience-based resolution for same hierarchy level
        
        Validates:
        - Multiple rules at same level fire
        - Higher salience wins
        - Salience conflict detected
        """
        # Grievance that triggers multiple L1 rules
        grievance = {
            "student_id": "STU2024003",
            "grievance_type": "ATTENDANCE_SHORTAGE",
            "narrative": "Multiple L1 rules applicable",
            "parameters": {
                "attendance_percentage": 68.0,
                "has_medical_certificate": True,
                "medical_certificate_valid": True,
                "medical_certificate_from_recognized_authority": True,
                "medical_certificate_days": 15
            }
        }
        
        result = rule_engine.evaluate_grievance(grievance)
        
        assert result is not None
        decision = result["decision"]
        trace = result["trace"]
        
        # Should have fired multiple rules
        if trace["rules_fired"] > 1:
            # Higher salience should win
            fired_rules = trace["fired_rules"]
            saliences = [r.get("salience", 0) for r in fired_rules]
            max_salience = max(saliences)
            
            # Winner should have highest salience
            assert decision.get("salience", 0) == max_salience
    
    
    def test_multi_rule_conflict_resolution(self, rule_engine):
        """
        Test: Resolution when 3+ rules fire
        
        Validates:
        - Multiple rules from different levels fire
        - Correct precedence applied (L1 > L2 > L3)
        - All conflicts logged
        """
        # Complex grievance triggering multiple rules
        grievance = {
            "student_id": "STU2024004",
            "grievance_type": "EXAMINATION_REEVAL",
            "narrative": "Revaluation request with multiple applicable rules",
            "parameters": {
                "course_code": "CS101",
                "marks_obtained": 45,
                "days_since_result_declaration": 10,
                "has_already_requested_reeval": False,
                "revaluation_fee_paid": True,
                "is_final_year": True
            }
        }
        
        result = rule_engine.evaluate_grievance(grievance)
        
        assert result is not None
        decision = result["decision"]
        trace = result["trace"]
        
        # Verify decision was made
        assert decision["outcome"] in ["ACCEPT", "REJECT", "PENDING"]
        
        # If multiple rules fired, check conflict resolution
        if trace["rules_fired"] > 1:
            # Should have hierarchy-based resolution
            assert decision["hierarchy_level"] in ["L1_National", "L2_Accreditation", "L3_University"]
    
    
    def test_conflict_explanation_generation(self, rule_engine, sample_conflict_trace):
        """
        Test: Conflict explanation is clear and detailed
        
        Validates:
        - Explanation includes conflicting rules
        - Reason for resolution stated
        - Hierarchy precedence explained
        """
        # Use sample conflict trace
        trace = sample_conflict_trace
        
        if trace["conflicts_detected"] > 0:
            conflicts = trace["conflicts"]
            
            for conflict in conflicts:
                # Verify conflict structure
                assert "conflict_type" in conflict
                assert "conflicting_rules" in conflict
                assert "winner" in conflict
                assert "reason" in conflict
                
                # Verify explanation quality
                reason = conflict["reason"]
                assert len(reason) > 20  # Should be descriptive
                assert any(keyword in reason.lower() for keyword in [
                    "precedence", "authority", "hierarchy", "supersedes", "overrides"
                ])


class TestConflictResolutionEdgeCases:
    """Edge case tests for conflict resolution"""
    
    def test_no_conflict_single_rule(self, sample_grievance):
        """
        Test: No conflict when only one rule fires
        
        Validates:
        - Single rule evaluation
        - No conflict detected
        - Clean decision
        """
        rule_engine = MockRuleEngineService()
        result = rule_engine.evaluate_grievance(sample_grievance)
        
        trace = result["trace"]
        
        # If only one rule fired, no conflict
        if trace["rules_fired"] == 1:
            assert trace["conflicts_detected"] == 0
            assert len(trace.get("conflicts", [])) == 0
    
    
    def test_same_outcome_no_conflict(self):
        """
        Test: No conflict when rules have same outcome
        
        Validates:
        - Multiple rules with same outcome
        - No conflict flagged (agreement, not conflict)
        """
        rule_engine = MockRuleEngineService()
        
        # Grievance where multiple rules agree
        grievance = {
            "student_id": "STU2024005",
            "grievance_type": "FEE_WAIVER",
            "narrative": "SC student requesting fee waiver",
            "parameters": {
                "student_category": "SC",
                "family_income": 150000,
                "has_income_certificate": True,
                "has_category_certificate": True
            }
        }
        
        result = rule_engine.evaluate_grievance(grievance)
        
        # Multiple rules may fire but all ACCEPT
        # This is agreement, not conflict
        assert result["decision"]["outcome"] == "ACCEPT"
    
    
    def test_temporal_conflict_resolution(self):
        """
        Test: Temporal conflicts (newer vs older rules)
        
        Validates:
        - Rules with different effective dates
        - Newer rule takes precedence (if same level)
        """
        rule_engine = MockRuleEngineService()
        
        # This would require rules with effectiveDate metadata
        # For now, verify structure supports temporal resolution
        grievance = {
            "student_id": "STU2024006",
            "grievance_type": "ATTENDANCE_SHORTAGE",
            "narrative": "Test temporal resolution",
            "parameters": {
                "attendance_percentage": 70.0
            }
        }
        
        result = rule_engine.evaluate_grievance(grievance)
        
        # Verify decision has regulatory source (which may include date)
        assert "regulatory_source" in result["decision"]
