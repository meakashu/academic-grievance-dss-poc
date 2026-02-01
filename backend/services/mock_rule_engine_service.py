"""
Mock Rule Engine Service (for testing without Java/Maven)
This is a simplified version that simulates Drools behavior
"""
from typing import Dict, Any
import logging
import time

logger = logging.getLogger(__name__)


class MockRuleEngineService:
    """Mock service for testing without Java"""
    
    def __init__(self):
        logger.info("Mock Rule Engine initialized (Java/Drools not available)")
    
    def evaluate_grievance(self, grievance: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mock evaluation that simulates Drools behavior
        """
        logger.info(f"Mock evaluating grievance: {grievance.get('id')}")
        
        start_time = time.time()
        grievance_type = grievance.get('grievance_type', '')
        parameters = grievance.get('parameters', {})
        
        # Simulate rule evaluation based on type
        if grievance_type == 'ATTENDANCE_SHORTAGE':
            decision, trace = self._evaluate_attendance(parameters)
        elif grievance_type == 'EXAMINATION_REEVAL':
            decision, trace = self._evaluate_examination(parameters)
        elif grievance_type == 'FEE_WAIVER':
            decision, trace = self._evaluate_fee_waiver(parameters)
        else:
            decision, trace = self._default_evaluation()
        
        processing_time = int((time.time() - start_time) * 1000)
        trace['processing_time_ms'] = processing_time
        
        return {
            'decision': decision,
            'trace': trace,
            'rules_fired': len(trace.get('rules_evaluated', []))
        }
    
    def _evaluate_attendance(self, params: Dict[str, Any]) -> tuple:
        """Evaluate attendance shortage grievance"""
        attendance = params.get('attendance_percentage', 0)
        has_medical = params.get('has_medical_certificate', False)
        
        rules_evaluated = []
        conflicts = []
        
        # L1 National Rule
        if attendance < 75:
            rules_evaluated.append({
                'rule_id': 'UGC_Attendance_75Percent_Minimum',
                'hierarchy_level': 'L1_National',
                'salience': 1500,
                'fired': True,
                'outcome': 'REJECT',
                'source': 'UGC Regulations 2018, Section 4.2'
            })
        
        # L3 University Rule (if medical cert)
        if has_medical and attendance >= 65:
            rules_evaluated.append({
                'rule_id': 'University_Medical_Excuse_Attendance',
                'hierarchy_level': 'L3_University',
                'salience': 500,
                'fired': True,
                'outcome': 'ACCEPT',
                'source': 'University Statute 12.3'
            })
            
            # Conflict detected
            if attendance < 75:
                conflicts.append({
                    'type': 'AUTHORITY_CONFLICT',
                    'conflicting_rules': [
                        'UGC_Attendance_75Percent_Minimum (L1_National)',
                        'University_Medical_Excuse_Attendance (L3_University)'
                    ],
                    'resolution_strategy': 'Authority Precedence',
                    'winning_rule': 'UGC_Attendance_75Percent_Minimum',
                    'reason': 'L1_National supersedes L3_University'
                })
        
        # Final decision (highest salience wins)
        if attendance < 75:
            decision = {
                'outcome': 'REJECT',
                'applicable_rule': 'UGC_Attendance_75Percent_Minimum',
                'regulatory_source': 'UGC Regulations 2018, Section 4.2',
                'hierarchy_level': 'L1_National',
                'salience': 1500,
                'reason': f'Attendance {attendance}% is below UGC-mandated 75% minimum',
                'explanation': f'The University Grants Commission (UGC) mandates a minimum of 75% attendance for all students. Your attendance of {attendance}% does not meet this requirement. Even with a medical certificate, the national regulation takes precedence over university policies.',
                'action_required': None,
                'human_review_required': False
            }
        else:
            decision = {
                'outcome': 'ACCEPT',
                'applicable_rule': 'UGC_Attendance_Satisfied',
                'regulatory_source': 'UGC Regulations 2018, Section 4.2',
                'hierarchy_level': 'L1_National',
                'salience': 1500,
                'reason': f'Attendance {attendance}% meets UGC requirement',
                'explanation': f'Your attendance of {attendance}% meets the UGC-mandated minimum of 75%.',
                'action_required': None,
                'human_review_required': False
            }
        
        trace = {
            'rules_evaluated': rules_evaluated,
            'conflicts_detected': conflicts,
            'final_decision': decision
        }
        
        return decision, trace
    
    def _evaluate_examination(self, params: Dict[str, Any]) -> tuple:
        """Evaluate examination revaluation grievance"""
        days_since = params.get('days_since_result_declaration', 999)
        fee_paid = params.get('revaluation_fee_paid', False)
        
        rules_evaluated = []
        
        if days_since <= 15 and fee_paid:
            outcome = 'ACCEPT'
            reason = 'Revaluation request within timeline and fee paid'
        elif days_since > 15:
            outcome = 'REJECT'
            reason = f'Revaluation request submitted {days_since} days after result (deadline: 15 days)'
        else:
            outcome = 'PENDING_CLARIFICATION'
            reason = 'Revaluation fee payment required'
        
        rules_evaluated.append({
            'rule_id': 'University_Revaluation_Timeline',
            'hierarchy_level': 'L3_University',
            'salience': 1000,
            'fired': True,
            'outcome': outcome,
            'source': 'University Examination Rules 2023'
        })
        
        decision = {
            'outcome': outcome,
            'applicable_rule': 'University_Revaluation_Timeline',
            'regulatory_source': 'University Examination Rules 2023, Section 8.4',
            'hierarchy_level': 'L3_University',
            'salience': 1000,
            'reason': reason,
            'explanation': f'Revaluation requests must be submitted within 15 days of result declaration with the prescribed fee. Your request was submitted after {days_since} days.',
            'action_required': 'Pay revaluation fee' if not fee_paid else None,
            'human_review_required': False
        }
        
        trace = {
            'rules_evaluated': rules_evaluated,
            'conflicts_detected': [],
            'final_decision': decision
        }
        
        return decision, trace
    
    def _evaluate_fee_waiver(self, params: Dict[str, Any]) -> tuple:
        """Evaluate fee waiver grievance"""
        category = params.get('student_category', 'GENERAL')
        income = params.get('family_income', 999999)
        has_income_cert = params.get('has_income_certificate', False)
        
        rules_evaluated = []
        
        # SC/ST students
        if category in ['SC', 'ST']:
            outcome = 'ACCEPT'
            reason = 'SC/ST students eligible for full fee waiver'
            rule_id = 'National_SC_ST_Fee_Waiver'
            hierarchy = 'L1_National'
            salience = 1500
        # EWS students
        elif category == 'EWS' and income < 800000 and has_income_cert:
            outcome = 'ACCEPT'
            reason = 'EWS student with income below threshold'
            rule_id = 'National_EWS_Fee_Waiver'
            hierarchy = 'L1_National'
            salience = 1400
        else:
            outcome = 'REJECT'
            reason = 'Does not meet fee waiver criteria'
            rule_id = 'Fee_Waiver_General_Rule'
            hierarchy = 'L3_University'
            salience = 500
        
        rules_evaluated.append({
            'rule_id': rule_id,
            'hierarchy_level': hierarchy,
            'salience': salience,
            'fired': True,
            'outcome': outcome,
            'source': 'UGC/University Fee Rules'
        })
        
        decision = {
            'outcome': outcome,
            'applicable_rule': rule_id,
            'regulatory_source': 'UGC Fee Waiver Guidelines 2020',
            'hierarchy_level': hierarchy,
            'salience': salience,
            'reason': reason,
            'explanation': f'Based on your category ({category}) and family income (₹{income}), your fee waiver request has been evaluated.',
            'action_required': 'Submit income certificate' if not has_income_cert and category == 'EWS' else None,
            'human_review_required': False
        }
        
        trace = {
            'rules_evaluated': rules_evaluated,
            'conflicts_detected': [],
            'final_decision': decision
        }
        
        return decision, trace
    
    def _default_evaluation(self) -> tuple:
        """Default evaluation for unknown types"""
        decision = {
            'outcome': 'PENDING_CLARIFICATION',
            'applicable_rule': 'Default_Review_Required',
            'regulatory_source': 'University General Rules',
            'hierarchy_level': 'L3_University',
            'salience': 100,
            'reason': 'Grievance requires manual review',
            'explanation': 'This type of grievance requires human review to determine the appropriate course of action.',
            'action_required': 'Provide additional details',
            'human_review_required': True
        }
        
        trace = {
            'rules_evaluated': [{
                'rule_id': 'Default_Review_Required',
                'hierarchy_level': 'L3_University',
                'salience': 100,
                'fired': True,
                'outcome': 'PENDING_CLARIFICATION',
                'source': 'University General Rules'
            }],
            'conflicts_detected': [],
            'final_decision': decision
        }
        
        return decision, trace
    
    def reload_rules(self):
        """Mock reload"""
        logger.info("Mock: Rules reloaded")
    
    def shutdown(self):
        """Mock shutdown"""
        logger.info("Mock: Rule engine shutdown")


# Singleton instance
_mock_rule_engine_service = None


def get_mock_rule_engine_service():
    """Get or create mock rule engine service instance"""
    global _mock_rule_engine_service
    if _mock_rule_engine_service is None:
        _mock_rule_engine_service = MockRuleEngineService()
    return _mock_rule_engine_service
