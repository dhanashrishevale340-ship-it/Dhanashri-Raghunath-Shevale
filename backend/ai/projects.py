def extract_projects(text):

    projects = []

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    collecting = False

    current = ""

    stop_words = [

        "education",
        "experience",
        "skills",
        "technical skills",
        "certification",
        "languages",
        "hobbies"

    ]

    for line in lines:

        lower = line.lower()

        if "project" in lower:

            collecting = True

            if current:

                projects.append(current.strip())

            current = line

            continue

        if collecting:

            if any(word in lower for word in stop_words):

                if current:

                    projects.append(current.strip())

                break

            current += "\n• " + line

    if current:

        projects.append(current.strip())

    return projects