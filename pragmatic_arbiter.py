"""
Pragmatic Arbiter module for the Belief Explorer.

This module examines practical utility, real-world implications, and functional value of claims.
"""

import logging
import google.generativeai as genai
from utils.config import get_gemini_api_key

logger = logging.getLogger(__name__)

class PragmaticArbiter:
    """
    Evaluates claims based on practical utility, real-world implications, and functional value.
    """
    
    def __init__(self):
        """Initialize the PragmaticArbiter with Gemini API."""
        self.api_key = get_gemini_api_key()
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            logger.error("No Gemini API key found. PragmaticArbiter will not function.")
        
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
        Analyze a claim from a pragmatic perspective.
        
        Args:
            claim (str): The claim to analyze
            
        Returns:
            dict: Analysis results including scores and reasoning
        """
        if not claim or not self.api_key:
            return self._get_default_analysis()
        
        try:
            # Create the prompt for pragmatic analysis
            prompt = f"""
            You are the Pragmatic Arbiter, a specialized analytical system that evaluates claims based on practical utility, real-world implications, and functional value.
            
            Analyze the following claim from a pragmatic perspective:
            "{claim}"
            
            Focus your analysis on:
            1. Practical utility: Does the claim have practical applications or usefulness?
            2. Consequences: What are the potential consequences of accepting this claim?
            3. Stakeholder impact: How does this claim affect different stakeholders?
            4. Alternative framings: Are there more useful ways to frame this issue?
            
            Provide your analysis in JSON format with the following structure:
            {{
                "pragmaticScore": 0.0 to 1.0, // Overall pragmatic utility score
                "components": {{
                    "utility": 0.0 to 1.0,
                    "consequences": 0.0 to 1.0,
                    "stakeholderValue": 0.0 to 1.0,
                    "adaptability": 0.0 to 1.0
                }},
                "reasoning": "Your detailed reasoning explaining the scores",
                "keyStakeholders": ["stakeholder1", "stakeholder2"] // Optional list of key stakeholders
            }}
            
            Ensure your analysis is balanced, nuanced, and focused solely on pragmatic considerations.
            """
            
            # Generate response from Gemini
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config
            )
            
            response = model.generate_content(prompt)
            
            # Process the response to extract the analysis
            analysis = self._parse_analysis_from_response(response.text)
            
            logger.info(f"Completed pragmatic analysis for claim: {claim[:50]}...")
            return analysis
            
        except Exception as e:
            logger.error(f"Error in pragmatic analysis: {str(e)}", exc_info=True)
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
                
                if "pragmaticScore" not in analysis:
                    analysis["pragmaticScore"] = 0.5
                
                if "components" not in analysis or not isinstance(analysis["components"], dict):
                    analysis["components"] = {
                        "utility": 0.5,
                        "consequences": 0.5,
                        "stakeholderValue": 0.5,
                        "adaptability": 0.5
                    }
                
                if "reasoning" not in analysis:
                    analysis["reasoning"] = "Analysis reasoning not provided."
                
                return analysis
            
            raise ValueError("Could not find JSON in response")
            
        except Exception as e:
            logger.error(f"Error parsing pragmatic analysis: {str(e)}", exc_info=True)
            return self._get_default_analysis()
    
    def _get_default_analysis(self):
        """
        Provide a default analysis when the API fails.
        
        Returns:
            dict: A default analysis structure
        """
        return {
            "pragmaticScore": 0.5,
            "components": {
                "utility": 0.5,
                "consequences": 0.5,
                "stakeholderValue": 0.5,
                "adaptability": 0.5
            },
            "reasoning": "Unable to perform pragmatic analysis. This is a default response.",
            "keyStakeholders": []
        }
