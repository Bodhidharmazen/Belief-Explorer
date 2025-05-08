"""
Deployment script for the Belief Explorer application.

This script prepares the application for deployment.
"""

import os
import sys
import shutil
import logging
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_deployment_package():
    """Create a deployment package for the Belief Explorer application."""
    logger.info("Creating deployment package...")
    
    # Create deployment directory
    deploy_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'deployment')
    os.makedirs(deploy_dir, exist_ok=True)
    
    # Create directories for frontend and backend
    frontend_dir = os.path.join(deploy_dir, 'frontend')
    backend_dir = os.path.join(deploy_dir, 'backend')
    os.makedirs(frontend_dir, exist_ok=True)
    os.makedirs(backend_dir, exist_ok=True)
    
    try:
        # Copy frontend files
        logger.info("Copying frontend files...")
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Copy index.html
        shutil.copy(os.path.join(project_root, 'index.html'), frontend_dir)
        
        # Copy static files
        static_src = os.path.join(project_root, 'static')
        static_dest = os.path.join(frontend_dir, 'static')
        if os.path.exists(static_dest):
            shutil.rmtree(static_dest)
        shutil.copytree(static_src, static_dest)
        
        # Copy backend files
        logger.info("Copying backend files...")
        backend_src = os.path.join(project_root, 'backend')
        if os.path.exists(backend_dir):
            shutil.rmtree(backend_dir)
        shutil.copytree(backend_src, backend_dir)
        
        # Create requirements.txt
        logger.info("Creating requirements.txt...")
        with open(os.path.join(deploy_dir, 'requirements.txt'), 'w') as f:
            f.write("flask==3.1.0\n")
            f.write("flask-cors==4.0.0\n")
            f.write("google-generativeai==0.8.4\n")
            f.write("python-dotenv==1.1.0\n")
            f.write("gunicorn==21.2.0\n")
        
        # Create .env.example file
        logger.info("Creating .env.example file...")
        with open(os.path.join(deploy_dir, '.env.example'), 'w') as f:
            f.write("# Environment variables for Belief Explorer\n")
            f.write("GEMINI_API_KEY=your_gemini_api_key_here\n")
            f.write("PORT=5000\n")
            f.write("FLASK_ENV=production\n")
        
        # Create run.py file
        logger.info("Creating run.py file...")
        with open(os.path.join(deploy_dir, 'run.py'), 'w') as f:
            f.write("""
import os
import sys
from backend.app import app

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port)
""")
        
        # Create README.md file
        logger.info("Creating README.md file...")
        with open(os.path.join(deploy_dir, 'README.md'), 'w') as f:
            f.write("""# Belief Explorer

A multi-perspective critical thinking analysis system designed to help users examine and reflect on their beliefs.

## Setup Instructions

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file based on `.env.example` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   PORT=5000
   FLASK_ENV=production
   ```

3. Run the application:
   ```
   python run.py
   ```

4. Access the application at http://localhost:5000

## Deployment Options

### Option 1: Deploy as a standalone web application
- Host the backend on a VPS or cloud service (AWS, GCP, DigitalOcean, etc.)
- Use Gunicorn as a production WSGI server:
  ```
  gunicorn -w 4 -b 0.0.0.0:5000 run:app
  ```
- Set up Nginx as a reverse proxy (recommended for production)

### Option 2: Deploy frontend and backend separately
- Host the frontend on GitHub Pages or any static hosting service
- Deploy the backend as an API service
- Update the API_URL in static/js/main.js to point to your backend URL
""")
        
        logger.info(f"Deployment package created successfully in {deploy_dir}")
        return deploy_dir
        
    except Exception as e:
        logger.error(f"Error creating deployment package: {str(e)}", exc_info=True)
        return None

def create_zip_package(deploy_dir):
    """Create a zip package of the deployment directory."""
    if not deploy_dir or not os.path.exists(deploy_dir):
        logger.error("Deployment directory does not exist")
        return None
    
    try:
        # Create zip file
        zip_file = deploy_dir + '.zip'
        logger.info(f"Creating zip package: {zip_file}")
        
        shutil.make_archive(deploy_dir, 'zip', os.path.dirname(deploy_dir), os.path.basename(deploy_dir))
        
        logger.info(f"Zip package created successfully: {zip_file}")
        return zip_file
        
    except Exception as e:
        logger.error(f"Error creating zip package: {str(e)}", exc_info=True)
        return None

if __name__ == "__main__":
    # Create deployment package
    deploy_dir = create_deployment_package()
    
    if deploy_dir:
        # Create zip package
        zip_file = create_zip_package(deploy_dir)
        
        if zip_file:
            print(f"\nDeployment package created successfully: {zip_file}")
            print("You can now deploy this package to your preferred hosting platform.")
        else:
            print("\nFailed to create zip package.")
    else:
        print("\nFailed to create deployment package.")
