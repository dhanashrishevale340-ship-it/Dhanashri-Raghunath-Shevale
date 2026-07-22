SKILLS = [

    "Python",
    "Java",
    "C",
    "C++",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Flask",
    "Django",
    "SQL",
    "MySQL",
    "MongoDB",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "NLP",
    "Prompt Engineering",
    "ANN",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Scikit-learn",
    "Git",
    "GitHub",
    "VS Code",
    "Jupyter",
    "Google Colab",
    "Azure",
    "Power BI",
    "Excel",
    "ChatGPT"

]


def extract_skills(text):

    found = []

    lower_text = text.lower()

    for skill in SKILLS:

        if skill.lower() in lower_text:

            found.append(skill)

    return list(dict.fromkeys(found))