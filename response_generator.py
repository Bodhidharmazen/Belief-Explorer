"""
Response Generator module for the Belief Explorer.

This module generates thoughtful, non-judgmental responses to user beliefs.
"""

import logging
import google.generativeai as genai
from utils.config import get_gemini_api_key

logger = logging.getLogger(__name__)

class ResponseGenerator:
    """
    Generates thoughtful, non-judgmental responses to user beliefs using Gemini 2.5 Pro.
    """
    
    def __init__(self):
        """Initialize the ResponseGenerator with Gemini API."""
        self.api_key = get_gemini_api_key()
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            logger.error("No Gemini API key found. ResponseGenerator will not function.")
        
        # Configure the model
        self.model_name = "models/gemini-2.5-pro"
        self.generation_config = {
            "temperature": 0.7,  # Balanced temperature for natural responses
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
    
    def generate_response(self, claim, analysis, conversation_history):
        """
        Generate a thoughtful response to a user's belief.
        
        Args:
            claim (str): The user's claim
            analysis (dict): The integrated analysis of the claim
            conversation_history (list): Previous conversation turns
            
        Returns:
            str: A thoughtful response to the user
        """
        if not claim or not self.api_key:
            return self._get_default_response(claim)
        
        try:
            # Extract key insights from the analysis
            verifact_score = analysis.get("verifactScore", {}).get("overallScore", 0.5)
            components = analysis.get("verifactScore", {}).get("components", {})
            empirical_score = components.get("empiricalVerifiability", 0.5)
            logical_score = components.get("logicalConsistency", 0.5)
            
            # Get perspectives if available
            perspectives = analysis.get("perspectives", [])
            perspective_insights = ""
            if perspectives and len(perspectives) > 0:
                perspective = perspectives[0]  # Use the first perspective for insights
                perspective_insights = f"""
                From a {perspective.get('name', 'different').lower()} perspective: {perspective.get('assessment', '')}
                """
            
            # Format conversation history for the prompt
            formatted_history = ""
            if conversation_history:
                for turn in conversation_history[-3:]:  # Use last 3 turns at most
                    role = turn.get("role", "")
                    content = turn.get("content", "")
                    if role and content:
                        formatted_history += f"{role.capitalize()}: {content}\n"
            
            # Create the prompt for response generation
            prompt = f"""
            You are a Belief Explorer, a helpful and curious AI assistant using the Socratic method. Your goal is to help the user reflect on their beliefs. Do NOT debate, agree, disagree, or give opinions.

            The user stated the belief: "{claim}"

            Analysis insights:
            - Empirical verifiability: {empirical_score:.2f}
            - Logical consistency: {logical_score:.2f}
            - Overall Verifact score: {verifact_score:.2f}
            {perspective_insights}

            Recent conversation:
            {formatted_history}

            Generate a thoughtful, non-judgmental response that:
            1. Acknowledges the user's belief without agreeing or disagreeing
            2. Asks one or two open-ended, reflective questions about this specific belief
            3. Encourages the user to think about their reasoning or the evidence
            4. Uses a warm, curious tone that invites further exploration

            Your response should be 2-4 sentences long and end with a question.
            """
            
            # Generate response from Gemini
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config
            )
            
            response = model.generate_content(prompt)
            
            # Clean up the response
            response_text = response.text.strip()
            
            # Remove any prefixes like "Response:" or "Assistant:"
            response_text = response_text.replace("Response:", "").replace("Assistant:", "").strip()
            
            logger.info(f"Generated response for claim: {claim[:50]}...")
            return response_text
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}", exc_info=True)
            return self._get_default_response(claim)
    
    def _get_default_response(self, claim=None):
        """
        Provide a default response when the API fails.
        
        Args:
            claim (str, optional): The user's claim
            
        Returns:
            str: A default response
        """
        if claim:
            return f"I find your statement that \"{claim}\" interesting to explore. What led you to this viewpoint? What evidence or reasoning supports it?"
        else:
            return "I'm interested in exploring your perspective further. Could you share more about your reasoning on this topic?"
