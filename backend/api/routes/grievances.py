"""
API routes for grievance operations
"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from uuid import UUID
import logging

from models import (
    Grievance, GrievanceCreate, GrievanceResponse,
    Decision, RuleTrace
)
from services.llm_service import get_llm_service
from services.fairness_service import get_fairness_service

logger = logging.getLogger(__name__)

router = APIRouter()

# Dynamic database service loader
def get_db_service():
    """Get database service (real or mock)"""
    try:
        from services.database_service import get_database_service
        return get_database_service()
    except:
        from services.mock_database_service import get_mock_database_service
        return get_mock_database_service()


@router.post("/grievances", response_model=dict, status_code=status.HTTP_201_CREATED)
async def submit_grievance(
    grievance: GrievanceCreate,
    db_service = Depends(get_db_service),
    llm_service = Depends(get_llm_service),
    fairness_service = Depends(get_fairness_service)
):
    """
    Submit a new grievance for evaluation
    
    This endpoint:
    1. Validates and stores the grievance
    2. Detects ambiguity using LLM
    3. Evaluates using Drools rule engine (or mock)
    4. Monitors fairness
    5. Returns decision with complete trace
    """
    try:
        logger.info(f"Received grievance submission from student: {grievance.student_id}")
        
        # Get rule engine (real or mock)
        try:
            from services.rule_engine_service import get_rule_engine_service
            rule_engine = get_rule_engine_service()
        except:
            from services.mock_rule_engine_service import get_mock_rule_engine_service
            rule_engine = get_mock_rule_engine_service()
            logger.info("Using mock rule engine")
        
        # Step 1: Create grievance in database
        grievance_id = db_service.create_grievance(
            student_id=grievance.student_id,
            grievance_type=grievance.grievance_type,
            narrative=grievance.narrative,
            parameters=grievance.parameters
        )
        
        logger.info(f"Created grievance {grievance_id}")
        
        # Step 2: Detect ambiguity in narrative
        ambiguity_report = llm_service.detect_ambiguity(grievance.narrative)
        
        if ambiguity_report.requires_human_review:
            logger.warning(
                f"Grievance {grievance_id} requires human review due to ambiguity"
            )
        
        # Step 3: Evaluate using rule engine
        grievance_dict = {
            'id': str(grievance_id),
            'student_id': grievance.student_id,
            'grievance_type': grievance.grievance_type,
            'narrative': grievance.narrative,
            'parameters': grievance.parameters
        }
        
        evaluation_result = rule_engine.evaluate_grievance(grievance_dict)
        decision_data = evaluation_result['decision']
        trace_data = evaluation_result['trace']
        
        # Step 4: Store decision
        if decision_data:
            decision_id = db_service.create_decision(
                grievance_id=grievance_id,
                outcome=decision_data['outcome'],
                applicable_rule=decision_data['applicable_rule'],
                regulatory_source=decision_data['regulatory_source'],
                hierarchy_level=decision_data['hierarchy_level'],
                salience=decision_data['salience'],
                reason=decision_data['reason'],
                explanation=decision_data.get('explanation'),
                action_required=decision_data.get('action_required'),
                human_review_required=(
                    decision_data.get('human_review_required', False) or
                    ambiguity_report.requires_human_review
                )
            )
            
            logger.info(f"Created decision {decision_id}")
            
            # Add decision ID to trace
            trace_data['decision_id'] = str(decision_id)
            decision_data['id'] = str(decision_id)
        else:
            decision_id = None
            logger.warning(f"No decision generated for grievance {grievance_id}")
        
        # Step 5: Store rule trace
        trace_id = db_service.create_rule_trace(
            grievance_id=grievance_id,
            decision_id=decision_id,
            rules_evaluated=trace_data.get('rules_evaluated', []),
            conflicts_detected=trace_data.get('conflicts_detected', []),
            final_decision=trace_data.get('final_decision', {}),
            processing_time_ms=trace_data.get('processing_time_ms', 0)
        )
        
        logger.info(f"Created rule trace {trace_id}")
        
        # Step 6: Monitor fairness
        if decision_data:
            fairness_report = fairness_service.monitor_fairness(
                grievance_id=grievance_id,
                decision=decision_data,
                grievance_type=grievance.grievance_type,
                parameters=grievance.parameters
            )
            
            logger.info(
                f"Fairness check complete: consistency={fairness_report['consistency_score']:.3f}, "
                f"anomaly={fairness_report['anomaly_detected']}"
            )
        else:
            fairness_report = None
        
        # Step 7: Update grievance status
        db_service.update_grievance_status(
            grievance_id=grievance_id,
            status='RESOLVED' if decision_data else 'PENDING_CLARIFICATION'
        )
        
        # Return comprehensive response
        return {
            "success": True,
            "message": "Grievance evaluated successfully",
            "grievance_id": str(grievance_id),
            "decision": decision_data,
            "trace": {
                "trace_id": str(trace_id),
                "rules_fired": evaluation_result.get('rules_fired', 0),
                "conflicts_detected": len(trace_data.get('conflicts_detected', [])),
                "processing_time_ms": trace_data.get('processing_time_ms', 0)
            },
            "ambiguity": {
                "requires_human_review": ambiguity_report.requires_human_review,
                "ambiguous_terms_count": len(ambiguity_report.ambiguous_terms),
                "clarification_questions": ambiguity_report.clarification_questions
            },
            "fairness": fairness_report if fairness_report else None
        }
        
    except Exception as e:
        logger.error(f"Error processing grievance: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process grievance: {str(e)}"
        )


@router.get("/grievances/{grievance_id}", response_model=dict)
async def get_grievance(
    grievance_id: UUID,
    db_service = Depends(get_db_service)
):
    """Get grievance by ID"""
    try:
        grievance = db_service.get_grievance(grievance_id)
        
        if not grievance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grievance {grievance_id} not found"
            )
        
        return {
            "success": True,
            "grievance": grievance
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving grievance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/grievances/student/{student_id}", response_model=dict)
async def get_student_grievances(
    student_id: str,
    db_service = Depends(get_db_service)
):
    """Get all grievances for a student"""
    try:
        grievances = db_service.get_grievances_by_student(student_id)
        
        return {
            "success": True,
            "count": len(grievances),
            "grievances": grievances
        }
        
    except Exception as e:
        logger.error(f"Error retrieving student grievances: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
