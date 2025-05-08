"""
Claim Extractor module for the Belief Explorer.

This module is responsible for extracting claims from user statements.
"""

import logging
import google.generativeai as genai
from utils.config import get_gemini_api_key

logger = logging.getLogger(__name__)

class ClaimExtractor:
    """
    Extracts claims from user statements using Gemini 2.5 Pro.
    """
    
    def __init__(self):
        """Initialize the ClaimExtractor with Gemini API."""
        self.api_key = get_gemini_api_key()
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            logger.error("No Gemini API key found. ClaimExtractor will not function.")
        
        # Configure the model
        self.model_name = "models/gemini-2.5-pro"
        self.generation_config = {
            "temperature": 0.2,  # Low temperature for more deterministic outputs
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
    
    def extract_claims(self, statement):
        """
        Extract claims from a user statement.
        
        Args:
            statement (str): The user's statement or belief
            
        Returns:
            list: A list of extracted claims as strings
        """
        if not statement or not self.api_key:
            return []
        
        try:
            # Create the prompt for claim extraction
            prompt = f"""
            Extract the main claims or beliefs from the following statement. 
            Focus on extracting clear, specific claims that can be analyzed.
            If multiple claims are present, extract up to 3 of the most significant ones.
            If no clear claims are present, extract the main point as a claim.
            
            Statement: "{statement}"
            
            Output the claims as a Python list of strings, with the most significant claim first.
            Example output format: ["Main claim here", "Secondary claim here"]
            """
            
            # Generate response from Gemini
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config
            )
            
            response = model.generate_content(prompt)
            
            # Process the response to extract the claims list
            response_text = response.text
            
            # Extract the list from the response
            claims = self._parse_claims_from_response(response_text)
            
            logger.info(f"Extracted {len(claims)} claims from statement")
            return claims
            
        except Exception as e:
            logger.error(f"Error extracting claims: {str(e)}", exc_info=True)
            
            # Fallback to simple extraction if API fails
            return self._fallback_extraction(statement)
    
    def _parse_claims_from_response(self, response_text):
        """
        Parse claims from the model's response text.
        
        Args:
            response_text (str): The raw response from the model
            
        Returns:
            list: A list of extracted claims
        """
        try:
            # Try to find a list-like structure in the response
            if "[" in response_text and "]" in response_text:
                list_text = response_text[response_text.find("["):response_text.rfind("]")+1]
                # Safely evaluate the string as a Python list
                claims = eval(list_text)
                if isinstance(claims, list) and all(isinstance(item, str) for item in claims):
                    return claims
            
            # If we can't parse a list, try to extract claims line by line
            lines = [line.strip() for line in response_text.split("\n") if line.strip()]
            claims = []
            for line in lines:
                # Remove common prefixes like numbers, dashes, etc.
                clean_line = line.lstrip("0123456789.- *\"'")
                if clean_line and len(clean_line) > 10:  # Minimum length for a claim
                    claims.append(clean_line)
            
            return claims[:3]  # Return up to 3 claims
            
        except Exception as e:
            logger.error(f"Error parsing claims from response: {str(e)}", exc_info=True)
            return []
    
    def _fallback_extraction(self, statement):
        """
        Simple fallback method for claim extraction when the API fails.
        
        Args:
            statement (str): The user's statement or belief
            
        Returns:
            list: A list containing the statement as a single claim
        """
        # Simple sentence splitting
        sentences = [s.strip() for s in statement.split(".") if len(s.strip()) > 10]
        
        if sentences:
            return sentences[:3]  # Return up to 3 sentences as claims
        else:
            return [statement]  # Return the whole statement as a claim
