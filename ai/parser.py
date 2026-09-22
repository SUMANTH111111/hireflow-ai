import re

SKILLS = [
    "python", "java", "sql", "mysql",
    "flask", "django", "fastapi",
    "html", "css", "javascript",
    "react", "node.js", "git",
    "docker", "kubernetes",
    "aws", "azure",
    "langchain", "llamaindex",
    "rag", "llm",
    "gpt-4", "claude",
    "pinecone", "faiss",
    "vector database",
    "prompt engineering",
    "transformers",
    "hugging face",
    "pytorch", "tensorflow",
    "pandas", "numpy"
]


def parse_resume(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    years = 0

    match = re.search(r"(\\d+)\\+?\\s+years", text)

    if match:
        years = int(match.group(1))

    certifications = len(
        re.findall(r"certified|certificate", text)
    )

    projects = len(
        re.findall(r"project", text)
    )

    education = (
        "bachelor" in text or
        "b.tech" in text or
        "computer science" in text
    )

    return {
        "skills": found_skills,
        "years": years,
        "projects": projects,
        "certifications": certifications,
        "education": education
    }