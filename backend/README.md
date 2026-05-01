# AI UI Recommendation Agent - Backend

An intelligent AI-powered system for analyzing UI screenshots and code to provide comprehensive recommendations for improving user experience.

## Architecture Overview

```
Input (UI Screenshot / Code)
        ↓
Preprocessing
        ↓
AI Models (CV + NLP + ML)
        ↓
UX Rule Engine
        ↓
Recommendation Generator
        ↓
Output (Suggestions + Score)
```

## Features

### 1. **Image Preprocessing & Analysis**

- Screenshot upload and preprocessing
- UI region extraction (header, content, footer, sidebar)
- Color histogram analysis
- Edge detection and contrast analysis
- White space calculation
- Layout complexity assessment

### 2. **Code Preprocessing & Analysis**

- HTML structure parsing and semantic tag detection
- CSS metrics extraction
- Accessibility assessment
- Form label coverage analysis
- Code quality scoring

### 3. **AI Models**

- **Computer Vision (CV)**: Visual analysis of UI screenshots
  - Edge detection and contrast analysis
  - Symmetry detection
  - Layout complexity measurement
  - Text region analysis
- **Natural Language Processing (NLP)**: Code analysis
  - HTML semantic structure evaluation
  - Accessibility text analysis
  - Code quality indicators
  - Best practices detection

- **Machine Learning (ML)**: Predictive quality scoring
  - Feature extraction and normalization
  - Composite quality scoring
  - Pattern recognition

### 4. **UX Rule Engine**

Comprehensive set of UX best practices organized by category:

- **Accessibility**: Alt text, keyboard navigation, color contrast, form labels
- **Usability**: Navigation consistency, CTA clarity, responsive design
- **Design**: Visual hierarchy, whitespace usage, font readability
- **Performance**: Page load speed
- **SEO**: Semantic HTML, meta tags
- **Security**: HTTPS usage

### 5. **Recommendation Generator**

- Categorized recommendations by priority (Critical, High, Medium, Low)
- Actionable suggestions with code examples
- Implementation roadmap
- Quick wins identification
- Letter grading (A-F)

## Project Structure

```
backend/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── preprocessing/
│   ├── __init__.py
│   └── preprocessor.py             # Image & code preprocessing
├── models/
│   ├── __init__.py
│   ├── ai_models.py               # CV, NLP, ML models
│   └── recommendation_generator.py # Recommendations engine
├── ux_engine/
│   ├── __init__.py
│   └── rules.py                   # UX rules and best practices
├── utils/
│   ├── __init__.py
│   └── [utilities]
└── .env.example                   # Environment configuration
```

## API Endpoints

### Health Check

```
GET /api/health
```

### Screenshot Analysis

```
POST /api/analyze/screenshot
Content-Type: multipart/form-data

Body:
- image: [binary image data]

Response:
{
  "status": "success",
  "analysis_type": "screenshot",
  "scores": { ... },
  "report": { ... },
  "visual_analysis": { ... },
  "rule_details": { ... }
}
```

### Code Analysis

```
POST /api/analyze/code
Content-Type: application/json

Body:
{
  "html": "<html>...</html>",
  "css": "body { ... }",
  "js": "..."
}

Response:
{
  "status": "success",
  "analysis_type": "code",
  "scores": { ... },
  "report": { ... },
  "code_analysis": { ... },
  "rule_details": { ... }
}
```

### Hybrid Analysis

```
POST /api/analyze/hybrid
Content-Type: multipart/form-data

Body:
- image: [binary image data]
- html: [HTML code]
- css: [CSS code (optional)]

Response:
{
  "status": "success",
  "analysis_type": "hybrid",
  ...
}
```

### Get History

```
GET /api/history?limit=10

Response:
{
  "status": "success",
  "count": 10,
  "history": [ ... ]
}
```

### Get Rules

```
GET /api/rules

Response:
{
  "status": "success",
  "total_rules": 17,
  "categories": [ ... ],
  "rules": [ ... ]
}
```

### Export Report

```
POST /api/export-report
Content-Type: application/json

Body:
{
  "analysis_index": -1,
  "format": "json"
}
```

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. **Clone or navigate to the backend directory**

```bash
cd backend
```

2. **Create virtual environment**

```bash
python -m venv venv
```

3. **Activate virtual environment**

Windows:

```bash
.\venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Download required NLP models (Optional)**

```bash
python -c "import nltk; nltk.download('punkt')"
```

6. **Create .env file**

```bash
cp .env.example .env
```

7. **Run the application**

```bash
python app.py
```

Server will start at `http://localhost:5000`

