from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from extract_skills import extract_skills_from_resume
from compare_skills import compare_skills
import json

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

with open("job_skills.json", "r", encoding="utf-8") as f:
    JOB_SKILLS = json.load(f)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "resume" not in request.files:
            return "No file part"
        
        file = request.files["resume"]
        job_role = request.form["job_role"]

        if file.filename == "":
            return "No selected file"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            extracted_skills, missing_skills, additional_skills = compare_skills(file_path, job_role)

            return render_template(
                "results.html",
                job_role=job_role,
                extracted_skills=extracted_skills,
                missing_skills=missing_skills,
                additional_skills=additional_skills
            )

    return render_template("index.html", job_roles=JOB_SKILLS.keys())

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(debug=True)
