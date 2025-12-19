<<<<<<< HEAD
📄 Resume ATS Score Analyzer
A Flask-based web application that analyzes resumes against job descriptions using NLP and provides ATS compatibility scores with recommendations.

🎯 Overview
This application helps job seekers optimize their resumes by:

Analyzing keyword matches with job descriptions
Extracting and comparing technical skills
Calculating ATS compatibility scores (0-100%)
Providing actionable recommendations


✨ Features

📊 Multi-dimensional ATS scoring (Keywords 40%, Skills 30%, Semantic 30%)
📁 Support for PDF, DOCX, and TXT files
🎨 Modern, responsive UI
🔌 RESTful API with 5 endpoints
🐳 Docker containerization
🧪 Unit tests with pytest


🛠️ Tech Stack
Backend: Python 3.11, Flask 3.0.0, spaCy, NLTK, scikit-learn
Frontend: HTML5, CSS3, JavaScript
DevOps: Docker, Docker Compose

📂 Project Structure
resume-analyzer/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── utils/
│   │   ├── ats_analyzer.py
│   │   └── pdf_parser.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/main.js
│   └── templates/
│       ├── base.html
│       ├── index.html
│       └── analyze.html
├── tests/
│   ├── test_routes.py
│   └── test_analyzer.py
├── uploads/
├── config.py
├── run.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md

🚀 Installation & Setup
Method 1: Docker (Recommended)
bash# Clone and navigate
git clone https://github.com/Shreyas963/resume-analyzer.git
cd resume-analyzer

# Build and run
docker-compose up --build

# Access at http://localhost:5000
Method 2: Local Setup
bash# Clone repository
git clone https://github.com/Shreyas963/resume-analyzer.git
cd resume-analyzer

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Download NLP models
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"

# Setup environment
cp .env.example .env
# Add your SECRET_KEY to .env

# Run application
python run.py

# Access at http://localhost:5000

🎮 Usage
Web Interface

Go to http://localhost:5000
Upload resume (PDF/DOCX/TXT)
Paste or upload job description
Click "Analyze Resume"
View results and recommendations



Parameters:
- resume_file: Resume file
- job_description_text: Job description text
Analyze Resume (Text):
bashPOST /api/analyze/text
Content-Type: application/json

Body:
{
  "resume_text": "Your resume...",
  "job_description": "Job description..."
}

🧪 Testing
bash# Run all tests
pytest

# With coverage
pytest --cov=app tests/

# Verbose output
pytest -v

🐳 Docker Commands
bash# Start
docker-compose up

# Start in background
docker-compose up -d

# Stop
docker-compose down

# Rebuild
docker-compose up --build

# View logs
docker-compose logs -f

✅ Project Requirements Compliance
RequirementStatusFlask Framework✅Frontend + Backend✅3+ Routes✅ (5 routes)API Endpoints✅Data Processing✅ (NLP)ML Component✅ (spaCy, NLTK)Containerization✅ (Docker)Testing✅ (pytest)Project Structure✅Code Quality✅ (PEP 8)

👥 Team

[Shreyas Ugra T V] - Backend, NLP, Docker
[Sandeep Sabavath] - Frontend, UI/UX, Testing


🔧 Troubleshooting
Port 5000 in use:
bashnetstat -ano | findstr :5000
taskkill /PID <PID> /F
spaCy model not found:
bashpython -m spacy download en_core_web_sm
NLTK data missing:
bashpython -c "import nltk; nltk.download('all')"

📧 Contact
1. Shreyas Ugra Tarikere Vasudeva Murty
2. Sandeep Sabavath

Repository: https://github.com/Shreyas963/resume-analyzer
Course: Python Programming WS 2025
Institution: SRH University
Instructor: esam.sharaf@srh-hochschulen.de

📄 License
MIT License - see LICENSE file for details

💻To run the project : docker run -p 5000:5000 resume-analyzer-app
or python run.py(after downloading all the requirements)

Submission: December 19, 2025 | Subject: Python Foundations
=======
# Resume
Resume analyzer using python flask
>>>>>>> 027b6ff992d662cbc42dfcb5b575160bd1557990