## Usage Examples

### Using the API with curl

**Screenshot Analysis:**

```bash
curl -X POST http://localhost:5000/api/analyze/screenshot \
  -F "image=@screenshot.png"
```

**Code Analysis:**

```bash
curl -X POST http://localhost:5000/api/analyze/code \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<html><body><h1>Test</h1></body></html>",
    "css": "body { color: #333; }"
  }'
```

### Using Python requests

```python
import requests

# Screenshot analysis
with open('screenshot.png', 'rb') as img:
    files = {'image': img}
    response = requests.post(
        'http://localhost:5000/api/analyze/screenshot',
        files=files
    )
    print(response.json())

# Code analysis
data = {
    'html': '<html><body></body></html>',
    'css': 'body { color: #333; }'
}
response = requests.post(
    'http://localhost:5000/api/analyze/code',
    json=data
)
print(response.json())
```

## Response Structure

### Score Object

```json
{
  "visual_quality_score": 75.5,
  "structural_quality_score": 82.3,
  "css_quality_score": 70.0,
  "overall_quality_score": 76.0
}
```

### Report Object

```json
{
  "overall_score": 76.0,
  "grade": "C",
  "total_issues": 8,
  "critical_issues": 0,
  "high_issues": 2,
  "medium_issues": 4,
  "low_issues": 2,
  "category_breakdown": {
    "accessibility": {
      "total_rules": 4,
      "passed": 2,
      "failed": 2,
      "average_score": 65.0,
      "pass_rate": 50.0
    }
  },
  "recommendations": {
    "critical": [],
    "high": [...],
    "medium": [...],
    "low": [...]
  }
}
```

## UX Rules

The system evaluates 17 UX best practice rules:

### Accessibility (4 rules)

- Alt text for images
- Keyboard navigation
- Color contrast
- Form labels

### Usability (3 rules)

- Consistent navigation
- Clear CTA buttons
- Responsive design

### Design (3 rules)

- Visual hierarchy
- Whitespace usage
- Font readability

### Performance (1 rule)

- Page load speed

### SEO (2 rules)

- Semantic HTML
- Meta tags

### Security (1 rule)

- HTTPS usage

### Mobile (1 rule)

- Mobile responsiveness

## Configuration

Edit `.env` file to configure:

```
PORT=5000                    # Server port
DEBUG=False                  # Debug mode
FLASK_ENV=production         # Flask environment
CORS_ORIGINS=...            # Allowed origins
LOG_LEVEL=INFO              # Logging level
```

## Performance Optimization

- Image processing uses OpenCV for efficient operations
- ML models are loaded once and cached
- Responses are structured for efficient JSON serialization
- Implements streaming for large file uploads

## Error Handling

All endpoints return consistent error responses:

```json
{
  "error": "Error message description"
}
```

HTTP Status Codes:

- `200`: Success
- `400`: Bad request (missing/invalid data)
- `404`: Not found
- `500`: Server error

## Logging

Logs are configured to help debug issues:

```
INFO: High-level analysis progress
WARNING: Potential issues
ERROR: Critical failures
DEBUG: Detailed execution information (when DEBUG=True)
```

## Dependencies

Key dependencies:

- **Flask 2.3.3**: Web framework
- **Flask-CORS**: CORS support
- **OpenCV 4.8.0**: Image processing
- **Pillow**: Image manipulation
- **scikit-learn**: ML operations
- **TensorFlow**: Deep learning (optional)
- **Transformers**: NLP models (optional)
- **NLTK**: Natural language processing

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'cv2'**

   ```bash
   pip install opencv-python
   ```

2. **Port already in use**

   ```bash
   python app.py --port 5001
   ```

3. **CORS errors**
   - Update `CORS_ORIGINS` in `.env`
   - Ensure frontend and backend have correct URLs

4. **Memory issues with large images**
   - Reduce image size before upload
   - Increase server memory

## Future Enhancements

- Database integration for persistent storage
- User authentication and project management
- Advanced ML models for pattern recognition
- Real-time collaboration features
- Performance metrics tracking
- Custom rule creation UI
- Report export to PDF/Word
- Integration with design tools (Figma, Sketch)

## Contributing

To extend the system:

1. Add new UX rules in `ux_engine/rules.py`
2. Implement new AI models in `models/ai_models.py`
3. Add new preprocessing logic in `preprocessing/preprocessor.py`
4. Create new API endpoints in `app.py`

## License

MIT License - Feel free to use and modify

## Support

For issues, questions, or suggestions, please open an issue or contact the development team.

---

**Made with ❤️ to improve UX design worldwide**
