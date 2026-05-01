# AI UI Recommendation Agent

A comprehensive AI-powered system for analyzing UI/UX and providing intelligent recommendations for improvement.

## 🎯 Overview

The AI UI Recommendation Agent is a full-stack application that leverages artificial intelligence (Computer Vision, Natural Language Processing, and Machine Learning) to:

- **Analyze UI Screenshots**: Extract visual features and design quality metrics
- **Analyze Code**: Evaluate HTML/CSS code structure and best practices
- **Apply UX Rules**: Check against 17+ UX best practices
- **Generate Recommendations**: Provide prioritized, actionable recommendations
- **Score and Grade**: Assign quality scores (0-100) and letter grades (A-F)

## 📊 System Architecture

```
┌─────────────────────────────────────────────────┐
│          User Input (Frontend)                  │
│   • Screenshot Upload • Code Paste              │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│          Image/Code Preprocessing               │
│   • Format normalization • Data extraction      │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│      AI Models (CV + NLP + ML Analysis)         │
│   • Computer Vision • NLP • Predictions         │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│          UX Rule Engine                         │
│   • Rule Evaluation • Best Practices Check      │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│      Recommendation Generator                   │
│   • Priority Assessment • Code Examples         │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│       Output (Suggestions + Scores)             │
│   • Recommendations • Reports • Grades          │
└─────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
AI_UI_recommend_agent/
├── backend/
│   ├── app.py                           # Flask application
│   ├── requirements.txt                 # Python dependencies
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   └── preprocessor.py              # Image & code preprocessing
│   ├── models/
│   │   ├── __init__.py
│   │   ├── ai_models.py                 # CV, NLP, ML models
│   │   └── recommendation_generator.py  # Recommendations engine
│   ├── ux_engine/
│   │   ├── __init__.py
│   │   └── rules.py                     # UX rules & best practices
│   ├── utils/
│   │   └── __init__.py
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── ImageUploader.js
│   │   │   ├── ImageUploader.module.css
│   │   │   ├── CodeEditor.js
│   │   │   ├── CodeEditor.module.css
│   │   │   ├── RecommendationsPanel.js
│   │   │   └── RecommendationsPanel.module.css
│   │   ├── pages/
│   │   ├── services/
│   │   │   └── analysisService.js
│   │   ├── App.js
│   │   ├── App.module.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   ├── .env.example
│   └── README.md
│
└── README.md (this file)
```

## 🚀 Quick Start

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run server
python app.py
```

Backend will be available at `http://localhost:5000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm start
```

Frontend will be available at `http://localhost:3000`

## 🔌 API Endpoints

### Analysis Endpoints

| Endpoint                  | Method | Description               |
| ------------------------- | ------ | ------------------------- |
| `/api/health`             | GET    | Health check              |
| `/api/analyze/screenshot` | POST   | Analyze UI screenshot     |
| `/api/analyze/code`       | POST   | Analyze HTML/CSS code     |
| `/api/analyze/hybrid`     | POST   | Analyze screenshot + code |
| `/api/history`            | GET    | Get analysis history      |
| `/api/rules`              | GET    | Get all UX rules          |
| `/api/export-report`      | POST   | Export report             |

## 🎯 Key Features

### 1. Screenshot Analysis

- Visual quality assessment
- Design pattern detection
- Contrast and readability analysis
- Layout complexity evaluation
- Color distribution analysis

### 2. Code Analysis

- HTML semantic structure checking
- CSS metrics extraction
- Accessibility assessment
- Code quality scoring
- Best practices validation

### 3. UX Rule Engine

17 comprehensive rules across 8 categories:

- ✅ **Accessibility** (4 rules)
- ✅ **Usability** (3 rules)
- ✅ **Design** (3 rules)
- ✅ **Mobile** (1 rule)
- ✅ **Performance** (1 rule)
- ✅ **SEO** (2 rules)
- ✅ **Security** (1 rule)

### 4. Intelligent Recommendations

