from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import ppt_service

router = APIRouter()

class PresentationRequest(BaseModel):
    title: str
    slides: list[dict]

@router.get("/")
async def get_presentations():
    """Get list of available presentations"""
    return {"presentations": []}

@router.post("/create")
async def create_presentation(request: PresentationRequest):
    """Create a new PowerPoint presentation"""
    try:
        result = await ppt_service.create_presentation(request.title, request.slides)
        return {"message": "Presentation created successfully", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{presentation_id}")
async def get_presentation(presentation_id: str):
    """Get a specific presentation by ID"""
    return {"presentation_id": presentation_id, "status": "not_implemented"}
