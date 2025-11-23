# PowerPoint Automation Backend

FastAPI backend for PowerPoint automation web application.

## Features

- RESTful API for PowerPoint generation
- Python-pptx integration for PowerPoint manipulation
- CORS enabled for frontend communication
- Automatic file management

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

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/ppt` - Get list of presentations
- `POST /api/ppt/create` - Create a new presentation
- `GET /api/ppt/{presentation_id}` - Get specific presentation

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

## Technologies

- **FastAPI** - Modern, fast web framework
- **python-pptx** - PowerPoint file manipulation
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
