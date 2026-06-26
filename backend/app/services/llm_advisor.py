from google import genai
from dotenv import load_dotenv
from functools import lru_cache
import os
import json


@lru_cache(maxsize=1)
def get_advisor_client():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY_ADVISOR")

    if not api_key:
        raise ValueError("GEMINI_API_KEY_ADVISOR is not configured.")

    return genai.Client(
        api_key=api_key
    )


def generate_llm_advice(
    ats_score,
    matched_skills,
    missing_skills,
    strong_evidence,
    limited_evidence,
    projects_text,
    experience_text
):

    prompt = f"""
You are an expert AI Career Advisor.

Analyze the candidate using:

ATS Score: {ats_score}

Matched Skills:
{matched_skills}

Missing Skills:
{missing_skills}

Strong Evidence Skills:
{strong_evidence}

Limited Evidence Skills:
{limited_evidence}

Projects:
{projects_text}

Experience:
{experience_text}

Return ONLY valid JSON.

Schema:

{{
    "strengths": [],
    "improvement_areas": [],
    "learning_roadmap": [],
    "interview_readiness": {{
        "score": 0,
        "level": "",
        "reason": ""
    }}
}}

Do not write explanations.
Do not write markdown.
Return JSON only.
"""


    try:
        response = get_advisor_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        cleaned = response.text.strip()
        cleaned = cleaned.replace("```json", "")
        cleaned = cleaned.replace("```", "").strip()

        advisor_data = json.loads(cleaned)
        return advisor_data

    except Exception as e:

        return {
            "strengths": [],
            "improvement_areas": [],
            "learning_roadmap": [],
            "interview_readiness": {
                "score": 0,
                "level": "Unavailable",
                "reason": str(e)
            }
        }
    


if __name__ == "__main__":

    result = generate_llm_advice(
        ats_score=78,

        matched_skills=[
            "Java",
            "SQL",
            "Git"
        ],

        missing_skills=[
            "Docker",
            "AWS"
        ],

        strong_evidence=[
            "Java",
            "SQL"
        ],

        limited_evidence=[
            "Docker"
        ],

        projects_text="""
        Library Management System
        using Java and MySQL
        """,

        experience_text="""
        Cloud Internship
        Web Development Internship
        """
    )

    print(result)
