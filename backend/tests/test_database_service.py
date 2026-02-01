"""
Unit Tests for Database Service
Tests CRUD operations and data persistence
"""
import pytest
from uuid import uuid4, UUID
from typing import Dict, Any

from services.mock_database_service import MockDatabaseService


class TestDatabaseService:
    """Test suite for database service"""
    
    @pytest.fixture
    def db_service(self):
        """Create fresh database service instance"""
        db = MockDatabaseService()
        db.grievances.clear()
        db.decisions.clear()
        db.rule_traces.clear()
        return db
    
    
    def test_create_grievance(self, db_service):
        """
        Test: Create new grievance
        
        Validates:
        - Grievance created successfully
        - Returns valid UUID
        - Data stored correctly
        """
        grievance_id = db_service.create_grievance(
            student_id="STU2024001",
            grievance_type="ATTENDANCE_SHORTAGE",
            narrative="Test narrative",
            parameters={"attendance_percentage": 70.0}
        )
        
        assert isinstance(grievance_id, UUID)
        assert grievance_id in db_service.grievances
        
        grievance = db_service.grievances[grievance_id]
        assert grievance["student_id"] == "STU2024001"
        assert grievance["grievance_type"] == "ATTENDANCE_SHORTAGE"
        assert grievance["parameters"]["attendance_percentage"] == 70.0
    
    
    def test_get_grievance_by_id(self, db_service):
        """
        Test: Retrieve grievance by ID
        
        Validates:
        - Correct grievance returned
        - All fields present
        """
        # Create test grievance
        grievance_id = db_service.create_grievance(
            student_id="STU2024002",
            grievance_type="EXAMINATION_REEVAL",
            narrative="Revaluation request",
            parameters={"course_code": "CS101"}
        )
        
        # Retrieve it
        retrieved = db_service.get_grievance(grievance_id)
        
        assert retrieved is not None
        assert retrieved["id"] == grievance_id
        assert retrieved["student_id"] == "STU2024002"
        assert retrieved["grievance_type"] == "EXAMINATION_REEVAL"
    
    
    def test_get_grievances_by_student(self, db_service):
        """
        Test: Get all grievances for a student
        
        Validates:
        - Returns all student's grievances
        - Correct count
        - Filtered properly
        """
        student_id = "STU2024003"
        
        # Create multiple grievances for same student
        id1 = db_service.create_grievance(
            student_id=student_id,
            grievance_type="ATTENDANCE_SHORTAGE",
            narrative="First grievance",
            parameters={}
        )
        
        id2 = db_service.create_grievance(
            student_id=student_id,
            grievance_type="FEE_WAIVER",
            narrative="Second grievance",
            parameters={}
        )
        
        # Create grievance for different student
        db_service.create_grievance(
            student_id="STU2024999",
            grievance_type="ATTENDANCE_SHORTAGE",
            narrative="Other student",
            parameters={}
        )
        
        # Get student's grievances
        student_grievances = db_service.get_grievances_by_student(student_id)
        
        assert len(student_grievances) == 2
        assert all(g["student_id"] == student_id for g in student_grievances)
        
        grievance_ids = [g["id"] for g in student_grievances]
        assert id1 in grievance_ids
        assert id2 in grievance_ids
    
    
    def test_update_grievance_status(self, db_service):
        """
        Test: Update grievance status
        
        Validates:
        - Status updated correctly
        - Timestamp updated
        """
        grievance_id = db_service.create_grievance(
            student_id="STU2024004",
            grievance_type="ATTENDANCE_SHORTAGE",
            narrative="Test",
            parameters={}
        )
        
        # Update status
        db_service.update_grievance_status(grievance_id, "RESOLVED")
        
        grievance = db_service.get_grievance(grievance_id)
        assert grievance["status"] == "RESOLVED"
        assert "updated_at" in grievance
    
    
    def test_store_decision(self, db_service):
        """
        Test: Store decision for grievance
        
        Validates:
        - Decision created successfully
        - Linked to grievance
        - All fields stored
        """
        # Create grievance first
        grievance_id = db_service.create_grievance(
            student_id="STU2024005",
            grievance_type="ATTENDANCE_SHORTAGE",
            narrative="Test",
            parameters={"attendance_percentage": 70.0}
        )
        
        # Create decision
        decision_id = db_service.create_decision(
            grievance_id=grievance_id,
            outcome="REJECT",
            applicable_rule="UGC_Attendance_75Percent_Minimum",
            regulatory_source="UGC Regulations 2018",
            hierarchy_level="L1_National",
            salience=1500,
            reason="Below 75% threshold",
            human_review_required=False
        )
        
        assert isinstance(decision_id, UUID)
        assert decision_id in db_service.decisions
        
        decision = db_service.decisions[decision_id]
        assert decision["grievance_id"] == grievance_id
        assert decision["outcome"] == "REJECT"
        assert decision["applicable_rule"] == "UGC_Attendance_75Percent_Minimum"
        assert decision["hierarchy_level"] == "L1_National"
    
    
    def test_get_similar_cases(self, db_service):
        """
        Test: Retrieve similar historical cases
        
        Validates:
        - Similar cases found based on type and parameters
        - Correct filtering
        """
        # Create several attendance shortage cases
        for i in range(3):
            gid = db_service.create_grievance(
                student_id=f"STU202400{i}",
                grievance_type="ATTENDANCE_SHORTAGE",
                narrative=f"Case {i}",
                parameters={"attendance_percentage": 70.0 + i}
            )
            
            db_service.create_decision(
                grievance_id=gid,
                outcome="REJECT",
                applicable_rule="UGC_Attendance_75Percent_Minimum",
                regulatory_source="UGC Regulations 2018",
                hierarchy_level="L1_National",
                salience=1500,
                reason="Below threshold"
            )
        
        # Create different type
        gid_diff = db_service.create_grievance(
            student_id="STU2024999",
            grievance_type="FEE_WAIVER",
            narrative="Different type",
            parameters={}
        )
        
        # Get similar cases
        similar = db_service.get_similar_cases(
            grievance_type="ATTENDANCE_SHORTAGE",
            parameters={"attendance_percentage": 71.0}
        )
        
        assert len(similar) >= 2  # Should find the attendance cases
        assert all(case["grievance_type"] == "ATTENDANCE_SHORTAGE" for case in similar)


