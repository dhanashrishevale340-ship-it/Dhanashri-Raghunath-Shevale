def recommend_jobs(skills):

    job_database = [

        {
            "title": "Python Developer",
            "skills": ["Python", "Flask", "SQL"],
            "salary": "₹6 - ₹10 LPA"
        },

        {
            "title": "Backend Developer",
            "skills": ["Python", "MySQL"],
            "salary": "₹5 - ₹8 LPA"
        },

        {
            "title": "Frontend Developer",
            "skills": ["HTML", "CSS", "JavaScript"],
            "salary": "₹4 - ₹7 LPA"
        },

        {
            "title": "Full Stack Developer",
            "skills": ["Python", "Flask", "HTML", "CSS", "JavaScript"],
            "salary": "₹8 - ₹12 LPA"
        },

        {
            "title": "Data Analyst",
            "skills": ["Python", "SQL", "Excel"],
            "salary": "₹5 - ₹9 LPA"
        }

    ]

    recommended = []

    for job in job_database:

        matched = []

        for skill in job["skills"]:

            if skill in skills:
                matched.append(skill)

        if len(job["skills"]) > 0:
            match = int((len(matched) / len(job["skills"])) * 100)
        else:
            match = 0

        if match > 0:

            recommended.append({

                "title": job["title"],

                "match": match,

                "salary": job["salary"],

                "matched_skills": matched

            })

    recommended.sort(key=lambda x: x["match"], reverse=True)

    return recommended