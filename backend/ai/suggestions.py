def get_suggestions(skills):

    suggestions = []

    if "Python" in skills:
        if "SQL" not in skills:
            suggestions.append("Learn SQL")

        if "Git" not in skills:
            suggestions.append("Learn Git & GitHub")

        if "Flask" not in skills:
            suggestions.append("Learn Flask")

    if "Machine Learning" not in skills:
        suggestions.append("Learn Machine Learning")

    suggestions.append("Add Projects in Resume")
    suggestions.append("Add Internship Experience")
    suggestions.append("Improve Resume Formatting")

    return suggestions