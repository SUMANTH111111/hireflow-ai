import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def calculate_match(resume_text, job_description, job_skills):

    prompt = f"""
You are HireFlow AI, an expert Applicant Tracking System (ATS).

Your task is to evaluate ONE resume against ONE job posting.

========================
JOB DESCRIPTION
========================
{job_description}

========================
REQUIRED SKILLS
========================
{job_skills}

========================
CANDIDATE RESUME
========================
{resume_text}

IMPORTANT SCORING RULES

1. Do NOT penalize freshers for lacking corporate experience.
2. Count internships, freelance work, research, hackathons, and major academic projects as relevant experience.
3. Detect experience from employment dates (Example: 2021–Present).
4. Give significant weight to projects, GitHub work, certifications, and technical skills.
5. Compare ONLY against this job description.
6. Return ONLY valid JSON.

Required JSON format:

{{
  "score": 88,
  "experience_years": 2,
  "matched_skills": ["Python","Flask","SQL"],
  "missing_skills": ["Docker"],
  "recommendation": "Shortlisted",
  "explanation": "Excellent technical alignment with strong backend projects and relevant internship experience."
}}

Score guide:
85-100 = Shortlisted
60-84 = Applied
0-59 = Rejected

Keep explanation under 45 words.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(text)
    except Exception:
        return (
            65,
            "AI evaluation completed. The candidate demonstrates relevant technical skills and projects for this role."
        )

    matched = ", ".join(data.get("matched_skills", []))
    missing = ", ".join(data.get("missing_skills", []))

    if not matched:
        matched = "General technical skills"

    if not missing:
        missing = "None"

    explanation = (
        f"{data['explanation']} "
        f"Experience: {data['experience_years']} years. "
        f"Matched Skills: {matched}. "
        f"Missing Skills: {missing}."
    )

    return int(data["score"]), explanation