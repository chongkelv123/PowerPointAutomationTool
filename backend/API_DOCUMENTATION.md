# PowerPoint Generation API Documentation

## Endpoint: POST /api/ppt/generate-ppt

Generate a PowerPoint presentation with advanced features including images, text, and bullet points.

### Request Format

```json
{
  "title": "string",
  "content": [
    {
      "title": "string",
      "content": {
        "text": "string (optional)",
        "bullet_points": ["string"] (optional)
      },
      "images": [ (optional)
        {
          "url": "string (optional)",
          "base64": "string (optional)",
          "position": {
            "left": number,
            "top": number,
            "width": number,
            "height": number
          } (optional)
        }
      ]
    }
  ],
  "images": [ (optional, for title slide)
    {
      "url": "string (optional)",
      "base64": "string (optional)",
      "position": {
        "left": number,
        "top": number,
        "width": number,
        "height": number
      } (optional)
    }
  ]
}
```

### Parameters

#### Root Level
- **title** (string, required): The presentation title displayed on the first slide
- **content** (array, required): Array of slide objects
- **images** (array, optional): Array of image objects to display on the title slide

#### Content Slide Object
- **title** (string, required): The slide title
- **content** (object, required): The slide content
  - **text** (string, optional): Plain text content for the slide
  - **bullet_points** (array of strings, optional): List of bullet points
- **images** (array, optional): Array of image objects for this slide

#### Image Object
- **url** (string, optional): HTTP/HTTPS URL of the image to download
- **base64** (string, optional): Base64 encoded image data (with or without data URI prefix)
- **position** (object, optional): Image positioning
  - **left** (number): Left position in inches (default: varies by slide)
  - **top** (number): Top position in inches (default: varies by slide)
  - **width** (number): Image width in inches (default: 4)
  - **height** (number): Image height in inches (default: 3)

**Note**: Provide either `url` OR `base64` for each image, not both.

### Response

Returns a `.pptx` file as a download with:
- **Content-Type**: `application/vnd.openxmlformats-officedocument.presentationml.presentation`
- **Content-Disposition**: `attachment; filename=<generated_filename>.pptx`

### Example Requests

#### Example 1: Simple Text and Bullets

```bash
curl -X POST http://localhost:8000/api/ppt/generate-ppt \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Project Overview",
    "content": [
      {
        "title": "Introduction",
        "content": {
          "text": "Welcome to our project presentation",
          "bullet_points": [
            "Goal: Improve efficiency",
            "Timeline: Q1 2025",
            "Team: 5 developers"
          ]
        }
      },
      {
        "title": "Key Features",
        "content": {
          "bullet_points": [
            "Automated PowerPoint generation",
            "Support for images and charts",
            "RESTful API interface",
            "Easy integration"
          ]
        }
      }
    ]
  }' \
  --output presentation.pptx
```

#### Example 2: With Images from URL

```bash
curl -X POST http://localhost:8000/api/ppt/generate-ppt \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Product Showcase",
    "content": [
      {
        "title": "Our Product",
        "content": {
          "text": "Check out our amazing product",
          "bullet_points": [
            "High quality",
            "Affordable price",
            "Great reviews"
          ]
        },
        "images": [
          {
            "url": "https://example.com/product.jpg",
            "position": {
              "left": 6,
              "top": 2,
              "width": 3.5,
              "height": 4
            }
          }
        ]
      }
    ]
  }' \
  --output product_showcase.pptx
```

#### Example 3: With Base64 Image

```bash
curl -X POST http://localhost:8000/api/ppt/generate-ppt \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Company Logo",
    "content": [
      {
        "title": "About Us",
        "content": {
          "bullet_points": [
            "Founded in 2020",
            "Global presence",
            "Award winning"
          ]
        },
        "images": [
          {
            "base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
            "position": {
              "left": 7,
              "top": 2.5,
              "width": 2,
              "height": 2
            }
          }
        ]
      }
    ]
  }' \
  --output company_presentation.pptx
```

#### Example 4: Python Usage

```python
import requests

url = "http://localhost:8000/api/ppt/generate-ppt"
data = {
    "title": "Sales Report",
    "content": [
        {
            "title": "Q4 Results",
            "content": {
                "text": "Outstanding performance this quarter",
                "bullet_points": [
                    "Revenue up 25%",
                    "New customers: 150",
                    "Retention rate: 95%"
                ]
            }
        },
        {
            "title": "Next Steps",
            "content": {
                "bullet_points": [
                    "Expand to new markets",
                    "Launch new product line",
                    "Increase marketing budget"
                ]
            }
        }
    ]
}

response = requests.post(url, json=data)

if response.status_code == 200:
    with open("sales_report.pptx", "wb") as f:
        f.write(response.content)
    print("Presentation created successfully!")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

### Error Responses

#### 500 Internal Server Error
```json
{
  "detail": "Error message describing what went wrong"
}
```

Common causes:
- Invalid image URL
- Malformed base64 data
- Network timeout downloading images
- Invalid content structure

### Notes

1. **Image Sources**: Each image must have either a `url` or `base64` field, but not both
2. **Image URLs**: Must be publicly accessible HTTP/HTTPS URLs
3. **Base64 Format**: Can include or exclude the data URI prefix (e.g., `data:image/png;base64,`)
4. **Positioning**: All position values are in inches
5. **File Size**: Be mindful of image sizes when using base64 encoding
6. **Slide Layouts**:
   - Slides with images use a blank layout with custom positioning
   - Text-only slides use standard bullet layout
7. **Error Handling**: If an image fails to load, the presentation will still be generated without that image

### Testing

A test script is provided in `test_generate_ppt.py`. Run it with:

```bash
# Make sure the server is running first
uvicorn app.main:app --reload

# In another terminal
cd backend
python test_generate_ppt.py
```

### Interactive Documentation

FastAPI provides interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
