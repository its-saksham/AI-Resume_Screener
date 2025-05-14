import os
import PyPDF2
import docx
import fitz  

def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_resume_text(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX file.")


file_path = "C:/Users/hp/OneDrive/Desktop/Placements/Ai-Resume/uploads/DS_AI_ML.pdf" 

if os.path.exists(file_path):
    try:
        resume_text = extract_resume_text(file_path)
        print(resume_text) 
    except ValueError as e:
        print(f"Error: {e}")
else:
    print(f"File not found: {file_path}")
