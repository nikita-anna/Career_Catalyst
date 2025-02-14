import json
from extract_skills import extract_skills_from_resume

JOB_SKILLS_FILE = "job_skills.json"

def load_job_skills():
    """Load job roles and required skills from JSON."""
    with open(JOB_SKILLS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def compare_skills(resume_path, job_role):
    """Compares extracted skills with required job skills."""
    job_skills = load_job_skills()
    required = set(job_skills.get(job_role, []))
    extracted = extract_skills_from_resume(resume_path)

    if not extracted:
        return set(), set(), set()

    missing_skills = required - extracted
    additional_skills = extracted - required

    return list(extracted), list(missing_skills), list(additional_skills)
