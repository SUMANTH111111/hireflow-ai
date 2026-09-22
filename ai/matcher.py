from ai.parser import parse_resume
from ai.scorer import semantic_similarity


def calculate_match(resume_text, job_description, job_skills):

    parsed = parse_resume(resume_text)

    job_text = f"{job_description} {job_skills}"

    semantic = semantic_similarity(
        resume_text,
        job_text
    )

    # -----------------------------
    # Intelligent scoring
    # -----------------------------

    score = semantic * 60

    score += min(len(parsed["skills"]), 10) * 3

    score += min(parsed["years"], 5) * 2

    score += min(parsed["projects"], 5)

    score += min(parsed["certifications"], 3)

    if parsed["education"]:
        score += 2

    score = round(min(score, 98))

    # -----------------------------
    # AI Explanation
    # -----------------------------

    if score >= 90:
        level = "Excellent Match"

    elif score >= 75:
        level = "Strong Match"

    elif score >= 60:
        level = "Moderate Match"

    else:
        level = "Weak Match"

    skills = parsed["skills"][:8]

    skill_text = (
        ", ".join(skills)
        if skills
        else "general software engineering skills"
    )

    explanation = (
        f"{level}. "
        f"The resume demonstrates approximately {parsed['years']} years of relevant experience, "
        f"{parsed['projects']} project(s), and expertise in {skill_text}. "
        "Semantic analysis indicates that the candidate aligns well with the responsibilities and technical requirements of this job role."
    )

    return score, explanation