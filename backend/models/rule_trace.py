"""
Pydantic models for Rule Trace data
"""
from pydantic import BaseModel, Field, UUID4
from typing import List, Dict, Any, Optional
from datetime import datetime


class ConditionCheck(BaseModel):
    """Model for a single condition check"""
    condition: str = Field(..., description="Condition expression")
    satisfied: bool = Field(..., description="Whether condition was satisfied")
    value: Optional[Any] = Field(None, description="Actual value checked")


class FiredRuleInfo(BaseModel):
    """Information about a fired rule"""
    rule_id: str = Field(..., description="Rule identifier")
    hierarchy_level: str = Field(..., description="Regulatory hierarchy level")
    salience: int = Field(..., description="Rule salience/priority")
    conditions_checked: List[ConditionCheck] = Field(default_factory=list, description="Conditions evaluated")
    fired: bool = Field(..., description="Whether the rule actually fired")
    outcome: Optional[str] = Field(None, description="Outcome if rule fired")
    reason: Optional[str] = Field(None, description="Reason for outcome")
    source: Optional[str] = Field(None, description="Regulatory source")
    timestamp: Optional[datetime] = Field(None, description="When rule was evaluated")


class ConflictInfo(BaseModel):
    """Information about a rule conflict"""
    type: str = Field(..., description="Type of conflict (AUTHORITY, TEMPORAL, SPECIFICITY)")
    conflicting_rules: List[str] = Field(..., description="Rules in conflict")
    resolution_strategy: str = Field(..., description="Strategy used to resolve conflict")
    winning_rule: str = Field(..., description="Rule that won the conflict")
    reason: str = Field(..., description="Explanation of why this rule won")


class RuleTraceBase(BaseModel):
    """Base rule trace model"""
    rules_evaluated: List[FiredRuleInfo] = Field(default_factory=list, description="All rules evaluated")
    conflicts_detected: List[ConflictInfo] = Field(default_factory=list, description="Conflicts detected")
    final_decision: Dict[str, Any] = Field(default_factory=dict, description="Final decision summary")
    processing_time_ms: int = Field(..., ge=0, description="Processing time in milliseconds")


class RuleTraceCreate(RuleTraceBase):
    """Model for creating a new rule trace"""
    grievance_id: UUID4
    decision_id: Optional[UUID4] = None


class RuleTrace(RuleTraceBase):
    """Complete rule trace model with database fields"""
    id: UUID4
    grievance_id: UUID4
    decision_id: Optional[UUID4] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "323e4567-e89b-12d3-a456-426614174000",
                "grievance_id": "123e4567-e89b-12d3-a456-426614174000",
                "decision_id": "223e4567-e89b-12d3-a456-426614174000",
                "rules_evaluated": [
                    {
                        "rule_id": "UGC_Attendance_75Percent_Minimum",
                        "hierarchy_level": "L1_National",
                        "salience": 1500,
                        "conditions_checked": [
                            {"condition": "type == 'ATTENDANCE_SHORTAGE'", "satisfied": True},
                            {"condition": "attendancePercentage < 75", "satisfied": True, "value": 72.0},
                            {"condition": "hasMedicalCertificate == false", "satisfied": True}
                        ],
                        "fired": True,
                        "outcome": "REJECT",
                        "reason": "Attendance below UGC-mandated 75% minimum",
                        "source": "UGC Regulations 2018, Section 4.2"
                    }
                ],
                "conflicts_detected": [
                    {
                        "type": "AUTHORITY_CONFLICT",
                        "conflicting_rules": [
                            "UGC_Attendance_75Percent_Minimum (L1_National)",
                            "University_Medical_Excuse_Attendance (L3_University)"
                        ],
                        "resolution_strategy": "Authority Precedence",
                        "winning_rule": "UGC_Attendance_75Percent_Minimum",
                        "reason": "L1_National supersedes L3_University based on authority precedence"
                    }
                ],
                "final_decision": {
                    "outcome": "REJECT",
                    "applicable_rule": "UGC_Attendance_75Percent_Minimum",
                    "hierarchy_level": "L1_National"
                },
                "processing_time_ms": 145,
                "created_at": "2024-02-01T10:05:00Z"
            }
        }


class RuleTraceResponse(BaseModel):
    """API response for rule trace operations"""
    success: bool
    message: str
    trace: Optional[RuleTrace] = None
