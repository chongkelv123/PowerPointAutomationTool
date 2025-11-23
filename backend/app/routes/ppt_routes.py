from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from app.services import ppt_service, template_service
import os
import json

router = APIRouter()

class PresentationRequest(BaseModel):
    title: str
    slides: list[dict]

class ImageData(BaseModel):
    url: Optional[str] = None
    base64: Optional[str] = None
    position: Optional[dict] = None  # {"left": 1, "top": 1, "width": 4, "height": 3}

class SlideContent(BaseModel):
    text: Optional[str] = None
    bullet_points: Optional[list[str]] = None

class ContentSlide(BaseModel):
    title: str
    content: SlideContent
    images: Optional[list[ImageData]] = None

class GeneratePPTRequest(BaseModel):
    title: str
    content: list[ContentSlide]
    images: Optional[list[ImageData]] = None  # Images for title slide

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

@router.post("/generate-ppt")
async def generate_ppt(request: GeneratePPTRequest):
    """
    Generate a PowerPoint presentation with advanced features

    Accepts:
    - title (string): Presentation title
    - content (array): Array of slide objects with:
      - title (string): Slide title
      - content (object): Slide content with:
        - text (string, optional): Main text content
        - bullet_points (array, optional): Array of bullet point strings
      - images (array, optional): Array of image objects for this slide
    - images (array, optional): Array of image objects for title slide

    Each image object can have:
    - url (string, optional): Image URL to download
    - base64 (string, optional): Base64 encoded image
    - position (object, optional): Image position {left, top, width, height} in inches

    Returns the .pptx file as a download
    """
    try:
        # Generate the presentation
        result = await ppt_service.generate_advanced_presentation(
            title=request.title,
            content=request.content,
            title_images=request.images
        )

        # Return the file as a download
        filepath = result["filepath"]
        filename = result["filename"]

        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Generated file not found")

        return FileResponse(
            path=filepath,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            filename=filename,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-ppt-with-template")
async def generate_ppt_with_template(
    data: str = Form(...),
    template: UploadFile = File(None)
):
    """
    Generate a PowerPoint presentation using a custom template

    Accepts:
    - data (form field): JSON string with presentation data (same structure as /generate-ppt)
    - template (file upload, optional): Custom .pptx template file

    The template file will be used as the base, maintaining all its styles, colors, and layouts.
    Content will be filled into the template's slide layouts.

    Returns the .pptx file as a download
    """
    try:
        # Parse the JSON data
        request_data = json.loads(data)

        # Validate structure
        if 'title' not in request_data or 'content' not in request_data:
            raise HTTPException(status_code=400, detail="Missing required fields: title and content")

        template_path = None

        # Handle template file if provided
        if template and template.filename:
            if not template.filename.endswith('.pptx'):
                raise HTTPException(status_code=400, detail="Template must be a .pptx file")

            # Save the uploaded template
            template_content = await template.read()
            template_path = template_service.save_template(template_content, template.filename)

        # Generate the presentation
        result = await ppt_service.generate_advanced_presentation(
            title=request_data['title'],
            content=request_data['content'],
            title_images=request_data.get('images'),
            template_path=template_path
        )

        # Return the file as a download
        filepath = result["filepath"]
        filename = result["filename"]

        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Generated file not found")

        return FileResponse(
            path=filepath,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            filename=filename,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in data field")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates")
async def list_templates():
    """List all available templates"""
    try:
        templates = template_service.list_templates()
        return {"templates": templates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/templates/upload")
async def upload_template(template: UploadFile = File(...)):
    """
    Upload a PowerPoint template

    The template can be used later for generating presentations
    """
    try:
        if not template.filename.endswith('.pptx'):
            raise HTTPException(status_code=400, detail="Template must be a .pptx file")

        # Save the uploaded template
        template_content = await template.read()
        template_path = template_service.save_template(template_content, template.filename)

        return {
            "message": "Template uploaded successfully",
            "filename": os.path.basename(template_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/templates/{filename}")
async def delete_template(filename: str):
    """Delete a template by filename"""
    try:
        success = template_service.delete_template(filename)
        if success:
            return {"message": "Template deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Template not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
