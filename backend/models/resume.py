from extensions import db
from ai.certifications import extract_certifications

class Resume(db.Model):

    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(db.String(255))

    candidate_name = db.Column(db.String(100))

    email = db.Column(db.String(100))

    phone = db.Column(db.String(20))

    education = db.Column(db.Text)

    experience = db.Column(db.Text)

    projects = db.Column(db.Text)
    

    skills = db.Column(db.Text)

    score = db.Column(db.Integer)

    uploaded_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )