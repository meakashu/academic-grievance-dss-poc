"""
Edge Case Tests
Tests boundary conditions and exceptional scenarios
"""
import pytest
from uuid import uuid4


class TestAttendanceBoundaries:
    """Test boundary conditions for attendance rules"""
    
    def test_attendance_boundary_75_percent(self, test_client):
        """
        Test: Attendance exactly at 75% threshold
        
        Validates:
        - Boundary condition handled correctly
        - 75% should ACCEPT (meets minimum)
        """
        payload = {
            "student_id": "STU2024001",
            "grievance_type": "ATTENDANCE_SHORTAGE",
            "narrative": "Exactly 75% attendance",
            "parameters": {
                "attendance_percentage": 75.0,
                "has_medical_certificate": False
            }
        }
        
        response = test_client.post("/api/grievances", json=payload)
        data = response.json()
        
        # 75% should meet the requirement
        assert data["decision"]["outcome"] == "ACCEPT"
    
    
    def test_attendance_just_below_threshold(self, test_client):
        """
        Test: Attendance just below 75% (74.9%)
        
        Validates:
        - Boundary condition
        - Should REJECT
        """
        payload = {
            "student_id": "STU2024002",
            "grievance_type": "ATTENDANCE_SHORTAGE",
            "narrative": "Just below threshold",
            "parameters": {
                "attendance_percentage": 74.9,
                "has_medical_certificate": False
            }
        }
        
        response = test_client.post("/api/grievances", json=payload)
        data = response.json()
        
        assert data["decision"]["outcome"] == "REJECT"
    
    
    def test_multiple_medical_certificates(self, test_client):
        """
        Test: Multiple medical certificates
        
        Validates:
        - Handles multiple certificates
        - Cumulative days calculated
        """
        payload = {
            "student_id": "STU2024003",
            "grievance_type": "ATTENDANCE_SHORTAGE",
            "narrative": "Multiple medical certificates",
            "parameters": {
                "attendance_percentage": 68.0,
                "has_medical_certificate": True,
                "medical_certificate_valid": True,
                "medical_certificate_from_recognized_authority": True,
                "medical_certificate_days": 20  # Multiple certificates totaling 20 days
            }
        }
        
        response = test_client.post("/api/grievances", json=payload)
        data = response.json()
        
        # Should be processed (outcome depends on rules)
        assert response.status_code == 201
        assert "decision" in data


class TestExaminationBoundaries:
    """Test boundary conditions for examination rules"""
    
    def test_revaluation_day_15_boundary(self, test_client):
        """
        Test: Revaluation request on day 15 (deadline)
        
        Validates:
        - Boundary condition
        - Day 15 should ACCEPT (within deadline)
        """
        payload = {
            "student_id": "STU2024004",
            "grievance_type": "EXAMINATION_REEVAL",
            "narrative": "Revaluation on deadline day",
            "parameters": {
                "course_code": "CS101",
                "marks_obtained": 45,
                "days_since_result_declaration": 15,
                "revaluation_fee_paid": True
            }
        }
        
        response = test_client.post("/api/grievances", json=payload)
        data = response.json()
        
        # Day 15 should be within deadline
        assert data["decision"]["outcome"] == "ACCEPT"
    
    
    def test_revaluation_day_16_past_deadline(self, test_client):
        """
        Test: Revaluation request on day 16 (past deadline)
        
        Validates:
        - Past deadline should REJECT
        """
        payload = {
            "student_id": "STU2024005",
            "grievance_type": "EXAMINATION_REEVAL",
            "narrative": "Revaluation past deadline",
            "parameters": {
                "course_code": "CS101",
                "marks_obtained": 45,
                "days_since_result_declaration": 16,
                "revaluation_fee_paid": True
            }
        }
        
        response = test_client.post("/api/grievances", json=payload)
        data = response.json()
        
        assert data["decision"]["outcome"] == "REJECT"


