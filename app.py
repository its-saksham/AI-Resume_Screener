from flask import Flask, render_template, request, redirect, url_for
from screener import extract_text, extract_skills, calculate_match_score
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/ping', methods=['GET'])
def ping():
    try:
        # Perform minimal processing or just return a success response
        return jsonify({"status": "success"}), 200
    except Exception as e:
        # In case of errors, return minimal error information
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/parse_resume', methods=['POST'])
def parse_resume():
    if 'resume' not in request.files:
        return "No file part", 400  
    file = request.files['resume']
    
    if file.filename == '':
        return "No selected file", 400  
    
    required_skills_raw = request.form.get('required_skills', '')
    required_skills = [skill.strip().lower() for skill in required_skills_raw.split(',') if skill.strip()]

   
    file_path = f"temp_{file.filename}"
    file.save(file_path)
    
   
    resume_text = extract_text(file_path)
    os.remove(file_path) 

    extracted_skills = extract_skills(resume_text)
    match_score, matched_skills = calculate_match_score(extracted_skills, required_skills)

    return render_template("result.html",
                           extracted_skills=extracted_skills,
                           required_skills=required_skills,
                           matched_skills=matched_skills,
                           match_score=round(match_score, 2),
                           resume_text=resume_text)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
