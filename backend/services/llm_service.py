"""
LLM Service for Ambiguity Detection and Parameter Extraction
Uses OpenAI GPT-4 for identifying discretionary language in regulations
"""
from openai import OpenAI
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import json
import logging

from config import settings

logger = logging.getLogger(__name__)


# MANDATORY PROMPT - Must appear in research paper
AMBIGUITY_DETECTION_PROMPT = """
Identify ambiguous or discretionary terms in the following education regulation.
Classify each term as: subjective, permissive, or context-dependent.

Regulation: {regulation_text}

Return JSON:
{{
  "ambiguous_terms": [
    {{"term": "...", "type": "subjective|permissive|context-dependent", "reason": "..."}}
  ],
  "requires_human_review": true|false,
  "clarification_questions": ["..."]
}}
"""


class AmbiguousTerm(BaseModel):
    """Model for an ambiguous term"""
    term: str
    type: str  # subjective, permissive, context-dependent
    reason: str


class AmbiguityReport(BaseModel):
    """Model for ambiguity detection report"""
    ambiguous_terms: List[AmbiguousTerm]
    requires_human_review: bool
    clarification_questions: List[str]
    llm_response: Optional[Dict[str, Any]] = None


class LLMService:
    """Service for LLM-based ambiguity detection and parameter extraction"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize LLM service
        
        Args:
            api_key: OpenAI API key (defaults to settings)
        """
        self.api_key = api_key or settings.openai_api_key
        self.client = OpenAI(api_key=self.api_key)
        self.model = settings.openai_model
        self.max_tokens = settings.openai_max_tokens
        self.temperature = settings.openai_temperature
        
        logger.info(f"LLM Service initialized with model: {self.model}")
    
    def detect_ambiguity(self, regulation_text: str) -> AmbiguityReport:
        """
        Detect ambiguous or discretionary terms in a regulation
        
        This is the core LLM integration for identifying subjective language
        that requires human review.
        
        Args:
            regulation_text: The regulation text to analyze
            
        Returns:
            AmbiguityReport with detected ambiguous terms
        """
        try:
            logger.info("Detecting ambiguity in regulation text")
            
            # Format the mandatory prompt
            prompt = AMBIGUITY_DETECTION_PROMPT.format(
                regulation_text=regulation_text
            )
            
            # Call GPT-4
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in education law and policy analysis. Your task is to identify ambiguous, subjective, or discretionary language in regulations that may require human judgment."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            result = json.loads(response.choices[0].message.content)
            
            # Convert to AmbiguityReport
            ambiguous_terms = [
                AmbiguousTerm(**term) for term in result.get("ambiguous_terms", [])
            ]
            
            report = AmbiguityReport(
                ambiguous_terms=ambiguous_terms,
                requires_human_review=result.get("requires_human_review", False),
                clarification_questions=result.get("clarification_questions", []),
                llm_response=result
            )
            
            logger.info(f"Detected {len(ambiguous_terms)} ambiguous terms, "
                       f"human review required: {report.requires_human_review}")
            
            return report
            
        except Exception as e:
            logger.error(f"Error detecting ambiguity: {str(e)}")
            # Return empty report on error
            return AmbiguityReport(
                ambiguous_terms=[],
                requires_human_review=True,  # Err on the side of caution
                clarification_questions=["Error occurred during ambiguity detection. Please review manually."],
                llm_response={"error": str(e)}
            )
    
    def extract_parameters(self, narrative: str, grievance_type: str) -> Dict[str, Any]:
        """
        Extract structured parameters from a grievance narrative
        
        Args:
            narrative: Student's narrative description
            grievance_type: Type of grievance
            
        Returns:
            Dictionary of extracted parameters
        """
        try:
            logger.info(f"Extracting parameters from narrative (type: {grievance_type})")
            
            prompt = f"""
Extract structured parameters from the following student grievance narrative.

Grievance Type: {grievance_type}
Narrative: {narrative}

Based on the grievance type, extract relevant parameters such as:
- For ATTENDANCE_SHORTAGE: attendance_percentage, has_medical_certificate, days_absent, etc.
- For EXAMINATION_REEVAL: course_code, marks_obtained, days_since_result_declaration, etc.
- For FEE_WAIVER: student_category, family_income, has_income_certificate, etc.

Return JSON with extracted parameters. Use null for missing information.
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at extracting structured information from unstructured text. Extract only factual information present in the narrative."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Lower temperature for extraction
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            
            parameters = json.loads(response.choices[0].message.content)
            logger.info(f"Extracted {len(parameters)} parameters")
            
            return parameters
            
        except Exception as e:
            logger.error(f"Error extracting parameters: {str(e)}")
            return {}
    
    def generate_clarification_questions(self, grievance_narrative: str, 
                                        missing_parameters: List[str]) -> List[str]:
        """
        Generate clarification questions for missing parameters
        
        Args:
            grievance_narrative: Student's narrative
            missing_parameters: List of missing parameter names
            
        Returns:
            List of clarification questions
        """
        try:
            logger.info(f"Generating clarification questions for {len(missing_parameters)} missing parameters")
            
            prompt = f"""
A student has submitted a grievance with the following narrative:
{grievance_narrative}

The following required parameters are missing:
{', '.join(missing_parameters)}

Generate clear, specific questions to ask the student to obtain this information.
Return JSON with a list of questions.
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant helping students complete their grievance submissions. Generate clear, respectful questions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            questions = result.get("questions", [])
            
            logger.info(f"Generated {len(questions)} clarification questions")
            return questions
            
        except Exception as e:
            logger.error(f"Error generating clarification questions: {str(e)}")
            return [f"Please provide: {param}" for param in missing_parameters]
    
    def analyze_grievance_sentiment(self, narrative: str) -> Dict[str, Any]:
        """
        Analyze the sentiment and urgency of a grievance narrative
        
        Args:
            narrative: Student's narrative
            
        Returns:
            Dictionary with sentiment analysis
        """
        try:
            prompt = f"""
Analyze the following student grievance narrative for:
1. Sentiment (positive, neutral, negative)
2. Urgency level (low, medium, high, critical)
3. Emotional tone
4. Key concerns

Narrative: {narrative}

Return JSON with analysis.
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in analyzing student communications for sentiment and urgency."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return {
                "sentiment": "neutral",
                "urgency": "medium",
                "error": str(e)
            }


# Singleton instance
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """Get or create LLM service instance"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
