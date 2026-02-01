"""
API routes for rule metadata
Exposes rule provenance and regulatory sources
"""
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
import logging

from services.rule_metadata_extractor import get_rule_metadata_extractor

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/rules", response_model=dict)
async def list_all_rules():
    """
    List all loaded rules with metadata
    
    Returns:
        Dictionary with all rules and their metadata
    """
    try:
        extractor = get_rule_metadata_extractor()
        rules = extractor.get_all_rules_metadata()
        
        return {
            "success": True,
            "count": len(rules),
            "rules": rules
        }
    except Exception as e:
        logger.error(f"Error listing rules: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/rules/{rule_name}/metadata", response_model=dict)
async def get_rule_metadata(rule_name: str):
    """
    Get metadata for a specific rule
    
    Args:
        rule_name: Name of the rule
        
    Returns:
        Rule metadata including authority, source, hierarchy level
    """
    try:
        extractor = get_rule_metadata_extractor()
        metadata = extractor.get_rule_metadata(rule_name)
        
        if not metadata:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rule '{rule_name}' not found"
            )
        
        return {
            "success": True,
            "rule_name": rule_name,
            "metadata": metadata
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting rule metadata: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/rules/level/{hierarchy_level}", response_model=dict)
async def get_rules_by_level(hierarchy_level: str):
    """
    Get all rules at a specific hierarchy level
    
    Args:
        hierarchy_level: L1_National, L2_Accreditation, or L3_University
        
    Returns:
        List of rules at that level
    """
    try:
        extractor = get_rule_metadata_extractor()
        rules = extractor.get_rules_by_level(hierarchy_level)
        
        return {
            "success": True,
            "hierarchy_level": hierarchy_level,
            "count": len(rules),
            "rules": rules
        }
    except Exception as e:
        logger.error(f"Error getting rules by level: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/rules/category/{category}", response_model=dict)
async def get_rules_by_category(category: str):
    """
    Get all rules in a specific category
    
    Args:
        category: Attendance, Examination, Fee, etc.
        
    Returns:
        List of rules in that category
    """
    try:
        extractor = get_rule_metadata_extractor()
        rules = extractor.get_rules_by_category(category)
        
        return {
            "success": True,
            "category": category,
            "count": len(rules),
            "rules": rules
        }
    except Exception as e:
        logger.error(f"Error getting rules by category: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/rules/search", response_model=dict)
async def search_rules(q: str):
    """
    Search rules by keyword
    
    Args:
        q: Search query
        
    Returns:
        List of matching rules
    """
    try:
        extractor = get_rule_metadata_extractor()
        rules = extractor.search_rules(q)
        
        return {
            "success": True,
            "query": q,
            "count": len(rules),
            "rules": rules
        }
    except Exception as e:
        logger.error(f"Error searching rules: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/rules/hierarchy/summary", response_model=dict)
async def get_hierarchy_summary():
    """
    Get summary of rule hierarchy
    
    Returns:
        Summary with counts by level, category, and authority
    """
    try:
        extractor = get_rule_metadata_extractor()
        summary = extractor.get_hierarchy_summary()
        
        return {
            "success": True,
            "summary": summary
        }
    except Exception as e:
        logger.error(f"Error getting hierarchy summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
