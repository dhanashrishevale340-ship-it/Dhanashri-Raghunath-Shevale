import os
import json

from flask import Blueprint, request, jsonify, render_template
from werkzeug.utils import secure_filename

from resume_parser import extract_text
from ai.details import extract_details
from ai.education import extract_education
from ai.experience import extract_experience
from ai.projects import extract_projects
from ai.skills import extract_skills
from ai.scoring import calculate_score
from ai.jobs import recommend_jobs
from ai.suggestions import get_suggestions
from pdf_report import create_pdf

from models.resume import Resume
from extensions import db


resume = Blueprint("resume", __name__)


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# Allowed File
# ==========================================

def allowed_file(filename):

    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ==========================================
# Resume Validation
# ==========================================

def is_resume(text):

    text = text.lower()

    resume_keywords = [

        "education",
        "experience",
        "skills",
        "projects",
        "project",
        "summary",
        "objective",
        "profile",
        "internship",
        "certification",
        "technical skills",
        "career objective",
        "email",
        "phone",
        "mobile",
        "@"

    ]

    invalid_keywords = [

        "marksheet",
        "mark sheet",
        "result",
        "board examination",
        "higher secondary",
        "secondary school",
        "seat no",
        "roll no",
        "exam centre",
        "statement of marks",
        "percentage",
        "grade sheet"

    ]

    # Reject if document looks like marksheet/result

    invalid_count = 0

    for word in invalid_keywords:

        if word in text:

            invalid_count += 1

    if invalid_count >= 3:

        return False

    # Resume should contain minimum resume keywords

    count = 0

    for word in resume_keywords:

        if word in text:

            count += 1

    return count >= 5


# ==========================================
# Upload Resume
# ==========================================

@resume.route("/upload_resume", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:

        return jsonify({
            "message": "No file selected"
        }), 400


    file = request.files["resume"]


    if file.filename == "":

        return jsonify({
            "message": "Please select a resume"
        }), 400


    if not allowed_file(file.filename):

        return jsonify({
            "message": "Only PDF, DOC and DOCX files are allowed"
        }), 400


    try:

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(filepath)

        resume_text = extract_text(filepath)


        if resume_text.strip() == "":

            return jsonify({
                "message": "Unable to read resume"
            }), 400


        # Resume Validation

        if not is_resume(resume_text):

            os.remove(filepath)

            return jsonify({

                "message":
                "Invalid document! Please upload a valid Resume only."

            }), 400


        details = extract_details(resume_text)

        education = extract_education(resume_text)

        experience = extract_experience(resume_text)

        projects = extract_projects(resume_text)

        skills = extract_skills(resume_text)

        print("====================================")
        print("Education :", education)
        print("Experience:", experience)
        print("Projects  :", projects)
        print("Skills    :", skills)
        print("====================================")
        score = calculate_score(
            details,
            education,
            experience,
            projects,
            skills
        )

        jobs = recommend_jobs(skills)

        suggestions = get_suggestions(skills)


        # ===========================
        # Save Resume
        # ===========================

        new_resume = Resume(

            filename=filename,

            candidate_name=details.get(
                "name",
                "Not Found"
            ),

            email=details.get(
                "email",
                "Not Found"
            ),

            phone=details.get(
                "phone",
                "Not Found"
            ),

            education=json.dumps(
                education,
                ensure_ascii=False
            ),

            experience=json.dumps(
                experience,
                ensure_ascii=False
            ),

            projects=json.dumps(
                projects,
                ensure_ascii=False
            ),

            skills=json.dumps(
                skills,
                ensure_ascii=False
            ),

            score=score

        )

        db.session.add(new_resume)

        db.session.commit()


        # ===========================
        # Create PDF Report
        # ===========================

        os.makedirs(
            "reports",
            exist_ok=True
        )

        pdf_path = os.path.join(

            "reports",

            f"{filename}.pdf"

        )

        create_pdf(

            pdf_path,

            details,

            education,

            experience,

            projects,

            skills,

            score

        )


        return jsonify({

            "message": "Resume Uploaded Successfully",

            "filename": filename,

            "details": details,

            "education": education,

            "experience": experience,

            "projects": projects,

            "skills": skills,

            "score": score,

            "jobs": jobs,

            "suggestions": suggestions,

            "pdf": filename + ".pdf"

        }), 200


    except Exception as e:

        print("ERROR :", e)

        return jsonify({

            "message": str(e)

        }), 500


# ==========================================
# Resume History
# ==========================================

@resume.route("/history", methods=["GET"])
def resume_history():

    resumes = Resume.query.order_by(
        Resume.uploaded_at.desc()
    ).all()

    history = []

    for item in resumes:

        history.append({

            "id": item.id,

            "filename": item.filename,

            "candidate_name": item.candidate_name,

            "email": item.email,

            "phone": item.phone,

            "score": item.score,

            "uploaded_at": item.uploaded_at.strftime(
                "%d-%m-%Y %H:%M"
            )

        })

    return jsonify(history)


# ==========================================
# History Page
# ==========================================

@resume.route("/history_page")
def history_page():

    return render_template(
        "history.html"
    )


# ==========================================
# Dashboard
# ==========================================

@resume.route("/dashboard_data", methods=["GET"])
def dashboard_data():

    resumes = Resume.query.all()

    total = len(resumes)

    scores = [

        r.score

        for r in resumes

        if r.score is not None

    ]

    average = (

        round(
            sum(scores) / len(scores),
            2
        )

        if scores else 0

    )

    highest = max(scores) if scores else 0

    latest = Resume.query.order_by(

        Resume.uploaded_at.desc()

    ).limit(5).all()

    recent = []

    for r in latest:

        recent.append({

            "name": r.candidate_name,

            "score": r.score,

            "date": r.uploaded_at.strftime(
                "%d-%m-%Y"
            )

        })

    return jsonify({

        "total": total,

        "average": average,

        "highest": highest,

        "recent": recent

    })
# ==========================================
# View Resume Details
# ==========================================

@resume.route("/resume/<int:id>", methods=["GET"])
def get_resume(id):

    resume_data = Resume.query.get(id)

    if resume_data is None:

        return jsonify({

            "message": "Resume not found"

        }), 404


    return jsonify({

        "id": resume_data.id,

        "name": resume_data.candidate_name,

        "email": resume_data.email,

        "phone": resume_data.phone,

        "education": resume_data.education,

        "experience": resume_data.experience,

        "projects": resume_data.projects,

        "skills": resume_data.skills,

        "score": resume_data.score,

        "uploaded_at": resume_data.uploaded_at.strftime(
            "%d-%m-%Y %H:%M"
        )

    })


# ==========================================
# Delete Resume
# ==========================================

@resume.route("/delete_resume/<int:id>", methods=["DELETE"])
def delete_resume(id):

    resume_data = Resume.query.get(id)

    if resume_data is None:

        return jsonify({

            "message": "Resume not found"

        }), 404


    # Delete uploaded resume file

    try:

        resume_path = os.path.join(
            UPLOAD_FOLDER,
            resume_data.filename
        )

        if os.path.exists(resume_path):

            os.remove(resume_path)

    except Exception:

        pass


    # Delete generated PDF

    try:

        pdf_path = os.path.join(
            "reports",
            f"{resume_data.filename}.pdf"
        )

        if os.path.exists(pdf_path):

            os.remove(pdf_path)

    except Exception:

        pass


    db.session.delete(resume_data)

    db.session.commit()


    return jsonify({

        "message": "Resume deleted successfully"

    }), 200