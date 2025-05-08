"""
Logical Arbiter module for the Belief Explorer.

This module assesses logical structure, consistency, fallacies, and argument patterns.
"""

import logging
import google.generativeai as genai
from utils.config import get_gemini_api_key

logger = logging.getLogger(__name__)

class LogicalArbiter:
    """
    Evaluates claims based on logical structure, consistency, and reasoning patterns.
    """
    
    def __init__(self):
        """Initialize the LogicalArbiter with Gemini API."""
        self.api_key = get_gemini_api_key()
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            logger.error("No Gemini API key found. LogicalArbiter will not function.")
        
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
        Analyze a claim from a logical perspective.
        
        Args:
            claim (str): The claim to analyze
            
        Returns:
            dict: Analysis results including scores and reasoning
        """
        if not claim or not self.api_key:
            return self._get_default_analysis()
        
        try:
            # Create the prompt for logical analysis
            prompt = f"""
            You are the Logical Arbiter, a specialized analytical system that evaluates claims based on logical structure, consistency, and reasoning patterns.
            
            Analyze the following claim from a logical perspective:
            "{claim}"
            
            Focus your analysis on:
            1. Premise-conclusion structure: Does the claim have clear premises and conclusion?
            2. Internal consistency: Is the claim free from contradictions?
            3. Deductive validity: If structured as a deductive argument, is it valid?
            4. Inductive strength: If structured as an inductive argument, is it strong?
            5. Fallacies: Does the claim contain logical fallacies?
            
            Provide your analysis in JSON format with the following structure:
            {{
                "logicalScore": 0.0 to 1.0, // Overall logical consistency score
                "components": {{
                    "structure": 0.0 to 1.0,
                    "consistency": 0.0 to 1.0,
                    "validity": 0.0 to 1.0,
                    "fallacies": 0.0 to 1.0 // Higher score means fewer fallacies
                }},
                "reasoning": "Your detailed reasoning explaining the scores",
                "identifiedFallacies": ["fallacy1", "fallacy2"] // Optional list of identified fallacies
            }}
            
            Ensure your analysis is balanced, nuanced, and focused solely on logical considerations.
            """
            
            # Generate response from Gemini
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config
            )
            
            response = model.generate_content(prompt)
            
            # Process the response to extract the analysis
            analysis = self._parse_analysis_from_response(response.text)
            
            logger.info(f"Completed logical analysis for claim: {claim[:50]}...")
            return analysis
            
        except Exception as e:
            logger.error(f"Error in logical analysis: {str(e)}", exc_info=True)
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
                
                if "logicalScore" not in analysis:
                    analysis["logicalScore"] = 0.5
                
                if "components" not in analysis or not isinstance(analysis["components"], dict):
                    analysis["components"] = {
                        "structure": 0.5,
                        "consistency": 0.5,
                        "validity": 0.5,
                        "fallacies": 0.5
                    }
                
                if "reasoning" not in analysis:
                    analysis["reasoning"] = "Analysis reasoning not provided."
                
                return analysis
            
            raise ValueError("Could not find JSON in response")
            
        except Exception as e:
            logger.error(f"Error parsing logical analysis: {str(e)}", exc_info=True)
            return self._get_default_analysis()
    
    def _get_default_analysis(self):
        """
        Provide a default analysis when the API fails.
        
        Returns:
            dict: A default analysis structure
        """
        return {
            "logicalScore": 0.5,
            "components": {
                "structure": 0.5,
                "consistency": 0.5,
                "validity": 0.5,
                "fallacies": 0.5
            },
            "reasoning": "Unable to perform logical analysis. This is a default response.",
            "identifiedFallacies": []
        }
