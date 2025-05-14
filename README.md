# PDF Data Extraction API

A FastAPI-based service that extracts data from PDF documents using OpenAI's GPT models.

## Features

- PDF document upload and processing
- OpenAI GPT integration for intelligent data extraction
- Docker support for easy deployment
- Interactive API documentation (Swagger UI and ReDoc)
- Environment-based configuration
- Comprehensive error handling

## Project Structure

```
.
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pdf_service.py
│   │   └── openai_service.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Prerequisites

- Docker and Docker Compose
- OpenAI API key

## Getting Started

1. Clone the repository
2. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```
3. Build and run the Docker container:
   ```bash
   docker-compose up --build
   ```

The API will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### POST /api/v1/extract
Upload a PDF file and extract data using OpenAI.

**Request:**
- Content-Type: multipart/form-data
- Body: PDF file

**Response:**
```json
{
    "extracted_data": {
        // Extracted data from the PDF
    },
    "metadata": {
        "filename": "example.pdf",
        "pages": 5,
        "processing_time": "2.5s"
    }
}
```

## Development

### Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Running Tests

```bash
pytest
```

## Docker Support

The project includes Docker configuration for easy deployment:

```bash
# Build and run
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop containers
docker-compose down
```

## Environment Variables

Create a `.env` file with the following variables:

```
OPENAI_API_KEY=your_api_key_here
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 