class TestDatabaseServiceEdgeCases:
    """Edge case tests for database service"""
    
    def test_get_nonexistent_grievance(self, mock_db):
        """
        Test: Get grievance that doesn't exist
        
        Validates:
        - Returns None or raises appropriate error
        """
        fake_id = uuid4()
        result = mock_db.get_grievance(fake_id)
        
        assert result is None
    
    
    def test_get_grievances_for_nonexistent_student(self, mock_db):
        """
        Test: Get grievances for student with no records
        
        Validates:
        - Returns empty list
        - No errors
        """
        grievances = mock_db.get_grievances_by_student("NONEXISTENT")
        
        assert isinstance(grievances, list)
        assert len(grievances) == 0
    
    
    def test_update_nonexistent_grievance_status(self, mock_db):
        """
        Test: Update status of nonexistent grievance
        
        Validates:
        - Handles gracefully
        """
        fake_id = uuid4()
        
        # Should not raise exception
        try:
            mock_db.update_grievance_status(fake_id, "RESOLVED")
        except Exception as e:
            # If it raises, should be a clear error
            assert "not found" in str(e).lower() or "does not exist" in str(e).lower()
    
    
    def test_create_decision_for_nonexistent_grievance(self, mock_db):
        """
        Test: Create decision for nonexistent grievance
        
        Validates:
        - Handles gracefully or raises clear error
        """
        fake_grievance_id = uuid4()
        
        try:
            decision_id = mock_db.create_decision(
                grievance_id=fake_grievance_id,
                outcome="ACCEPT",
                applicable_rule="Test",
                regulatory_source="Test",
                hierarchy_level="L1_National",
                salience=1000,
                reason="Test"
            )
            # If it succeeds, decision should be created
            assert isinstance(decision_id, UUID)
        except Exception as e:
            # If it fails, should have clear error message
            assert "grievance" in str(e).lower()
