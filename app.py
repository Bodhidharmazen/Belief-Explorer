"""
Belief Explorer - Backend Application
A Flask-based backend for the Belief Explorer critical thinking platform.
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import logging

# Import custom modules
from arbiters.empirical_arbiter import EmpiricalArbiter
from arbiters.logical_arbiter import LogicalArbiter
from arbiters.pragmatic_arbiter import PragmaticArbiter
from models.claim_extractor import ClaimExtractor
from models.analysis_integrator import AnalysisIntegrator
from models.perspective_generator import PerspectiveGenerator
from models.response_generator import ResponseGenerator
from utils.config import configure_logging

# Load environment variables
load_dotenv()

# Configure logging
configure_logging()
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='../static')

# Initialize components
claim_extractor = ClaimExtractor()
empirical_arbiter = EmpiricalArbiter()
logical_arbiter = LogicalArbiter()
pragmatic_arbiter = PragmaticArbiter()
analysis_integrator = AnalysisIntegrator()
perspective_generator = PerspectiveGenerator()
response_generator = ResponseGenerator()

@app.route('/')
def index():
    """Serve the main application page."""
    return send_from_directory('../', 'index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_belief():
    """
    Analyze a belief statement using the multi-arbiter system.
    
    Expected JSON payload:
    {
        "statement": "The belief statement to analyze",
        "history": [
            {"role": "assistant", "content": "Previous assistant message"},
            {"role": "user", "content": "Previous user message"}
        ]
    }
    
    Returns:
    {
        "Response": "Assistant's response to the user",
        "AnalysisJSON": "[{...analysis data...}]"
    }
    """
    try:
        # Get request data
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        user_statement = data.get('statement')
        conversation_history = data.get('history', [])
        
        if not user_statement:
            return jsonify({"error": "No statement provided"}), 400
        
        logger.info(f"Received statement for analysis: {user_statement[:50]}...")
        
        # Extract claims from the statement
        claims = claim_extractor.extract_claims(user_statement)
        
        if not claims:
            logger.warning("No claims extracted from statement")
            return jsonify({
                "Response": "I couldn't identify a specific claim to analyze in your statement. Could you rephrase it as a more specific belief or claim?",
                "AnalysisJSON": "[]"
            })
        
        # Analyze the primary claim with each arbiter
        primary_claim = claims[0]
        logger.info(f"Analyzing primary claim: {primary_claim}")
        
        empirical_analysis = empirical_arbiter.analyze(primary_claim)
        logical_analysis = logical_arbiter.analyze(primary_claim)
        pragmatic_analysis = pragmatic_arbiter.analyze(primary_claim)
        
        # Integrate the analyses
        integrated_analysis = analysis_integrator.integrate(
            primary_claim,
            empirical_analysis,
            logical_analysis,
            pragmatic_analysis
        )
        
        # Generate perspectives
        perspectives = perspective_generator.generate_perspectives(primary_claim)
        integrated_analysis['perspectives'] = perspectives
        
        # Generate response
        response = response_generator.generate_response(
            primary_claim,
            integrated_analysis,
            conversation_history
        )
        
        # Prepare final output
        result = {
            "Response": response,
            "AnalysisJSON": [integrated_analysis]
        }
        
        logger.info("Analysis completed successfully")
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({
            "error": "An error occurred while processing your request",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=True)
