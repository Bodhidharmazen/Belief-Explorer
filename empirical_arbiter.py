"""
Empirical Arbiter module for the Belief Explorer.

This module evaluates claims based on empirical evidence, measurement, and observation.
"""

import logging
import google.generativeai as genai
from utils.config import get_gemini_api_key

logger = logging.getLogger(__name__)

class EmpiricalArbiter:
    """
    Evaluates claims based on empirical evidence, measurement, and observation.
    """
    
    def __init__(self):
        """Initialize the EmpiricalArbiter with Gemini API."""
        self.api_key = get_gemini_api_key()
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            logger.error("No Gemini API key found. EmpiricalArbiter will not function.")
        
        # Configure the model
        self.model_name = "models/gemini-2.5-pro"
        self.generation_config = {
            "temperature": 0.1,  # Very low temperature for consistent analysis
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
    
    def analyze(self, claim):
        """
        Analyze a claim from an empirical perspective.
        
        Args:
            claim (str): The claim to analyze
            
        Returns:
            dict: Analysis results including scores and reasoning
        """
        if not claim or not self.api_key:
            return self._get_default_analysis()
        
        try:
            # Create the prompt for empirical analysis
            prompt = f"""
            You are the Empirical Arbiter, a specialized analytical system that evaluates claims based on empirical evidence, measurement, and observation.
            
            Analyze the following claim from an empirical perspective:
            "{claim}"
            
            Focus your analysis on:
            1. Evidence availability: Is there empirical evidence available to evaluate this claim?
            2. Measurability: Can the claim be measured or quantified?
            3. Observability: Can the phenomena in the claim be directly or indirectly observed?
            4. Testability: Can experiments be designed to test this claim?
            
            Provide your analysis in JSON format with the following structure:
            {{
                "empiricalScore": 0.0 to 1.0, // Overall empirical verifiability score
                "components": {{
                    "evidenceAvailability": 0.0 to 1.0,
                    "measurability": 0.0 to 1.0,
                    "observability": 0.0 to 1.0,
                    "testability": 0.0 to 1.0
                }},
                "reasoning": "Your detailed reasoning explaining the scores"
            }}
            
            Ensure your analysis is balanced, nuanced, and focused solely on empirical considerations.
            """
            
            # Generate response from Gemini
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config
            )
            
            response = model.generate_content(prompt)
            
            # Process the response to extract the analysis
            analysis = self._parse_analysis_from_response(response.text)
            
            logger.info(f"Completed empirical analysis for claim: {claim[:50]}...")
            return analysis
            
        except Exception as e:
            logger.error(f"Error in empirical analysis: {str(e)}", exc_info=True)
            return self._get_default_analysis()
    
    def _parse_analysis_from_response(self, response_text):
        """
        Parse analysis from the model's response text.
        
        Args:
            response_text (str): The raw response from the model
            
        Returns:
            dict: The parsed analysis
        """
        try:
            # Try to find a JSON-like structure in the response
            import json
            import re
            
            # Extract JSON object using regex
            json_match = re.search(r'({[\s\S]*})', response_text)
            if json_match:
                json_str = json_match.group(1)
                analysis = json.loads(json_str)
                
                # Validate the structure
                if not isinstance(analysis, dict):
                    raise ValueError("Analysis is not a dictionary")
                
                if "empiricalScore" not in analysis:
                    analysis["empiricalScore"] = 0.5
                
                if "components" not in analysis or not isinstance(analysis["components"], dict):
                    analysis["components"] = {
                        "evidenceAvailability": 0.5,
                        "measurability": 0.5,
                        "observability": 0.5,
                        "testability": 0.5
                    }
                
                if "reasoning" not in analysis:
                    analysis["reasoning"] = "Analysis reasoning not provided."
                
                return analysis
            
            raise ValueError("Could not find JSON in response")
            
        except Exception as e:
            logger.error(f"Error parsing empirical analysis: {str(e)}", exc_info=True)
            return self._get_default_analysis()
    
    def _get_default_analysis(self):
        """
        Provide a default analysis when the API fails.
        
        Returns:
            dict: A default analysis structure
        """
        return {
            "empiricalScore": 0.5,
            "components": {
                "evidenceAvailability": 0.5,
                "measurability": 0.5,
                "observability": 0.5,
                "testability": 0.5
            },
            "reasoning": "Unable to perform empirical analysis. This is a default response."
        }
