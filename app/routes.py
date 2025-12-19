from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from typing import Dict, Any
from app.analyzer import ResumeAnalyzer

main = Blueprint('main', __name__)
analyzer = ResumeAnalyzer()

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route 1: Home Page
@main.route('/')
def index() -> str:
    """Render the home page."""
    return render_template('index.html')

# Route 2: Upload Page
@main.route('/upload')
def upload_page() -> str:
    """Render the upload page."""
    return render_template('upload.html')

# Route 3: API - Analyze Resume
@main.route('/api/analyze', methods=['POST'])
def analyze_resume() -> Dict[str, Any]:
    """
    API endpoint to analyze uploaded resume.
    Returns JSON with extracted information and analysis.
    """
    if 'resume' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['resume']
    job_description: str = request.form.get('job_description', '')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        
        try:
            # Analyze resume
            results: Dict[str, Any] = analyzer.analyze(filepath, job_description)
            
            # Clean up file
            os.remove(filepath)
            
            return jsonify(results), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

# Route 4: API - Get Skills
@main.route('/api/skills', methods=['GET'])
def get_skills() -> Dict[str, Any]:
    """API endpoint to get common skills list."""
    skills: list = analyzer.get_common_skills()
    return jsonify({'skills': skills}), 200

# Route 5: Results Page
@main.route('/results')
def results() -> str:
    """Render results page."""
    return render_template('results.html')