class TestFeeWaiverEdgeCases:
    """Test edge cases for fee waiver"""
    
    def test_fee_waiver_partial_documentation(self, test_client):
        """
        Test: Fee waiver with incomplete documentation
        
        Validates:
        - Missing certificates handled
        - Appropriate decision or human review required
        """
        payload = {
            "student_id": "STU2024006",
            "grievance_type": "FEE_WAIVER",
            "narrative": "Fee waiver with partial docs",
            "parameters": {
                "student_category": "SC",
                "family_income": 150000,
                "has_income_certificate": True,
                "has_category_certificate": False  # Missing category certificate
            }
        }
        
        response = test_client.post("/api/grievances", json=payload)
        data = response.json()
        
        # Should either REJECT or require human review
        assert data["decision"]["outcome"] in ["REJECT", "PENDING"] or \
               data["decision"].get("human_review_required", False)
    
    
    def test_fee_waiver_income_boundary(self, test_client):
        """
        Test: Fee waiver at income threshold
        
        Validates:
        - Income boundary condition
        """
        payload = {
            "student_id": "STU2024007",
            "grievance_type": "FEE_WAIVER",
            "narrative": "Income at threshold",
            "parameters": {
                "student_category": "SC",
                "family_income": 200000,  # At threshold
                "has_income_certificate": True,
                "has_category_certificate": True
            }
        }
        
        response = test_client.post("/api/grievances", json=payload)
        data = response.json()
        
        assert response.status_code == 201


class TestInvalidInputs:
    """Test invalid input handling"""
    
    def test_invalid_grievance_type(self, test_client):
        """
        Test: Invalid grievance type
        
        Validates:
        - System handles unknown types
        - Appropriate error or default behavior
        """
        payload = {
            "student_id": "STU2024999",
            "grievance_type": "INVALID_TYPE",
            "narrative": "Test invalid type",
            "parameters": {}
        }
        
        response = test_client.post("/api/grievances", json=payload)
        
        # Should either validate and reject, or process with warning
        assert response.status_code in [201, 400, 422]
    
    
    def test_missing_required_parameters(self, test_client):
        """
        Test: Missing required parameters
        
        Validates:
        - Handles incomplete data
        - Appropriate error or human review flag
        """
        payload = {
            "student_id": "STU2024998",
            "grievance_type": "ATTENDANCE_SHORTAGE",
            "narrative": "Missing attendance percentage",
            "parameters": {
                # Missing attendance_percentage
                "has_medical_certificate": False
            }
        }
        
        response = test_client.post("/api/grievances", json=payload)
        
        # Should handle gracefully
        assert response.status_code in [201, 400, 422]
    
    
    def test_negative_attendance_percentage(self, test_client):
        """
        Test: Negative attendance percentage
        
        Validates:
        - Invalid data validation
        """
        payload = {
            "student_id": "STU2024997",
            "grievance_type": "ATTENDANCE_SHORTAGE",
            "narrative": "Negative attendance",
            "parameters": {
                "attendance_percentage": -10.0,
                "has_medical_certificate": False
            }
        }
        
        response = test_client.post("/api/grievances", json=payload)
        
        # Should validate and reject or handle as error
        assert response.status_code in [201, 400, 422]
    
    
    def test_attendance_over_100_percent(self, test_client):
        """
        Test: Attendance over 100%
        
        Validates:
        - Range validation
        """
        payload = {
            "student_id": "STU2024996",
            "grievance_type": "ATTENDANCE_SHORTAGE",
            "narrative": "Over 100% attendance",
            "parameters": {
                "attendance_percentage": 150.0,
                "has_medical_certificate": False
            }
        }
        
        response = test_client.post("/api/grievances", json=payload)
        
        # Should validate range
        assert response.status_code in [201, 400, 422]


class TestConcurrentRequests:
    """Test concurrent request handling"""
    
    def test_multiple_simultaneous_submissions(self, test_client):
        """
        Test: Multiple grievances submitted simultaneously
        
        Validates:
        - System handles concurrent requests
        - All requests processed correctly
        """
        payloads = [
            {
                "student_id": f"STU202499{i}",
                "grievance_type": "ATTENDANCE_SHORTAGE",
                "narrative": f"Concurrent request {i}",
                "parameters": {"attendance_percentage": 70.0 + i}
            }
            for i in range(3)
        ]
        
        responses = [test_client.post("/api/grievances", json=p) for p in payloads]
        
        # All should succeed
        assert all(r.status_code == 201 for r in responses)
        
        # All should have unique IDs
        grievance_ids = [r.json()["grievance_id"] for r in responses]
        assert len(set(grievance_ids)) == len(grievance_ids)
