from google import genai
from dotenv import load_dotenv
from functools import lru_cache
import os
import json


@lru_cache(maxsize=1)
def get_tailor_client():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY_TAILOR")

    if not api_key:
        raise ValueError("GEMINI_API_KEY_TAILOR is not configured.")

    return genai.Client(
        api_key=api_key
    )


def generate_tailored_resume(
    projects_text,
    experience_text,
    matched_skills,
    missing_skills
):

    prompt = f"""
You are an expert ATS Resume Writer.

Projects:
{projects_text}

Experience:
{experience_text}

Matched Skills:
{matched_skills}

Missing Skills:
{missing_skills}

Your task:

1. Write a professional summary tailored to the job.
2. Improve project descriptions.
3. Improve experience descriptions.
4. Make wording stronger and ATS friendly.
5. Highlight existing strengths.

IMPORTANT:
- Do NOT invent experience.
- Do NOT add skills that are not present in the resume.
- Do NOT claim expertise in missing skills.
- Do NOT add fake projects.
- Do NOT add fake certifications.
- Only improve wording and presentation.

Return ONLY valid JSON.

Schema:

{{
    "professional_summary": "",

    "project_improvements": [
        {{
            "original": "",
            "improved": ""
        }}
    ],

    "experience_improvements": [
        {{
            "original": "",
            "improved": ""
        }}
    ]
}}

Return JSON only.
"""

    try:

        response = get_tailor_client().models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        cleaned = response.text.strip()

        cleaned = cleaned.replace("```json", "")
        cleaned = cleaned.replace("```", "").strip()

        tailored_data = json.loads(cleaned)

        return tailored_data

    except Exception as e:

        error_message = str(e)

        if "RESOURCE_EXHAUSTED" in error_message:
            error_message = (
                "Gemini quota exceeded. Please wait a minute and try again."
            )

        return {
            "professional_summary": "",
            "project_improvements": [],
            "experience_improvements": [],
            "error": error_message
        }
