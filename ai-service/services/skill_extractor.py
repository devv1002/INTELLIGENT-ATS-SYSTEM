SKILLS_DB = [

    "Python",
    "JavaScript",
    "React",
    "Node.js",
    "MongoDB",
    "Express.js",
    "FastAPI",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "RAG",
    "Docker",
    "AWS",
    "Kubernetes",
    "SQL",
    "TensorFlow",
    "PyTorch",
    "OpenCV",
    "Git",
    "REST API",
]


def extract_skills(text):

    found_skills = []

    for skill in SKILLS_DB:

        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills