"""
Conflict Resolution Explanation Service
Generates human-readable explanations for hierarchical conflict resolution
"""
from typing import List, Dict, Any
from models.rule_trace import ConflictInfo
from models.decision import Decision


def generate_conflict_resolution_explanation(
    conflicts: List[ConflictInfo],
    final_decision: Decision
) -> Dict[str, str]:
    """
    Generate detailed explanation for conflict resolution
    
    Args:
        conflicts: List of detected conflicts
        final_decision: The winning decision after conflict resolution
        
    Returns:
        Dictionary with conflict resolution narrative
    """
    if not conflicts or len(conflicts) == 0:
        return {
            "summary": "No conflicts detected",
            "explanation": "Only one rule was applicable to this grievance.",
            "resolution_strategy": "N/A"
        }
    
    explanations = []
    
    for conflict in conflicts:
        conflict_type = conflict.conflict_type
        conflicting_rules = conflict.conflicting_rules
        winner = conflict.winner
        reason = conflict.reason
        resolution_strategy = conflict.resolution_strategy
        
        # Generate detailed explanation based on conflict type
        if conflict_type == "AUTHORITY_CONFLICT":
            explanation = _explain_authority_conflict(
                conflicting_rules, winner, reason, resolution_strategy
            )
        elif conflict_type == "SALIENCE_CONFLICT":
            explanation = _explain_salience_conflict(
                conflicting_rules, winner, reason
            )
        elif conflict_type == "TEMPORAL_CONFLICT":
            explanation = _explain_temporal_conflict(
                conflicting_rules, winner, reason
            )
        else:
            explanation = _explain_generic_conflict(
                conflicting_rules, winner, reason, resolution_strategy
            )
        
        explanations.append(explanation)
    
    # Combine all explanations
    summary = f"{len(conflicts)} conflict(s) detected and resolved"
    full_explanation = "\n\n".join(explanations)
    
    # Add final decision context
    final_context = _generate_final_decision_context(final_decision, conflicts)
    
    return {
        "summary": summary,
        "explanation": full_explanation,
        "final_decision_context": final_context,
        "resolution_strategy": conflicts[0].resolution_strategy if conflicts else "N/A",
        "conflicts_count": len(conflicts)
    }


def _explain_authority_conflict(
    conflicting_rules: List[str],
    winner: str,
    reason: str,
    resolution_strategy: str
) -> str:
    """
    Explain authority-based conflict resolution
    
    Returns:
        Detailed explanation of authority precedence
    """
    # Extract hierarchy levels from rule names
    hierarchy_levels = []
    for rule in conflicting_rules:
        if "L1" in rule or "National" in rule:
            hierarchy_levels.append("L1 (National Law)")
        elif "L2" in rule or "Accreditation" in rule:
            hierarchy_levels.append("L2 (Accreditation Standards)")
        elif "L3" in rule or "University" in rule:
            hierarchy_levels.append("L3 (University Policy)")
    
    explanation = f"""
**Authority Conflict Detected**

**Conflicting Rules:**
{_format_rule_list(conflicting_rules)}

**Conflict Type:** Hierarchical Authority Precedence

**Resolution:**
The rule '{winner}' was selected based on the established legal hierarchy:
- L1 (National Laws/UGC Regulations) > L2 (Accreditation Standards/NAAC/NBA) > L3 (University Statutes)

**Rationale:**
{reason}

**Legal Principle:**
In Indian higher education governance, national regulations (UGC, MHRD) supersede accreditation body guidelines (NAAC, NBA), which in turn supersede university-level policies. This ensures compliance with constitutional and statutory mandates.

**Resolution Strategy:** {resolution_strategy}
"""
    return explanation.strip()


def _explain_salience_conflict(
    conflicting_rules: List[str],
    winner: str,
    reason: str
) -> str:
    """
    Explain salience-based conflict resolution
    
    Returns:
        Detailed explanation of salience precedence
    """
    explanation = f"""
**Salience Conflict Detected**

**Conflicting Rules (Same Hierarchy Level):**
{_format_rule_list(conflicting_rules)}

**Resolution:**
The rule '{winner}' was selected based on higher salience (priority score).

**Rationale:**
{reason}

**Technical Detail:**
When multiple rules at the same hierarchy level fire, the Drools engine uses salience values to determine precedence. Higher salience indicates higher priority, typically assigned to:
- Exception rules over general rules
- Specific conditions over broad conditions
- Mandatory provisions over discretionary provisions

**Resolution Strategy:** Salience-Based Priority
"""
    return explanation.strip()


def _explain_temporal_conflict(
    conflicting_rules: List[str],
    winner: str,
    reason: str
) -> str:
    """
    Explain temporal conflict resolution (newer vs older rules)
    
    Returns:
        Detailed explanation of temporal precedence
    """
    explanation = f"""
**Temporal Conflict Detected**

**Conflicting Rules (Different Effective Dates):**
{_format_rule_list(conflicting_rules)}

**Resolution:**
The rule '{winner}' was selected based on effective date precedence.

**Rationale:**
{reason}

**Legal Principle:**
When regulations are amended or superseded, the most recent regulation takes precedence unless explicitly stated otherwise. This ensures compliance with current legal frameworks.

**Resolution Strategy:** Temporal Precedence
"""
    return explanation.strip()


def _explain_generic_conflict(
    conflicting_rules: List[str],
    winner: str,
    reason: str,
    resolution_strategy: str
) -> str:
    """
    Explain generic conflict resolution
    
    Returns:
        Generic conflict explanation
    """
    explanation = f"""
**Conflict Detected**

**Conflicting Rules:**
{_format_rule_list(conflicting_rules)}

**Resolution:**
The rule '{winner}' was selected.

**Rationale:**
{reason}

**Resolution Strategy:** {resolution_strategy}
"""
    return explanation.strip()


def _format_rule_list(rules: List[str]) -> str:
    """
    Format list of rules for display
    
    Returns:
        Formatted bullet list of rules
    """
    return "\n".join([f"- {rule}" for rule in rules])


def _generate_final_decision_context(
    final_decision: Decision,
    conflicts: List[ConflictInfo]
) -> str:
    """
    Generate context for final decision after conflict resolution
    
    Returns:
        Context explaining why this decision was final
    """
    context = f"""
**Final Decision:** {final_decision.outcome}

**Applicable Rule:** {final_decision.applicable_rule}

**Hierarchy Level:** {final_decision.hierarchy_level}

**Regulatory Source:** {final_decision.regulatory_source}

**Why This Decision:**
After resolving {len(conflicts)} conflict(s), this decision represents the highest authority applicable to this grievance. The decision is based on {final_decision.hierarchy_level} regulations, which take precedence over lower-level policies.

**Confidence:** {final_decision.confidence if hasattr(final_decision, 'confidence') else 'N/A'}

**Human Review Required:** {'Yes' if final_decision.human_review_required else 'No'}
"""
    return context.strip()


def get_conflict_summary(conflicts: List[ConflictInfo]) -> str:
    """
    Get brief summary of conflicts
    
    Args:
        conflicts: List of conflicts
        
    Returns:
        Brief summary string
    """
    if not conflicts:
        return "No conflicts"
    
    conflict_types = [c.conflict_type for c in conflicts]
    unique_types = set(conflict_types)
    
    summary_parts = []
    for conflict_type in unique_types:
        count = conflict_types.count(conflict_type)
        summary_parts.append(f"{count} {conflict_type.replace('_', ' ').title()}")
    
    return ", ".join(summary_parts)
