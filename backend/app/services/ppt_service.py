from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE_TYPE, PP_PLACEHOLDER
import os
import base64
import io
import requests
from datetime import datetime
from typing import Optional
from PIL import Image
from app.services.template_analyzer import (
    TemplateAnalyzer,
    adjust_font_size_for_overflow,
    split_bullet_points,
    should_split_content
)

async def create_presentation(title: str, slides: list[dict]) -> dict:
    """
    Create a PowerPoint presentation with the given title and slides

    Args:
        title: Presentation title
        slides: List of slide dictionaries with 'title' and 'content' keys

    Returns:
        Dictionary with presentation details
    """
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # Add title slide
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    slide.shapes.title.text = title

    # Add content slides
    for slide_data in slides:
        bullet_slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(bullet_slide_layout)
        shapes = slide.shapes

        title_shape = shapes.title
        body_shape = shapes.placeholders[1]

        title_shape.text = slide_data.get('title', 'Untitled Slide')

        if 'content' in slide_data:
            text_frame = body_shape.text_frame
            text_frame.text = slide_data['content']

    # Save presentation
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{title.replace(' ', '_')}_{timestamp}.pptx"
    filepath = os.path.join(output_dir, filename)

    prs.save(filepath)

    return {
        "filename": filename,
        "filepath": filepath,
        "slide_count": len(prs.slides)
    }

def download_image(url: str) -> io.BytesIO:
    """Download image from URL and return as BytesIO object"""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return io.BytesIO(response.content)

def decode_base64_image(base64_string: str) -> io.BytesIO:
    """Decode base64 image string and return as BytesIO object"""
    # Remove data URI prefix if present
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]

    image_data = base64.b64decode(base64_string)
    return io.BytesIO(image_data)

def add_image_to_slide(slide, image_data: dict, default_left: float = 1, default_top: float = 2):
    """
    Add an image to a slide

    Args:
        slide: PowerPoint slide object
        image_data: Dictionary with 'url' or 'base64' and optional 'position'
        default_left: Default left position in inches
        default_top: Default top position in inches
    """
    try:
        # Get image as BytesIO
        if image_data.get('url'):
            img_stream = download_image(image_data['url'])
        elif image_data.get('base64'):
            img_stream = decode_base64_image(image_data['base64'])
        else:
            return  # No image source provided

        # Get position or use defaults
        position = image_data.get('position', {})
        left = Inches(position.get('left', default_left))
        top = Inches(position.get('top', default_top))
        width = Inches(position.get('width', 4))
        height = Inches(position.get('height', 3))

        # Add image to slide
        slide.shapes.add_picture(img_stream, left, top, width=width, height=height)
    except Exception as e:
        print(f"Error adding image: {str(e)}")
        # Continue without the image rather than failing the entire presentation

