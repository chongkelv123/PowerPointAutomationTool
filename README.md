# PowerPoint Automation Tool

A modern web application for automating PowerPoint presentation creation with a React frontend and FastAPI backend.

## Overview

This tool allows users to quickly create PowerPoint presentations through a simple web interface. The application features a React + Vite frontend for an intuitive user experience and a FastAPI backend with python-pptx for PowerPoint generation.

## Project Structure

```
PowerPointAutomationTool/
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API service layer
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom hooks
│   │   ├── App.jsx         # Main App component
│   │   └── main.jsx        # Entry point
│   ├── public/             # Static assets
│   ├── package.json
│   └── vite.config.js
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI app
│   │   ├── routes/         # API routes
│   │   │   └── ppt_routes.py
│   │   └── services/       # Business logic
│   │       └── ppt_service.py
│   ├── venv/               # Virtual environment
│   ├── requirements.txt    # Python dependencies
│   └── .env.example       # Environment template
└── README.md              # This file
```

## Features

### Frontend
- Modern React UI with hooks
- Real-time form validation
- Dynamic slide management (add/remove slides)
- Responsive design
- API integration layer

### Backend
- RESTful API with FastAPI
- PowerPoint generation using python-pptx
- CORS enabled for frontend communication
- Health check endpoints
- Automatic file management

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Git

### 1. Clone the Repository

```bash
git clone <repository-url>
cd PowerPointAutomationTool
```

### 2. Set Up Backend

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env if needed

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### 3. Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env if needed

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

## Usage

1. Open the frontend at `http://localhost:5173`
2. Enter a presentation title
3. Add slides with titles and content
4. Click "Create Presentation" to generate your PowerPoint
5. The generated file will be saved in `backend/output/`

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/ppt` - List presentations
- `POST /api/ppt/create` - Create new presentation
- `GET /api/ppt/{id}` - Get specific presentation

## Technologies

### Frontend
- React 18
- Vite 6
- Modern JavaScript (ES6+)

### Backend
- FastAPI
- Python-pptx
- Uvicorn (ASGI server)
- Pydantic (data validation)

## Development

### Backend Development

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Building for Production

Frontend:
```bash
cd frontend
npm run build
```

Backend:
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Configuration

### Backend (.env)
```
APP_NAME=PowerPoint Automation API
DEBUG=True
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:5173
OUTPUT_DIR=output
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=PowerPoint Automation Tool
```

## Project Documentation

- [Frontend README](./frontend/README.md)
- [Backend README](./backend/README.md)

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues or questions, please open an issue on the GitHub repository.
