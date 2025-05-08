"""
Main run script for the Belief Explorer application.

This script runs the Flask application.
"""

import os
import sys
from dotenv import load_dotenv
from backend.app import app

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=False)
