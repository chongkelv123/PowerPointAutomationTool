"""
Template management service for PowerPoint templates
"""
import os
import shutil
from datetime import datetime
from typing import Optional

TEMPLATES_DIR = "templates"

def save_template(file_content: bytes, filename: str) -> str:
    """
    Save an uploaded template file

    Args:
        file_content: Binary content of the template file
        filename: Original filename

    Returns:
        Path to the saved template file
    """
    os.makedirs(TEMPLATES_DIR, exist_ok=True)

    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = filename.replace(" ", "_")
    template_filename = f"template_{timestamp}_{safe_filename}"
    template_path = os.path.join(TEMPLATES_DIR, template_filename)

    # Save the file
    with open(template_path, "wb") as f:
        f.write(file_content)

    return template_path

def get_template_path(filename: str) -> Optional[str]:
    """
    Get the full path to a template file

    Args:
        filename: Name of the template file

    Returns:
        Full path to the template file if it exists, None otherwise
    """
    template_path = os.path.join(TEMPLATES_DIR, filename)
    if os.path.exists(template_path):
        return template_path
    return None

def list_templates() -> list[dict]:
    """
    List all available templates

    Returns:
        List of dictionaries with template information
    """
    if not os.path.exists(TEMPLATES_DIR):
        return []

    templates = []
    for filename in os.listdir(TEMPLATES_DIR):
        if filename.endswith('.pptx'):
            filepath = os.path.join(TEMPLATES_DIR, filename)
            stat = os.stat(filepath)
            templates.append({
                "filename": filename,
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })

    return templates

def delete_template(filename: str) -> bool:
    """
    Delete a template file

    Args:
        filename: Name of the template file to delete

    Returns:
        True if deleted successfully, False otherwise
    """
    template_path = os.path.join(TEMPLATES_DIR, filename)
    if os.path.exists(template_path):
        os.remove(template_path)
        return True
    return False
