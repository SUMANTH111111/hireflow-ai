import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def calculate_match(resume_text, job_description, job_skills):

    prompt = f"""
You are an expert ATS (Applicant Tracking System).

Evaluate ONLY this resume against the given job.

JOB DESCRIPTION:
{job_description}

REQUIRED SKILLS:
{job_skills}

RESUME:
{resume_text}

Return ONLY valid JSON.

{{
  "score": 91,
  "experience_years": 5,
  "matched_skills": ["Python","LangChain"],
  "missing_skills": ["Docker"],
  "recommendation": "Shortlisted",
  "explanation": "Strong prompt engineering experience with relevant AI projects."
}}

Rules:
- Score between 0 and 100
- Detect experience from dates like 2021–Present
- 85+ = Shortlisted
- 60–84 = Applied
- Below 60 = Rejected
- Explanation under 60 words
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    data = json.loads(text)

    explanation = (
        f"{data['explanation']} "
        f"Experience: {data['experience_years']} years. "
        f"Matched Skills: {', '.join(data['matched_skills'])}. "
        f"Missing Skills: {', '.join(data['missing_skills']) if data['missing_skills'] else 'None'}."
    )

    return int(data["score"]), explanation