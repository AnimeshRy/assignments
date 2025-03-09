# Document Management and RAG-based Q&A Application

This application provides a backend service for document management and question-answering using Retrieval-Augmented Generation (RAG).

## Features

- Document ingestion and embedding generation
- RAG-based Q&A system
- Document selection for targeted Q&A
- User management
- Asynchronous API design

## Tech Stack

- **Backend**: FastAPI, Python 3.9+
- **Database**: PostgreSQL
- **Embedding Generation**: Sentence Transformers
- **RAG Implementation**: LangChain
- **Testing**: Pytest
- **Containerization**: Docker
- **CI/CD**: GitHub Actions

## Setup and Installation

### Prerequisites

- Python 3.9+
- PostgreSQL
- Docker (optional)

### Local Development Setup

1. Clone the repository

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```
   # Make sure PostgreSQL is running
   ./scripts/init_db.py
   ```

6. (Optional) Generate test data:
   ```
   ./scripts/generate_test_data.py
   ```

7. Start the application:
   ```
   ./run.py
   # Or alternatively:
   uvicorn app.main:app --reload
   ```

8. Access the API documentation at http://localhost:8000/api/docs

### Docker Setup

1. Build and run with Docker Compose:
   ```
   docker-compose up --build
   ```

2. Access the API documentation at http://localhost:8000/api/docs

## API Documentation

### Authentication API
- `POST /api/auth/login`: Login and get access token

### User Management API
- `POST /api/users`: Create a new user (superuser only)
- `GET /api/users/me`: Get current user information
- `PUT /api/users/me`: Update current user information
- `GET /api/users/{user_id}`: Get user by ID (superuser only)
- `GET /api/users`: List all users (superuser only)

### Document Ingestion API
- `POST /api/documents`: Create a new document
- `POST /api/documents/upload`: Upload a document file
- `GET /api/documents`: List all documents
- `GET /api/documents/{document_id}`: Get document details
- `DELETE /api/documents/{document_id}`: Delete a document

### Q&A API
- `POST /api/qa/sessions`: Create a new QA session with selected documents
- `GET /api/qa/sessions`: List all QA sessions
- `GET /api/qa/sessions/{qa_session_id}`: Get QA session details
- `PUT /api/qa/sessions/{qa_session_id}`: Update a QA session
- `DELETE /api/qa/sessions/{qa_session_id}`: Delete a QA session
- `POST /api/qa/ask`: Ask a question and get an answer based on the documents

## Testing

Run tests with:
```
pytest
```

Generate coverage report:
```
pytest --cov=app tests/
```

## CI/CD Pipeline

This project uses GitHub Actions for CI/CD:

1. **Continuous Integration**: Runs tests and linting on every push and pull request
2. **Continuous Deployment**: Builds and deploys Docker images to the container registry

## Architecture and Design

For detailed information about the architecture, design decisions, and implementation details, see [ARCHITECTURE.md](ARCHITECTURE.md).

## License

MIT
