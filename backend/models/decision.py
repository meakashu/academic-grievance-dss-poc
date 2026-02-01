"""
Pydantic models for Decision data
"""
from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime
from enum import Enum


class DecisionOutcome(str, Enum):
    """Enumeration of decision outcomes"""
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    PARTIAL_ACCEPT = "PARTIAL_ACCEPT"
    PENDING_CLARIFICATION = "PENDING_CLARIFICATION"


class HierarchyLevel(str, Enum):
    """Enumeration of regulatory hierarchy levels"""
    L1_NATIONAL = "L1_National"
    L2_ACCREDITATION = "L2_Accreditation"
    L3_UNIVERSITY = "L3_University"


class DecisionBase(BaseModel):
    """Base decision model"""
    outcome: DecisionOutcome = Field(..., description="Decision outcome")
    applicable_rule: str = Field(..., description="Rule that determined the decision")
    regulatory_source: str = Field(..., description="Source regulation citation")
    hierarchy_level: HierarchyLevel = Field(..., description="Regulatory hierarchy level")
    salience: int = Field(..., ge=0, description="Rule salience/priority")
    reason: str = Field(..., min_length=10, description="Brief reason for decision")
    explanation: Optional[str] = Field(None, description="Detailed human-readable explanation")
    action_required: Optional[str] = Field(None, description="Action required from student")
    human_review_required: bool = Field(default=False, description="Whether human review is needed")


class DecisionCreate(DecisionBase):
    """Model for creating a new decision"""
    grievance_id: UUID4


class Decision(DecisionBase):
    """Complete decision model with database fields"""
    id: UUID4
    grievance_id: UUID4
    decided_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "223e4567-e89b-12d3-a456-426614174000",
                "grievance_id": "123e4567-e89b-12d3-a456-426614174000",
                "outcome": "REJECT",
                "applicable_rule": "UGC_Attendance_75Percent_Minimum",
                "regulatory_source": "UGC Regulations 2018, Section 4.2",
                "hierarchy_level": "L1_National",
                "salience": 1500,
                "reason": "Attendance below UGC-mandated 75% minimum without medical excuse",
                "explanation": "Despite having a valid medical certificate, the attendance of 72% does not meet the UGC-mandated minimum of 75%. The medical excuse exception requires attendance of at least 65%, which is met, but the national law takes precedence over university policy.",
                "action_required": None,
                "human_review_required": False,
                "decided_at": "2024-02-01T10:05:00Z",
                "created_at": "2024-02-01T10:05:00Z"
            }
        }


class DecisionResponse(BaseModel):
    """API response for decision operations"""
    success: bool
    message: str
    decision: Optional[Decision] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Decision generated successfully",
                "decision": {
                    "id": "223e4567-e89b-12d3-a456-426614174000",
                    "outcome": "REJECT",
                    "applicable_rule": "UGC_Attendance_75Percent_Minimum",
                    "hierarchy_level": "L1_National"
                }
            }
        }
