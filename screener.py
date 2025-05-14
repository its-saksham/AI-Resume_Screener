import os
import re
import docx
import fitz  


def extract_text(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text("text")
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text

def extract_skills(text):
    skill_pattern = re.compile(r"\b(Python|Java|C\+\+|Machine Learning|Data Science|Flask|React|TensorFlow|SQL|JavaScript|AWS|Kubernetes|Docker|Linux|Git|Agile|Scrum|Deep Learning|NLP)\b", re.IGNORECASE)
    found_skills = set(skill_pattern.findall(text))
    return list(map(lambda x: x.lower(), found_skills))  

def calculate_match_score(extracted_skills, job_required_skills):
    extracted_skills_set = set(skill.lower() for skill in extracted_skills)
    job_required_skills_set = set(skill.lower() for skill in job_required_skills)

    matched_skills = extracted_skills_set.intersection(job_required_skills_set)
    score = len(matched_skills) / len(job_required_skills_set) if job_required_skills_set else 0.0
    return round(score * 100, 2), list(matched_skills)

if __name__ == "__main__":
    file_path = "C:/Users/hp/OneDrive/Desktop/Placements/Ai-Resume/uploads/DS _ AI _ ML.pdf"  # Change to your file path
    resume_text = extract_text(file_path)
    extracted_skills = extract_skills(resume_text)
    

  