"""
Frontend-backend integration test for the Belief Explorer.

This script tests the integration between the frontend and backend components.
"""

import os
import sys
import json
import logging
import webbrowser
import time
import threading
import subprocess
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import backend components
from backend.utils.config import configure_logging

# Configure logging
configure_logging()
logger = logging.getLogger(__name__)

def start_dev_server():
    """Start the development server in a separate process."""
    logger.info("Starting development server...")
    try:
        # Use subprocess to run the dev_server.py script
        process = subprocess.Popen(
            [sys.executable, os.path.join(os.path.dirname(__file__), 'dev_server.py')],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Give the server time to start
        time.sleep(3)
        
        return process
    except Exception as e:
        logger.error(f"Error starting development server: {str(e)}", exc_info=True)
        return None

def open_browser():
    """Open the browser to the application."""
    logger.info("Opening browser...")
    try:
        # Open the browser to the application URL
        webbrowser.open('http://localhost:5000')
    except Exception as e:
        logger.error(f"Error opening browser: {str(e)}", exc_info=True)

def run_integration_test():
    """Run the frontend-backend integration test."""
    logger.info("Starting frontend-backend integration test...")
    
    # Start the development server
    server_process = start_dev_server()
    
    if not server_process:
        logger.error("Failed to start development server")
        return
    
    try:
        # Open the browser to the application
        open_browser()
        
        # Print instructions for manual testing
        print("\n=== FRONTEND-BACKEND INTEGRATION TEST ===")
        print("The Belief Explorer application should now be open in your browser.")
        print("Please test the application by entering a belief statement and clicking 'Explore'.")
        print("Check that the analysis panel appears with the expected results.")
        print("Press Ctrl+C to stop the test when finished.")
        
        # Keep the server running until interrupted
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        logger.info("Test interrupted by user")
    finally:
        # Terminate the server process
        if server_process:
            logger.info("Terminating development server...")
            server_process.terminate()
            server_process.wait()

if __name__ == "__main__":
    run_integration_test()
