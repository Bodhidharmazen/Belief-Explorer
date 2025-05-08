"""
Perspective Generator module for the Belief Explorer.

This module generates multiple perspectives on a claim.
"""

import logging
import google.generativeai as genai
from utils.config import get_gemini_api_key

logger = logging.getLogger(__name__)

class PerspectiveGenerator:
    """
    Generates multiple perspectives on a claim using Gemini 2.5 Pro.
    """
    
    def __init__(self):
        """Initialize the PerspectiveGenerator with Gemini API."""
        self.api_key = get_gemini_api_key()
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            logger.error("No Gemini API key found. PerspectiveGenerator will not function.")
        
        # Configure the model
        self.model_name = "models/gemini-2.5-pro"
        self.generation_config = {
            "temperature": 0.7,  # Higher temperature for more diverse perspectives
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
    
    def generate_perspectives(self, claim):
        """
        Generate multiple perspectives on a claim.
        
        Args:
            claim (str): The claim to analyze
            
        Returns:
            list: A list of perspective objects
        """
        if not claim or not self.api_key:
            return self._get_default_perspectives(claim)
        
        try:
            # Create the prompt for perspective generation
            prompt = f"""
            You are analyzing this specific claim: "{claim}"

            Generate EXACTLY 3 different perspectives on THIS CLAIM ONLY.

            Your response must be a JSON array with 3 objects, each containing:
            - "name": Brief title of perspective (e.g., "Scientific" or "Ethical")
            - "description": One sentence explaining this viewpoint
            - "assessment": One sentence evaluating THE CLAIM from this perspective
            - "score": A score from 0.0 to 1.0 representing how well the claim aligns with this perspective

            Do not add any text outside the JSON array.
            Example format (but about the provided claim, not this example):
            [
              {{
                "name": "Perspective1",
                "description": "Description of this perspective.",
                "assessment": "Assessment of the original claim from this perspective.",
                "score": 0.7
              }},
              {{
                "name": "Perspective2",
                "description": "Description of perspective 2.",
                "assessment": "Assessment from perspective 2.",
                "score": 0.5
              }},
              {{
                "name": "Perspective3", 
                "description": "Description of perspective 3.",
                "assessment": "Assessment from perspective 3.",
                "score": 0.3
              }}
            ]
            """
            
            # Generate response from Gemini
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config
            )
            
            response = model.generate_content(prompt)
            
            # Process the response to extract the perspectives
            perspectives = self._parse_perspectives_from_response(response.text)
            
            logger.info(f"Generated {len(perspectives)} perspectives for claim: {claim[:50]}...")
            return perspectives
            
        except Exception as e:
            logger.error(f"Error generating perspectives: {str(e)}", exc_info=True)
            return self._get_default_perspectives(claim)
    
    def _parse_perspectives_from_response(self, response_text):
        """
        Parse perspectives from the model's response text.
        
        Args:
            response_text (str): The raw response from the model
            
        Returns:
            list: A list of perspective objects
        """
        try:
            # Try to find a JSON-like structure in the response
            import json
            import re
            
            # Extract JSON array using regex
            json_match = re.search(r'(\[[\s\S]*\])', response_text)
            if json_match:
                json_str = json_match.group(1)
                perspectives = json.loads(json_str)
                
                # Validate the structure
                if not isinstance(perspectives, list):
                    raise ValueError("Perspectives is not a list")
                
                # Ensure each perspective has the required fields
                valid_perspectives = []
                for perspective in perspectives:
                    if not isinstance(perspective, dict):
                        continue
                    
                    # Ensure required fields exist
                    if not all(key in perspective for key in ["name", "description", "assessment"]):
                        continue
                    
                    # Add score if missing
                    if "score" not in perspective:
                        perspective["score"] = 0.5
                    
                    valid_perspectives.append(perspective)
                
                # Ensure we have at least one valid perspective
                if not valid_perspectives:
                    raise ValueError("No valid perspectives found")
                
                return valid_perspectives
            
            raise ValueError("Could not find JSON array in response")
            
        except Exception as e:
            logger.error(f"Error parsing perspectives: {str(e)}", exc_info=True)
            return self._get_default_perspectives()
    
    def _get_default_perspectives(self, claim=None):
        """
        Provide default perspectives when the API fails.
        
        Args:
            claim (str, optional): The claim being analyzed
            
        Returns:
            list: A list of default perspective objects
        """
        claim_text = claim if claim else "the claim"
        
        return [
            {
                "name": "Empirical",
                "description": "Based on observable evidence and data.",
                "assessment": f"The claim '{claim_text}' would need to be evaluated against empirical evidence.",
                "score": 0.5
            },
            {
                "name": "Logical",
                "description": "Concerned with consistent reasoning and structure.",
                "assessment": f"The logical structure and premises of '{claim_text}' require examination.",
                "score": 0.5
            },
            {
                "name": "Pragmatic",
                "description": "Focused on practical implications and utility.",
                "assessment": f"The practical consequences of accepting '{claim_text}' should be considered.",
                "score": 0.5
            }
        ]
