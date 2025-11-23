"""
Test script for the /generate-ppt endpoint

This script demonstrates how to use the new generate-ppt endpoint
"""
import requests
import json

# API endpoint
API_URL = "http://localhost:8000/api/ppt/generate-ppt"

# Example 1: Simple presentation with text and bullet points
def test_simple_presentation():
    data = {
        "title": "My Test Presentation",
        "content": [
            {
                "title": "Introduction",
                "content": {
                    "text": "Welcome to our presentation",
                    "bullet_points": [
                        "First key point",
                        "Second key point",
                        "Third key point"
                    ]
                }
            },
            {
                "title": "Features",
                "content": {
                    "bullet_points": [
                        "Easy to use API",
                        "Supports images",
                        "Custom positioning",
                        "Multiple content types"
                    ]
                }
            }
        ]
    }

    print("Testing simple presentation...")
    response = requests.post(API_URL, json=data)

    if response.status_code == 200:
        with open("test_output_simple.pptx", "wb") as f:
            f.write(response.content)
        print("✓ Simple presentation created: test_output_simple.pptx")
    else:
        print(f"✗ Error: {response.status_code} - {response.text}")

# Example 2: Presentation with images from URL
def test_presentation_with_images():
    data = {
        "title": "Presentation with Images",
        "content": [
            {
                "title": "Beautiful Nature",
                "content": {
                    "text": "Here are some amazing images",
                    "bullet_points": [
                        "High quality",
                        "Beautiful scenery"
                    ]
                },
                "images": [
                    {
                        "url": "https://picsum.photos/400/300",
                        "position": {
                            "left": 5.5,
                            "top": 2,
                            "width": 4,
                            "height": 3
                        }
                    }
                ]
            }
        ]
    }

    print("\nTesting presentation with images...")
    response = requests.post(API_URL, json=data)

    if response.status_code == 200:
        with open("test_output_images.pptx", "wb") as f:
            f.write(response.content)
        print("✓ Presentation with images created: test_output_images.pptx")
    else:
        print(f"✗ Error: {response.status_code} - {response.text}")

# Example 3: Presentation with base64 image
def test_presentation_with_base64():
    # Small 1x1 pixel red PNG as base64
    red_pixel_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="

    data = {
        "title": "Base64 Image Example",
        "content": [
            {
                "title": "Embedded Image",
                "content": {
                    "text": "This slide has a base64 encoded image"
                },
                "images": [
                    {
                        "base64": red_pixel_base64,
                        "position": {
                            "left": 6,
                            "top": 2.5,
                            "width": 3,
                            "height": 3
                        }
                    }
                ]
            }
        ]
    }

    print("\nTesting presentation with base64 image...")
    response = requests.post(API_URL, json=data)

    if response.status_code == 200:
        with open("test_output_base64.pptx", "wb") as f:
            f.write(response.content)
        print("✓ Presentation with base64 image created: test_output_base64.pptx")
    else:
        print(f"✗ Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing PowerPoint Generation API")
    print("=" * 60)
    print("\nMake sure the API server is running on http://localhost:8000")
    print("Start it with: uvicorn app.main:app --reload\n")

    try:
        test_simple_presentation()
        test_presentation_with_images()
        test_presentation_with_base64()
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to API server")
        print("Please start the server first: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
