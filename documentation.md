# Belief Explorer Documentation

## Overview

Belief Explorer is a sophisticated AI-powered critical thinking platform designed to help users examine and reflect on their beliefs through multiple analytical perspectives. This document provides comprehensive information about the system architecture, components, and deployment instructions.

## System Architecture

The Belief Explorer consists of two main components:

1. **Frontend**: A single-page web application built with HTML, CSS, and JavaScript
2. **Backend**: A Python/Flask API server with Gemini 2.5 Pro integration

### Frontend Components

- **User Interface**: Clean, responsive design with dark/light mode support
- **Chat Interface**: Conversational interface for belief exploration
- **Analysis Panel**: Displays critical thinking analysis with three tabs:
  - Critical Thinking: Shows claim analysis with scores
  - Perspectives: Displays multiple perspectives on the claim
  - Advanced Metrics: Shows radar chart and detailed metrics

### Backend Components

- **Flask Application**: Main API server handling requests
- **Multi-Arbiter System**: Three specialized arbiters analyzing claims:
  - Empirical Arbiter: Evaluates claims based on evidence and observation
  - Logical Arbiter: Assesses logical structure and consistency
  - Pragmatic Arbiter: Examines practical utility and implications
- **Integration Engine**: Combines arbiter outputs into comprehensive analysis
- **Perspective Generator**: Creates multiple perspectives on claims
- **Response Generator**: Produces thoughtful, Socratic responses

## Critical Thinking Framework

The system employs a formalized critical thinking framework with these key components:

- **Verifact Score**: A composite measure (0.0-1.0) of how empirically verifiable and logically consistent a claim is
- **Model Diversity Quotient (MDQ)**: Measures the degree of agreement/disagreement between different reasoning approaches
- **Contextual Sensitivity Index (CSI)**: Evaluates how appropriate the claim is within its relevant context
- **Reflective Index**: Assesses awareness of assumptions and bias recognition

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Gemini API key

### Backend Setup

1. Clone the repository or extract the deployment package
2. Navigate to the project directory
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   PORT=5000
   FLASK_ENV=production
   ```

### Running the Application

1. Start the backend server:
   ```
   python run.py
   ```
2. Access the application at http://localhost:5000

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

## API Documentation

### Analyze Endpoint

**URL**: `/api/analyze`
**Method**: `POST`
**Content Type**: `application/json`

**Request Body**:
```json
{
  "statement": "The belief statement to analyze",
  "history": [
    {"role": "assistant", "content": "Previous assistant message"},
    {"role": "user", "content": "Previous user message"}
  ]
}
```

**Response**:
```json
{
  "Response": "Assistant's response to the user",
  "AnalysisJSON": "[{...analysis data...}]"
}
```

## Code Structure

```
belief_explorer/
├── backend/
│   ├── arbiters/
│   │   ├── __init__.py
│   │   ├── empirical_arbiter.py
│   │   ├── logical_arbiter.py
│   │   └── pragmatic_arbiter.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── analysis_integrator.py
│   │   ├── claim_extractor.py
│   │   ├── perspective_generator.py
│   │   └── response_generator.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── config.py
│   └── app.py
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── main.js
│   └── img/
│       └── logo.svg
├── tests/
│   ├── dev_server.py
│   ├── prepare_deployment.py
│   ├── test_frontend_backend.py
│   └── test_integration.py
├── .env.example
├── index.html
└── run.py
```

## Development

### Running Tests

1. Backend integration test:
   ```
   python tests/test_integration.py
   ```

2. Frontend-backend integration test:
   ```
   python tests/test_frontend_backend.py
   ```

### Development Server

For development purposes, you can use the development server:
```
python tests/dev_server.py
```

### Preparing for Deployment

To create a deployment package:
```
python tests/prepare_deployment.py
```

## Troubleshooting

### Common Issues

1. **API Key Issues**: Ensure your Gemini API key is correctly set in the `.env` file
2. **CORS Errors**: If deploying frontend and backend separately, ensure CORS is properly configured
3. **Module Import Errors**: Check that all dependencies are installed and the directory structure is maintained

### Logging

Logs are stored in the `logs` directory. Check these logs for detailed error information.

## Future Enhancements

Potential areas for future development:

1. User accounts and saved analyses
2. Expanded domain coverage
3. Integration with educational platforms
4. Collaborative analysis features
5. Mobile application

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For support or inquiries, contact: info@metacognitioninstitute.com