- Prioritized by severity (Critical → Low)
- Organized by effort (Quick wins → Long-term)
- Includes code examples
- Impact assessment
- Implementation guidance

### 5. Scoring System

- Numeric score (0-100)
- Letter grade (A-F)
- Category breakdown
- Pass rate calculation

## 📊 Report Structure

```json
{
  "overall_score": 76.5,
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

## 🛠️ Technology Stack

### Backend

- **Python 3.8+**
- **Flask 2.3+** - Web framework
- **OpenCV 4.8+** - Computer Vision
- **scikit-learn** - ML algorithms
- **TensorFlow** - Deep learning (optional)
- **Transformers** - NLP models (optional)

### Frontend

- **React 18.2+** - UI framework
- **Axios** - HTTP client
- **CSS Modules** - Component styling
- **React Icons** - Icon library
- **React Dropzone** - File upload

## 📝 Usage Examples

### Python (Backend)

```python
import requests

# Screenshot Analysis
with open('screenshot.png', 'rb') as img:
    response = requests.post(
        'http://localhost:5000/api/analyze/screenshot',
        files={'image': img}
    )
    print(response.json())

# Code Analysis
data = {
    'html': '<html><body><h1>Hello</h1></body></html>',
    'css': 'h1 { color: blue; }'
}
response = requests.post(
    'http://localhost:5000/api/analyze/code',
    json=data
)
print(response.json())
```

### JavaScript (Frontend)

```javascript
import { analysisService } from "./services/analysisService";

// Screenshot Analysis
const response = await analysisService.analyzeScreenshot(imageFile);
console.log(response.data.report);

// Code Analysis
const response = await analysisService.analyzeCode(htmlCode, cssCode);
console.log(response.data.report);
```

## 📈 Performance

- **Screenshot Processing**: 1-3 seconds
- **Code Analysis**: < 1 second
- **Report Generation**: < 1 second
- **Total Response Time**: 2-4 seconds

## 🔒 Security

- Input validation on all endpoints
- File type validation
- Size limits on uploads (10MB)
- CORS configuration
- Environment variable protection

## 📱 Responsive Design

- Mobile-first approach
- Tablet optimization
- Desktop full experience
- Touch-friendly interface

## 🧪 Testing

### Backend

```bash
cd backend
pytest tests/
```

### Frontend

```bash
cd frontend
npm test
```

## 📚 Documentation

Detailed documentation available in:

- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**

   ```bash
   # Change port in backend/.env
   PORT=5001
   ```

2. **CORS errors**

   ```bash
   # Update CORS_ORIGINS in backend/.env
   CORS_ORIGINS=http://localhost:3000
   ```

3. **API connection failed**
   - Check backend is running
   - Verify API URL in frontend/.env
   - Check network connectivity

4. **Image upload failed**
   - Check file size (< 10MB)
   - Verify file format (PNG, JPG, GIF, WebP)
   - Check disk space

## 🚀 Deployment

### Backend (Heroku)

```bash
cd backend
heroku create your-app-name
git push heroku main
```

### Frontend (Vercel)

```bash
cd frontend
vercel deploy
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📋 Roadmap

- [ ] Database integration (PostgreSQL)
- [ ] User authentication
- [ ] Project management
- [ ] Advanced ML models
- [ ] Real-time collaboration
- [ ] PDF report export
- [ ] Design tool integrations
- [ ] Custom rules builder
- [ ] Performance tracking
- [ ] API rate limiting

## 📄 License

MIT License - See LICENSE file for details

## 👥 Authors

- AI UI Team
- Contributors welcome!

## 💬 Support

- 📖 Check the documentation
- 🐛 Open an issue for bugs
- 💡 Suggest features via discussions
- 📧 Contact: support@aiuirecommendation.com

## ⭐ Show Your Support

If you find this project helpful, please give it a star! It helps others discover this tool.

---

**Improving UI/UX Design Worldwide with AI** 🌍✨

Made with ❤️ for designers and developers
