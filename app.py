from flask import Flask, render_template, request, redirect, url_for, send_file
from screener import extract_text, extract_skills, calculate_match_score
import os
import io
import base64
import matplotlib.pyplot as plt
from weasyprint import HTML
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/parse_resume', methods=['POST'])
def parse_resume():
    if 'resume' not in request.files:
        return "No file part", 400

    files = request.files.getlist('resume')
    if not files or all(f.filename == '' for f in files):
        return "No selected files", 400

    required_skills_raw = request.form.get('required_skills', '')
    if not required_skills_raw.strip():
        return "Required skills not provided", 400

    required_skills = [skill.strip().lower() for skill in required_skills_raw.split(',') if skill.strip()]

    results = []

    for file in files:
        if file.filename == '':
            continue

        file_path = f"temp_{file.filename}"
        file.save(file_path)

        resume_text = extract_text(file_path)
        os.remove(file_path)

        extracted_skills = extract_skills(resume_text)
        match_score, matched_skills = calculate_match_score(extracted_skills, required_skills)
        missing_skills = [skill for skill in required_skills if skill not in matched_skills]

        results.append({
            'filename': file.filename,
            'extracted_skills': extracted_skills,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'match_score': round(match_score, 2),
            'resume_text': resume_text
        })

   
    return render_template("result.html",
                           required_skills=required_skills,
                           results=results)


from flask import request, render_template_string, make_response
from xhtml2pdf import pisa
from io import BytesIO

@app.route("/download_report", methods=["POST"])
def download_report():
   
    filename = request.form.get("filename", "Unnamed")
    match_score = request.form.get("match_score", "N/A")
    resume_text = request.form.get("resume_text", "No text found.")

    extracted_skills = request.form.getlist("extracted_skills[]")
    matched_skills = request.form.getlist("matched_skills[]")
    missing_skills = request.form.getlist("missing_skills[]")

   
    pdf_template = f"""
    <html>
    <head><style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        h1 {{ text-align: center; }}
        ul {{ margin-left: 20px; }}
    </style></head>
    <body>
        <h1>Resume Screening Report</h1>
        <p><strong>Filename:</strong> {filename}</p>
        <p><strong>Match Score:</strong> {match_score}</p>

        <h3>Extracted Skills</h3>
        <ul>
            {''.join(f'<li>{skill}</li>' for skill in extracted_skills)}
        </ul>

        <h3>Matched Skills</h3>
        <ul>
            {''.join(f'<li>{skill}</li>' for skill in matched_skills)}
        </ul>

        <h3>Missing Skills</h3>
        <ul>
            {''.join(f'<li>{skill}</li>' for skill in missing_skills)}
        </ul>

        <h3>Resume Text</h3>
        <p>{resume_text[:1000]}...</p>
    </body>
    </html>
    """

    
    result = BytesIO()
    pisa_status = pisa.CreatePDF(pdf_template, dest=result)

    if pisa_status.err:
        return f"PDF generation failed: {pisa_status.errstr}", 500

    response = make_response(result.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename=report_{filename}.pdf"
    return response

if __name__ == '__main__':
    app.run(debug=True)
