"""
Unit Tests for LLM Service
Tests ambiguity detection, parameter extraction, and sentiment analysis
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

from services.llm_service import LLMService, AmbiguityReport, AmbiguousTerm


class TestLLMService:
    """Test suite for LLM service"""
    
    @pytest.fixture
    def llm_service(self):
        """Create LLM service instance for testing"""
        return LLMService(api_key="test-key-mock")
    
    
    def test_detect_ambiguity_subjective_terms(self, llm_service):
        """
        Test: Detect subjective terms in regulations
        
        Validates:
        - Identifies subjective language ("reasonable", "appropriate", "sufficient")
        - Flags for human review
        - Generates clarification questions
        """
        regulation_text = """
        Students may be granted attendance relaxation if they have reasonable cause.
        The authority shall determine if the excuse is appropriate and sufficient.
        """
        
        # Mock the OpenAI API call
        with patch.object(llm_service, 'client') as mock_client:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = """{
                "ambiguous_terms": [
                    {"term": "reasonable", "type": "subjective", "reason": "Subjective term requiring interpretation"},
                    {"term": "appropriate", "type": "subjective", "reason": "Subjective judgment required"},
                    {"term": "sufficient", "type": "subjective", "reason": "No clear threshold defined"}
                ],
                "requires_human_review": true,
                "clarification_questions": [
                    "What constitutes 'reasonable cause'?",
                    "Who determines if an excuse is 'appropriate'?"
                ]
            }"""
            mock_client.chat.completions.create.return_value = mock_response
            
            report = llm_service.detect_ambiguity(regulation_text)
            
            assert isinstance(report, AmbiguityReport)
            assert len(report.ambiguous_terms) >= 1
            assert report.requires_human_review == True
            assert len(report.clarification_questions) >= 1
            
            # Check for subjective terms
            terms = [t.term for t in report.ambiguous_terms]
            assert any(term in ["reasonable", "appropriate", "sufficient"] for term in terms)
    
    
    def test_detect_ambiguity_permissive_language(self, llm_service):
        """
        Test: Detect permissive language in regulations
        
        Validates:
        - Identifies permissive terms ("may", "should", "can")
        - Flags discretionary authority
        """
        regulation_text = """
        The committee may grant exemptions in special cases.
        Students should submit applications within 7 days.
        The dean can approve extensions at their discretion.
        """
        
        with patch.object(llm_service, 'client') as mock_client:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = """{
                "ambiguous_terms": [
                    {"term": "may", "type": "permissive", "reason": "Discretionary authority"},
                    {"term": "should", "type": "permissive", "reason": "Not mandatory"},
                    {"term": "can", "type": "permissive", "reason": "Optional action"}
                ],
                "requires_human_review": true,
                "clarification_questions": [
                    "Under what conditions 'may' exemptions be granted?",
                    "Is 'should' mandatory or optional?"
                ]
            }"""
            mock_client.chat.completions.create.return_value = mock_response
            
            report = llm_service.detect_ambiguity(regulation_text)
            
            assert isinstance(report, AmbiguityReport)
            assert len(report.ambiguous_terms) >= 1
            
            # Check for permissive terms
            terms = [t.term for t in report.ambiguous_terms]
            assert any(term in ["may", "should", "can"] for term in terms)
    
    
    def test_extract_parameters_from_narrative(self, llm_service):
        """
        Test: Extract structured parameters from grievance narrative
        
        Validates:
        - Parses natural language narrative
        - Extracts relevant parameters
        - Returns structured data
        """
        narrative = """
        I am a student in Computer Science department. My attendance is 68% due to 
        medical reasons. I was hospitalized for 15 days and have a valid medical 
        certificate from City Hospital.
        """
        
        with patch.object(llm_service, 'client') as mock_client:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = """{
                "attendance_percentage": 68.0,
                "has_medical_certificate": true,
                "medical_certificate_days": 15,
                "medical_facility": "City Hospital",
                "department": "Computer Science"
            }"""
            mock_client.chat.completions.create.return_value = mock_response
            
            parameters = llm_service.extract_parameters(narrative, "ATTENDANCE_SHORTAGE")
            
            assert isinstance(parameters, dict)
            assert "attendance_percentage" in parameters
            assert parameters["attendance_percentage"] == 68.0
            assert parameters["has_medical_certificate"] == True
    
    
    def test_generate_clarification_questions(self, llm_service):
        """
        Test: Generate clarification questions for missing parameters
        
        Validates:
        - Identifies missing information
        - Generates relevant questions
        - Returns list of questions
        """
        narrative = "I need fee waiver"
        missing_params = ["family_income", "student_category", "has_income_certificate"]
        
        with patch.object(llm_service, 'client') as mock_client:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = """{
                "questions": [
                    "What is your family's annual income?",
                    "Which category do you belong to (SC/ST/OBC/General)?",
                    "Do you have a valid income certificate?"
                ]
            }"""
            mock_client.chat.completions.create.return_value = mock_response
            
            questions = llm_service.generate_clarification_questions(narrative, missing_params)
            
            assert isinstance(questions, list)
            assert len(questions) >= 1
            assert all(isinstance(q, str) for q in questions)
    
    
    def test_analyze_sentiment(self, llm_service):
        """
        Test: Analyze sentiment and urgency of grievance narrative
        
        Validates:
        - Sentiment analysis (positive/negative/neutral)
        - Urgency detection
        - Emotional tone assessment
        """
        narrative = """
        This is extremely urgent! I am facing severe financial hardship and cannot 
        pay my fees. My family is in crisis and I desperately need help immediately.
        """
        
        with patch.object(llm_service, 'client') as mock_client:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = """{
                "sentiment": "negative",
                "urgency": "high",
                "emotional_tone": "distressed",
                "key_phrases": ["extremely urgent", "severe hardship", "desperately need help"]
            }"""
            mock_client.chat.completions.create.return_value = mock_response
            
            analysis = llm_service.analyze_grievance_sentiment(narrative)
            
            assert isinstance(analysis, dict)
            assert "sentiment" in analysis
            assert "urgency" in analysis
            assert analysis["urgency"] == "high"
    
    
    def test_mock_llm_fallback(self):
        """
        Test: Mock LLM service when API unavailable
        
        Validates:
        - System works without OpenAI API key
        - Fallback to mock responses
        - Graceful degradation
        """
        # Create service without API key
        llm_service = LLMService(api_key=None)
        
        regulation_text = "Students may be granted exemptions."
        
        # Should not raise exception
        try:
            report = llm_service.detect_ambiguity(regulation_text)
            # Mock service should return a basic report
            assert isinstance(report, AmbiguityReport)
        except Exception as e:
            # If it raises, it should be a clear error message
            assert "API key" in str(e) or "mock" in str(e).lower()


class TestAmbiguityDetectionIntegration:
    """Integration tests for ambiguity detection"""
    
    def test_detect_context_dependent_terms(self, llm_service):
        """
        Test: Detect context-dependent terms
        
        Validates:
        - Identifies terms requiring context ("exceptional circumstances", "special cases")
        - Flags for human review
        """
        regulation_text = """
        Exemptions may be granted in exceptional circumstances or special cases
        where the student demonstrates genuine need.
        """
        
        with patch.object(llm_service, 'client') as mock_client:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = """{
                "ambiguous_terms": [
                    {"term": "exceptional circumstances", "type": "context-dependent", "reason": "No clear definition"},
                    {"term": "special cases", "type": "context-dependent", "reason": "Requires interpretation"},
                    {"term": "genuine need", "type": "subjective", "reason": "Subjective assessment"}
                ],
                "requires_human_review": true,
                "clarification_questions": [
                    "What qualifies as 'exceptional circumstances'?",
                    "How is 'genuine need' determined?"
                ]
            }"""
            mock_client.chat.completions.create.return_value = mock_response
            
            report = llm_service.detect_ambiguity(regulation_text)
            
            assert isinstance(report, AmbiguityReport)
            assert report.requires_human_review == True
            assert len(report.ambiguous_terms) >= 1
    
    
    def test_no_ambiguity_detected(self, llm_service):
        """
        Test: Clear regulation with no ambiguity
        
        Validates:
        - System correctly identifies clear regulations
        - No false positives
        """
        regulation_text = """
        Students must maintain 75% attendance.
        The deadline is 15 days from result declaration.
        Fee waiver requires income below Rs. 200,000.
        """
        
        with patch.object(llm_service, 'client') as mock_client:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = """{
                "ambiguous_terms": [],
                "requires_human_review": false,
                "clarification_questions": []
            }"""
            mock_client.chat.completions.create.return_value = mock_response
            
            report = llm_service.detect_ambiguity(regulation_text)
            
            assert isinstance(report, AmbiguityReport)
            assert report.requires_human_review == False
            assert len(report.ambiguous_terms) == 0
