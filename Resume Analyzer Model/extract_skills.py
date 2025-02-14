import spacy
import fitz  # PyMuPDF
import re

MODEL_DIR = "ner_model"

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text("text") for page in doc)
    return text

def extract_skills_section(resume_text):
    """Extract skills under the 'SKILLS' section including subcategories."""
    match = re.search(r"SKILLS\s*(.*?)\n(?:\n[A-Z]|$)", resume_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def extract_skills_from_resume(resume_path):
    """Load the NER model and extract skills from the 'SKILLS' section of a resume."""
    nlp = spacy.load(MODEL_DIR)
    resume_text = extract_text_from_pdf(resume_path)

    skills_section = extract_skills_section(resume_text)

    if not skills_section:
        print("Skills section not found in the resume.")
        return set()

    doc = nlp(skills_section)
    skills = {ent.text for ent in doc.ents if ent.label_ == "SKILL"}
    
    return skills

if __name__ == "__main__":
    resume_file = r"C:\Users\Nikita Anna\Final Project\Resume Analyzer Model\resume8.pdf"
    extracted_skills = extract_skills_from_resume(resume_file)
    print("Extracted Skills:", extracted_skills)
