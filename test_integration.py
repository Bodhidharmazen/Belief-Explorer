"""
Integration test script for the Belief Explorer backend.

This script tests the integration of all backend components.
"""

import os
import sys
import json
import logging

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import backend components
from backend.models.claim_extractor import ClaimExtractor
from backend.arbiters.empirical_arbiter import EmpiricalArbiter
from backend.arbiters.logical_arbiter import LogicalArbiter
from backend.arbiters.pragmatic_arbiter import PragmaticArbiter
from backend.models.analysis_integrator import AnalysisIntegrator
from backend.models.perspective_generator import PerspectiveGenerator
from backend.models.response_generator import ResponseGenerator
from backend.utils.config import configure_logging

# Configure logging
configure_logging()
logger = logging.getLogger(__name__)

def test_backend_integration(statement):
    """
    Test the integration of all backend components with a sample statement.
    
    Args:
        statement (str): The statement to analyze
    """
    logger.info(f"Testing backend integration with statement: {statement}")
    
    try:
        # Initialize components
        claim_extractor = ClaimExtractor()
        empirical_arbiter = EmpiricalArbiter()
        logical_arbiter = LogicalArbiter()
        pragmatic_arbiter = PragmaticArbiter()
        analysis_integrator = AnalysisIntegrator()
        perspective_generator = PerspectiveGenerator()
        response_generator = ResponseGenerator()
        
        # Extract claims
        logger.info("Extracting claims...")
        claims = claim_extractor.extract_claims(statement)
        
        if not claims:
            logger.warning("No claims extracted from statement")
            return
        
        # Analyze the primary claim with each arbiter
        primary_claim = claims[0]
        logger.info(f"Analyzing primary claim: {primary_claim}")
        
        logger.info("Running empirical analysis...")
        empirical_analysis = empirical_arbiter.analyze(primary_claim)
        
        logger.info("Running logical analysis...")
        logical_analysis = logical_arbiter.analyze(primary_claim)
        
        logger.info("Running pragmatic analysis...")
        pragmatic_analysis = pragmatic_arbiter.analyze(primary_claim)
        
        # Integrate the analyses
        logger.info("Integrating analyses...")
        integrated_analysis = analysis_integrator.integrate(
            primary_claim,
            empirical_analysis,
            logical_analysis,
            pragmatic_analysis
        )
        
        # Generate perspectives
        logger.info("Generating perspectives...")
        perspectives = perspective_generator.generate_perspectives(primary_claim)
        integrated_analysis['perspectives'] = perspectives
        
        # Generate response
        logger.info("Generating response...")
        conversation_history = []
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
        
        # Print results
        logger.info("Integration test completed successfully")
        print("\n=== TEST RESULTS ===")
        print(f"Statement: {statement}")
        print(f"Primary Claim: {primary_claim}")
        print(f"Response: {response}")
        print("\nAnalysis Summary:")
        print(f"Verifact Score: {integrated_analysis['verifactScore']['overallScore']}")
        print(f"Domain: {integrated_analysis['domain']}")
        print(f"Assumptions: {integrated_analysis['assumptions']}")
        print(f"Number of Perspectives: {len(perspectives)}")
        
        # Save results to file for inspection
        with open('integration_test_results.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        logger.info("Test results saved to integration_test_results.json")
        
    except Exception as e:
        logger.error(f"Error in integration test: {str(e)}", exc_info=True)
        print(f"Integration test failed: {str(e)}")

if __name__ == "__main__":
    # Test with a sample statement
    test_statement = "The Earth is flat because the horizon looks flat from where I'm standing."
    
    # Allow command line argument to override the test statement
    if len(sys.argv) > 1:
        test_statement = sys.argv[1]
    
    test_backend_integration(test_statement)
