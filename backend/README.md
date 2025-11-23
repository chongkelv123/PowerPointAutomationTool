# PowerPoint Automation Backend

FastAPI backend for PowerPoint automation web application.

## Features

- RESTful API for PowerPoint generation
- Python-pptx integration for PowerPoint manipulation
- Advanced presentation generation with:
  - Support for images from URLs or base64
  - Text and bullet point content
  - Custom image positioning
  - Automatic slide layout management
- **Template support** - Use custom .pptx templates to maintain branding
- Template management (upload, list, delete)
- CORS enabled for frontend communication
- Automatic file management
- File download responses

## Setup

### 1. Activate Virtual Environment

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running the Server

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation will be available at `http://localhost:8000/docs`

## API Endpoints

### Presentation Generation
- `POST /api/ppt/create` - Create a new presentation (simple)
- `POST /api/ppt/generate-ppt` - Generate advanced presentation with images and structured content
- `POST /api/ppt/generate-ppt-with-template` - Generate presentation using a custom template
- `GET /api/ppt/{presentation_id}` - Get specific presentation
- `GET /api/ppt` - Get list of presentations

### Template Management
- `GET /api/ppt/templates` - List all uploaded templates
- `POST /api/ppt/templates/upload` - Upload a PowerPoint template
- `DELETE /api/ppt/templates/{filename}` - Delete a template

### System
- `GET /` - Root endpoint
- `GET /health` - Health check

For detailed API documentation, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── routes/              # API route handlers
│   │   ├── __init__.py
│   │   └── ppt_routes.py    # PowerPoint-related routes
│   └── services/            # Business logic
│       ├── __init__.py
│       └── ppt_service.py   # PowerPoint generation service
├── venv/                    # Virtual environment
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Testing

Run the test script to verify the API:

```bash
python test_generate_ppt.py
```

This will create sample presentations demonstrating various features.

## Technologies

- **FastAPI** - Modern, fast web framework
- **python-pptx** - PowerPoint file manipulation
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Requests** - HTTP library for image downloads
- **Pillow** - Image processing
