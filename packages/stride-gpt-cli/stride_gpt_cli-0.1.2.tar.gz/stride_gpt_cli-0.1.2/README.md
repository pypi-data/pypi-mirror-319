# STRIDE GPT Pro

An enterprise-grade API service that leverages Large Language Models (LLMs) to generate comprehensive threat models and attack trees based on the STRIDE methodology. Perfect for security teams, developers, and organizations looking to integrate automated threat modeling into their development lifecycle.

## Core Features

- **Advanced Threat Modeling**
  - STRIDE-based threat model generation
  - Context-aware threat identification
  - Customizable threat modeling parameters

- **Enterprise API**
  - RESTful API with OpenAPI/Swagger documentation
  - Authentication with API keys
  - Rate limiting and usage tracking
  - Secure, encrypted communications

- **Integration Ready**
  - Structured JSON responses
  - Comprehensive error handling
  - API client libraries (coming soon)

## Project Structure

```
├── src/
│   ├── api/            # FastAPI application and endpoints
│   │   ├── main.py     # Main application entry point
│   │   ├── routes/     # API route handlers
│   │   ├── deps.py     # Dependency injection
│   │   └── middleware/ # Authentication and logging middleware
│   ├── client/         # API client library
│   │   ├── __init__.py # Client package initialization
│   │   ├── auth.py     # Authentication helpers
│   │   └── api.py      # API client implementation
│   ├── models/         # Data models and schemas
│   │   ├── __init__.py # Models package initialization
│   │   ├── threat.py   # Threat model schemas
│   │   └── user.py     # User and authentication schemas
│   ├── services/       # Business logic and services
│   │   ├── __init__.py # Services package initialization
│   │   ├── llm.py      # LLM integration service
│   │   └── threat.py   # Threat analysis service
│   ├── utils/          # Utility functions
│   │   ├── __init__.py # Utils package initialization
│   │   ├── security.py # Security helpers
│   │   └── logger.py   # Logging configuration
│   ├── tests/          # Test files
│   │   ├── __init__.py # Tests package initialization
│   │   ├── conftest.py # Test configuration
│   │   ├── test_api/   # API endpoint tests
│   │   ├── test_services/ # Service layer tests
│   │   └── test_models/   # Data model tests
│   └── __init__.py     # Main package initialization
├── requirements.txt    # Project dependencies
├── requirements-dev.txt # Development dependencies
├── pyproject.toml     # Project metadata and build configuration
└── README.md          # Project documentation
```

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd stride-gpt-pro
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_for_jwt
ENVIRONMENT=development
LOG_LEVEL=DEBUG
RATE_LIMIT_PER_MINUTE=60
```

5. Run the development server:
```bash
uvicorn src.api.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation will be available at `http://localhost:8000/docs`

## Development

- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Write tests for new features
- Document all functions and classes with docstrings
- Follow the git commit conventions as specified in CONTRIBUTING.md

## Testing

Run tests using pytest:
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src tests/
```

## API Documentation

Full API documentation is available:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

## Planned Features

### Deployment
- Docker containerization for easy deployment
- DigitalOcean App Platform integration
- CI/CD pipeline setup
- Production deployment guides

### Integration
- Webhook support for automated analysis
- Integration with issue tracking systems
- Multi-environment configuration
- Automated backup and recovery

### Enterprise Features
- Team collaboration tools
- Advanced usage analytics
- Custom deployment support
- Priority support system

## License

Proprietary Software License

Copyright (c) 2024 Matthew Adams. All Rights Reserved.

This software and associated documentation files (the "Software") are proprietary and confidential. 
The Software is protected by copyright laws and international copyright treaties, as well as other 
intellectual property laws and treaties.

No part of this Software may be reproduced, distributed, disclosed, or transmitted in any form or 
by any means, electronic or mechanical, for any purpose, without the prior written permission of 
the copyright holder.

The Software is provided "AS IS", without warranty of any kind, express or implied, including but 
not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. 
In no event shall the authors or copyright holders be liable for any claim, damages or other liability, 
whether in an action of contract, tort or otherwise, arising from, out of or in connection with the 
Software or the use or other dealings in the Software.

Unauthorized copying, distribution, modification, public display, or public performance of this 
Software is strictly prohibited. This Software cannot be copied or distributed without the express 
prior written consent of the copyright holder. 