async def generate_advanced_presentation(
    title: str,
    content: list,
    title_images: Optional[list] = None,
    template_path: Optional[str] = None
) -> dict:
    """
    Generate a PowerPoint presentation with advanced features including images and bullet points

    Args:
        title: Presentation title
        content: List of slide objects with title, content (text/bullet_points), and images
        title_images: Optional list of images for the title slide
        template_path: Optional path to a .pptx template file

    Returns:
        Dictionary with presentation details
    """
    # Load template or create blank presentation
    use_smart_layout = False
    analyzer = None

    if template_path and os.path.exists(template_path):
        prs = Presentation(template_path)
        # Analyze template for smart layout selection
        analyzer = TemplateAnalyzer(prs)
        use_smart_layout = True
    else:
        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)

    # Add title slide
    if use_smart_layout and analyzer:
        # Use smart title slide builder
        from app.services.smart_slide_builder import add_title_slide
        title_slide = add_title_slide(prs, analyzer, title, images=title_images)
    else:
        # Use simple title slide creation
        title_slide_layout = prs.slide_layouts[0]
        title_slide = prs.slides.add_slide(title_slide_layout)

        # Set title - find the title placeholder
        if title_slide.shapes.title:
            title_slide.shapes.title.text = title
        else:
            # If no title placeholder, try to find a text box
            for shape in title_slide.shapes:
                if shape.has_text_frame:
                    shape.text = title
                    break

        # Add images to title slide if provided
        if title_images:
            for idx, img_data in enumerate(title_images):
                # Position images on right side of title slide
                add_image_to_slide(
                    title_slide,
                    img_data,
                    default_left=6 + (idx * 0.5),
                    default_top=2
                )

    # Add content slides
    for slide_data in content:
        # Use smart layout if template analyzer is available
        if use_smart_layout and analyzer:
            from app.services.smart_slide_builder import add_slide_with_smart_layout

            slide_title = slide_data.get('title', 'Untitled Slide')
            slide_content = slide_data.get('content', {})
            slide_images = slide_data.get('images', [])

            # Check if content should be split
            bullet_points = slide_content.get('bullet_points', [])
            if bullet_points and len(bullet_points) > 6:
                # Split bullet points across multiple slides
                point_groups = split_bullet_points(bullet_points, max_per_slide=6)
                for idx, points in enumerate(point_groups):
                    slide_title_suffix = f" ({idx + 1}/{len(point_groups)})" if len(point_groups) > 1 else ""
                    add_slide_with_smart_layout(
                        prs,
                        analyzer,
                        slide_title + slide_title_suffix,
                        {'bullet_points': points},
                        slide_images if idx == 0 else None
                    )
            else:
                add_slide_with_smart_layout(
                    prs,
                    analyzer,
                    slide_title,
                    slide_content,
                    slide_images
                )
            continue

        # Fall through to legacy slide creation for non-template presentations
        slide_title = slide_data.get('title', 'Untitled Slide')
        slide_content = slide_data.get('content', {})
        slide_images = slide_data.get('images', [])

        # Determine slide layout based on content type
        if slide_images:
            # Use blank layout for slides with images (or last layout if template has fewer layouts)
            try:
                slide_layout = prs.slide_layouts[6]  # Blank layout
            except IndexError:
                slide_layout = prs.slide_layouts[-1]  # Use last available layout
            slide = prs.slides.add_slide(slide_layout)

            # Add title manually
            left = Inches(0.5)
            top = Inches(0.5)
            width = Inches(9)
            height = Inches(0.8)
            title_box = slide.shapes.add_textbox(left, top, width, height)
            title_frame = title_box.text_frame
            title_frame.text = slide_title
            title_paragraph = title_frame.paragraphs[0]
            title_paragraph.font.size = Pt(32)
            title_paragraph.font.bold = True

            # Add images
            for img_data in slide_images:
                add_image_to_slide(slide, img_data, default_left=5.5, default_top=1.5)

            # Add text/bullet points on the left side
            content_left = Inches(0.5)
            content_top = Inches(1.5)
            content_width = Inches(4.5)
            content_height = Inches(5)

        else:
            # Use standard bullet layout for text-only slides (or first content layout available)
            try:
                slide_layout = prs.slide_layouts[1]
            except IndexError:
                slide_layout = prs.slide_layouts[0] if len(prs.slide_layouts) > 0 else prs.slide_layouts[0]
            slide = prs.slides.add_slide(slide_layout)

            # Set slide title - handle different template structures
            if slide.shapes.title:
                slide.shapes.title.text = slide_title
            else:
                # Try to find the first text placeholder
                for shape in slide.shapes:
                    if shape.has_text_frame and shape.is_placeholder:
                        shape.text = slide_title
                        break

            content_left = None  # Will use placeholder
            content_top = None
            content_width = None
            content_height = None

        # Add text content
        text_content = slide_content.get('text')
        bullet_points = slide_content.get('bullet_points')

        if text_content or bullet_points:
            # Get or create text box
            if content_left is not None:
                # Create text box for image slides
                text_box = slide.shapes.add_textbox(content_left, content_top, content_width, content_height)
                text_frame = text_box.text_frame
                text_frame.word_wrap = True
            else:
                # Use placeholder for standard slides
                text_frame = slide.shapes.placeholders[1].text_frame

            # Clear existing text
            text_frame.clear()

            # Add plain text if provided
            if text_content:
                p = text_frame.paragraphs[0]
                p.text = text_content
                p.level = 0
                p.font.size = Pt(18)

            # Add bullet points
            if bullet_points:
                for idx, bullet in enumerate(bullet_points):
                    if idx == 0 and not text_content:
                        # Use first paragraph
                        p = text_frame.paragraphs[0]
                    else:
                        # Add new paragraph
                        p = text_frame.add_paragraph()

                    p.text = bullet
                    p.level = 0
                    p.font.size = Pt(18)

    # Save presentation
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{title.replace(' ', '_')}_{timestamp}.pptx"
    filepath = os.path.join(output_dir, filename)

    prs.save(filepath)

    return {
        "filename": filename,
        "filepath": filepath,
        "slide_count": len(prs.slides)
    }
