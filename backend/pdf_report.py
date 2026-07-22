from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(filepath, details, education, experience, projects, skills, score):

    doc = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Resume Screening Report</b>", styles["Heading1"]))

    story.append(Paragraph(f"<b>Name:</b> {details.get('name', 'Not Found')}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Email:</b> {details.get('email', 'Not Found')}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Phone:</b> {details.get('phone', 'Not Found')}", styles["BodyText"]))

    story.append(Paragraph("<br/>", styles["BodyText"]))

    story.append(Paragraph(f"<b>Education:</b> {education}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Experience:</b> {experience}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Projects:</b> {projects}", styles["BodyText"]))

    story.append(Paragraph("<br/>", styles["BodyText"]))

    story.append(Paragraph(f"<b>Skills:</b> {', '.join(skills)}", styles["BodyText"]))

    story.append(Paragraph(f"<b>ATS Score:</b> {score}/100", styles["Heading2"]))

    doc.build(story)