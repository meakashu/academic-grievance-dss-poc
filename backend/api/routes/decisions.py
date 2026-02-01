"""
API routes for decision and trace operations
"""
from fastapi import APIRouter, HTTPException, Depends, status
from uuid import UUID
import logging

from services.database_service import get_database_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/decisions/{decision_id}", response_model=dict)
async def get_decision(
    decision_id: UUID,
    db_service = Depends(get_database_service)
):
    """
    Get decision by ID
    
    Returns complete decision with explanation and regulatory source
    """
    try:
        decision = db_service.get_decision(decision_id)
        
        if not decision:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Decision {decision_id} not found"
            )
        
        return {
            "success": True,
            "decision": decision
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving decision: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/decisions/grievance/{grievance_id}", response_model=dict)
async def get_decision_by_grievance(
    grievance_id: UUID,
    db_service = Depends(get_database_service)
):
    """
    Get decision for a specific grievance
    
    Returns the most recent decision for the grievance
    """
    try:
        decision = db_service.get_decision_by_grievance(grievance_id)
        
        if not decision:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No decision found for grievance {grievance_id}"
            )
        
        return {
            "success": True,
            "decision": decision
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving decision: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/trace/{trace_id}", response_model=dict)
async def get_trace(
    trace_id: UUID,
    db_service = Depends(get_database_service)
):
    """
    Get rule trace by ID
    
    Returns complete execution trace with all rules evaluated,
    conflicts detected, and resolution strategy
    """
    try:
        trace = db_service.get_rule_trace(trace_id)
        
        if not trace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Trace {trace_id} not found"
            )
        
        return {
            "success": True,
            "trace": trace
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving trace: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/trace/grievance/{grievance_id}", response_model=dict)
async def get_trace_by_grievance(
    grievance_id: UUID,
    db_service = Depends(get_database_service)
):
    """
    Get rule trace for a specific grievance
    
    Returns the complete execution trace showing:
    - All rules evaluated
    - Conditions checked
    - Conflicts detected
    - Resolution strategy applied
    - Final decision
    - Processing time
    """
    try:
        trace = db_service.get_rule_trace_by_grievance(grievance_id)
        
        if not trace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No trace found for grievance {grievance_id}"
            )
        
        # Enhance trace with human-readable summary
        rules_evaluated = trace.get('rules_evaluated', [])
        conflicts_detected = trace.get('conflicts_detected', [])
        
        summary = {
            "total_rules_evaluated": len(rules_evaluated),
            "rules_fired": sum(1 for r in rules_evaluated if r.get('fired', False)),
            "conflicts_detected": len(conflicts_detected),
            "processing_time_ms": trace.get('processing_time_ms', 0),
            "hierarchy_levels_involved": list(set(
                r.get('hierarchy_level') for r in rules_evaluated
            ))
        }
        
        return {
            "success": True,
            "trace": trace,
            "summary": summary
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving trace: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/fairness/consistency", response_model=dict)
async def get_fairness_metrics(
    db_service = Depends(get_database_service)
):
    """
    Get overall fairness and consistency metrics
    
    Returns aggregate statistics on decision consistency
    and anomaly detection across all cases
    """
    try:
        from services.fairness_service import get_fairness_service
        fairness_service = get_fairness_service()
        
        metrics = fairness_service.get_fairness_metrics()
        
        return {
            "success": True,
            "metrics": metrics
        }
        
    except Exception as e:
        logger.error(f"Error retrieving fairness metrics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
