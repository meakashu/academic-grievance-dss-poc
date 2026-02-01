"""
Pydantic models for Grievance data
"""
from pydantic import BaseModel, Field, UUID4
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class GrievanceType(str, Enum):
    """Enumeration of grievance types"""
    ATTENDANCE_SHORTAGE = "ATTENDANCE_SHORTAGE"
    EXAMINATION_REEVAL = "EXAMINATION_REEVAL"
    GRADE_APPEAL = "GRADE_APPEAL"
    FEE_WAIVER = "FEE_WAIVER"
    FEE_INSTALLMENT_REQUEST = "FEE_INSTALLMENT_REQUEST"
    TRANSCRIPT_DELAY = "TRANSCRIPT_DELAY"
    OTHER = "OTHER"


class GrievanceStatus(str, Enum):
    """Enumeration of grievance statuses"""
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"
    PENDING_CLARIFICATION = "PENDING_CLARIFICATION"


class GrievanceBase(BaseModel):
    """Base grievance model"""
    student_id: str = Field(..., description="Student identifier")
    grievance_type: GrievanceType = Field(..., description="Type of grievance")
    narrative: str = Field(..., min_length=10, description="Student's narrative description")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Structured parameters")


class GrievanceCreate(GrievanceBase):
    """Model for creating a new grievance"""
    pass


class GrievanceUpdate(BaseModel):
    """Model for updating a grievance"""
    narrative: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    status: Optional[GrievanceStatus] = None


class Grievance(GrievanceBase):
    """Complete grievance model with database fields"""
    id: UUID4
    status: GrievanceStatus = GrievanceStatus.PENDING
    submitted_at: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "student_id": "STU2024001",
                "grievance_type": "ATTENDANCE_SHORTAGE",
                "narrative": "I have 72% attendance with a valid medical certificate for 15 days of absence due to hospitalization.",
                "parameters": {
                    "attendance_percentage": 72.0,
                    "has_medical_certificate": True,
                    "medical_certificate_valid": True,
                    "medical_certificate_from_recognized_authority": True,
                    "days_absent": 15
                },
                "status": "PENDING",
                "submitted_at": "2024-02-01T10:00:00Z",
                "created_at": "2024-02-01T10:00:00Z",
                "updated_at": "2024-02-01T10:00:00Z"
            }
        }


class GrievanceResponse(BaseModel):
    """API response for grievance operations"""
    success: bool
    message: str
    grievance: Optional[Grievance] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Grievance submitted successfully",
                "grievance": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "student_id": "STU2024001",
                    "grievance_type": "ATTENDANCE_SHORTAGE",
                    "status": "PENDING"
                }
            }
        }
