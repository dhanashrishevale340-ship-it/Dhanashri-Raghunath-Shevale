import re

def extract_experience(text):

    experience = []

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    collect = False

    current = ""

    stop = [

        "education",
        "projects",
        "skills",
        "certification",
        "languages"

    ]

    for line in lines:

        lower = line.lower()

        if "experience" in lower or "internship" in lower:

            collect = True

            current = line

            continue

        if collect:

            if any(s in lower for s in stop):

                break

            current += " " + line

    if current:

        experience.append(current)

    return experience