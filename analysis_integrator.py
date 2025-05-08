"""
Analysis Integrator module for the Belief Explorer.

This module combines the outputs from different arbiters into a comprehensive analysis.
"""

import logging
import math

logger = logging.getLogger(__name__)

class AnalysisIntegrator:
    """
    Integrates analyses from different arbiters into a comprehensive analysis.
    """
    
    def __init__(self):
        """Initialize the AnalysisIntegrator."""
        pass
    
    def integrate(self, claim, empirical_analysis, logical_analysis, pragmatic_analysis):
        """
        Integrate analyses from different arbiters.
        
        Args:
            claim (str): The claim being analyzed
            empirical_analysis (dict): Analysis from the Empirical Arbiter
            logical_analysis (dict): Analysis from the Logical Arbiter
            pragmatic_analysis (dict): Analysis from the Pragmatic Arbiter
            
        Returns:
            dict: Integrated analysis with composite metrics
        """
        try:
            # Extract scores from each analysis
            empirical_score = empirical_analysis.get("empiricalScore", 0.5)
            logical_score = logical_analysis.get("logicalScore", 0.5)
            pragmatic_score = pragmatic_analysis.get("pragmaticScore", 0.5)
            
            # Calculate Verifact Score (weighted geometric mean of empirical and logical scores)
            # Pragmatic score is considered separately as it measures a different dimension
            verifact_score = math.sqrt(empirical_score * logical_score)
            
            # Calculate Model Diversity Quotient (MDQ)
            # Measures the degree of agreement/disagreement between different reasoning approaches
            scores = [empirical_score, logical_score, pragmatic_score]
            mean_score = sum(scores) / len(scores)
            variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
            mdq = min(1.0, math.sqrt(variance) * 5)  # Scale up to make it more meaningful
            
            # Calculate Contextual Sensitivity Index (CSI)
            # For now, we'll use a combination of components from different arbiters
            empirical_components = empirical_analysis.get("components", {})
            logical_components = logical_analysis.get("components", {})
            pragmatic_components = pragmatic_analysis.get("components", {})
            
            csi_components = [
                empirical_components.get("observability", 0.5),
                logical_components.get("consistency", 0.5),
                pragmatic_components.get("stakeholderValue", 0.5),
                pragmatic_components.get("adaptability", 0.5)
            ]
            csi = sum(csi_components) / len(csi_components)
            
            # Calculate Reflective Index
            # Measures awareness of assumptions and bias recognition
            # For now, we'll derive it from logical and pragmatic components
            reflective_components = [
                logical_components.get("fallacies", 0.5),
                pragmatic_components.get("consequences", 0.5)
            ]
            reflective_index = sum(reflective_components) / len(reflective_components)
            
            # Detect domain based on claim content
            domain = self._detect_domain(claim)
            
            # Detect assumptions
            assumptions = self._detect_assumptions(claim, logical_analysis)
            
            # Compile all components for the integrated analysis
            components = {
                "empiricalVerifiability": empirical_score,
                "logicalConsistency": logical_score,
                "pragmaticUtility": pragmatic_score,
                "modelDiversity": mdq,
                "contextualSensitivity": csi,
                "reflectiveIndex": reflective_index,
                "falsifiability": empirical_components.get("testability", 0.5)
            }
            
            # Create the integrated analysis
            integrated_analysis = {
                "claim": claim,
                "domain": domain,
                "assumptions": assumptions,
                "verifactScore": {
                    "overallScore": round(verifact_score, 2),
                    "components": {k: round(v, 2) for k, v in components.items()}
                },
                "empiricalAnalysis": {
                    "score": empirical_score,
                    "reasoning": empirical_analysis.get("reasoning", "")
                },
                "logicalAnalysis": {
                    "score": logical_score,
                    "reasoning": logical_analysis.get("reasoning", ""),
                    "fallacies": logical_analysis.get("identifiedFallacies", [])
                },
                "pragmaticAnalysis": {
                    "score": pragmatic_score,
                    "reasoning": pragmatic_analysis.get("reasoning", ""),
                    "stakeholders": pragmatic_analysis.get("keyStakeholders", [])
                }
            }
            
            logger.info(f"Successfully integrated analysis for claim: {claim[:50]}...")
            return integrated_analysis
            
        except Exception as e:
            logger.error(f"Error integrating analyses: {str(e)}", exc_info=True)
            return self._get_default_integrated_analysis(claim)
    
    def _detect_domain(self, claim):
        """
        Detect the domain of a claim based on its content.
        
        Args:
            claim (str): The claim to analyze
            
        Returns:
            str: The detected domain
        """
        claim_lower = claim.lower()
        
        # Simple keyword-based domain detection
        domains = {
            "science": ["scientific", "science", "research", "study", "evidence", "data", "experiment", "theory", "hypothesis"],
            "philosophy": ["philosophy", "philosophical", "ethics", "moral", "metaphysics", "epistemology", "knowledge", "reality", "existence"],
            "politics": ["politics", "political", "government", "policy", "election", "democracy", "republican", "democrat", "liberal", "conservative"],
            "religion": ["religion", "religious", "god", "faith", "belief", "spiritual", "divine", "sacred", "holy", "soul"],
            "health": ["health", "medical", "medicine", "disease", "treatment", "doctor", "patient", "therapy", "diagnosis", "symptom"],
            "technology": ["technology", "tech", "computer", "digital", "software", "hardware", "internet", "ai", "algorithm", "device"],
            "conspiracy": ["conspiracy", "cover-up", "secret", "hidden", "truth", "reveal", "government cover", "they don't want you to know"]
        }
        
        # Count matches for each domain
        domain_scores = {domain: 0 for domain in domains}
        for domain, keywords in domains.items():
            for keyword in keywords:
                if keyword in claim_lower:
                    domain_scores[domain] += 1
        
        # Find the domain with the highest score
        max_score = max(domain_scores.values())
        if max_score > 0:
            for domain, score in domain_scores.items():
                if score == max_score:
                    return domain
        
        # Default domain if no matches
        return "general"
    
    def _detect_assumptions(self, claim, logical_analysis):
        """
        Detect assumptions in a claim.
        
        Args:
            claim (str): The claim to analyze
            logical_analysis (dict): Analysis from the Logical Arbiter
            
        Returns:
            str: Description of detected assumptions
        """
        claim_lower = claim.lower()
        
        # Check for absolute terms
        absolute_terms = ["all", "everyone", "always", "never", "nobody", "certainly", 
                         "definitely", "obviously", "clearly", "absolutely", "undoubtedly",
                         "every", "no one", "must", "should", "will", "won't", "proven"]
        
        for term in absolute_terms:
            if f" {term} " in f" {claim_lower} ":
                return f"Contains absolute terms (e.g., '{term}')"
        
        # Check for fallacies identified by the logical arbiter
        fallacies = logical_analysis.get("identifiedFallacies", [])
        if fallacies:
            return f"May contain logical fallacies: {', '.join(fallacies)}"
        
        # Default if no obvious assumptions detected
        return "No obvious absolutes or fallacies identified"
    
    def _get_default_integrated_analysis(self, claim):
        """
        Provide a default integrated analysis when integration fails.
        
        Args:
            claim (str): The claim being analyzed
            
        Returns:
            dict: A default integrated analysis structure
        """
        return {
            "claim": claim,
            "domain": "general",
            "assumptions": "Analysis could not determine assumptions",
            "verifactScore": {
                "overallScore": 0.5,
                "components": {
                    "empiricalVerifiability": 0.5,
                    "logicalConsistency": 0.5,
                    "pragmaticUtility": 0.5,
                    "modelDiversity": 0.5,
                    "contextualSensitivity": 0.5,
                    "reflectiveIndex": 0.5,
                    "falsifiability": 0.5
                }
            },
            "empiricalAnalysis": {
                "score": 0.5,
                "reasoning": "Default empirical analysis"
            },
            "logicalAnalysis": {
                "score": 0.5,
                "reasoning": "Default logical analysis",
                "fallacies": []
            },
            "pragmaticAnalysis": {
                "score": 0.5,
                "reasoning": "Default pragmatic analysis",
                "stakeholders": []
            }
        }
