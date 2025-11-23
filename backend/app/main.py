from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import ppt_routes

app = FastAPI(
    title="PowerPoint Automation API",
    description="API for automating PowerPoint generation and manipulation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ppt_routes.router, prefix="/api/ppt", tags=["PowerPoint"])

@app.get("/")
async def root():
    return {"message": "PowerPoint Automation API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
