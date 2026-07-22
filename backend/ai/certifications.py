import re

def extract_certifications(text):

    certs = []

    keywords = [
        "certification",
        "certifications",
        "certificate",
        "udemy",
        "coursera",
        "nptel",
        "prompt engineering",
        "aws",
        "oracle",
        "google",
        "microsoft"
    ]

    for line in text.split("\n"):

        line = re.sub(r"\s+", " ", line).strip()

        if not line:
            continue

        if any(k in line.lower() for k in keywords):
            certs.append(line)

    return list(dict.fromkeys(certs))