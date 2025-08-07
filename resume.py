from flask import *
import fitz
import docx2txt
import re
import os
import tempfile

resumee = Blueprint('resumee', __name__)

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path)

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+", text)
    return match.group() if match else ""

def extract_phone(text):
    match = re.search(r"\b(\+91[-\s]?)?\(?\d{3,5}\)?[-.\s]?\d{5,10}\b", text)
    return match.group() if match else ""

def extract_name(text):
    lines = text.strip().split("\n")
    for line in lines[:5]:
        if re.search(r"[A-Z][a-z]+\s[A-Z][a-z]+", line):
            return line.strip()
    return lines[0].strip()

def extract_section(text, section_titles):
    pattern = '|'.join([re.escape(title) for title in section_titles])
    split_sections = re.split(rf"\n({pattern})\n", text, flags=re.IGNORECASE)
    
    sections = {}
    current_section = "About"
    sections[current_section] = ""

    i = 1
    while i < len(split_sections):
        section_title = split_sections[i].strip()
        section_content = split_sections[i+1].strip()
        sections[section_title] = section_content
        i += 2

    return sections


@resumee.route('/resume', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    filename = file.filename

    if not filename.lower().endswith(('.pdf', '.docx')):
        return jsonify({"error": "Only PDF and DOCX files are supported"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
        file.save(tmp.name)
        filepath = tmp.name

    try:
        if filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(filepath)
        else:
            text = extract_text_from_docx(filepath)

        data = {
            "Name": extract_name(text),
            "Email": extract_email(text),
            "Phone": extract_phone(text)
        }

        section_titles = [
            "Skills", "Experience", "Work Experience", "Education", 
            "Projects", "Certifications", "Languages", "Achievements", 
            "Internships", "Technical Skills", "Other", "Hobbies", "Interests"
        ]
        
        sections = extract_section(text, section_titles)

        for key in section_titles:
            if key in sections:
                if key.lower() in ["experience", "projects", "education", "certifications", "internships"]:
                    data[key] = sections[key].split("\n")
                else:
                    data[key] = sections[key]

        return jsonify(data)

    finally:
        os.unlink(filepath)
