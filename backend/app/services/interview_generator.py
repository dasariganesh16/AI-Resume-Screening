from google import genai
from dotenv import load_dotenv
from functools import lru_cache
import os
import json


@lru_cache(maxsize=1)
def get_interview_client():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY_INTERVIEW")

    if not api_key:
        raise ValueError("GEMINI_API_KEY_INTERVIEW is not configured.")

    return genai.Client(
        api_key=api_key
    )


def generate_interview_questions(
    ats_score,
    matched_skills,
    missing_skills,
    projects_text,
    experience_text,
    jd_text
):

    prompt = f"""
You are a Senior Software Engineering Interviewer.

Candidate ATS Score:
{ats_score}

Matched Skills:
{matched_skills}

Missing Skills:
{missing_skills}

Projects:
{projects_text}

Experience:
{experience_text}

Job Description:
{jd_text}

Generate interview questions based on the candidate profile.

Rules:

- Ask questions relevant to the Job Description.
- Focus on the candidate's projects.
- Ask about matched skills.
- Include a few questions about missing skills.
- Difficulty should depend on ATS Score.

If ATS Score >= 80:
Ask advanced questions.

If ATS Score is between 60 and 79:
Ask intermediate questions.

If ATS Score < 60:
Ask beginner-friendly questions.

Return ONLY valid JSON.

Schema:

{{
    "technical_questions": [],
    "project_questions": [],
    "behavioral_questions": [],
    "hr_questions": []
}}

Return JSON only.
"""

    try:
        response = get_interview_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        cleaned = response.text.strip()
        cleaned = cleaned.replace("```json", "")
        cleaned = cleaned.replace("```", "").strip()

        interview_data = json.loads(cleaned)

        return {
            "technical_questions": interview_data.get("technical_questions", []),
            "project_questions": interview_data.get("project_questions", []),
            "behavioral_questions": interview_data.get("behavioral_questions", []),
            "hr_questions": interview_data.get("hr_questions", []),
        }

    except Exception as e:
        raise RuntimeError(f"Gemini interview generation failed: {e}") from e
