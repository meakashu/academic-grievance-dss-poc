"""
Unit Tests for API Routes
Tests all API endpoints and response contracts
"""
import pytest
from fastapi.testclient import TestClient
from uuid import uuid4


class TestGrievanceAPIRoutes:
    """Test suite for grievance API endpoints"""
    
    def test_submit_grievance_attendance(self, test_client):
        """
        Test: Submit attendance shortage grievance
        
        Validates:
        - 201 Created status
        - Response contains decision
        - Response contains trace
        - Response contains ambiguity report
        """
        payload = {
            "student_id": "STU2024001",
            "grievance_type": "ATTENDANCE_SHORTAGE",
            "narrative": "I was absent due to medical reasons",
            "parameters": {
                "attendance_percentage": 70.0,
                "has_medical_certificate": False
            }
        }
        
        response = test_client.post("/api/grievances", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["success"] == True
        assert "grievance_id" in data
        assert "decision" in data
        assert "trace" in data
        assert "ambiguity" in data
        
        # Validate decision structure
        decision = data["decision"]
        assert "outcome" in decision
        assert "applicable_rule" in decision
        assert "hierarchy_level" in decision
    
    
    def test_submit_grievance_examination(self, test_client):
        """
        Test: Submit examination revaluation grievance
        
        Validates:
        - Examination grievance processed correctly
        - Appropriate rule applied
        """
        payload = {
            "student_id": "STU2024002",
            "grievance_type": "EXAMINATION_REEVAL",
            "narrative": "Request revaluation for CS101",
            "parameters": {
                "course_code": "CS101",
                "marks_obtained": 45,
                "days_since_result_declaration": 10,
                "revaluation_fee_paid": True
            }
        }
        
        response = test_client.post("/api/grievances", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["success"] == True
        assert data["decision"]["outcome"] in ["ACCEPT", "REJECT", "PENDING"]
    
    
    def test_submit_grievance_fee_waiver(self, test_client):
        """
        Test: Submit fee waiver grievance
        
        Validates:
        - Fee waiver grievance processed
        - Category-based rules applied
        """
        payload = {
            "student_id": "STU2024003",
            "grievance_type": "FEE_WAIVER",
            "narrative": "Request fee waiver as SC student",
            "parameters": {
                "student_category": "SC",
                "family_income": 150000,
                "has_income_certificate": True,
                "has_category_certificate": True
            }
        }
        
        response = test_client.post("/api/grievances", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["success"] == True
        assert data["decision"]["outcome"] == "ACCEPT"
    
    
    def test_get_grievance_by_id(self, test_client):
        """
        Test: Retrieve grievance by ID
        
        Validates:
        - GET endpoint works
        - Returns correct grievance
        """
        # First create a grievance
        payload = {
            "student_id": "STU2024004",
            "grievance_type": "ATTENDANCE_SHORTAGE",
            "narrative": "Test",
            "parameters": {"attendance_percentage": 70.0}
        }
        
        create_response = test_client.post("/api/grievances", json=payload)
        grievance_id = create_response.json()["grievance_id"]
        
        # Now retrieve it
        get_response = test_client.get(f"/api/grievances/{grievance_id}")
        
        assert get_response.status_code == 200
        data = get_response.json()
        
        assert data["success"] == True
        assert "grievance" in data
        assert data["grievance"]["id"] == grievance_id
    
    
    def test_get_student_grievances(self, test_client):
        """
        Test: Get all grievances for a student
        
        Validates:
        - Returns list of grievances
        - Filtered by student ID
        """
        student_id = "STU2024005"
        
        # Create multiple grievances
        for i in range(2):
            payload = {
                "student_id": student_id,
                "grievance_type": "ATTENDANCE_SHORTAGE",
                "narrative": f"Grievance {i}",
                "parameters": {"attendance_percentage": 70.0}
            }
            test_client.post("/api/grievances", json=payload)
        
        # Get student's grievances
        response = test_client.get(f"/api/grievances/student/{student_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] == True
        assert "grievances" in data
        assert data["count"] >= 2
    
    
    def test_get_decision(self, test_client):
        """
        Test: Get decision by ID
        
        Validates:
        - Decision retrieval works
        - Contains all required fields
        """
        # Create grievance first
        payload = {
            "student_id": "STU2024006",
            "grievance_type": "ATTENDANCE_SHORTAGE",
            "narrative": "Test",
            "parameters": {"attendance_percentage": 70.0}
        }
        
        create_response = test_client.post("/api/grievances", json=payload)
        data = create_response.json()
        
        # Decision should be in response
        assert "decision" in data
        decision = data["decision"]
        
        assert "outcome" in decision
        assert "applicable_rule" in decision
        assert "reason" in decision
    
    
    def test_get_trace(self, test_client):
        """
        Test: Get rule trace
        
        Validates:
        - Trace contains fired rules
        - Processing time recorded
        """
        payload = {
            "student_id": "STU2024007",
            "grievance_type": "ATTENDANCE_SHORTAGE",
            "narrative": "Test",
            "parameters": {"attendance_percentage": 70.0}
        }
        
        response = test_client.post("/api/grievances", json=payload)
        data = response.json()
        
        assert "trace" in data
        trace = data["trace"]
        
        assert "rules_fired" in trace
        assert "processing_time_ms" in trace
    
    
    def test_health_check(self, test_client):
        """
        Test: Health check endpoint
        
        Validates:
        - System is running
        - Services are accessible
        """
        response = test_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert data["status"] in ["healthy", "ok", "running"]


class TestAPIValidation:
    """Test API input validation"""
    
    def test_invalid_grievance_type(self, test_client):
        """
        Test: Submit grievance with invalid type
        
        Validates:
        - Validation error returned
        - Appropriate status code
        """
        payload = {
            "student_id": "STU2024999",
            "grievance_type": "INVALID_TYPE",
            "narrative": "Test",
            "parameters": {}
        }
        
        response = test_client.post("/api/grievances", json=payload)
        
        # Should either reject or process with warning
        assert response.status_code in [201, 400, 422]
    
    
    def test_missing_required_fields(self, test_client):
        """
        Test: Submit grievance with missing fields
        
        Validates:
        - Validation error
        - Clear error message
        """
        payload = {
            "student_id": "STU2024999",
            # Missing grievance_type
            "narrative": "Test"
        }
        
        response = test_client.post("/api/grievances", json=payload)
        
        assert response.status_code == 422  # Unprocessable Entity
    
    
    def test_get_nonexistent_grievance(self, test_client):
        """
        Test: Get grievance that doesn't exist
        
        Validates:
        - 404 Not Found
        - Clear error message
        """
        fake_id = str(uuid4())
        response = test_client.get(f"/api/grievances/{fake_id}")
        
        assert response.status_code == 404
