from fastapi import APIRouter

from app.schemas.interview import InterviewRequest, InterviewResponse
from app.services.interview_generator import generate_interview_questions


router = APIRouter(
    prefix="/interview",
    tags=["Interview Questions"]
)


@router.post('/', response_model=InterviewResponse)
def create_interview_questions(request: InterviewRequest):

    analysis = request.analysis

    return generate_interview_questions(
        ats_score=analysis.ats_score,
        matched_skills=analysis.matched_skills,
        missing_skills=analysis.missing_skills,
        projects_text=analysis.projects_text,
        experience_text=analysis.experience_text,
        jd_text=analysis.job_description
    )
