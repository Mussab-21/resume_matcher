import re
import spacy

nlp = spacy.load("en_core_web_md")

SKILLS_DB = {
    "python", "javascript", "java", "c++", "sql", "react", "flutter",
    "tensorflow", "pytorch", "aws", "docker", "kubernetes", "fastapi",
    "machine learning", "deep learning", "nlp", "computer vision",
    "n8n", "supabase", "postgresql", "llm", "langchain", "keras",
    "scikit-learn", "pandas", "numpy", "git", "linux",
}

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.\w+")
YEAR_RE  = re.compile(r"(\d+)\+?\s*years?", re.IGNORECASE)

def extract_email(text):
    m = EMAIL_RE.search(text)
    return m.group(0) if m else ""

def extract_name(text):
    doc = nlp(text[:500])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return ""

def extract_skills(text):
    t = text.lower()
    return [s for s in SKILLS_DB if s in t]

def extract_experience_years(text):
    matches = YEAR_RE.findall(text)
    return max((float(y) for y in matches), default=0.0)

def extract_education(text):
    degrees = ["bachelor", "master", "phd", "b.s", "m.s", "bsc", "msc", "b.e", "m.e"]
    lines = text.lower().split("\n")
    return [l.strip() for l in lines if any(d in l for d in degrees)][:3]

def parse_resume(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "skills": extract_skills(text),
        "experience_years": extract_experience_years(text),
        "education": extract_education(text),
        "raw_text": text,
    }

def parse_job_description(text, title=""):
    return {
        "title": title,
        "required_skills": extract_skills(text),
        "preferred_skills": [],
        "min_experience_years": extract_experience_years(text),
        "raw_text": text,
    }