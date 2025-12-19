# app/analyzer.py
# Docker + Python 3.10 compatible version

from PyPDF2 import PdfReader
import docx
import re
from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ResumeAnalyzer:
    """Resume analyzer using regex and ML without SpaCy dependency."""

    def __init__(self):
        """Initialize the analyzer with common skills list."""
        self.common_skills: List[str] = [
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'SQL',
            'HTML', 'CSS', 'React', 'Angular', 'Vue', 'Node.js', 'Flask',
            'Django', 'FastAPI', 'Spring Boot', 'Machine Learning', 'Deep Learning',
            'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy',
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Git', 'GitHub',
            'REST API', 'GraphQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis',
            'Agile', 'Scrum', 'CI/CD', 'Jenkins', 'Linux', 'Bash', 'PowerShell',
            'Data Analysis', 'Data Science', 'Statistics', 'Excel', 'Tableau',
            'Power BI', 'Spark', 'Hadoop', 'ETL', 'API Development', 'Microservices',
            'Cloud Computing', 'DevOps', 'Security', 'Testing', 'Selenium'
        ]

    # -------------------------
    # TEXT EXTRACTION
    # -------------------------

    def extract_text_from_pdf(self, filepath: str) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with open(filepath, "rb") as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
        except Exception as e:
            raise ValueError(f"Error reading PDF: {str(e)}")

        return text

    def extract_text_from_docx(self, filepath: str) -> str:
        """Extract text from DOCX file."""
        try:
            doc = docx.Document(filepath)
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception as e:
            raise ValueError(f"Error reading DOCX: {str(e)}")

    def extract_text_from_txt(self, filepath: str) -> str:
        """Extract text from TXT file."""
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                return file.read()
        except Exception as e:
            raise ValueError(f"Error reading TXT: {str(e)}")

    def extract_text(self, filepath: str) -> str:
        """Extract text based on file extension."""
        if filepath.lower().endswith(".pdf"):
            return self.extract_text_from_pdf(filepath)
        elif filepath.lower().endswith(".docx"):
            return self.extract_text_from_docx(filepath)
        elif filepath.lower().endswith(".txt"):
            return self.extract_text_from_txt(filepath)
        else:
            raise ValueError("Unsupported file format")

    # -------------------------
    # INFORMATION EXTRACTION
    # -------------------------

    def extract_email(self, text: str) -> str:
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        match = re.search(pattern, text)
        return match.group(0) if match else "Not found"

    def extract_phone(self, text: str) -> str:
        patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\b\d{10}\b'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return "Not found"

    def extract_skills(self, text: str) -> List[str]:
        found = []
        text_lower = text.lower()
        for skill in self.common_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found.append(skill)
        return sorted(set(found))

    def extract_name(self, text: str) -> str:
        lines = text.split("\n")
        for line in lines[:5]:
            line = line.strip()
            pattern = r'^([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)$'
            match = re.match(pattern, line)
            if match:
                return match.group(1)
        return "Not found"

    def extract_education(self, text: str) -> List[str]:
        keywords = [
            'Bachelor', 'Master', 'PhD', 'B.Tech', 'M.Tech',
            'B.Sc', 'M.Sc', 'MBA', 'University', 'College'
        ]
        results = []
        for line in text.split("\n"):
            for kw in keywords:
                if kw.lower() in line.lower():
                    results.append(line.strip())
        return list(set(results))[:5]

    def extract_experience_years(self, text: str) -> str:
        patterns = [
            r'(\d+)\+?\s+years?\s+of\s+experience',
            r'experience[:\s]+(\d+)\+?\s+years?'
        ]
        for p in patterns:
            match = re.search(p, text.lower())
            if match:
                return f"{match.group(1)}+ years"
        return "Not specified"

    # -------------------------
    # ANALYSIS
    # -------------------------

    def calculate_match_score(self, resume_text: str, job_description: str) -> float:
        if not job_description.strip():
            return 0.0
        try:
            vectorizer = TfidfVectorizer(stop_words="english", max_features=500)
            vectors = vectorizer.fit_transform([resume_text, job_description])
            score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            return round(score * 100, 2)
        except Exception:
            return 0.0

    def analyze_keywords(self, text: str) -> Dict[str, int]:
        return {
            "experience": len(re.findall(r'\bexperience\b', text.lower())),
            "project": len(re.findall(r'\bproject\b', text.lower())),
            "skill": len(re.findall(r'\bskill\b', text.lower())),
            "education": len(re.findall(r'\beducation\b', text.lower())),
            "certification": len(re.findall(r'\bcertificat(?:e|ion)\b', text.lower()))
        }

    def analyze(self, filepath: str, job_description: str = "") -> Dict[str, Any]:
        text = self.extract_text(filepath)

        if len(text.strip()) < 50:
            raise ValueError("Insufficient resume text extracted")

        skills = self.extract_skills(text)

        return {
            "name": self.extract_name(text),
            "email": self.extract_email(text),
            "phone": self.extract_phone(text),
            "skills": skills,
            "entities": {
                "education": self.extract_education(text),
                "skills_count": len(skills),
                "experience": self.extract_experience_years(text),
            },
            "match_score": self.calculate_match_score(text, job_description),
            "word_count": len(text.split()),
            "keywords": self.analyze_keywords(text),
            "text_preview": text[:500] + "..." if len(text) > 500 else text
        }

    def get_common_skills(self) -> List[str]:
        return sorted(self.common_skills)
