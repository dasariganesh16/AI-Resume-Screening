from fastapi import APIRouter

from app.schemas.advice import AdviceRequest, AdviceResponse
from app.services.llm_advisor import generate_llm_advice


router = APIRouter(
    prefix="/advice",
    tags=["AI Career Advice"]
)


@router.post("/", response_model=AdviceResponse)
def create_advice(request: AdviceRequest):
    return generate_llm_advice(
        ats_score=request.ats_score,
        matched_skills=request.matched_skills,
        missing_skills=request.missing_skills,
        strong_evidence=request.strong_evidence,
        limited_evidence=request.limited_evidence,
        projects_text=request.projects_text,
        experience_text=request.experience_text
    )
