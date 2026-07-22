import re

def extract_education(text):

    education = []

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    keywords = [

        "b.e",
        "be",
        "b.tech",
        "m.tech",
        "b.sc",
        "m.sc",
        "bca",
        "mca",
        "bcom",
        "b.com",
        "mba",
        "diploma",
        "ssc",
        "hsc",
        "computer science",
        "computer engineering",
        "information technology",
        "electronics",
        "mechanical",
        "civil",
        "cgpa",
        "%"
    ]

    i = 0

    while i < len(lines):

        current = lines[i]

        if any(k in current.lower() for k in keywords):

            education_line = current

            j = i + 1

            while j < len(lines):

                nxt = lines[j]

                if any(word in nxt.lower() for word in [

                    "experience",
                    "project",
                    "projects",
                    "skills",
                    "technical skills",
                    "certification",
                    "language"

                ]):

                    break

                if len(nxt) < 80:

                    education_line += " | " + nxt

                    j += 1

                else:

                    break

            education.append(education_line)

            i = j

        else:

            i += 1

    return list(dict.fromkeys(education))