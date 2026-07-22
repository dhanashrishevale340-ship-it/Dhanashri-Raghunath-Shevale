def calculate_score(details, education, experience, projects, skills):

    score = 0

    # Contact Details (20 Marks)
    if details.get("name") != "Not Found":
        score += 5

    if details.get("email") != "Not Found":
        score += 5

    if details.get("phone") != "Not Found":
        score += 10

    # Education (20 Marks)
    if len(education) > 0:
        score += 20

    # Experience (20 Marks)
    if len(experience) > 0:
        score += 20

    # Projects (20 Marks)
    if len(projects) > 0:
        score += 20

    # Skills (20 Marks)
    if len(skills) >= 5:
        score += 20
    elif len(skills) >= 3:
        score += 15
    elif len(skills) >= 1:
        score += 10

    if score > 100:
        score = 100

    return score