import re
import pdfplumber
import docx2txt
import spacy
import torch
from sentence_transformers import SentenceTransformer, util


nlp = spacy.load('en_core_web_sm')

#predefinedSkills list (example)
SKILLS_DB = ['Java', 'Spring Boot', 'MySQL', 'Microservices','Python', 'Django',
             'Node.js', 'React', 'SQL', 'AWS', 'Docker', 'Kubernetes', 'MongoDB',
             'PostgresSQL', 'Machine Learning', 'REST API']

#Extract text from PDF file
def extract_text_from_pdf(file_path):
    text=""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

#Extract text from DOCX file
def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

#Extract Email
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

#Extract Phone number
def extract_phone(text):
    match = re.search(r'\+?\d[\d\s-]{7,}\d', text)
    return match.group(0) if match else None

#Extract Name
def extract_name(text):
    # very simple placeholder
    match = re.search(r"Name:\s*(.*)", text)
    return match.group(1).strip() if match else None


#Extract skills
def extract_skills(text):
    skills_found = []
    for skill in SKILLS_DB:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.I):
            skills_found.append(skill)
    return skills_found


# Create AI Helper #

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')  # Load once globally

def calculate_similarity(resume_text, job_text):
    # Encode both texts into embeddings
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_text, convert_to_tensor=True)

    # Cosine similarity returns a tensor with single element
    similarity_score = util.cos_sim(resume_embedding, job_embedding)  # shape: [1,1]

    return similarity_score.item()  # Convert to float scalar
